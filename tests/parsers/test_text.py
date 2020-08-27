from easytxt import TextParser

from tests.factory import features_samples
from tests.factory import sentences_samples
from tests.parsers import test_table

features_test_text = '- color: Black - material: Aluminium'
test_text_sentences = 'first sentence! - second sentence.  Third'
test_text_sentences_v2 = ('Features: <ul><li>* FaceTime HD camera </li>'
                          '<li>* Multi-touch <b>trackpad</b>. </li></ul>')


def test_text_parser_to_sentences():
    for test_sentence_tuple in sentences_samples.english:
        test_sentences, expected_sentences = test_sentence_tuple
        text_obj = TextParser(test_sentences)
        assert text_obj.sentences == expected_sentences


def test_text_parser_to_text():
    for test_sentence_tuple in sentences_samples.english:
        test_sentences, expected_sentences = test_sentence_tuple
        text_obj = TextParser(test_sentences)
        assert text_obj.text == ' '.join(expected_sentences)


def test_text_parser_to_features():
    for test_sentence_tuple in features_samples.english:
        test_sentences, expected_sentences = test_sentence_tuple
        text_obj = TextParser(test_sentences)
        assert text_obj.features == expected_sentences


def test_text_parser_to_features_dict():
    expected_results = {'Color': 'Black', 'Material': 'Aluminium'}
    assert TextParser(features_test_text).features_dict == expected_results


def test_text_parser_to_feature():
    assert TextParser(features_test_text).feature('color') == 'Black'
    assert TextParser(features_test_text).feature('Col') == 'Black'
    assert TextParser(features_test_text).feature('Size') is None


def test_text_parser_to_feature_exact():
    assert TextParser(features_test_text).feature_exact('Color') == 'Black'
    assert TextParser(features_test_text).feature_exact('col') is None


def test_text_parser_to_raw_features():
    test_text = 'Some sentence - color: Black'
    expected_results = ['Some sentence.', ('Color', 'Black')]
    assert TextParser(test_text).raw_features == expected_results


def test_text_parser_feature_split_keys():
    # Lets first test with default split keys
    test_text = 'Color: Black. Material; Aluminium'
    expected_results = [('Color', 'Black')]
    assert TextParser(test_text).features == expected_results

    # Lets add custom split keys
    expected_results = [('Color', 'Black'), ('Material', 'Aluminium')]
    text_parser = TextParser(test_text, feature_split_keys=[':', ';'])
    assert text_parser.features == expected_results


def test_text_parser_allow():
    text_parser = TextParser(
        test_text_sentences,
        allow=['first']
    )
    assert text_parser.sentences == ['First sentence!']

    text_parser = TextParser(
        test_text_sentences,
        allow=['first', 'third']
    )
    assert text_parser.sentences == ['First sentence!', 'Third.']


def test_text_parser_callow():
    text_parser = TextParser(
        test_text_sentences,
        callow=['First', 'third']
    )
    assert text_parser.sentences == ['First sentence!']


def test_text_parser_deny():
    text_parser = TextParser(
        test_text_sentences,
        deny=['second', 'third']
    )
    assert text_parser.sentences == ['First sentence!']

    text_parser = TextParser(
        test_text_sentences,
        deny=['secon']
    )
    assert text_parser.sentences == ['First sentence!', 'Third.']


def test_text_parser_cdeny():
    text_parser = TextParser(
        test_text_sentences,
        cdeny=['first', 'Second', 'Thir']
    )
    assert text_parser.sentences == ['First sentence!']


def test_text_parser_capitalize_false():
    text_parser = TextParser(
        test_text_sentences,
        capitalize=False
    )
    assert text_parser.text == 'first sentence! second sentence. Third.'


def test_text_parser_lowercase_true():
    text_parser = TextParser(
        test_text_sentences,
        lowercase=True
    )
    assert text_parser.text == 'first sentence! second sentence. third.'


def test_text_parser_uppercase_true():
    text_parser = TextParser(
        test_text_sentences,
        uppercase=True
    )
    assert text_parser.text == 'FIRST SENTENCE! SECOND SENTENCE. THIRD.'


def test_text_parser_sentence_separator():
    text_parser = TextParser(
        test_text_sentences,
        sentence_separator=' | '
    )
    assert text_parser.text == 'First sentence! | Second sentence. | Third.'


