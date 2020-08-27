from typing import List, Optional, Union
from easytxt import text as utext


def parse_string(
        raw_text: Union[str, float, int, bytes],
        normalize: bool = True,
        replace_keys: Optional[list] = None,
        remove_keys: Optional[list] = None,
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

    return utext.normalize_spaces(raw_text)