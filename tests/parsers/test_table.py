from easytxt import TableParser

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
<div>
    <p>This text should be ignored by TableReader.</p>
</div>
<table>
    <tr>
        <td>Height</td><td>2</td>
    </tr>
    <tr>
        <td>Width</td><td>3</td>
    </tr>
</table>
<div>
    <p>This text should be ignored by TableReader.</p>
</div>
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
            <td scope="row">Type</td>
            <td>Easybook Pro</td>
        </tr>
        <tr>
            <td scope="row">Operating system</td>
            <td>etOS</td>
        </tr>
    </tbody>
</table>
"""


def test_table_parser_with_header():
    table_rows = TableParser(table_with_header)
    expected_results = [
        {'Height': '10', 'Width': '12', 'Depth': '5'},
        {'Height': '2', 'Width': '3', 'Depth': '5'}
    ]
    assert list(table_rows) == expected_results


def test_table_parser_sentences():
    table_rows = TableParser(table_with_header)
    expected_results = [
        'Height/Width/Depth: 10/12/5',
        'Height/Width/Depth: 2/3/5'
    ]
    assert table_rows.sentences == expected_results


def test_table_parser_text():
    table_rows = TableParser(table_with_header)
    expected_results = (
        '* Height/Width/Depth: 10/12/5 '
        '* Height/Width/Depth: 2/3/5'
    )
    assert table_rows.text == expected_results


def test_table_parser_get_header_values():
    table_rows = TableParser(table_with_header)
    assert table_rows.header_values == ['Height', 'Width', 'Depth']


def test_table_parser_has_header():
    table_rows = TableParser(table_with_header)
    assert table_rows.has_header()


def test_table_parser_with_header_allow():
    table_rows = TableParser(
        table_with_header,
        allow_cols=['depth']
    )
    expected_results = [
        {'Depth': '5'},
        {'Depth': '5'}
    ]
    results = [table_row for table_row in table_rows]
    assert results == expected_results


def test_table_parser_with_header_deny_cols():
    table_rows = TableParser(
        table_with_header,
        deny_cols=['width']
    )
    expected_results = [
        {'Height': '10', 'Depth': '5'},
        {'Height': '2', 'Depth': '5'}
    ]
    assert list(table_rows) == expected_results


def test_table_parser_without_header():
    table_rows = TableParser(table_without_header)
    expected_results = [
        {'Height': '2'},
        {'Width': '3'}
    ]
    assert list(table_rows) == expected_results


def test_table_parser_without_header_v2():
    table_rows = TableParser(table_without_header_v2)
    expected_results = [
        {'Height': '2; 4'},
        {'Width': '3; 8'}
    ]
    assert list(table_rows) == expected_results


def test_table_parser_without_header_v2_custom_separator():
    table_rows = TableParser(
        table_without_header_v2,
        separator='|'
    )
    expected_results = [
        {'Height': '2|4'},
        {'Width': '3|8'}
    ]
    assert list(table_rows) == expected_results


def test_table_parser_without_header_v2_skip_row_without_value_false():
    table_rows = TableParser(
        table_without_header_v2,
        skip_row_without_value=False
    )
    expected_results = [
        {'DIMENSIONS:': ''},
        {'Height': '2; 4'},
        {'Width': '3; 8'}
    ]
    assert list(table_rows) == expected_results


def test_table_parser_without_header_v3():
    table_rows = TableParser(table_without_header_v3)
    expected_results = [
        {'Type': 'Easybook Pro'},
        {'Operating system': 'etOS'}
    ]
    assert list(table_rows) == expected_results
