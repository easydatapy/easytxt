from easytxt import xhtml

table_with_header = """
<table>
    <tr>
        <th>Height</th><th>Width</th><th>Depth</th>
    </tr>
    <tr>
        <td>10</td><td>12</td><td>5</td>
    </tr>
    <tr>
        <td>2</td><td>3</td><td>5</td>
    </tr>
</table>
"""

table_without_header = """
<table>
    <tr>
        <td>Height</td><td>2</td>
    </tr>
    <tr>
        <td>Width</td><td>3</td>
    </tr>
</table>
"""

table_without_header_v2 = """
<table>
    <tr>
        <td>DIMENSIONS:</td><td></td><td></td>
    </tr>
    <tr>
        <td>Height</td><td>2</td><td>4</td>
    </tr>
    <tr>
        <td>Width</td><td>3</td><td>8</td>
    </tr>
</table>
"""

table_without_header_v3 = """
<table>
    <tbody>
        <tr>
            <th scope="row">Type</th>
            <td>Easybook Pro</td>
        </tr>
    </tbody>
    <tbody>
        <tr>
            <th scope="row">Operating system</th>
            <td>etOS</td>
        </tr>
    </tbody>
</table>
"""


def test_to_text():
    test_html_texts = [
        ('<p>Some sentence</p>', 'Some sentence')
    ]
    for text_html_tuple in test_html_texts:
        html_text, expected_text = text_html_tuple

        assert xhtml.to_text(html_text) == expected_text


def test_validate():
    test_valid_html_texts = [
        '<p>Some sentence</p>',
        'some <br/>sentence',
        'some <BR>sentence',
        'some <img src="Something" /> sentence',
        '<title>Hallo</title>'
    ]
    for test_valid_html_text in test_valid_html_texts:
        assert xhtml.validate(test_valid_html_text)


def test_validate_invalid():
    test_invalid_html_texts = [
        'Some sentence'
    ]
    for test_invalid_html_text in test_invalid_html_texts:
        assert xhtml.validate(test_invalid_html_text) is False


def test_table_reader_with_header():
    table_rows = xhtml.TableReader(table_with_header)
    expected_results = [
        {'Height': '10', 'Width': '12', 'Depth': '5'},
        {'Height': '2', 'Width': '3', 'Depth': '5'}
    ]
    results = [table_row for table_row in table_rows]
    assert results == expected_results


def test_table_reader_with_header_allow():
    table_rows = xhtml.TableReader(
        table_with_header,
        allow_cols=['depth']
    )
    expected_results = [
        {'Depth': '5'},
        {'Depth': '5'}
    ]
    results = [table_row for table_row in table_rows]
    assert results == expected_results


def test_table_reader_with_header_deny_cols():
    table_rows = xhtml.TableReader(
        table_with_header,
        deny_cols=['width']
    )
    expected_results = [
        {'Height': '10', 'Depth': '5'},
        {'Height': '2', 'Depth': '5'}
    ]
    results = [table_row for table_row in table_rows]
    assert results == expected_results


def test_table_reader_without_header():
    table_rows = xhtml.TableReader(table_without_header)
    expected_results = [
        {'Height': '2'},
        {'Width': '3'}
    ]
    results = [table_row for table_row in table_rows]
    assert results == expected_results


def test_table_reader_without_header_v2():
    table_rows = xhtml.TableReader(table_without_header_v2)
    expected_results = [
        {'Height': '2; 4'},
        {'Width': '3; 8'}
    ]
    results = [table_row for table_row in table_rows]
    assert results == expected_results


def test_table_reader_without_header_v2_custom_separator():
    table_rows = xhtml.TableReader(
        table_without_header_v2,
        separator='|'
    )
    expected_results = [
        {'Height': '2|4'},
        {'Width': '3|8'}
    ]
    results = [table_row for table_row in table_rows]
    assert results == expected_results


def test_table_reader_without_header_v2_skip_row_without_value_false():
    table_rows = xhtml.TableReader(
        table_without_header_v2,
        skip_row_without_value=False
    )
    expected_results = [
        {'DIMENSIONS:': ''},
        {'Height': '2; 4'},
        {'Width': '3; 8'}
    ]
    results = [table_row for table_row in table_rows]
    assert results == expected_results


def test_table_reader_without_header_v3():
    table_rows = xhtml.TableReader(table_without_header_v3)
    expected_results = [
        {'Type': 'Easybook Pro'},
        {'Operating system': 'etOS'}
    ]
    results = [table_row for table_row in table_rows]
    assert results == expected_results
