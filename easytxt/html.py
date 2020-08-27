import re
from typing import List, Optional, Union

from lxml import etree
from pyquery import PyQuery

from easytxt.config import HTML_RE_VALIDATOR, INLINE_TAGS


def to_sentences(
        html_text: str,
        css_query: Optional[str] = None,
        exclude_css: Optional[Union[List[str], str]] = None,
        max_chars: int = 1
) -> List[str]:

    pq_object = PyQuery(html_text)

    if css_query:
        pq_object = pq_object(css_query)

    # remove scripts and styles otherwise there could be errors when
    # converting html to text
    pq_object.remove('script')
    pq_object.remove('style')

    if exclude_css:
        if isinstance(exclude_css, str):
            exclude_css = [exclude_css]

        for exclude_css_selector in exclude_css:
            pq_object.remove(exclude_css_selector)

    return to_raw_sentences(
        html_text=pq_object,
        max_chars=max_chars
    )


def to_pq(html_text: Union[str, PyQuery]) -> PyQuery:
    if isinstance(html_text, PyQuery):
        return html_text
    else:
        return PyQuery(html_text)


def to_raw_sentences(
        html_text: Union[str, PyQuery],
        max_chars: int = 1
) -> List[str]:

    pq = to_pq(html_text)

    if not pq.text():
        return []

    # Easier to additionally split sentences later on with sentence.from_text
    # than to do it here since in some cases split doesn't always work
    pq('br').replaceWith('\n')

    raw_sentences = []

    if _pq_has_only_inline_tags(pq):
        inline_raw_sentences = _pq_content_to_sentences(pq)

        raw_sentences.append(' '.join(inline_raw_sentences))
    else:
        raw_sentences += _pq_content_to_sentences(pq, raw_sentences)

    return [rs for rs in raw_sentences if rs and len(rs.strip()) > max_chars]


def validate(text: str) -> bool:
    return bool(re.search(HTML_RE_VALIDATOR, text, re.IGNORECASE))


def validate_html_table(text: str) -> bool:
    return bool(re.search('(<th>|<td>)', text, re.IGNORECASE))


def _pq_content_to_sentences(
        pq: PyQuery,
        raw_sentences: Optional[List[str]] = None
) -> List[str]:

    if not raw_sentences:
        raw_sentences = []

    for el in pq.contents():
        if isinstance(el, etree._Element) and _has_table_tag(el.tag):
            if el.tag != 'table':
                table_html = pq.outer_html()
            else:
                table_html = PyQuery(el).outer_html()

            raw_sentences += TableReader(table_html).sentences

            if el.tag != 'table':
                break

        elif isinstance(el, str):
            raw_sentences.append(el.strip())
        elif PyQuery(el).text():
            raw_sentences += to_raw_sentences(el)

    return raw_sentences


def _pq_has_only_inline_tags(pq: PyQuery) -> bool:
    children_tags = [el.tag for el in pq.children()]
    return all([tag in INLINE_TAGS for tag in children_tags])


def _has_table_tag(tag: str) -> bool:
    return tag in ['table', 'tr', 'td', 'th', 'tbody', 'thead']


class TableReader(object):
    __cached_rows: List[List[str]] = []

    def __init__(
            self,
            html_text: Optional[Union[str, PyQuery]] = None,
            pq: Optional[PyQuery] = None,
            allow_cols: Optional[List[str]] = None,
            callow_cols: Optional[List[str]] = None,
            deny_cols: Optional[List[str]] = None,
            cdeny_cols: Optional[List[str]] = None,
            separator: str = '; ',
            header: bool = True,
            skip_row_without_value: bool = True
    ):

        if isinstance(html_text, str):
            self._pq = PyQuery(html_text)
        else:
            self._pq = pq

        self._allow_cols = allow_cols
        self._callow_cols = callow_cols
        self._deny_cols = deny_cols
        self._cdeny_cols = cdeny_cols
        self._separator = separator
        self._header = header
        self._skip_row_without_value = skip_row_without_value

    def __iter__(self):
        dict_iterator = self._iter_dict()

        for table_row_data in dict_iterator:
            if self._allow_cols:
                table_row_data = self._filter_allow_cols(
                    table_row_dict=table_row_data,
                    allow_cols=self._allow_cols,
                    case_sensitive=False
                )

            if self._callow_cols:
                table_row_data = self._filter_allow_cols(
                    table_row_dict=table_row_data,
                    allow_cols=self._callow_cols,
                    case_sensitive=True
                )

            if self._deny_cols:
                table_row_data = self._filter_deny_cols(
                    table_row_dict=table_row_data,
                    deny_cols=self._deny_cols,
                    case_sensitive=False
                )

            if self._cdeny_cols:
                table_row_data = self._filter_deny_cols(
                    table_row_dict=table_row_data,
                    deny_cols=self._cdeny_cols,
                    case_sensitive=True
                )

            if not table_row_data:
                continue

            yield table_row_data

    def _iter_dict(self):
        list_iterator = self._iter_list()

        if self._header and self.has_header():
            yield from self._iter_dict_with_header(list_iterator)
        else:
            yield from self._iter_dict_without_header(list_iterator)

    def _iter_list(self):
        if not self.__cached_rows:
            yield from self.__cached_rows

        for tr_pq in self._pq('tr').items():
            row_data = [td_pq.text() for td_pq in tr_pq('td,th').items()]

            self.__cached_rows.append(row_data)

            yield row_data

    @property
    def sentences(self):
        raw_sentences = []

        for table_row_data in self.__iter__():
            feature_key = '/'.join(table_row_data.keys())
            feature_value = '/'.join(table_row_data.values())
            feature = '{}: {}'.format(feature_key, feature_value)

            raw_sentences.append(feature)

        return raw_sentences

    @property
    def text(self):
        raw_sentences = self.sentences

        if raw_sentences:
            return '* {}'.format(' * '.join(raw_sentences))

        return ''

    @property
    def header_values(self):
        return next(self._iter_list())

    def has_header(self) -> bool:
        if self._pq('tbody') and not self._pq('thead'):
            return False

        return bool(self._pq('th')) or bool(self._pq('thead'))

    def _filter_allow_cols(
            self,
            table_row_dict: dict,
            allow_cols: Optional[List[str]],
            case_sensitive: bool = False
    ) -> dict:

        ignore_case = 0 if case_sensitive else re.IGNORECASE

        filtered_row_dict = {}

        for key, value in table_row_dict.items():
            if any(re.search(allow_key, key, ignore_case)
                   for allow_key in allow_cols):

                filtered_row_dict[key] = value

        return filtered_row_dict

    def _filter_deny_cols(
            self,
            table_row_dict: dict,
            deny_cols: Optional[List[str]],
            case_sensitive: bool = False
    ) -> dict:

        ignore_case = 0 if case_sensitive else re.IGNORECASE

        filtered_row_dict = {}

        for key, value in table_row_dict.items():
            if not any(re.search(deny_key, key, ignore_case)
                       for deny_key in deny_cols):

                filtered_row_dict[key] = value

        return filtered_row_dict

    def _iter_dict_with_header(self, list_iterator):
        header_row_values = next(list_iterator)

        for body_row_values in list_iterator:
            yield dict(zip(header_row_values, body_row_values))

    def _iter_dict_without_header(self, list_iterator):
        for body_row_data in list_iterator:
            dict_key = body_row_data[0]

            body_row_values = [v for v in body_row_data[1:] if v]

            if self._skip_row_without_value and not body_row_values:
                continue

            dict_value = self._separator.join(body_row_values)

            yield {dict_key: dict_value}
