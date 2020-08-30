from easytxt import parse_text

from tests.factory import features_samples
from tests.factory import sentences_samples
from tests.parsers import test_table

features_test_text = '- color: Black - material: Aluminium'
test_text_sentences = 'first sentence! - second sentence.  Third'
test_text_sentences_v2 = ('Features: <ul><li>* FaceTime HD camera </li>'
                          '<li>* Multi-touch <b>trackpad</b>. </li></ul>')
test_text_sentences_v3 = 'First txt. Second txt. 3 Txt. FOUR txt.'


def test_parse_text_to_sentences():
    for test_sentence_tuple in sentences_samples.english:
        test_sentences, expected_sentences = test_sentence_tuple
        assert parse_text(test_sentences).sentences == expected_sentences


def test_parse_text_to_text():
    for test_sentence_tuple in sentences_samples.english:
        test_sentences, expected_sentences = test_sentence_tuple
        assert parse_text(test_sentences).text == ' '.join(expected_sentences)


def test_parse_text_to_features():
    for test_sentence_tuple in features_samples.english:
        test_sentences, expected_sentences = test_sentence_tuple
        assert parse_text(test_sentences).features == expected_sentences


def test_parse_text_to_features_dict():
    expected_results = {'Color': 'Black', 'Material': 'Aluminium'}
    assert parse_text(features_test_text).features_dict == expected_results


def test_parse_text_to_feature():
    assert parse_text(features_test_text).feature('color') == 'Black'
    assert parse_text(features_test_text).feature('Col') == 'Black'
    assert parse_text(features_test_text).feature('Size') is None


def test_parse_text_to_feature_exact():
    assert parse_text(features_test_text).feature_exact('Color') == 'Black'
    assert parse_text(features_test_text).feature_exact('col') is None


def test_parse_text_to_raw_features():
    test_text = 'Some sentence - color: Black'
    expected_results = ['Some sentence.', ('Color', 'Black')]
    assert parse_text(test_text).raw_features == expected_results


def test_parse_text_feature_split_keys():
    # Lets first test with default split keys
    test_text = 'Color: Black. Material; Aluminium'
    expected_results = [('Color', 'Black')]
    assert parse_text(test_text).features == expected_results

    # Lets add custom split keys
    expected_results = [('Color', 'Black'), ('Material', 'Aluminium')]
    tp = parse_text(test_text, feature_split_keys=[':', ';'])
    assert tp.features == expected_results


def test_parse_text_allow():
    tp = parse_text(
        test_text_sentences,
        allow=['first']
    )
    assert list(tp) == ['First sentence!']

    tp = parse_text(
        test_text_sentences,
        allow=['first', 'third']
    )
    assert list(tp) == ['First sentence!', 'Third.']


def test_parse_text_case_sensitive_allow():
    tp = parse_text(
        test_text_sentences,
        callow=['First', 'third']
    )
    assert list(tp) == ['First sentence!']


def test_parse_text_from_allow():
    tp = parse_text(
        test_text_sentences_v3,
        from_allow=['second']
    )
    assert str(tp) == 'Second txt. 3 Txt. FOUR txt.'


def test_parse_text_from_callow():
    tp = parse_text(
        test_text_sentences_v3,
        from_callow=['Second']
    )
    assert str(tp) == 'Second txt. 3 Txt. FOUR txt.'

    # Lets test with wrong case
    tp = parse_text(
        test_text_sentences_v3,
        from_callow=['second']
    )
    assert str(tp) == ''


def test_parse_text_to_allow():
    tp = parse_text(
        test_text_sentences_v3,
        to_allow=['four']
    )
    assert str(tp) == 'First txt. Second txt. 3 Txt.'


def test_parse_text_to_callow():
    tp = parse_text(
        test_text_sentences_v3,
        to_callow=['FOUR']
    )
    assert str(tp) == 'First txt. Second txt. 3 Txt.'

    # Lets test with wrong case
    tp = parse_text(
        test_text_sentences_v3,
        to_callow=['four']
    )
    assert str(tp) == 'First txt. Second txt. 3 Txt. FOUR txt.'


