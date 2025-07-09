# template-analyzer
A tool to help identify repetitive html by counting the occurrences of each tag + class combination, using sqlite3 and BeautifulSoup. Reads all .html files in a directory, analyzes the tag+class frequency, and puts output in a CSV file. 

## Setup

1. Download the repo
2. To install the dependencies, run ```pip install -r requirements.txt```

## Usage
```python analyze.py <analysis-path> [-o <output-file> | --output <output-file>] [-mc <value> | --min-classes <value>] [-mo <value> | --min-occurrences <value>] [-ml <value> | --min-locations <value>] [-s | --short] ```

* ```<analysis-path>``` is the path to a directory or file to analyze

### Options
* ```--output <output-file>``` specifies the path/name that will be used for the output file. Defaults to template_analysis.csv
* ```--min-classes <value>``` specifies the minimum number of classes that tags must have to be included. Defaults to 1.
* ```--min-occurrences <value>``` specifies the minimum number of occurrences that tags+classes must have to be included. Defaults to 2.
* ```--min-occurrences <value>``` specifies the minimum number of unique file locations that tags+classes must have to be included. Defaults to 1.
* ```--short``` displays only the names of files where the tag+class was found, rather than file paths

### Examples
```python analyze.py src/templates``` will search all .html files in the src/templates directory for tag+class combinations that occur at least twice, with at least 1 class, and put the results in ./template_analysis.csv
```python analyze.py detail.html -o detail_analysis.csv -mc 5 -mo 3``` will search detail.html for tag+class combinations that have at least 5 classes, and occur at least 3 times, and put the output in ./detail_analysis.csv 