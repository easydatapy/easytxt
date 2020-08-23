import re
from typing import List, Optional, Union

from pyquery import PyQuery

from easytxt.constants import HTML_RE_VALIDATOR


def to_text(
        html_text: str,
        css_query: Optional[str] = None,
        exclude_css: Optional[Union[List[str], str]] = None,
) -> str:

    pq_object = PyQuery(html_text)

    if css_query:
        pq_object = pq_object(css_query)

    # remove scripts or styles otherwise there could be errors when
    # converting html to text
    pq_object = pq_object.clone().remove('script').remove('style')

    if exclude_css:
        if isinstance(exclude_css, str):
            exclude_css = [exclude_css]

        for exclude_css_selector in exclude_css:
            pq_object = pq_object.remove(exclude_css_selector)

    return pq_object.text()


def validate(text: str) -> bool:
    return bool(re.search(HTML_RE_VALIDATOR, text, re.IGNORECASE))


def validate_html_table(text: str) -> bool:
    return bool(re.search('(<th>|<td>)', text, re.IGNORECASE))


class TableReader(object):
    def __init__(
            self,
            html_text: str,
            allow_cols: Optional[List[str]] = None,
            callow_cols: Optional[List[str]] = None,
            deny_cols: Optional[List[str]] = None,
            cdeny_cols: Optional[List[str]] = None,
            separator: str = '; ',
            header: bool = True,
            skip_row_without_value: bool = True
    ):

        if not html_text:
            raise ValueError('html_text arg cannot be empty!')

        if not validate(html_text):
            raise ValueError('html_text is not valid html/xml!')

        self._pq = PyQuery(html_text)

        self._allow_cols = allow_cols
        self._callow_cols = callow_cols
        self._deny_cols = deny_cols
        self._cdeny_cols = cdeny_cols
        self._separator = separator
        self._header = header
        self._skip_row_without_value = skip_row_without_value

    def __iter__(self):
        dict_iterator = self.iter_dict()

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

    def iter_dict(self):
        list_iterator = self.iter_list()

        if self._header and self.has_header():
            yield from self._iter_dict_with_header(list_iterator)
        else:
            yield from self._iter_dict_without_header(list_iterator)

    def iter_list(self):
        for tr_pq in self._pq('tr').items():
            yield [td_pq.text() for td_pq in tr_pq('td,th').items()]

    def get_header_values(self):
        return next(self.iter_list())

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
