from easytxt import sentences

from tests.factory import sentences_samples


# def test_from_text() -> None:
#     for assert_paragraph in text_to_sentences_samples.english:
#         paragraph, test_sentences = assert_paragraph
#
#         assert sentences.from_text(paragraph) == test_sentences
#
#
# def test_from_text_normalize() -> None:
#     paragraph = 'uÌˆnicode. HTML entities &lt;3!'
#     final_sentences = sentences.from_text(paragraph, normalize=False)
#     assert final_sentences == ['UÌˆnicode.', 'HTML entities &lt;3!']


def test_merge() -> None:
    test_sentences = ['Color:', 'Black.', 'Some paragraph!']
    merged_sentences = ['Color: Black.', 'Some paragraph!']
    assert sentences.merge(test_sentences) == merged_sentences


def test_add_stop() -> None:
    test_sentences = ['Color', 'Material']
    assert sentences.add_stop(test_sentences) == ['Color.', 'Material.']


def test_add_stop_custom_stop_key() -> None:
    test_sentences = ['Color', 'Material']
    assert sentences.add_stop(test_sentences, '!') == ['Color!', 'Material!']


def test_capitalize() -> None:
    test_sentences = ['hello John.', 'Where are you?', 'i am hungry!']
    final_sentences = sentences.capitalize_sentence(test_sentences)
    assert final_sentences == ['Hello John.', 'Where are you?', 'I am hungry!']


def test_replace_chars_by_keys() -> None:
    test_sentences = ['Hello John.', 'How are you?', 'Be okay!']
    replace_key_list = [('How', 'WHERE'), ('john', 'Trevor')]
    final_sentences = sentences.replace_chars_by_keys(
        test_sentences,
        replace_key_list
    )
    assert final_sentences == ['Hello Trevor.', 'WHERE are you?', 'Be okay!']


def test_remove_empty() -> None:
    test_sentences = ['Hello John.', '.', 'Am', '', None, 'How are you?']
    final_sentences = sentences.remove_empty(test_sentences)
    assert final_sentences == ['Hello John.', 'How are you?']


def test_allow_contains() -> None:
    allow_keys = ['color:', 'material:']
    test_sentences = ['Color: Black.', 'Some text!', 'Material: Aluminium!']
    expected_sentences = ['Color: Black.', 'Material: Aluminium!']
    final_sentences = sentences.allow_contains(test_sentences, allow_keys)
    assert final_sentences == expected_sentences


def test_allow_contains_case() -> None:
    keys = ['color:', 'Material:']
    test_sentences = ['Color: Black.', 'Some text!', 'Material: Aluminium!']
    expected_sentences = ['Material: Aluminium!']
    final_sentences = sentences.allow_contains(test_sentences, keys, True)
    assert final_sentences == expected_sentences


def test_ignore_contains() -> None:
    ignore_keys = ['made in', 'sku#']
    test_sentences = ['SKU# 1234.', 'Some paragraph!', 'Made in Slovenia!']
    expected_sentences = ['Some paragraph!']
    final_sentences = sentences.deny_contains(test_sentences, ignore_keys)
    assert final_sentences == expected_sentences


def test_ignore_contains_case() -> None:
    keys = ['made in', 'SKU#']
    test_sentences = ['SKU# 1234.', 'Some paragraph!', 'Made in Slovenia!']
    expected_sentences = ['Some paragraph!', 'Made in Slovenia!']
    final_sentences = sentences.deny_contains(test_sentences, keys, True)
    assert final_sentences == expected_sentences


def test_to_text() -> None:
    test_sentences = ['Hello John.', 'Where have you been?', 'I am hungry!']
    paragraph = 'Hello John. Where have you been? I am hungry!'
    final_sentences = sentences.to_text(test_sentences)
    assert final_sentences == paragraph


def test_to_text_custom_separator() -> None:
    test_sentences = ['Hello John.', 'Where have you been?', 'I am hungry!']
    paragraph = 'Hello John. | Where have you been? | I am hungry!'
    assert sentences.to_text(test_sentences, ' | ') == paragraph
