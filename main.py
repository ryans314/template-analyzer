import sys
from typing import List, Any

def get_files(path: str) -> List[str]:
    """
    Given a directory path, return a list of all
    *.html filepaths in the directory
    """
    return ["hi"]

#TODO: strengthen spec
def parse_html(file_path: str) -> Any:
    """
    Given a filepath, return a useful data representation
    containing information about the tags and class sets
    in the html
    """
    pass

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

    #generate list of files

    #for each file:

        # html -> data
        # data -> db

    # aggregate data from db

    # aggregated data -> CSV output

    pass