import pytest

from easytxt import parse_text

from tests.factory import features_samples
from tests.factory import sentences_samples
from tests.parsers import test_table

features_test_text = '- color: Black - material: Aluminium'
test_text_sentences = 'first sentence! - second sentence.  Third'
test_text_sentences_v2 = ('Features: <ul><li>* FaceTime HD camera </li>'
                          '<li>* Multi-touch <b>trackpad</b>. </li></ul>')
test_text_sentences_v3 = 'First txt. Second txt. 3 Txt. FOUR txt.'


@pytest.mark.parametrize(
    'test_data, result',
    sentences_samples.english
)
def test_parse_text_to_sentences(test_data, result):
    assert parse_text(test_data).sentences == result


@pytest.mark.parametrize(
    'test_data, result',
    sentences_samples.english
)
def test_parse_text_to_text(test_data, result):
    assert parse_text(test_data).text == ' '.join(result)


@pytest.mark.parametrize(
    'test_data, result',
    features_samples.english
)
def test_parse_text_to_features(test_data, result):
    assert parse_text(test_data).features == result


def test_parse_text_to_features_dict():
    expected_results = {'Color': 'Black', 'Material': 'Aluminium'}
    assert parse_text(features_test_text).features_dict == expected_results


@pytest.mark.parametrize(
    'feature, test_data, result',
    [
        ('color', features_test_text, 'Black'),
        ('Col', features_test_text, 'Black'),
        ('Size', features_test_text, None),
    ]
)
def test_parse_text_to_feature(feature, test_data, result):
    assert parse_text(test_data).feature(feature) == result


@pytest.mark.parametrize(
    'test_data, feature, result',
    [
        (features_test_text, 'color', 'Black'),
        (features_test_text, 'col', None),
        (features_test_text, 'Size', None),
    ]
)
def test_parse_text_to_feature_exact(test_data, feature, result):
    assert parse_text(test_data).feature_exact(feature) == result


@pytest.mark.parametrize(
    'test_data, result',
    [
        (
                'Some sentence - color: Black',
                ['Some sentence.', ('Color', 'Black')]
        ),
    ]
)
def test_parse_text_to_raw_features(test_data, result):
    assert parse_text(test_data).raw_features == result


@pytest.mark.parametrize(
    'test_data, feature_split_keys, result',
    [
        (
                'Color: Black. Material; Aluminium',
                [':', ';'],
                [('Color', 'Black'), ('Material', 'Aluminium')]
        ),
    ]
)
def test_parse_text_feature_split_keys(test_data, feature_split_keys, result):
    tp = parse_text(test_data, feature_split_keys=feature_split_keys)
    assert tp.features == result


@pytest.mark.parametrize(
    'test_data, allow, result',
    [
        (test_text_sentences, ['first'], ['First sentence!']),
        (
                test_text_sentences,
                ['first', 'third'],
                ['First sentence!', 'Third.']
        ),
    ]
)
def test_parse_text_allow(test_data, allow, result):
    tp = parse_text(test_data, allow=allow)
    assert list(tp) == result


@pytest.mark.parametrize(
    'test_data, callow, result',
    [
        (test_text_sentences, ['First', 'third'], ['First sentence!']),
    ]
)
def test_parse_text_case_sensitive_allow(test_data, callow, result):
    tp = parse_text(test_data, callow=callow)
    assert list(tp) == result


@pytest.mark.parametrize(
    'test_data, from_allow, result',
    [
        (test_text_sentences_v3, ['second'], 'Second txt. 3 Txt. FOUR txt.'),
    ]
)
def test_parse_text_from_allow(test_data, from_allow, result):
    tp = parse_text(test_data, from_allow=from_allow)
    assert str(tp) == result


@pytest.mark.parametrize(
    'test_data, from_callow, result',
    [
        (test_text_sentences_v3, ['Second'], 'Second txt. 3 Txt. FOUR txt.'),
        # Test case with a wrong case
        (test_text_sentences_v3, ['second'], ''),
    ]
)
def test_parse_text_from_callow(test_data, from_callow, result):
    tp = parse_text(test_data, from_callow=from_callow)
    assert str(tp) == result


@pytest.mark.parametrize(
    'test_data, to_allow, result',
    [
        (test_text_sentences_v3, ['four'], 'First txt. Second txt. 3 Txt.'),
    ]
)
def test_parse_text_to_allow(test_data, to_allow, result):
    tp = parse_text(test_data, to_allow=to_allow)
    assert str(tp) == result


@pytest.mark.parametrize(
    'test_data, to_callow, result',
    [
        (test_text_sentences_v3, ['FOUR'], 'First txt. Second txt. 3 Txt.'),
        # Test case with a wrong case
        (
                test_text_sentences_v3,
                ['four'],
                'First txt. Second txt. 3 Txt. FOUR txt.'
        ),
    ]
)
def test_parse_text_to_callow(test_data, to_callow, result):
    tp = parse_text(test_text_sentences_v3, to_callow=to_callow)
    assert str(tp) == result


@pytest.mark.parametrize(
    'test_data, deny, result',
    [
        (test_text_sentences, ['second', 'third'], ['First sentence!']),
        (test_text_sentences, ['secon'], ['First sentence!', 'Third.']),
    ]
)
def test_parse_text_deny(test_data, deny, result):
    tp = parse_text(test_data, deny=deny)
    assert tp.sentences == result


@pytest.mark.parametrize(
    'test_data, cdeny, result',
    [
        (
                test_text_sentences,
                ['first', 'Second', 'Thir'],
                ['First sentence!']
        ),
    ]
)
def test_parse_text_case_sensitive_deny(test_data, cdeny, result):
    tp = parse_text(test_data, cdeny=cdeny)
    assert tp.sentences == result


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
