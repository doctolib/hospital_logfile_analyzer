from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.1.4'

setup(
  name = 'hospital_logfile_analyzer',
  packages = find_packages(),
  version = VERSION,
  license='MIT',
  description = 'Tool to convert plain-text hospital integration engines\' log files to structured data',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Pavlo Dyban (Doctolib GmbH)',
  author_email = 'pavlo.dyban@doctolib.com',
  url = 'https://github.com/doctolib/hospital_logfile_analyzer',
  download_url = f"https://github.com/doctolib/hospital_logfile_analyzer/archive/v.{VERSION}.tar.gz",
  keywords = ['logfile', 'parser', 'integration engine', 'communication server',
        'HIS', 'hospital', 'information system', 'communication',
        'TCP/IP', 'structured data'],
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: System Administrators',
    'Intended Audience :: Developers',
    'Topic :: Internet :: Log Analysis',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  test_suite="hospital_logfile_analyzer.test",
  entry_points={
    'console_scripts': [
        'hla = hospital_logfile_analyzer.__main__:main',
    ],
  },
)
