import pytest
from pytest import raises
from main import get_filepaths

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