def test_text_parser_replace_keys():
    text_parser = TextParser(
        test_text_sentences,
        replace_keys=[('third', 'Third sentence'), ('ence!', 'ence?')]
    )
    assert text_parser.text == 'First sentence? Second sentence. Third sentence.'


def test_text_parser_remove_keys():
    text_parser = TextParser(
        test_text_sentences,
        remove_keys=['sentence', '!']
    )
    assert text_parser.text == 'First. Second. Third.'


def test_text_parser_css_query():
    text_parser = TextParser(
        test_text_sentences_v2,
        css_query='ul'
    )
    expected_sentences = ['FaceTime HD camera.', 'Multi-touch trackpad.']
    assert text_parser.sentences == expected_sentences

    text_parser = TextParser(
        test_text_sentences_v2,
        css_query='ul li:eq(0)'
    )
    assert text_parser.sentences == ['FaceTime HD camera.']


def test_text_parser_exclude_css():
    text_parser = TextParser(
        test_text_sentences_v2,
        exclude_css='ul'
    )
    assert text_parser.sentences == ['Features:']

    text_parser = TextParser(
        test_text_sentences_v2,
        css_query='ul',
        exclude_css='li:last'
    )
    assert text_parser.sentences == ['FaceTime HD camera.']


def test_parser_merge_sentences_default():
    text_parser = TextParser(test_text_sentences_v2)
    expected_sentences = [
        'Features: FaceTime HD camera.',
        'Multi-touch trackpad.'
    ]
    assert text_parser.sentences == expected_sentences


def test_parser_merge_sentences_false():
    text_parser = TextParser(
        test_text_sentences_v2,
        merge_sentences=False
    )
    expected_sentences = [
        'Features:',
        'FaceTime HD camera.',
        'Multi-touch trackpad.'
    ]
    assert text_parser.sentences == expected_sentences


def test_parser_custom_inline_breaks():
    test_text = 'notebook > ultrabook'

    text_parser = TextParser(
        test_text,
        inline_breaks=['>']
    )
    assert text_parser.sentences == ['Notebook.', 'Ultrabook.']

    # Default without custom inline_breaks
    text_parser = TextParser(test_text)
    assert text_parser.sentences == ['Notebook > ultrabook.']


def test_parser_split_inline_breaks_false():
    test_text = '- notebook - ultrabook'

    text_parser = TextParser(
        test_text,
        split_inline_breaks=False
    )
    assert text_parser.sentences == ['- notebook - ultrabook.']

    # Default without custom inline_breaks
    text_parser = TextParser(test_text)
    assert text_parser.sentences == ['Notebook.', 'Ultrabook.']


def test_text_parser_stop_key():
    test_text = '* First feature * second feature?'

    # First lets test default stop key '.'
    text_parser = TextParser(test_text)
    assert text_parser.sentences == ['First feature.', 'Second feature?']

    # Lets test custom stop key '!'
    text_parser = TextParser(test_text, stop_key='!')
    assert text_parser.sentences == ['First feature!', 'Second feature?']


def test_text_parser_stop_keys_split():
    test_text = 'First sentence: center sentence? Last sentence!'

    # Lets test default stop split keys
    text_parser = TextParser(test_text)
    expected_result = ['First sentence: center sentence?', 'Last sentence!']
    assert text_parser.sentences == expected_result

    # Lets test custom stop split keys
    text_parser = TextParser(
        test_text,
        stop_keys_split=[':', '?'],
        stop_keys_ignore=[';']
    )
    expected_result = ['First sentence:', 'Center sentence?', 'Last sentence!']
    assert text_parser.sentences == expected_result


def test_text_parser_html_table():
    text_parser = TextParser(test_table.table_without_header_v3)
    expected_results = ['Type: Easybook Pro.', 'Operating system: etOS.']
    assert text_parser.sentences == expected_results

    text_parser = TextParser(test_table.table_with_header)
    expected_results = [
        'Height/Width/Depth: 10/12/5.',
        'Height/Width/Depth: 2/3/5.'
    ]
    assert text_parser.sentences == expected_results

    text_parser = TextParser(test_table.table_without_header_v2)
    assert text_parser.sentences == ['Height: 2; 4.', 'Width: 3; 8.']

    # Check if text with no html table returns empty string
    text_parser = TextParser(test_text_sentences)
    return text_parser == ''
