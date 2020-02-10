# Introduction
Tool to convert plain-text hospital integration engines' log files to
structured data. Currently supported logfile formats:
- Cloverleaf plain-text log files (NB: This tool is not affiliated with Infor Cloverleaf.)

![Convert plain-text log files to structured data](https://github.com/doctolib/hospital_logfile_analyzer/blob/master/preview.png?raw=true)

# How to install

## Install from Pypi
```bash
pip install hospital_logfile_analyzer
```

## Install from Github
Download the latest release as a `tar.gz` archive from the [Github repository page](https://github.com/doctolib/hospital_logfile_analyzer/releases):
```bash
wget https://github.com/doctolib/hospital_logfile_analyzer/archive/v.0.1.tar.gz
tar -xvf v.0.1.tar.gz
cd hospital_logfile_analyzer
rm v.0.1.tar.gz
python setup.py install
```


## Install from source code
Using git, clone the repository to your working directory, and install the package:
```bash
git clone git@github.com:doctolib/hospital_logfile_analyzer.git
cd hospital_logfile_analyzer
python setup.py install
```

## Prerequisites
This package supports Python 3 and has not been tested with Python 2.

To view and run the attached Jupyter Notebooks, best install an
[Anaconda environment](https://docs.anaconda.com/anaconda/install/).

## Command-line interface
You can execute the logfile parser in the command-line of your choice (e.g. bash).
`main.py` implements the command-line argument parser.
Display all options:
```bash
python -m hospital_logfile_analyzer --help
```

The easiest call to run the application:
```bash
python -m hospital_logfile_analyzer mylogfile.log output_structured_log.json
```

A more sophisticated application call would involve mapping and/or field filtering:
```bash
python -m hospital_logfile_analyzer mylogfile.log output_structured_log.json --mappingfile my_mapping.json --filterfile my_filter.json
```
For instructions on how to create field maps and filters,
see the respective sections in text below.

## Jupyter Notebook
You will find examples on how to execute this package in a Jupyter Notebook
inside [jupyter_notebooks](jupyter_notebooks) directory.

## Package
You can use the logfile parser directly in your Python code:
```python
from hospital_logfile_analyzer.parsers import parse
parser = parse('hospital_logfile_analyzer/test/test.log')
print(len(parser.events))
```

## How to create custom mappings and field filters

### Field Mapping
Fields can be mapped across different levels of hierarchy.
E.g. you can map `root.child1.child2.key1` to `root.key1`.
The mapping allows you to propagate fields from lower levels of hierarchy
to the top. Together with filters,
this allows for very efficient analysis of structured data.

Mapping is given by a JSON dictionary with the source field names being the
keys, and the target field names the values.
The field names inside subtrees are separated by dots.

The following example snippet will copy (or move, depending on the function
parameters) the value of field `Tree.Error Code` into `Error Code`:
```json
{
  "Tree.Error Code": "Error Code",
  "Tree.Result.Code": "Result Code"
}
```
The field map has to be stored as a UTF-8 encoded JSON file. For instructions
on how to pass this file to the application, see the CLI or the package usage
documentation in text above.

### Field Filters
Field filters allow to remove fields and subtrees from the structured data.

The following example will remove fields `Tree.Error Code` and will keep
`Tree.Result.Code`:
```json
{
  "Tree.Error Code": false,
  "Tree.Result.Code": true
}
```
The field map has to be stored as a UTF-8 encoded JSON file. For instructions
on how to pass this file to the application, see the CLI or the Python package
usage documentation in text above.

# How to test
Execute in the root folder of the repository:
```bash
python -m unittest
```
This will discover and execute all tests contained
inside `hospital_logfile_analyzer/test`.

# How to contribute
You can add your own logfile parsers:
1. Inherit `YourOwnParser` from the abstract parent interface [`LogfileParser`](hospital_logfile_analyzer/parsers/logfile_parser.py).
2. Add unit tests by adding `test_yourownparser.py` under `hospital_logfile_analyzer/test`.
3. Commit changes to your own branch and create a pull request.
The tests on the branch must run green before the
branch can be merged.

# License
See [LICENSE](LICENSE).
