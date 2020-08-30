from easytxt.parsers import parse_string


def test_parse_string_normalize_default():
    test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    assert parse_string(test_text) == 'Easybook Pro 13 <3 ünicode'


def test_parse_string_normalize_false():
    test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    parsed_string = parse_string(test_text, normalize=False)
    assert parsed_string == 'Easybook Pro 13 &lt;3 uÌˆnicode'


def test_parse_string_capitalize():
    test_text = 'easybook PRO 15'
    # Lets test first with default settings capitalize=False
    assert parse_string(test_text) == 'easybook PRO 15'

    test_text = 'easybook PRO 15'
    assert parse_string(test_text, capitalize=True) == 'Easybook PRO 15'


def test_parse_string_title():
    test_text = 'easybook PRO 15'
    assert parse_string(test_text, title=True) == 'Easybook Pro 15'


def test_parse_string_uppercase():
    test_text = 'easybook PRO 15'
    assert parse_string(test_text, uppercase=True) == 'EASYBOOK PRO 15'


def test_parse_string_lowercase():
    test_text = 'easybook PRO 15'
    assert parse_string(test_text, lowercase=True) == 'easybook pro 15'


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


def test_parse_string_max_chars():
    test_text = 'Easybook Pro 13'
    assert parse_string(test_text, max_chars=8) == 'Easybook'


def test_parse_string_fix_spaces():
    test_text = 'Easybook   Pro  15'
    # Lets test first with default settings
    assert parse_string(raw_text=test_text) == 'Easybook Pro 15'

    parsed_string = parse_string(
        raw_text=test_text,
        fix_spaces=False
    )
    assert parsed_string == 'Easybook   Pro  15'


def test_parse_string_escape_new_lines():
    test_text = 'Easybook\nPro\n15'
    # Lets test first with default settings
    assert parse_string(test_text) == 'Easybook Pro 15'

    parsed_string = parse_string(
        raw_text=test_text,
        escape_new_lines=False
    )
    assert parsed_string == 'Easybook\nPro\n15'


def test_parse_string_new_line_replacement():
    test_text = 'Easybook\nPro\n15'
    parsed_string = parse_string(
        raw_text=test_text,
        new_line_replacement='|'
    )
    assert parsed_string == 'Easybook|Pro|15'


def test_parse_string_text_num_to_numeric():
    test_text = 'two thousand and three words for the first time'
    parsed_string = parse_string(test_text, text_num_to_numeric=True)
    assert parsed_string == '2003 words for the 1 time'


def test_parse_string_add_stop():
    # Lets test default
    test_text = 'Easybook Pro 15'
    assert parse_string(test_text) == 'Easybook Pro 15'

    test_text = 'Easybook Pro 15'
    parsed_string = parse_string(
        raw_text=test_text,
        add_stop=True
    )
    assert parsed_string == 'Easybook Pro 15.'

    # Test add stop if already exists
    test_text = 'Easybook Pro 15!'
    parsed_string = parse_string(
        raw_text=test_text,
        add_stop=True
    )
    assert parsed_string == 'Easybook Pro 15!'


def test_parse_string_stop_key():
    test_text = 'Easybook Pro 15'
    parsed_string = parse_string(
        raw_text=test_text,
        add_stop='!'
    )
    assert parsed_string == 'Easybook Pro 15!'
