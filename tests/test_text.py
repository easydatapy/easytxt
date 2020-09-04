import pytest

from easytxt import text


def test_capitalize() -> None:
    assert text.capitalize('hello World!') == 'Hello World!'


def test_capitalize_paragraph():
    test_text = 'hello World !   how are you? i am fine. tomorrow'

    final_text = text.capitalize_paragraph(test_text)
    assert final_text == 'Hello World !   How are you? I am fine. Tomorrow'


@pytest.mark.parametrize(
    'test_data, rkey, rvalue, result',
    [
        ('It\'s a world.', 'world', 'city', 'It\'s a city.'),
    ]
)
def test_replace_chars_by_key(test_data, rkey, rvalue, result):
    assert text.replace_chars_by_key(test_data, rkey, rvalue) == result


@pytest.mark.parametrize(
    'test_data, replace_keys, result',
    [
        (
                'It\'s a Beautiful world.',
                [
                    ('beautiful', 'fine'),
                    ('world', 'town')
                ],
                'It\'s a fine town.'
        ),
    ]
)
def test_replace_chars_by_keys(test_data, replace_keys, result):
    assert text.replace_chars_by_keys(test_data, replace_keys) == result


@pytest.mark.parametrize(
    'test_data, result',
    [
        ('It\'s a beautiful world!', True),
        ('It\'s a beautiful world.', True),
        ('It\'s a beautiful world?   ', True),
        ('It\'s a beautiful world:', True),
        ('It\'s a beautiful world;', True),
        ('It\'s a beautiful world(', False),
        ('It\'s a beautiful world-', False),
        ('It\'s a beautiful world    ', False)
    ]
)
def test_has_stop_key(test_data, result):
    assert text.has_stop_key(test_data) is result


@pytest.mark.parametrize(
    'test_data, endswith_keys, result',
    [
        ('Hell:', ':', True),
        ('Hell:', '?', False),
        ('Hell?', ['-', ',', '?', ':'], True),
    ]
)
def test_endswith_key(test_data, endswith_keys, result):
    assert text.endswith_key('Hell:', ':')


@pytest.mark.parametrize(
    'test_data, stop_key, result',
    [
        ('It\'s a nice world', '.', 'It\'s a nice world.'),
        ('It\'s a world', '!', 'It\'s a world!'),
    ]
)
def test_add_stop_key(test_data, stop_key, result) -> None:
    assert text.add_stop_key(test_data, stop_key) == result


@pytest.mark.parametrize(
    'test_data, result',
    [
        ('It\'s a nice world.', 'It\'s a nice world'),
        ('It\'s a nice world?', 'It\'s a nice world'),
        ('It\'s a beautiful world!', 'It\'s a beautiful world'),
        ('It\'s a nice world?     ', 'It\'s a nice world'),
        ('It\'s a nice world ?', 'It\'s a nice world'),
    ]
)
def test_remove_stop_key(test_data, result) -> None:
    assert text.remove_stop_key(test_data) == result


@pytest.mark.parametrize(
    'test_data, stop_keys, result',
    [
        ('It\'s a world-', ['-'], 'It\'s a world'),
    ]
)
def test_remove_stop_key_custom(test_data, stop_keys, result) -> None:
    assert text.remove_stop_key(test_data, stop_keys) == result


@pytest.mark.parametrize(
    'test_data, keys, result',
    [
        ('Hello World!,', 'world', True),
        ('Hello World!', ['city', 'world'], True),
    ]
)
def test_contains(test_data, keys, result) -> None:
    assert text.contains(test_data, keys) is result


@pytest.mark.parametrize(
    'test_data, keys, case_sensitive, result',
    [
        ('Hello World!,', 'World', True, True),
        ('Hello World!,', 'world', True, False),
        ('Hello World!', ['city', 'World'], True, True),
    ]
)
def test_contains_case(test_data, keys, case_sensitive, result) -> None:
    assert text.contains(test_data, keys, case_sensitive) == result


@pytest.mark.parametrize(
    'test_data, result',
    [
        ('Some text   is here  ', 'Some text is here'),
        ('Some text   is here  .', 'Some text is here.')
    ]
)
def test_normalize_spaces(test_data, result) -> None:
    assert text.normalize(test_data) == result


@pytest.mark.parametrize(
    'test_data, result',
    [
        (
                'Hello World\n\nHow are you.\nBy by',
                'Hello World. How are you. By by.'
        ),
    ]
)
def test_normalize_breaks(test_data, result) -> None:
    assert text.normalize_breaks(test_data) == result


@pytest.mark.parametrize(
    'test_data, result',
    [
        (
                'Hello World\n\nHow are you.\nBy by',
                'Hello World How are you. By by'
        ),
    ]
)
def test_normalize_breaks_append_stops_false(test_data, result) -> None:
    assert text.normalize_breaks(test_data, False) == result


@pytest.mark.parametrize(
    'test_data, result',
    [
        ('uÌˆnicode', 'ünicode'),
        ('HTML entities &lt;3', 'HTML entities <3'),
    ]
)
def test_normalize(test_data, result) -> None:
    assert text.normalize(test_data) == result


@pytest.mark.parametrize(
    'test_data, result',
    [
        (1234, '1234'),
        (1234.25, '1234.25'),
        ('1234.25', '1234.25'),
    ]
)
def test_to_string(test_data, result) -> None:
    assert text.to_str(test_data) == result


@pytest.mark.parametrize(
    'test_data, split_key, result',
    [
        ('1,2,3 ,4', ',', ['1', '2', '3', '4']),
    ]
)
def test_to_list_split_key(test_data, split_key, result) -> None:
    assert text.to_list('1,2,3 ,4', ',') == ['1', '2', '3', '4']


@pytest.mark.parametrize(
    'test_data, multiply_keys, result',
    [
        (
                'its-one-s',
                ('-one-', ['-one-', '-two-', '-three-']),
                ['its-one-s', 'its-two-s', 'its-three-s']
        ),
        (
                'its-one-s',
                [
                    ('-two-', ['-two-', '-one-']),
                    ('-one-', ['-one-', '-two-', '-three-'])
                ],
                ['its-one-s', 'its-two-s', 'its-three-s']
        ),
    ]
)
def test_to_list_multiply_keys(test_data, multiply_keys, result) -> None:
    assert text.to_list(test_data, multiply_keys=multiply_keys) == result


@pytest.mark.parametrize(
    'test_data, inline_breaks, result',
    [
        ('* camera', ['*'], 'camera'),
    ]
)
def test_remove_inline_breaks(test_data, inline_breaks, result):
    assert text.remove_inline_breaks(test_data, inline_breaks) == result
