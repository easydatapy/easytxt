import pytest

from easytxt import parse_table
from tests.factory import table_samples


@pytest.mark.parametrize(
    "parser,result",
    [
        (
            parse_table(table_samples.table_without_header),
            [{"Height": "2"}, {"Width": "3"}],
        ),
        (
            parse_table(table_samples.table_without_header_v2),
            [{"Height": "2; 4"}, {"Width": "3; 8"}],
        ),
        (
            parse_table(
                table_samples.table_without_header_v2,
                separator="|",
            ),
            [{"Height": "2|4"}, {"Width": "3|8"}],
        ),
        (
            parse_table(
                table_samples.table_without_header_v2,
                skip_row_without_value=False,
            ),
            [{"DIMENSIONS:": ""}, {"Height": "2; 4"}, {"Width": "3; 8"}],
        ),
        (
            parse_table(table_samples.table_without_header_v3),
            [{"Type": "Easybook Pro"}, {"Operating system": "etOS"}],
        ),
        (
            parse_table(table_samples.table_without_header_v4),
            [{"Type": "Easybook Pro"}, {"Operating system": "etOS"}],
        ),
    ],
)
def test_parse_table_without_header(parser, result):
    assert list(parser) == result


def test_parse_table_with_header():
    table_rows = parse_table(table_samples.table_with_header)

    expected_results = [
        {"Height": "10", "Width": "12", "Depth": "5"},
        {"Height": "2", "Width": "3", "Depth": "5"},
    ]

    assert list(table_rows) == expected_results


def test_parse_table_sentences():
    table_rows = parse_table(table_samples.table_with_header)

    expected_results = ["Height/Width/Depth: 10/12/5", "Height/Width/Depth: 2/3/5"]

    assert table_rows.sentences == expected_results


def test_parse_table_text():
    table_rows = parse_table(table_samples.table_with_header)

    expected_results = "* Height/Width/Depth: 10/12/5 " "* Height/Width/Depth: 2/3/5"

    assert table_rows.text == expected_results


def test_parse_table_get_headers():
    table_rows = parse_table(table_samples.table_with_header)

    assert table_rows.headers == ["Height", "Width", "Depth"]


def test_parse_table_has_header():
    table_rows = parse_table(table_samples.table_with_header)
    assert table_rows.has_header()


def test_parse_table_with_header_allow():
    table_rows = parse_table(
        table_samples.table_with_header,
        allow_cols=["depth"],
    )

    expected_results = [{"Depth": "5"}, {"Depth": "5"}]

    results = [table_row for table_row in table_rows]

    assert results == expected_results


def test_parse_table_with_header_deny_cols():
    table_rows = parse_table(
        table_samples.table_with_header,
        deny_cols=["width"],
    )

    expected_results = [{"Height": "10", "Depth": "5"}, {"Height": "2", "Depth": "5"}]

    assert list(table_rows) == expected_results
