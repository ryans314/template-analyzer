import pytest
import sqlite3
import csv
from pytest import raises
from main import get_filepaths, parse_html, parse_data, analyze_db_info

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
    assert len(div_data) == 4 #Tag name, classes, num_classes, file_path
    assert div_data == ("div", "class-name", 1, "folder/file.html")

def test_parse_html_sorts_class_names() -> None:
    html_str = \
    "<div class='align-center w-auto py-5'></div>" \
    "<div class='w-auto align-center py-5'></div>"
    data = parse_html(html_str, "folder/file.html")
    assert len(data) == 2
    div1_data = data[0]
    div2_data = data[1]
    
    expected = ("div", "align-center py-5 w-auto", 3, "folder/file.html")
    assert div1_data == expected
    assert div2_data == expected

def test_parse_html_works_on_nested_elements() -> None:
    html_str = \
    "<div class='align-center w-auto py-5'>" \
        "<div class=\"sm:text-sm md:text-lg\"><p></p></div>" \
    "</div>"
    data = parse_html(html_str, "folder/file.html")
    assert len(data) == 2 #should not include p
    
    expected_outer = ("div", "align-center py-5 w-auto", 3, "folder/file.html")
    assert expected_outer in data
    expected_inner = ("div", "md:text-lg sm:text-sm", 2, "folder/file.html")
    assert expected_inner in data

def test_parse_html_works_with_duplicate_classes() -> None:
    html_str = \
    "<div class='align-center w-auto py-5'>" \
        "<div class=\"sm:text-sm sm:text-sm md:text-lg\"><p></p></div>" \
    "</div>"
    data = parse_html(html_str, "folder/file.html")
    assert len(data) == 2
    
    expected_outer = ("div", "align-center py-5 w-auto", 3, "folder/file.html")
    assert expected_outer in data
    expected_inner = ("div", "md:text-lg sm:text-sm", 2, "folder/file.html")
    assert expected_inner in data


#  ------------ Tests for parse_data -------------
def test_parse_data_creates_correct_table_headers() -> None:
    conn = sqlite3.connect(":memory:")
    parse_data([], conn)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tag_data")
    headers = [desc[0] for desc in cursor.description]
    expected_headers = {"id", "name", "classes", "num_classes", "file_path"}
    assert set(headers) == set(expected_headers)
    conn.close()

def test_parse_data_populates_table_correctly() -> None:
    data = [
        ("div", "flex flex-col gap-y-5 max-w-5xl mt-5 mx-auto", 6, "test_data/fake_path.html"),
        ("div", "flex flex-col gap-y-5 max-w-5xl mt-5 mx-auto", 6, "test_data/diff_path.html"),
        ("div", "flex flex-col", 2, "_table.html"),
        ("div", "", 0, "_table.html")
    ]
    conn = sqlite3.connect(":memory:")
    parse_data(data, conn)
    cursor = conn.cursor()
    cursor.execute("SELECT name, classes, num_classes, file_path FROM tag_data")
    rows = cursor.fetchall()
    assert len(rows) == 4
    assert set(rows) == set(data)
    conn.close()

#  ------------ Tests for analyze_db_info -------------
# NOTE: tests rely on parse_data working correctly

# def test_analyze_db_info_creates_correct_csv_with_empty_data() -> None:
#     data=[]
#     conn = sqlite3.connect(":memory:")
#     parse_data(data, conn)
#     analyze_db_info(conn)
#     conn.close()

#     with open("table.csv", "r") as f:
#         content = f.read().strip()
    
#     assert content == "name,num_instances,classes,file_paths"

# def test_analyze_db_info_creates_correct_csv() -> None:
#     data = [
#         ("div", "flex flex-col gap-y-5 max-w-5xl mt-5 mx-auto", 6, "test_data/fake_path.html"),
#         ("div", "flex flex-col gap-y-5 max-w-5xl mt-5 mx-auto", 6, "test_data/diff_path.html"),
#         ("div", "flex flex-col gap-y-5 max-w-5xl mt-5 mx-auto", 6, "test_data/diff_path.html"),
#         ("div", "flex", 2, "_table.html"),
#         ("div", "flex", 2, "_table.html"),
#     ]
#     conn = sqlite3.connect(":memory:")
#     parse_data(data, conn)
#     analyze_db_info(conn)
#     conn.close()

#     with open("table.csv", "r", newline='') as file:
#         reader = csv.reader(file)
#         headers = next(reader)
#         first = next(reader)        
#         second = next(reader)
    
#     expected_first_no_paths = ["div", "3", "flex flex-col gap-y-5 max-w-5xl mt-5 mx-auto"]
#     assert first[:3] == expected_first_no_paths
#     expected_second_no_paths = ["div", "2", "flex"]
#     assert second[:3] == expected_second_no_paths

#     expected_first_paths = {"test_data/fake_path.html", "test_data/diff_path.html"}
#     first_paths = first[3].split(",")
#     assert len(first_paths) == 2
#     assert set(first_paths) == expected_first_paths
    
#     assert second[3] == "_table.html"


