import sys
import os
from bs4 import BeautifulSoup, Tag
import sqlite3
from sqlite3 import Connection
import csv
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

def parse_html(content: str, file_path: str) -> List[Tuple[str, str, str]]:
    """
    Given a file_path and its content, return a 3-tuple for each tag in the file:
    (tag_name, class_strs, file_path), where class_strs is a alphabetically sorted,
    space separated string of classes in the tag. 
    """
    soup = BeautifulSoup(content, "html.parser")
    all_elements = soup.find_all(["div"])
    tags = [elem for elem in all_elements if isinstance(elem, Tag)]

    data = []
    for tag in tags:
        name = tag.name

        class_attr = tag.attrs.get("class")
        if class_attr is None:
            continue
        
        classes = sorted(list(set(class_attr)))
        classes.sort()
        num_classes = len(classes)
        class_strs = " ".join(str(class_name) for class_name in classes)
        data.append((name, class_strs, num_classes, file_path))

    return data

def parse_data(data: List[Tuple[str, str, str]], conn: Connection) -> None:
    """
    Given a data representation of tag data, update the
    database to include that data
    """
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tag_data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            classes TEXT,
            num_classes INTEGER,
            file_path TEXT
        )
    ''')

    cursor.executemany("INSERT INTO tag_data (name, classes, num_classes, file_path) VALUES(?, ?, ?, ?)", data)
    conn.commit()

def analyze_db_info(conn: Connection, min_classes=1, min_instances=2) -> None:
    """
    TODO: Fix this
    # Given a connection to a populated database, return a list of repeated tags and classes,
    # with each repeated tag being a 4-tuple of (name, classes, num_instances, file_paths),
    # where num_instances is the number of tags with the same name and classes set, 
    # and file_paths is the set of file_paths that include the tag. 

    # Only include tags with at least min_classes (default=1) classes that occur at least min_instances (default=2) times.  
    """
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT name, classes, COUNT(id) as num_instances, GROUP_CONCAT(file_path, ', ') as file_paths
        FROM tag_data
        WHERE num_classes >= {min_classes}
        GROUP BY name, classes
        HAVING num_instances >= {min_instances}
        ORDER BY num_instances DESC
    ''')
    query_data = cursor.fetchall()
    with open("table.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([header[0] for header in cursor.description])
        writer.writerows(query_data)

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

    # Set up sqlite3 db and add data
    conn = sqlite3.connect("database.db")
    parse_data(data, conn)

    # analyze data in db and write to csv 
    analyze_db_info(conn)

    # Clean up
    conn.cursor().execute("DROP TABLE tag_data")
    conn.close()