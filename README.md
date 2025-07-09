# template-analyzer
A tool to help identify repetitive html by counting the occurrences of each tag + class combination, using sqlite3 and BeautifulSoup. Reads all .html files in a directory, analyzes the tag+class frequency, and puts output in a CSV file. 

## Setup

1. Download the repo
2. To install the dependencies, run ```pip install -r requirements.txt```

## Usage
```python analyze.py <analysis-path> [-o <output-file> | --output <output-file>]```

* ```<analysis-path>``` is the path to a directory or file to analyze
* ```<output-file>``` is the path/name that will be used for the output file.

