# Inverted index: building it and using it

## About

Simple implementation of inverted index with sqlite.
Querying using inverted index and sequential file reading.
Report in the usual place. 

## Requirements

### Python

Download Python 3.6 or 3.7 from [Python website](https://www.python.org/downloads/). 
We don't guarantee that all libraries work with lower 3.x sub-versions. 
Do not use Python 2.7.

#### Note
All instructions are tested on Linux, we don't guarantee that everything will work on Windows or MacOS.
All further instructions are written with assumption that Python 3 is your default Python 
(be sure to check the PATH or write `python3` and `pip3` instead of `python` and `pip` ).

In case of `EnvironmentError`, run `pip install <module> --user`.
Or you can use pipenv. 
You need to install it first (`pip install pipenv`) and then run `pipenv shell`. 
Note that you must then install needed libraries with `pipenv` not `pip`.

#### Libraries

- BeautifulSoup4: run `pip install bs4`
- NLTK: run `pip install nltk`

## Running

- first run `python ./indexer/data_processor.py` to build the database for inverted index 
- then run `python ./indexer/index_search.py` to search with the inverted index
- then run `python ./indexer/naive_search.py` to search with sequential file reading

There are no parameters for selecting what to search.
The predefined search strings are defined in already mentioned files ending with `search.py`.
Go in the files and change the variable in line `text_for_query = get_text(queryX)`.
