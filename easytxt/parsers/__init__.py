from typing import List, Optional, Union
from easytxt import text as utext


def parse_string(
        raw_text: Union[str, float, int, bytes],
        normalize: bool = True,
        language: str = 'en',
        replace_keys: Optional[list] = None,
        remove_keys: Optional[list] = None,
        split_key: Optional[Union[str, tuple]] = None,
        split_keys: Optional[List[Union[str, tuple]]] = None,
        fix_spaces: bool = True,
        escape_new_lines: bool = False,
        text_num_to_numeric: bool = False,
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
        raw_text = utext.from_split_keys(
            text=raw_text,
            split_keys=split_keys
        )

    if text_num_to_numeric:
        raw_text = utext.to_numeric_from_text_num(
            text=raw_text,
            language=language
        )

    return utext.normalize_spaces(raw_text)
