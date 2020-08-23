import re
from typing import List, Optional, Union, Tuple

from easytxt import xhtml
from easytxt import sentences
from easytxt import text as utext


def parse_string(
        raw_text: Union[str, float, int, bytes],
        normalize: bool = True,
        replace_chars: Optional[list] = None,
        remove_chars: Optional[list] = None,
        split_key: Optional[Union[str, tuple]] = None,
        split_keys: Optional[List[Union[str, tuple]]] = None,
        fix_spaces: bool = True,
        escape_new_lines: bool = False,
        new_line_replacement: str = ' '
) -> str:

    split_keys = [split_key] if split_key else split_keys

    raw_text = utext.to_str(raw_text)

    if normalize:
        raw_text = utext.normalize(
            text=raw_text,
            fix_spaces=fix_spaces,
            escape_new_lines=escape_new_lines,
            new_line_replacement=new_line_replacement
        )

    if replace_chars:
        raw_text = utext.replace_chars_by_keys(
            text=raw_text,
            text_replacements=replace_chars
        )

    if split_keys:
        raw_text = utext.from_split_keys(
            text=raw_text,
            split_keys=split_keys
        )

    if remove_chars:
        raw_text = utext.remove_chars_by_keys(
            text=raw_text,
            remove_chars=remove_chars
        )

    return utext.normalize_spaces(raw_text)


class TextParser(object):
    cached_sentences = []
    cached_features = []

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
            split_inline_breaks: bool = True,
            inline_breaks: Optional[List[str]] = None,
            merge_sentences: bool = True,
            merge_keys: Optional[List[str]] = None,
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
        self._split_inline_breaks = split_inline_breaks
        self._inline_breaks = inline_breaks
        self._merge_sentences = merge_sentences
        self._merge_keys = merge_keys
        self._sentence_separator = sentence_separator
        self._feature_split_keys = feature_split_keys
        self._autodetect_html = autodetect_html

    def __iter__(self):
        for sentence in self.sentences:
            yield sentence

    @property
    def text(self) -> str:
        return sentences.to_text(
            sentences=self.sentences,
            separator=self._sentence_separator
        )

    @property
    def sentences(self):
        raw_sentences = self.raw_sentences

        return self._filter_raw_sentences(raw_sentences)

    @property
    def raw_sentences(self) -> List[str]:
        if self.cached_sentences:
            return self.cached_sentences

        self.cached_sentences = self._text_to_sentences()

        return self.cached_sentences

    @property
    def features(self) -> List[Tuple[str, str]]:
        raw_features = self.raw_features

        return [rf for rf in raw_features if isinstance(rf, tuple)]

    @property
    def features_dict(self):
        return {k: v for k, v in self.features}

    def feature(self, key: str) -> Optional[str]:
        for feature_data in self.features:
            feature_key, feature_value = feature_data

            if re.search(
                pattern=key,
                string=feature_key,
                flags=re.IGNORECASE
            ):

                return feature_value

        return None

    def feature_exact(self, key: str) -> Optional[str]:
        for feature_data in self.features:
            feature_key, feature_value = feature_data

            if feature_key.lower() == key.lower():
                return feature_value

        return None

    @property
    def raw_features(self) -> List[str]:
        if self.cached_features:
            return self.cached_features

        raw_sentences = self.sentences

        raw_features = []

        for raw_sentence in raw_sentences:
            raw_feature = utext.to_feature(
                text=raw_sentence,
                split_keys=self._feature_split_keys
            )

            raw_features.append(raw_feature)

        self.cached_features = raw_features

        return self.cached_features

    def _text_to_sentences(self):
        raw_sentences = self._text_to_raw_sentences()

        raw_sentences = self._manage_raw_sentences_inline_breaks(raw_sentences)

        if self._merge_sentences:
            raw_sentences = sentences.merge(
                sentences=raw_sentences,
                merge_keys=self._merge_keys
            )

        raw_sentences = sentences.add_stop(raw_sentences)

        if self._capitalize:
            raw_sentences = sentences.capitalize_sentence(raw_sentences)

        return raw_sentences

    def _text_to_raw_sentences(self):
        if self._autodetect_html and xhtml.validate_html_table(self._text):
            return self._html_table_to_raw_sentences()

        if self._autodetect_html and xhtml.validate(self._text):
            raw_text = xhtml.to_text(
                html_text=self._text,
                css_query=self._css_query,
                exclude_css=self._exclude_css
            )
        else:
            raw_text = self._text

        raw_text = self._normalize_raw_text(raw_text)

        return sentences.from_text(
            text=raw_text,
            language=self._language
        )

    def _html_table_to_raw_sentences(self):
        raw_sentences = []
        table_reader = xhtml.TableReader(html_text=self._text)

        for table_row_data in table_reader:
            feature_key = '/'.join(table_row_data.keys())
            feature_value = '/'.join(table_row_data.values())
            feature = '{}: {}'.format(feature_key, feature_value)

            raw_sentences.append(feature)

        return raw_sentences

    def _manage_raw_sentences_inline_breaks(
            self,
            raw_sentences: List[str]
    ) -> List[str]:

        if self._split_inline_breaks:
            raw_sentences = sentences.split_inline_breaks_to_sentences(
                sentences=raw_sentences,
                inline_breaks=self._inline_breaks
            )

        raw_sentences = sentences.remove_empty(raw_sentences)

        return raw_sentences

    def _filter_raw_sentences(self, raw_sentences: List[str]) -> List[str]:
        allow_keys = self._callow or self._allow

        if allow_keys:
            raw_sentences = sentences.allow_contains(
                sentences=raw_sentences,
                keys=allow_keys,
                case_sensitive=bool(self._callow)
            )

        deny_keys = self._cdeny or self._deny

        if deny_keys:
            raw_sentences = sentences.deny_contains(
                sentences=raw_sentences,
                keys=deny_keys,
                case_sensitive=bool(self._cdeny)
            )

        return raw_sentences

    def _normalize_raw_text(self, raw_text: Optional[Union[str, float, int]]):
        raw_text = utext.to_str(raw_text)

        if self._normalize:
            raw_text = utext.normalize_breaks(raw_text)
            raw_text = utext.normalize(raw_text)

        return raw_text
