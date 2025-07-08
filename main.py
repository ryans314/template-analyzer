import sys
import os
from bs4 import BeautifulSoup, Tag

from typing import List, Tuple, Any

def get_filepaths(path: str) -> List[str]:
    """
    path: a path to a file or directory

    returns: a list of filepaths to all .html files in the directory,
             or a list of a single filepath if path is to a file.
             If the path is invalid, raise an error
    """

    if (os.path.isfile(path)):
        return [path]
    elif (os.path.isdir(path)):
        directories = os.walk(path)
        filepaths = []
        for dirpath, dirnames, filenames in directories:
            for filename in filenames:
                if filename.endswith(".html"):
                    filepath = os.path.join(dirpath,filename)
                    filepaths.append(filepath)
        if (not filepaths):
            print("no .html files to analyze in the given directory.")
            sys.exit(0)
        return filepaths
    
    raise FileNotFoundError(f"\'{path}\' is not a path to a file or directory.")
    # if (os.path.isfile(path)):
    #     with open(path, "r") as f:
    #         content = f.read()
    #         return [content]
    # elif (os.path.isdir(path)):


def parse_html(content: str, file_path: str) -> Any:
    """
    Given a file_path and its content, return a 3-tuple for each tag in the file:
    (tag_name, class_list (sorted), file_path)
    """
    soup = BeautifulSoup(content, "html.parser")
    all_elements = soup.find_all(["div"])
    tags = [elem for elem in all_elements if isinstance(elem, Tag)]

    data = []
    for tag in tags:
        name = tag.name
        classes = sorted(tag.attrs["class"])
        classes.sort()
        
        data.append((name, classes, file_path))

    return data

def parse_data(data: dict) -> None:
    """
    Given a data representation of tag data, update the
    database to include that data
    """
    pass

def aggregate_data() -> None:
    """
    Given a sqlite3 database populated with tag data from
    many files, aggregate the data to include, for each unique 
    tag+class_set:
    - The tag
    - The set of classes
    - The number of occurrences
    - The locations where it occurs
    """
    pass

def format_aggregated_data() -> None:
    pass
if __name__ == "__main__":

    #parse command line arguments
    args = sys.argv
    if len(args) != 2:
        print("Error: please provide a file path or directory to analyze as a command-line argument.")
        sys.exit(1)
    path = args[1]
    
    file_paths = get_filepaths(path)

    data = []
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: the file \'{file_path}\' was not found")
            sys.exit(1)
        except IOError as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)

        data += parse_html(content, file_path)

    # aggregate data from db

    # aggregated data -> CSV output

    pass