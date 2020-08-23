import re
from typing import List, Optional, Union

from easytxt import abbreviations, constants, text as utext


def from_text(
        text: str,
        language: str = 'en',
        split_inline_breaks: bool = True,
        inline_breaks: Optional[List[str]] = None,
        min_char_len: int = 5
) -> List[str]:

    abbr_re = _get_abbr_re_pattern(language)

    raw_text = utext.normalize_spaces(text)

    stop_re = re.compile(r'([\.\?\!]\s+)')

    sentences = []

    text_parts = []

    for raw_sentence in stop_re.split(raw_text):
        sentence = ''.join(text_parts)

        if raw_sentence and text_parts and len(sentence) >= min_char_len:
            if stop_re.match(text_parts[-1]) and not abbr_re.search(sentence):
                sentences.append(sentence)

                text_parts = []

        if raw_sentence:
            text_parts.append(raw_sentence)

    if text_parts:
        sentences.append(''.join(text_parts))

    sentences = [sen.strip() for sen in sentences if sen.strip()]

    if split_inline_breaks:
        sentences = split_inline_breaks_to_sentences(
            sentences=sentences,
            inline_breaks=inline_breaks
        )

    return remove_empty(sentences)


def merge(
        sentences: list,
        merge_keys: Optional[List[str]] = None
) -> List[str]:

    if merge_keys is None:
        merge_keys = constants.MERGE_KEYS

    merged_sentences = []

    while sentences:
        sentence = sentences.pop(0)

        if sentences and utext.endswith_key(sentence, merge_keys):
            next_sentence = sentences.pop(0)

            sentence = '{} {}'.format(sentence, next_sentence)

        merged_sentences.append(sentence)

    return merged_sentences


def add_stop(
        sentences: List[str],
        stop_key: str = '.'
) -> List[str]:

    return [utext.add_stop_key(sentence, stop_key) for sentence in sentences]


def capitalize_sentence(sentences: List[str]) -> List[str]:
    return [utext.capitalize(sentence) for sentence in sentences]


def replace_chars_by_keys(
        sentences: List[str],
        text_replacements: list
) -> List[str]:

    return [utext.replace_chars_by_keys(sentence, text_replacements)
            for sentence in sentences]


def split_inline_breaks_to_sentences(
        sentences: list,
        inline_breaks: Optional[List[str]] = None
):
    if inline_breaks is None:
        inline_breaks = constants.INLINE_BREAKS
    else:
        inline_breaks += constants.INLINE_BREAKS

    inline_breaks_re = u'{}'.format('|'.join(inline_breaks))

    new_sentences = []

    for sentence in sentences:
        new_sentences = new_sentences + re.split(inline_breaks_re, sentence)

    return [new_sentence.strip() for new_sentence in new_sentences
            if new_sentence.strip()]


def remove_empty(sentences: list) -> List[str]:
    return [sentence for sentence in sentences if sentence and len(sentence) > 2]


def allow_contains(
        sentences: list,
        keys=Union[List[str], str],
        case_sensitive: bool = False
) -> List[str]:

    return [sentence for sentence in sentences
            if utext.contains(sentence, keys, case_sensitive)]


def deny_contains(
        sentences: list,
        keys=Union[List[str], str],
        case_sensitive: bool = False
) -> List[str]:

    return [sentence for sentence in sentences
            if not utext.contains(sentence, keys, case_sensitive)]


def to_text(
        sentences: List[str],
        separator: str = ' '
) -> str:

    return separator.join(sentences)


def _get_abbr_re_pattern(language='en'):
    abbr_list = getattr(abbreviations, language)
    abbr_pattern = r'(?:{})\.\s*$'.format(r'|\s'.join(abbr_list))
    return re.compile(abbr_pattern, re.IGNORECASE)
