import re
from typing import Any, List, Optional, Union, Tuple

from ftfy import fix_text
from number_parser import parse

from easytxt import config


def capitalize(text: str) -> str:
    return text[0].upper() + text[1:]


def capitalize_paragraph(text: str) -> str:
    return re.sub(
        r'([.?!]\s+|^)(\w+)',
        lambda m: m.group(1) + capitalize(m.group(2)),
        text
    )


def replace_chars_by_key(
        text: str,
        replace_key: str,
        replace_value: str
) -> str:

    if re.search(replace_key, text, flags=re.IGNORECASE):
        text: str = re.sub(
            replace_key,
            replace_value,
            text,
            flags=re.IGNORECASE
        )

    return text


def replace_chars_by_keys(
        text: str,
        replace_keys: List[Tuple[str, str]]
) -> str:

    for replace_key_tuple in replace_keys:
        replace_key, replace_value = replace_key_tuple

        text: str = replace_chars_by_key(
            text=text,
            replace_key=replace_key,
            replace_value=replace_value
        )

    return text


def remove_chars_by_keys(
        text: str,
        remove_keys: List[str]
):

    text_replacements = [(rc, '') for rc in remove_keys]

    return replace_chars_by_keys(text, text_replacements)


def has_stop_key(text: str) -> bool:
    text = text.strip()

    stop_keys = config.STOP_KEYS + config.STOP_KEYS_IGNORE

    return endswith_key(text, stop_keys)


def endswith_key(
        text: str,
        endswith_keys: Union[str, list]
) -> bool:

    if isinstance(endswith_keys, str):
        endswith_keys = [endswith_keys]

    return any(text.endswith(stop_key) for stop_key in endswith_keys)


def add_stop_key(
        text: str,
        stop_key: str = '.'
) -> str:

    if not has_stop_key(text):
        return '{}{}'.format(text.strip(), stop_key)

    return text


def remove_stop_key(
        text: str,
        stop_keys=None
) -> str:

    if stop_keys is None:
        stop_keys = config.STOP_KEYS

    text = text.strip()

    for stop_key in stop_keys:
        if text.endswith(stop_key):
            text = text.rstrip(stop_key)

            text = text.strip()

            break

    return text


def contains(
        text: str,
        keys: Union[List[str], str],
        case_sensitive: bool = False
) -> bool:

    if isinstance(keys, str):
        keys: list = [keys]

    ignore_case = 0 if case_sensitive else re.IGNORECASE

    for key in keys:
        if re.search(key, text, ignore_case):
            return True

    return False


def normalize_spaces(text: str) -> str:
    text = re.sub(r'\s\s+', ' ', text)
    return text.replace(' .', '.').strip()


def normalize_breaks(
        text: str,
        append_stops: bool = True
) -> str:

    sentences = []

    for raw_sentence in text.split('\n'):
        if len(raw_sentence) < 2:
            continue

        if append_stops and not has_stop_key(raw_sentence):
            raw_sentence = add_stop_key(raw_sentence)

        sentences.append(raw_sentence)

    return ' '.join(sentences)


def normalize(
        text: str,
        fix_spaces: bool = True,
        escape_new_lines: bool = False,
        new_line_replacement: str = ' '

) -> str:

    text = to_str(text)

    text = fix_text(text)

    if escape_new_lines:
        text = normalize_new_lines(
            text=text,
            new_line_replacement=new_line_replacement
        )

    if fix_spaces:
        text = normalize_spaces(text)

    return text.replace(':.', ':').strip()


def take(text: str, limit: int, strip=True):
    if limit == 0:
        raise ValueError('take limit cannot be 0!')

    if limit > len(text):
        return text

    text = text[0: limit]

    return text.strip() if strip else text


def skip(text: str, limit: int, strip=True):
    if limit > len(text):
        return ''

    text = text[limit:]

    return text.strip() if strip else text


def remove_inline_breaks(
        text: str,
        inline_breaks: List[str]
) -> str:

    text = text.strip()

    for inline_break in inline_breaks:
        if text.startswith(inline_break):
            text = text[1:]

        break

    return text.strip()


def normalize_new_lines(
        text: str,
        new_line_replacement: str = ' '
) -> str:

    return text.replace('\n', new_line_replacement)


def to_feature(
    text: str,
    split_keys: Optional[List[str]] = None
) -> Union[str, Tuple[str, str]]:

    if split_keys is None:
        split_keys = config.FEATURE_SPLIT_KEYS

    for split_key in split_keys:
        if split_key not in text:
            continue

        sentences = text.split(split_key)

        if len(sentences) == 1:
            return text

        feature_key = sentences[0]
        feature_value = split_key.join(sentences[1:])

        return (
            remove_stop_key(feature_key.strip()),
            remove_stop_key(feature_value.strip())
        )

    return text


def split_by_key(
        text: str,
        split_key: str,
        split_index: int = 0,
        case_sensitive: bool = False
) -> str:

    ignore_case = 0 if case_sensitive else re.IGNORECASE

    return re.split(split_key, text, ignore_case)[split_index]


def split_by_keys(
        text: str,
        split_keys: list,
        case_sensitive: bool = False
) -> str:

    for split_key in split_keys:
        if isinstance(split_key, tuple):
            sk, si = split_key
        else:
            sk, si = split_key, 0

        text = split_by_key(
            text=text,
            split_key=sk,
            split_index=si,
            case_sensitive=case_sensitive
        )

    return text


def to_str(
        value: Any,
        default: Optional[str] = ''
):

    if value is None:
        return default

    if isinstance(value, (int, float, bool)):
        value = str(value)

    return value


def to_numeric_from_text_num(text: str, language='en'):
    return parse(text, language=language)


def to_list(
        value: Any,
        split_key: Optional[str] = None,
        multiply_keys: Optional[Union[list, tuple]] = None
):

    if not value:
        return value

    value = to_str(value)

    if split_key:
        return [v.strip() for v in value.split(split_key)]

    if multiply_keys:
        multiple_values = []

        if isinstance(multiply_keys, tuple):
            multiply_keys = [multiply_keys]

        for replace_key, replace_values in multiply_keys:
            if replace_key not in value:
                continue

            for replace_value in replace_values:
                new_value = value.replace(replace_key, replace_value)
                multiple_values.append(new_value)

            if multiple_values:
                return multiple_values

    return [value]
