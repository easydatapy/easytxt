from easytxt.parsers import parse_string


def test_parse_string_normalize_default():
    test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    assert parse_string(test_text) == 'Easybook Pro 13 <3 ünicode'


def test_parse_string_normalize_false():
    test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    parsed_string = parse_string(test_text, normalize=False)
    assert parsed_string == 'Easybook Pro 13 &lt;3 uÌˆnicode'


def test_parse_string_replace_keys():
    test_text = 'Easybook Pro 15'
    parsed_string = parse_string(
        raw_text=test_text,
        replace_keys=[
            ('pro', 'Air'),
            ('15', '13')
        ]
    )
    assert parsed_string == 'Easybook Air 13'


def test_parse_string_remove_keys():
    test_text = 'Easybook Pro 15'
    parsed_string = parse_string(
        raw_text=test_text,
        remove_keys=['easy', 'pro']
    )
    assert parsed_string == 'book 15'


def test_parse_string_split_key():
    test_text = 'easybook-pro_13'
    parsed_string = parse_string(test_text, split_key='-')
    assert parsed_string == 'easybook'

    parsed_string = parse_string(
        test_text,
        split_key=('-', -1)  # custom index
    )
    assert parsed_string == 'pro_13'


def test_parse_string_split_keys():
    test_text = 'easybook-pro_13'
    parsed_string = parse_string(
        test_text,
        split_keys=[
            ('-', -1),
            '_'
        ]
    )
    assert parsed_string == 'pro'
