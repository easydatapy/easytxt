import re
from typing import List, Optional, Union

from easytxt import abbreviations, config, text as utext


def from_text(
        text: str,
        language: str = 'en',
        stop_keys: Optional[List[str]] = None,
        split_inline_breaks: bool = True,
        inline_breaks: Optional[List[str]] = None,
        min_chars: int = 5
) -> List[str]:

    if not stop_keys:
        stop_keys = config.STOP_KEYS

    stop_re = re.compile(r'([{}]\s+)'.format(''.join(stop_keys)))

    abbr_re = _get_abbr_re_pattern(language)

    raw_text = utext.normalize_spaces(text)

    sentences = []

    text_parts = []

    for raw_sentence in stop_re.split(raw_text):
        sentence = ''.join(text_parts)

        if raw_sentence and text_parts and len(sentence) >= min_chars:
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
        stop_keys_ignore: Optional[List[str]] = None
) -> List[str]:

    if stop_keys_ignore is None:
        stop_keys_ignore = config.STOP_KEYS_IGNORE

    merged_sentences = []

    while sentences:
        sentence = sentences.pop(0)

        if sentences and utext.endswith_key(sentence, stop_keys_ignore):
            next_sentence = sentences.pop(0)

            sentence = '{} {}'.format(sentence, next_sentence)

        merged_sentences.append(sentence)

    return merged_sentences


def add_stop(
        sentences: List[str],
        stop_key: str = '.'
) -> List[str]:

    return [utext.add_stop_key(sentence, stop_key) for sentence in sentences]


def capitalize(sentences: List[str]) -> List[str]:
    return [utext.capitalize(sentence) for sentence in sentences]


def title(sentences: List[str]) -> List[str]:
    return [sentence.title() for sentence in sentences if sentence]


def uppercase(sentences: List[str]) -> List[str]:
    return [sentence.upper() for sentence in sentences if sentence]


def lowercase(sentences: List[str]) -> List[str]:
    return [sentence.lower() for sentence in sentences if sentence]


def replace_chars_by_keys(
        sentences: List[str],
        replace_keys: list
) -> List[str]:

    sentences = [utext.replace_chars_by_keys(sentence, replace_keys)
                 for sentence in sentences]
    return [utext.normalize_spaces(sentence) for sentence in sentences]


def remove_chars_by_keys(
        sentences: List[str],
        remove_keys: list
) -> List[str]:

    sentences = [utext.remove_chars_by_keys(sentence, remove_keys)
                 for sentence in sentences]
    return [utext.normalize_spaces(sentence) for sentence in sentences]


def split_inline_breaks_to_sentences(
        sentences: list,
        inline_breaks: Optional[List[str]] = None
):
    if inline_breaks is None:
        inline_breaks = config.INLINE_BREAKS
    else:
        inline_breaks += config.INLINE_BREAKS

    inline_breaks_re = u'{}'.format('|'.join(inline_breaks))

    new_sentences = []

    for sentence in sentences:
        new_sentences = new_sentences + re.split(inline_breaks_re, sentence)

    return [new_sentence.strip() for new_sentence in new_sentences
            if new_sentence.strip()]


def remove_empty(sentences: list) -> List[str]:
    return [sentence for sentence in sentences if sentence and len(sentence) > 2]


def allow_contains(
        sentences: List[str],
        keys=Union[List[str], str],
        case_sensitive: bool = False
) -> List[str]:

    return [sentence for sentence in sentences
            if utext.contains(sentence, keys, case_sensitive)]


def from_allow_contains(
        sentences: List[str],
        keys=Union[List[str], str],
        case_sensitive: bool = False
):

    allowed_sentences = []

    for sentence in sentences:
        if allowed_sentences:
            allowed_sentences.append(sentence)
        else:
            if utext.contains(sentence, keys, case_sensitive):
                allowed_sentences.append(sentence)

    return allowed_sentences


def to_allow_contains(
        sentences: List[str],
        keys=Union[List[str], str],
        case_sensitive: bool = False
):

    allowed_sentences = []

    for sentence in sentences:
        if utext.contains(sentence, keys, case_sensitive):
            break

        allowed_sentences.append(sentence)

    return allowed_sentences


def deny_contains(
        sentences: List[str],
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