def test_parse_text_deny():
    tp = parse_text(
        test_text_sentences,
        deny=['second', 'third']
    )
    assert tp.sentences == ['First sentence!']

    tp = parse_text(
        test_text_sentences,
        deny=['secon']
    )
    assert tp.sentences == ['First sentence!', 'Third.']


def test_parse_text_case_sensitive_deny():
    tp = parse_text(
        test_text_sentences,
        cdeny=['first', 'Second', 'Thir']
    )
    assert tp.sentences == ['First sentence!']


def test_parse_text_capitalize_false():
    tp = parse_text(
        test_text_sentences,
        capitalize=False
    )
    assert tp.text == 'first sentence! second sentence. Third.'


def test_parse_text_title_true():
    tp = parse_text(
        test_text_sentences,
        title=True
    )
    assert tp.text == 'First Sentence! Second Sentence. Third.'


def test_parse_text_lowercase_true():
    tp = parse_text(
        test_text_sentences,
        lowercase=True
    )
    assert tp.text == 'first sentence! second sentence. third.'


def test_parse_text_uppercase_true():
    tp = parse_text(
        test_text_sentences,
        uppercase=True
    )
    assert tp.text == 'FIRST SENTENCE! SECOND SENTENCE. THIRD.'


def test_parse_text_sentence_separator():
    tp = parse_text(
        test_text_sentences,
        sentence_separator=' | '
    )
    assert tp.text == 'First sentence! | Second sentence. | Third.'


def test_parse_text_replace_keys():
    tp = parse_text(
        test_text_sentences,
        replace_keys=[('third', 'Third sentence'), ('ence!', 'ence?')]
    )
    assert tp.text == 'First sentence? Second sentence. Third sentence.'


def test_parse_text_remove_keys():
    tp = parse_text(
        test_text_sentences,
        remove_keys=['sentence', '!']
    )
    assert tp.text == 'First. Second. Third.'


def test_parse_text_css_query():
    tp = parse_text(
        test_text_sentences_v2,
        css_query='ul'
    )
    expected_sentences = ['FaceTime HD camera.', 'Multi-touch trackpad.']
    assert tp.sentences == expected_sentences

    tp = parse_text(
        test_text_sentences_v2,
        css_query='ul li:eq(0)'
    )
    assert tp.sentences == ['FaceTime HD camera.']


def test_parse_text_exclude_css():
    tp = parse_text(
        test_text_sentences_v2,
        exclude_css='ul'
    )
    assert tp.sentences == ['Features:']

    tp = parse_text(
        test_text_sentences_v2,
        css_query='ul',
        exclude_css='li:last'
    )
    assert tp.sentences == ['FaceTime HD camera.']


def test_parser_text_merge_sentences_default():
    tp = parse_text(test_text_sentences_v2)
    expected_sentences = [
        'Features: FaceTime HD camera.',
        'Multi-touch trackpad.'
    ]
    assert tp.sentences == expected_sentences


def test_parser_text_merge_sentences_false():
    tp = parse_text(
        test_text_sentences_v2,
        merge_sentences=False
    )
    expected_sentences = [
        'Features:',
        'FaceTime HD camera.',
        'Multi-touch trackpad.'
    ]
    assert tp.sentences == expected_sentences


def test_parser_text_split_inline_breaks_false():
    test_text = '- notebook - ultrabook'

    tp = parse_text(
        test_text,
        split_inline_breaks=False
    )
    assert tp.sentences == ['- notebook - ultrabook.']

    # Default without custom inline_breaks
    tp = parse_text(test_text)
    assert tp.sentences == ['Notebook.', 'Ultrabook.']


def test_parser_custom_inline_breaks():
    test_text = 'notebook > ultrabook'

    tp = parse_text(
        test_text,
        inline_breaks=['>']
    )
    assert tp.sentences == ['Notebook.', 'Ultrabook.']

    # Default without custom inline_breaks
    tp = parse_text(test_text)
    assert tp.sentences == ['Notebook > ultrabook.']


