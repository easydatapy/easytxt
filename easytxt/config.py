STOP_KEYS = ['.', '!', '?']

STOP_KEYS_IGNORE = [':', '|', ';']

FEATURE_SPLIT_KEYS = [':', '|']

INLINE_BREAKS = [r'^\-', u'^\u2022', r'\*', '^•', u'^\t\x95', ' - ']

INLINE_TAGS = [
    'a', 'span', 'b', 'em', 'i', 'sub', 'sup', 'strong', 'abbr', 'small', 'br'
]

HTML_RE_VALIDATOR = (r'<(?=.*? .*?/ ?>|br|hr|input|!--|wbr)[a-z]+.*?>|'
                     r'<([a-z]+).*?</\1>')
