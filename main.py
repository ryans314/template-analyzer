import sys
import os

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
    args = sys.argv
    if len(args) != 2:
        print("Error: please provide a filepath or directory to analyze as a command-line argument.")
        sys.exit(1)
    path = args[1]
    
    #parse command line arguments
    files = get_filepaths(path)
    print("h1")
    #generate list of files

    #for each file:

        # html -> data
        # data -> db

    # aggregate data from db

    # aggregated data -> CSV output

    pass