from typing import List, Optional, Union

from pyquery import PyQuery

from easytxt import text as utext

__all__ = ("parse_string",)


def parse_string(
    raw_text: Optional[Union[str, float, int, bytes, PyQuery]],
    normalize: bool = True,
    capitalize: bool = False,
    title: bool = False,
    uppercase: bool = False,
    lowercase: bool = False,
    replace_keys: Optional[list] = None,
    remove_keys: Optional[list] = None,
    split_key: Optional[Union[str, tuple]] = None,
    split_keys: Optional[List[Union[str, tuple]]] = None,
    take: Optional[int] = None,
    take_strip: bool = True,
    skip: Optional[int] = None,
    skip_strip: bool = True,
    text_num_to_numeric: bool = False,
    language: str = "en",
    fix_spaces: bool = True,
    escape_new_lines: bool = True,
    new_line_replacement: str = " ",
    add_stop: Optional[Union[bool, str]] = None,
) -> str:

    split_keys = [split_key] if split_key else split_keys

    raw_text = utext.to_str(raw_text)

    if normalize:
        raw_text = utext.normalize(
            text=raw_text,
            fix_spaces=fix_spaces,
            escape_new_lines=escape_new_lines,
            new_line_replacement=new_line_replacement,
        )

    raw_text = _parse_string_chars(
        raw_text=raw_text,
        replace_keys=replace_keys,
        remove_keys=remove_keys,
        split_keys=split_keys,
        text_num_to_numeric=text_num_to_numeric,
        language=language,
    )

    raw_text = _parse_string_case(
        raw_text=raw_text,
        capitalize=capitalize,
        title=title,
        uppercase=uppercase,
        lowercase=lowercase,
    )

    if fix_spaces:
        raw_text = utext.normalize_spaces(raw_text)

    raw_text = _parse_string_char_limit(
        raw_text=raw_text,
        take=take,
        take_strip=take_strip,
        skip=skip,
        skip_strip=skip_strip,
    )

    if add_stop:
        if isinstance(add_stop, bool):
            stop_key = "."
        else:
            stop_key = add_stop

        raw_text = utext.add_stop_key(text=raw_text, stop_key=stop_key)

    return raw_text


def _parse_string_chars(
    raw_text: str,
    replace_keys: Optional[list] = None,
    remove_keys: Optional[list] = None,
    split_keys: Optional[List[Union[str, tuple]]] = None,
    text_num_to_numeric: bool = False,
    language: str = "en",
) -> str:

    if replace_keys:
        raw_text = utext.replace_chars_by_keys(
            text=raw_text,
            replace_keys=replace_keys,
        )

    if remove_keys:
        raw_text = utext.remove_chars_by_keys(
            text=raw_text,
            remove_keys=remove_keys,
        )

    if split_keys:
        raw_text = utext.split_by_keys(
            text=raw_text,
            split_keys=split_keys,
        )

    if text_num_to_numeric:
        raw_text = utext.to_numeric_from_text_num(
            text=raw_text,
            language=language,
        )

    return raw_text


def _parse_string_case(
    raw_text: str,
    capitalize: bool = False,
    title: bool = False,
    uppercase: bool = False,
    lowercase: bool = False,
) -> str:

    if capitalize:
        raw_text = utext.capitalize(raw_text)
    elif title:
        raw_text = raw_text.title()
    elif uppercase:
        raw_text = raw_text.upper()
    elif lowercase:
        raw_text = raw_text.lower()

    return raw_text


def _parse_string_char_limit(
    raw_text: str,
    take: Optional[int] = None,
    take_strip: bool = True,
    skip: Optional[int] = None,
    skip_strip: bool = True,
) -> str:

    if take and raw_text:
        raw_text = utext.take(
            text=raw_text,
            limit=take,
            strip=take_strip,
        )

    if skip and raw_text:
        raw_text = utext.skip(
            text=raw_text,
            limit=skip,
            strip=skip_strip,
        )

    return raw_text