def test_parse_text_stop_key():
    test_text = '* First feature * second feature?'

    # First lets test default stop key '.'
    tp = parse_text(test_text)
    assert tp.sentences == ['First feature.', 'Second feature?']

    # Lets test custom stop key '!'
    tp = parse_text(test_text, stop_key='!')
    assert tp.sentences == ['First feature!', 'Second feature?']


def test_parse_text_stop_keys_split():
    test_text = 'First sentence: center sentence? Last sentence!'

    # Lets test default stop split keys
    tp = parse_text(test_text)
    expected_result = ['First sentence: center sentence?', 'Last sentence!']
    assert tp.sentences == expected_result

    # Lets test custom stop split keys
    tp = parse_text(
        test_text,
        stop_keys_split=[':', '?'],
        stop_keys_ignore=[';']
    )
    expected_result = ['First sentence:', 'Center sentence?', 'Last sentence!']
    assert tp.sentences == expected_result


def test_parse_text_replace_keys_raw_text():
    # Lets test default result with badly structured text
    test_text = 'Easybook pro 15 Color: Gray Material: Aluminium'
    pt = parse_text(test_text)
    assert pt.sentences == ['Easybook pro 15 Color: Gray Material: Aluminium.']

    replace_keys = [('Color:', '. Color:'), ('material:', '. Material:')]
    pt = parse_text(test_text, replace_keys_raw_text=replace_keys)
    assert pt.sentences == ['Easybook pro 15.', 'Color: Gray.', 'Material: Aluminium.']


def test_parse_text_remove_keys_raw_text():
    test_text = 'Easybook pro 15. Color: Gray'
    pt = parse_text(test_text, remove_keys_raw_text=['. color:'])
    assert pt.sentences == ['Easybook pro 15 Gray.']


def test_parse_text_html_table():
    tp = parse_text(test_table.table_without_header_v3)
    expected_results = ['Type: Easybook Pro.', 'Operating system: etOS.']
    assert tp.sentences == expected_results

    tp = parse_text(test_table.table_with_header)
    expected_results = [
        'Height/Width/Depth: 10/12/5.',
        'Height/Width/Depth: 2/3/5.'
    ]
    assert tp.sentences == expected_results

    tp = parse_text(test_table.table_without_header_v2)
    assert tp.sentences == ['Height: 2; 4.', 'Width: 3; 8.']

    # Check if text with no html table returns empty string
    tp = parse_text(test_text_sentences)
    return tp == ''


def test_parse_text_text_num_to_numeric():
    test_text = ('First Sentence. Two thousand and three has it. '
                 'Three Sentences.')
    expected_results = ['1 Sentence.', '2003 has it.', '3 Sentences.']
    tp = parse_text(test_text, text_num_to_numeric=True)
    assert list(tp.sentences) == expected_results


def test_parse_text_iter():
    test_text = '* First feature * second feature?'
    assert list(parse_text(test_text)) == ['First feature.', 'Second feature?']


def test_parse_text_str():
    test_text = '* First feature * second feature?'
    assert str(parse_text(test_text)) == 'First feature. Second feature?'


def test_parse_text_len():
    test_text = '* First feature * second feature?'
    assert len(parse_text(test_text)) == 2


def test_parse_text_add():
    test_text = '* First feature * second feature?'
    tp = parse_text(test_text) + 'hello World'
    assert str(tp) == 'First feature. Second feature? Hello World.'
    assert list(tp) == ['First feature.', 'Second feature?', 'Hello World.']

    tp = parse_text(test_text) + ['hello', 'World!']
    assert str(tp) == 'First feature. Second feature? Hello. World!'


def test_parse_text_radd():
    test_text = '* First feature * second feature?'
    tp = 'hello World' + parse_text(test_text)
    assert str(tp) == 'Hello World. First feature. Second feature?'

    tp = ['hello', 'World!'] + parse_text(test_text)
    assert str(tp) == 'Hello. World! First feature. Second feature?'
