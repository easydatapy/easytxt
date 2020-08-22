from easytxt import text


def test_capitalize() -> None:
    assert text.capitalize('hello World!') == 'Hello World!'


def test_capitalize_paragraph():
    test_text = 'hello World !   how are you? i am fine. tomorrow'
    final_text = text.capitalize_paragraph(test_text)
    assert final_text == 'Hello World !   How are you? I am fine. Tomorrow'


def test_replace_chars_by_key():
    test_text = 'It\'s a beautiful world.'
    final_text = text.replace_chars_by_key(test_text, 'world', 'city')
    assert final_text == 'It\'s a beautiful city.'


def test_replace_chars_by_keys():
    test_text = 'It\'s a Beautiful world.'
    replace_values = [
        ('beautiful', 'fine'),
        ('world', 'town')
    ]
    final_text = text.replace_chars_by_keys(test_text, replace_values)
    assert final_text == 'It\'s a fine town.'


def test_has_stop_key():
    assert text.has_stop_key('It\'s a beautiful world!')
    assert text.has_stop_key('It\'s a beautiful world.')
    assert text.has_stop_key('It\'s a beautiful world? ')
    assert text.has_stop_key('It\'s a beautiful world:')


def test_has_stop_key_false():
    assert not text.has_stop_key('It\'s a beautiful world ')
    assert not text.has_stop_key('It\'s a beautiful world-')


def test_endswith_key():
    assert text.endswith_key('Hell:', ':')


def test_endswith_false():
    assert not text.endswith_key('Hell:', '?')


def test_endswith_key_custom_endswith_keys():
    assert text.endswith_key('Hell?', ['-', ',', '?', ':'])


def test_add_stop_key() -> None:
    assert text.add_stop_key('It\'s a nice world') == 'It\'s a nice world.'


def test_add_stop_key_custom_stop_key() -> None:
    assert text.add_stop_key('It\'s a world', '!') == 'It\'s a world!'


def test_remove_stop_key() -> None:
    assert text.remove_stop_key('It\'s a nice world.') == 'It\'s a nice world'
    assert text.remove_stop_key('It\'s a nice world?') == 'It\'s a nice world'
    assert text.remove_stop_key('It\'s a nice world!') == 'It\'s a nice world'
    assert text.remove_stop_key('It\'s a nice world:') == 'It\'s a nice world'


def test_remove_stop_key_custom() -> None:
    assert text.remove_stop_key('It\'s a world-', ['-']) == 'It\'s a world'


def test_contains() -> None:
    assert text.contains('Hello World!', 'world')
    assert text.contains('Hello World!', ['city', 'world'])


def test_contains_case() -> None:
    assert not text.contains('Hello World!', 'world', True)
    assert text.contains('Hello World!', 'World', True)


def test_normalize_spaces() -> None:
    assert text.normalize('Some text   is here  ') == 'Some text is here'
    assert text.normalize('Some text   is here  .') == 'Some text is here.'


def test_normalize_breaks() -> None:
    test_text = 'Hello World\n\nHow are you.\nBy by'
    expected_text = 'Hello World. How are you. By by.'
    assert text.normalize_breaks(test_text) == expected_text


def test_normalize_breaks_append_stops_false() -> None:
    test_text = 'Hello World\n\nHow are you.\nBy by'
    expected_text = 'Hello World How are you. By by'
    assert text.normalize_breaks(test_text, False) == expected_text


def test_normalize() -> None:
    assert text.normalize('uÌˆnicode') == 'ünicode'
    assert text.normalize('HTML entities &lt;3') == 'HTML entities <3'


def test_to_string() -> None:
    assert text.to_str(1234) == '1234'
    assert text.to_str(1234.25) == '1234.25'
    assert text.to_str('1234.25') == '1234.25'


def test_to_list_split_key() -> None:
    assert text.to_list('1,2,3 ,4', ',') == ['1', '2', '3', '4']


def test_to_list_multiply_keys() -> None:
    test_text = 'its-one-s'
    multiply_keys = ('-one-', ['-one-', '-two-', '-three-'])
    expect_list = ['its-one-s', 'its-two-s', 'its-three-s']
    assert text.to_list(test_text, multiply_keys=multiply_keys) == expect_list

    multiply_keys = [
        ('-two-', ['-two-', '-one-']),
        ('-one-', ['-one-', '-two-', '-three-'])
    ]
    assert text.to_list(test_text, multiply_keys=multiply_keys) == expect_list
