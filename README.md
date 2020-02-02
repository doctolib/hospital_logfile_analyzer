# Introduction
Tool to convert plain-text hospital integration engines' log files to
structured data. Currently supported logfile formats:
- Cloverleaf plain-text log files (NB: This tool is not affiliated with Infor Cloverleaf.)

![Convert plain-text log files to structured data](preview.png)

# How to use
Using git, clone the repository to your working directory:
```bash
cd my_projects
git clone git@github.com:pavlodyban/hospital_logfile_analyzer.git
```

## Prerequisites
This package only support Python 3.

To view and run the Jupyter Notebook, you would best install an [Anaconda environment](https://docs.anaconda.com/anaconda/install/).

## Command-line interface
`main.py` implements a command-line argument parser.
Display all options:
```bash
python main.py --help
```

An easiest call to run the application:

```bash
python main.py mylogfile.log output_structured_log.json
```

A more sophisticated application call would involve mapping and/or field filtering:
```bash
python main.py mylogfile.log output_structured_log.json --mappingfile my_mapping.json --filterfile my_filter.json
```

## Package
You can use the logfile parser directly in your Python code:
```python
from parsers import parse
parser = parse('test/test.log')
print(len(parser.events))
```

# How to test
Execute `run_tests.sh` in your terminal, or run in the root folder of the package:
```bash
python -m unittest
```

# Todo

1. Add license.
2. Add authorship.
3. Publish to open source community.
