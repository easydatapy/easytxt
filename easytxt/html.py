import re
from typing import List, Optional, Union

from lxml import etree
from pyquery import PyQuery

from easytxt.config import HTML_RE_VALIDATOR, INLINE_TAGS
from easytxt.parsers.table import TableParser


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

    raw_sentences = _to_raw_sentences(
        html_text=pq_object,
        max_chars=max_chars
    )

    sentences = []

    for raw_sentence in raw_sentences:
        sentences += raw_sentence.split('<break>')

    return sentences


def _to_raw_sentences(
        html_text: Union[str, PyQuery],
        max_chars: int = 1
) -> List[str]:

    pq = to_pq(html_text)

    if not pq.text():
        return []

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


def to_pq(html_text: Union[str, PyQuery]) -> PyQuery:
    if isinstance(html_text, PyQuery):
        return html_text
    else:
        return PyQuery(html_text)


def _pq_content_to_sentences(
        pq: PyQuery,
        raw_sentences: Optional[List[str]] = None
) -> List[str]:

    if not raw_sentences:
        raw_sentences = []

    for el in pq.contents():
        if isinstance(el, etree._Element) and el.tag == 'br':
            el = '<break>'

        if isinstance(el, etree._Element) and _has_table_tag(el.tag):
            if el.tag != 'table':
                table_html = pq.outer_html()
            else:
                table_html = PyQuery(el).outer_html()

            raw_sentences += TableParser(table_html).sentences

            if el.tag != 'table':
                break

        elif isinstance(el, str):
            raw_sentences.append(el.strip())
        elif PyQuery(el).text():
            raw_sentences += _to_raw_sentences(el)

    return raw_sentences


def _pq_has_only_inline_tags(pq: PyQuery) -> bool:
    children_tags = [el.tag for el in pq.children()]
    return all([tag in INLINE_TAGS for tag in children_tags])


def _has_table_tag(tag: str) -> bool:
    return tag in ['table', 'tr', 'td', 'th', 'tbody', 'thead']
