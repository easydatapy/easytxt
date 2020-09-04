import pytest

from easytxt.parsers import parse_string

from tests.factory import string_samples


@pytest.mark.parametrize(
    'test_data, result',
    string_samples.english
)
def test_parse_string(test_data, result):
    assert parse_string(test_data) == result


def test_parse_string_normalize_false():
    test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    parsed_string = parse_string(test_text, normalize=False)
    assert parsed_string == 'Easybook Pro 13 &lt;3 uÌˆnicode'


def test_parse_string_capitalize():
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


@pytest.mark.parametrize(
    'split_key, test_data, result',
    [
        ('-', 'easybook-pro_13', 'easybook'),
        (('-', -1), 'easybook-pro_13', 'pro_13'),
    ]
)
def test_parse_string_split_key(split_key, test_data, result):
    assert parse_string(test_data, split_key=split_key) == result


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


@pytest.mark.parametrize(
    'take, test_data, result',
    [
        (1, 'Easybook', 'E'),
        (8, 'Easybook Pro 13', 'Easybook'),
        # To check if empty space gets stripped by default
        (9, 'Easybook Pro 13', 'Easybook'),
        (30, 'Easybook Pro 13', 'Easybook Pro 13'),
    ]
)
def test_parse_string_take(take, test_data, result):
    assert parse_string(test_data, take=take) == result


@pytest.mark.parametrize(
    'skip, test_data, result',
    [
        (8, 'Easybook Pro 13', 'Pro 13'),
        (0, 'Easybook Pro 13', 'Easybook Pro 13'),
        (30, 'Easybook Pro 13', ''),
    ]
)
def test_parse_string_skip(skip, test_data, result):
    assert parse_string(test_data, skip=skip) == result


def test_parse_string_fix_spaces_false():
    test_text = 'Easybook   Pro  15'

    parsed_string = parse_string(
        raw_text=test_text,
        fix_spaces=False
    )
    assert parsed_string == 'Easybook   Pro  15'


def test_parse_string_escape_new_lines():
    test_text = 'Easybook\nPro\n15'

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


@pytest.mark.parametrize(
    'add_stop, test_data, result',
    [
        (True, 'Easybook Pro 15', 'Easybook Pro 15.'),
        (True, 'Easybook Pro 15!', 'Easybook Pro 15!'),
        ('!', 'Easybook Pro 15', 'Easybook Pro 15!'),
    ]
)
def test_parse_string_add_stop(add_stop, test_data, result):
    parsed_string = parse_string(
        raw_text=test_data,
        add_stop=add_stop
    )
    assert parsed_string == result
