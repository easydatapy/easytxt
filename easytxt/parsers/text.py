import re
from typing import List, Optional, Union, Tuple

from easytxt import html
from easytxt import sentences
from easytxt import text as utext


class TextParser:
    cached_sentences = []
    cached_features = []

    def __init__(
            self,
            text: Optional[Union[str, float, int]] = None,
            language: str = 'en',
            css_query: Optional[str] = None,
            exclude_css: Optional[Union[List[str], str]] = None,
            allow: Optional[Union[str, List[str]]] = None,
            callow: Optional[Union[str, List[str]]] = None,
            from_allow: Optional[Union[str, List[str]]] = None,
            from_callow: Optional[Union[str, List[str]]] = None,
            to_allow: Optional[Union[str, List[str]]] = None,
            to_callow: Optional[Union[str, List[str]]] = None,
            deny: Optional[Union[str, List[str]]] = None,
            cdeny: Optional[Union[str, List[str]]] = None,
            normalize: bool = True,
            capitalize: bool = True,
            title: bool = False,
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
            text_num_to_numeric: bool = False,
            autodetect_html: bool = True
    ):

        self._text = text
        self._language = language
        self._css_query = css_query
        self._exclude_css = exclude_css
        self._allow = allow
        self._callow = callow
        self._from_allow = from_allow
        self._from_callow = from_callow
        self._to_allow = to_allow
        self._to_callow = to_callow
        self._deny = deny
        self._cdeny = cdeny
        self._normalize = normalize
        self._capitalize = capitalize
        self._title = title
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
        self._text_num_to_numeric = text_num_to_numeric
        self._autodetect_html = autodetect_html

    def __iter__(self):
        for sentence in self.sentences:
            yield sentence

    def __str__(self):
        return self.text

    def __len__(self):
        return len(self.sentences)

    def __add__(self, raw_sentences):
        if isinstance(raw_sentences, str):
            raw_sentences = [raw_sentences]

        raw_sentences = self._process_raw_sentences(raw_sentences)

        self.cached_sentences = self.sentences + raw_sentences

        return self

    def __radd__(self, raw_sentences):
        if isinstance(raw_sentences, str):
            raw_sentences = [raw_sentences]

        raw_sentences = self._process_raw_sentences(raw_sentences)

        self.cached_sentences = raw_sentences + self.sentences

        return self

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
        if self._autodetect_html and html.validate(self._text):
            raw_sentences = self._html_text_to_raw_sentences(self._text)
        else:
            raw_sentences = self._text_to_raw_sentences(self._text)

        return self._process_raw_sentences(raw_sentences)

    def _process_raw_sentences(self, raw_sentences) -> List[str]:
        if self._merge_sentences:
            raw_sentences = sentences.merge(
                sentences=raw_sentences,
                stop_keys_ignore=self._stop_keys_ignore
            )

        if self._replace_keys:
            raw_sentences = sentences.replace_chars_by_keys(
                sentences=raw_sentences,
                replace_keys=self._replace_keys
            )

        if self._remove_keys:
            raw_sentences = sentences.remove_chars_by_keys(
                sentences=raw_sentences,
                remove_keys=self._remove_keys
            )

        raw_sentences = self._min_chars_limit(raw_sentences)

        raw_sentences = sentences.add_stop(
            sentences=raw_sentences,
            stop_key=self._stop_key
        )

        raw_sentences = self._sentences_manage_case(raw_sentences)

        if self._text_num_to_numeric:
            raw_sentences = self._convert_text_num_to_numeric_in_sentences(
                raw_sentences
            )

        return raw_sentences

    def _html_text_to_raw_sentences(self, html_raw_text: str) -> List[str]:
        raw_text = self._manage_keys_raw_text(html_raw_text)

        html_raw_sentences = html.to_sentences(
            html_text=raw_text,
            css_query=self._css_query,
            exclude_css=self._exclude_css
        )

        raw_sentences = []

        for html_raw_sentence in html_raw_sentences:
            raw_sentences += self._text_to_raw_sentences(
                html_raw_sentence
            )

        return raw_sentences

    def _text_to_raw_sentences(self, raw_text: str) -> List[str]:
        raw_text = self._normalize_raw_text(raw_text)

        raw_text = self._manage_keys_raw_text(raw_text)

        return sentences.from_text(
            text=raw_text,
            language=self._language,
            stop_keys=self._stop_keys_split,
            split_inline_breaks=self._split_inline_breaks,
            inline_breaks=self._inline_breaks,
            min_chars=self._min_chars
        )

    def _filter_raw_sentences(self, raw_sentences: List[str]) -> List[str]:
        allow_keys = self._callow or self._allow

        if allow_keys:
            raw_sentences = sentences.allow_contains(
                sentences=raw_sentences,
                keys=allow_keys,
                case_sensitive=bool(self._callow)
            )

        from_allow_keys = self._from_allow or self._from_callow

        if from_allow_keys:
            raw_sentences = sentences.from_allow_contains(
                sentences=raw_sentences,
                keys=from_allow_keys,
                case_sensitive=bool(self._from_callow)
            )

        to_allow_keys = self._to_allow or self._to_callow

        if to_allow_keys:
            raw_sentences = sentences.to_allow_contains(
                sentences=raw_sentences,
                keys=to_allow_keys,
                case_sensitive=bool(self._to_callow)
            )

        deny_keys = self._cdeny or self._deny

        if deny_keys:
            raw_sentences = sentences.deny_contains(
                sentences=raw_sentences,
                keys=deny_keys,
                case_sensitive=bool(self._cdeny)
            )

        return raw_sentences

    def _min_chars_limit(self, raw_sentences: List[str]) -> List[str]:
        return [rs for rs in raw_sentences if len(rs) >= self._min_chars]

    def _normalize_raw_text(self, raw_text: Optional[Union[str, float, int]]):
        raw_text = utext.to_str(raw_text)

        if self._normalize:
            raw_text = utext.normalize_breaks(raw_text)
            raw_text = utext.normalize(raw_text)

        return raw_text

    def _sentences_manage_case(self, raw_sentences: List[str]) -> List[str]:
        if self._lowercase:
            raw_sentences = sentences.lowercase(raw_sentences)
        elif self._uppercase:
            raw_sentences = sentences.uppercase(raw_sentences)
        elif self._title:
            raw_sentences = sentences.title(raw_sentences)
        elif self._capitalize:
            raw_sentences = sentences.capitalize(raw_sentences)

        return raw_sentences

    def _convert_text_num_to_numeric_in_sentences(
            self,
            raw_sentences: List[str]
    ) -> List[str]:

        return [
            utext.to_numeric_from_text_num(rs, language=self._language)
            for rs in raw_sentences
        ]

    def _manage_keys_raw_text(self, raw_text: str):
        if self._replace_keys_raw_text:
            raw_text = utext.replace_chars_by_keys(
                text=raw_text,
                replace_keys=self._replace_keys_raw_text
            )

        if self._remove_keys_raw_text:
            raw_text = utext.remove_chars_by_keys(
                text=raw_text,
                remove_keys=self._remove_keys_raw_text
            )

        return raw_text
