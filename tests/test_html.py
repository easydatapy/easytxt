from easytxt import html


def test_to_text():
    test_html_texts = [("<p>Some sentence</p>", ["Some sentence"])]

    for text_html_tuple in test_html_texts:
        html_text, expected_text = text_html_tuple

        assert html.to_sentences(html_text) == expected_text


def test_validate():
    test_valid_html_texts = [
        "<p>Some sentence</p>",
        "some <br/>sentence",
        "some <BR>sentence",
        'some <img src="Something" /> sentence',
        "<title>Hallo</title>",
    ]
    for test_valid_html_text in test_valid_html_texts:
        assert html.validate(test_valid_html_text)


def test_validate_invalid():
    test_invalid_html_texts = ["Some sentence"]
    for test_invalid_html_text in test_invalid_html_texts:
        assert html.validate(test_invalid_html_text) is False
