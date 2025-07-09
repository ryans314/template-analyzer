import sys
import os
from pathlib import Path
from bs4 import BeautifulSoup, Tag
import sqlite3
from sqlite3 import Connection
import csv
from typing import List, Tuple, Any

type TagEntry = tuple[str, str, int, str]

def get_filepaths(path: str) -> List[str]:
    """
    path: a path to a file or directory

    returns: a list of (filepath, filename) to all .html files in the directory,
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

def parse_html(content: str, file_path: str) -> List[TagEntry]:
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

def parse_data(data: List[TagEntry], conn: Connection) -> None:
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
    cursor.close()

def analyze_db_info(conn: Connection, csv_path="template_analysis.csv", min_classes=1, min_instances=2) -> None:
    """
    Given a connection to a populated database, analyze the tag data in the database and
    create a csv file with (name, num_occurrences, classes, file_paths) for each unique
    component (tag + classes). 

    Only include tags with at least min_classes (default=1) classes that occur at least min_instances (default=2) times.  
    """
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT name, COUNT(id) as num_instances, classes, GROUP_CONCAT(DISTINCT file_path) as file_paths
        FROM tag_data
        WHERE num_classes >= {min_classes}
        GROUP BY name, classes
        HAVING num_instances >= {min_instances}
        ORDER BY num_instances DESC
    ''')
    query_data = cursor.fetchall()

    if "." not in csv_path:
        csv_path += ".csv"

    if not os.path.isdir(csv_path):
        csv_path = Path(csv_path)
        csv_path.parent.mkdir(exist_ok=True, parents=True)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([header[0] for header in cursor.description])
        writer.writerows(query_data)

def parse_args(args: List) -> List:
    if (len(args) == 1):
        raise ValueError("Error: please provide a file path or directory to analyze as a command-line argument.")

    analysis_dir = None
    # Default values
    output_file = "template_analysis.csv"
    min_classes = 1
    min_occurrences = 2
    is_short = False

    i = 1
    while i < len(args):
        arg = args[i]
        if arg in ["-s", "--short"]:
            is_short = True
        elif arg.startswith("-") and i + 1  >= len(args):
            raise ValueError(f"Error: {arg} requires an additional argument")
        elif arg in ["-o", "--output"]:
            output_file = args[i+1]
            i += 1
        elif arg in ["-mc", "--min-classes"]:
            try:
                min_classes = int(args[i+1])
            except ValueError:
                raise ValueError(f"Error: {args[i+1]} is not an integer")
            i += 1
        elif arg in ["-mo", "--min-occurrences"]:
            try:
                min_occurrences = int(args[i+1])
            except ValueError:
                raise ValueError(f"Error: {args[i+1]} is not an integer")
            i += 1
        elif arg.startswith("-"):
            raise ValueError(f"Error: {arg} is not a recognized option")
        elif analysis_dir is None:
            analysis_dir = arg
        else:
            raise ValueError(f"Error: too many arguments")
        i += 1
    
    if analysis_dir is None:
        raise ValueError("Error: no target file or directory specified")
    
    return [analysis_dir, output_file, min_classes, min_occurrences, is_short]


if __name__ == "__main__":

    #parse command line arguments
    try:
        analysis_dir, output_file, min_classes, min_occurrences, is_short = parse_args(sys.argv)
    except ValueError as e:
        print(e)
        sys.exit(1)
            
    try:
        file_paths = get_filepaths(analysis_dir)
    except FileNotFoundError:
        print(f"Error: {analysis_dir} is not a path to a file or directory.")
        sys.exit(1)

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
        if is_short:
            data += parse_html(content, os.path.basename(file_path))
        else:
            data += parse_html(content, file_path)

    # Set up sqlite3 db and add data
    conn = sqlite3.connect("database.db")
    parse_data(data, conn)

    # analyze data in db and write to csv 
    analyze_db_info(conn, output_file, min_classes, min_occurrences)
    print(f"Output file created at: {output_file}")

    # Clean up
    conn.cursor().execute("DROP TABLE tag_data")
    conn.close()
    os.remove("database.db")