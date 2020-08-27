from abc import ABC

from typing import List, Optional, Union


class BaseTextParser(ABC):
    def __init__(
            self,
            text: Optional[Union[str, float, int]] = None,
            language: str = 'en',
            css_query: Optional[str] = None,
            exclude_css: Optional[Union[List[str], str]] = None,
            deny: Optional[List[str]] = None,
            cdeny: Optional[List[str]] = None,
            allow: Optional[List[str]] = None,
            callow: Optional[List[str]] = None,
            normalize: bool = True,
            capitalize: bool = True,
            uppercase: bool = False,
            lowercase: bool = False,
            min_chars: int = 5,
            replace_keys: Optional[list] = None,
            remove_keys: Optional[list] = None,
            replace_keys_raw_text: Optional[list] = None,
            remove_keys_raw_text: Optional[list] = None,
            split_inline_breaks: bool = True,
            inline_breaks: Optional[List[str]] = None,
            merge_sentences: bool = True,
            stop_key: str = '.',
            stop_keys_split: Optional[List[str]] = None,
            stop_keys_ignore: Optional[List[str]] = None,
            sentence_separator: str = ' ',
            feature_split_keys: Optional[List[str]] = None,
            autodetect_html: bool = True
    ):

        self._text = text
        self._language = language
        self._css_query = css_query
        self._exclude_css = exclude_css
        self._deny = deny
        self._cdeny = cdeny
        self._allow = allow
        self._callow = callow
        self._normalize = normalize
        self._capitalize = capitalize
        self._uppercase = uppercase
        self._lowercase = lowercase
        self._min_chars = min_chars
        self._replace_keys = replace_keys
        self._remove_keys = remove_keys
        self._replace_keys_raw_text = replace_keys_raw_text
        self._remove_keys_raw_text = remove_keys_raw_text
        self._split_inline_breaks = split_inline_breaks
        self._inline_breaks = inline_breaks
        self._merge_sentences = merge_sentences
        self._stop_key = stop_key
        self._stop_keys_split = stop_keys_split
        self._stop_keys_ignore = stop_keys_ignore
        self._sentence_separator = sentence_separator
        self._feature_split_keys = feature_split_keys
        self._autodetect_html = autodetect_html
