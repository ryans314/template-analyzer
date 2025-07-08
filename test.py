import pytest
from pytest import raises
from main import get_filepaths, parse_html

#  ------------ Tests for get_filepath -------------
def test_get_filepaths_works_for_dir() -> None:
    result = get_filepaths("test_data")
    assert len(result) == 4
    assert "test_data\\ex_file_1.html" in result
    assert "test_data\\additional_files\\nested_2.html" in result

def test_get_filepaths_works_for_nested_dir() -> None:
    result = get_filepaths("test_data/additional_files")
    assert len(result) == 2
    assert "test_data/additional_files\\nested_1.html" in result
    assert "test_data/additional_files\\nested_2.html" in result

def test_get_filepaths_works_for_file() -> None:
    result = get_filepaths("test_data/ex_file_2.html")
    assert len(result) == 1
    assert "test_data/ex_file_2.html" in result

def test_get_filepaths_raises_error_for_invalid_path() -> None:
    with raises(FileNotFoundError):
        get_filepaths("additional_files")

#  ------------ Tests for parse_html -------------

def test_parse_html_has_correct_format() -> None:
    html_str = "<div class='class-name'></div>"
    data = parse_html(html_str, "folder/file.html")
    assert len(data) == 1
    div_data = data[0]
    assert len(div_data) == 3
    assert div_data == ("div", ["class-name"], "folder/file.html")

def test_parse_html_sorts_class_names() -> None:
    html_str = \
    "<div class='align-center w-auto py-5'></div>" \
    "<div class='w-auto align-center py-5'></div>"
    data = parse_html(html_str, "folder/file.html")
    assert len(data) == 2
    div1_data = data[0]
    div2_data = data[1]
    
    expected = ("div", ["align-center", "py-5", "w-auto"], "folder/file.html")
    assert div1_data == expected
    assert div2_data == expected

def test_parse_html_works_on_nested_elements() -> None:
    html_str = \
    "<div class='align-center w-auto py-5'>" \
        "<div class=\"sm:text-sm md:text-lg\"><p></p></div>" \
    "</div>"
    data = parse_html(html_str, "folder/file.html")
    assert len(data) == 2 #should not include p
    
    expected_outer = ("div", ["align-center", "py-5", "w-auto"], "folder/file.html")
    assert expected_outer in data
    expected_inner = ("div", ["md:text-lg", "sm:text-sm"], "folder/file.html")
    assert expected_inner in data