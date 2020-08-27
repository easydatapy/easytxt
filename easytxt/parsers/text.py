import re
from typing import List, Optional, Union, Tuple

from easytxt import html
from easytxt import sentences
from easytxt import text as utext
from easytxt.parsers.base import BaseTextParser


class TextParser(BaseTextParser):
    cached_sentences = []
    cached_features = []

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
        if self._autodetect_html and html.validate(self._text):
            html_raw_sentences = html.to_sentences(
                html_text=self._text,
                css_query=self._css_query,
                exclude_css=self._exclude_css
            )

            raw_sentences = []

            for html_raw_sentence in html_raw_sentences:
                raw_sentences += self._text_to_raw_sentences(
                    html_raw_sentence
                )

        else:
            raw_sentences = self._text_to_raw_sentences(self._text)

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

        return raw_sentences

    def _text_to_raw_sentences(self, raw_text: str) -> List[str]:
        raw_text = self._normalize_raw_text(raw_text)

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
        elif self._capitalize:
            raw_sentences = sentences.capitalize(raw_sentences)

        return raw_sentences
