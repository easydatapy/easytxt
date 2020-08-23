from easytxt import parse_string, TextParser

from tests.factory import features_samples
from tests.factory import sentences_samples
from tests import test_html

features_test_text = '- color: Black - material: Aluminium'
test_text_sentences = 'first sentence! - second sentence.  Third'
test_text_sentences_v2 = ('Features: <ul><li>* FaceTime HD camera </li>'
                          '<li>* Multi-touch <b>trackpad</b>. </li></ul>')


def test_parse_string_normalize_default():
    test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    assert parse_string(test_text) == 'Easybook Pro 13 <3 ünicode'


def test_parse_string_normalize_false():
    test_text = 'Easybook Pro 13 &lt;3 uÌˆnicode'
    parsed_string = parse_string(test_text, normalize=False)
    assert parsed_string == 'Easybook Pro 13 &lt;3 uÌˆnicode'


def test_parse_string_replace_chars():
    test_text = 'Easybook Pro 15'
    parsed_string = parse_string(
        raw_text=test_text,
        replace_chars=[
            ('pro', 'Air'),
            ('15', '13')
        ]
    )
    assert parsed_string == 'Easybook Air 13'


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


def test_text_parser_sentence_separator():
    text_parser = TextParser(
        test_text_sentences,
        sentence_separator=' | '
    )
    assert text_parser.text == 'First sentence! | Second sentence. | Third.'


def test_text_parser_html_table():
    text_parser = TextParser(test_html.table_without_header_v3)
    expected_results = ['Type: Easybook Pro.', 'Operating system: etOS.']
    assert text_parser.sentences == expected_results

    text_parser = TextParser(test_html.table_with_header)
    expected_results = [
        'Height/Width/Depth: 10/12/5.',
        'Height/Width/Depth: 2/3/5.'
    ]
    assert text_parser.sentences == expected_results

    text_parser = TextParser(test_html.table_without_header_v2)
    assert text_parser.sentences == ['Height: 2; 4.', 'Width: 3; 8.']


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
