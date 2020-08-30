from typing import List, Optional, Union
from easytxt import text as utext
from easytxt.parsers.text import TextParser


def parse_string(
        raw_text: Union[str, float, int, bytes],
        normalize: bool = True,
        capitalize: bool = False,
        title: bool = False,
        uppercase: bool = False,
        lowercase: bool = False,
        replace_keys: Optional[list] = None,
        remove_keys: Optional[list] = None,
        split_key: Optional[Union[str, tuple]] = None,
        split_keys: Optional[List[Union[str, tuple]]] = None,
        max_chars: Optional[int] = None,
        text_num_to_numeric: bool = False,
        language: str = 'en',
        fix_spaces: bool = True,
        escape_new_lines: bool = True,
        new_line_replacement: str = ' ',
        add_stop: Optional[Union[bool, str]] = None
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

    if replace_keys:
        raw_text = utext.replace_chars_by_keys(
            text=raw_text,
            replace_keys=replace_keys
        )

    if remove_keys:
        raw_text = utext.remove_chars_by_keys(
            text=raw_text,
            remove_keys=remove_keys
        )

    if split_keys:
        raw_text = utext.split_by_keys(
            text=raw_text,
            split_keys=split_keys
        )

    if text_num_to_numeric:
        raw_text = utext.to_numeric_from_text_num(
            text=raw_text,
            language=language
        )

    if capitalize:
        raw_text = utext.capitalize(raw_text)
    elif title:
        raw_text = raw_text.title()
    elif uppercase:
        raw_text = raw_text.upper()
    elif lowercase:
        raw_text = raw_text.lower()

    if fix_spaces:
        raw_text = utext.normalize_spaces(raw_text)

    if max_chars and raw_text and len(raw_text) >= max_chars:
        raw_text = utext.max_chars_limit(raw_text, max_chars)

    if add_stop:
        if add_stop is True:
            stop_key = '.'
        else:
            stop_key = add_stop

        raw_text = utext.add_stop_key(raw_text, stop_key)

    return raw_text
