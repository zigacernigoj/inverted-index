# DATA PROCESSOR:
# read HTML files
# get text from HTML files

import os
from os.path import isfile
from bs4 import BeautifulSoup


# returns only a text from HTML document
def get_text(filepath):
    if not isfile(filepath):
        return None

    # print(filepath)
    f = open(filepath, "r", encoding='utf-8', errors='ignore')
    content = f.read()
    f.close()

    parsed = BeautifulSoup(content, 'html.parser')
    for s in parsed("script"):
        s.decompose()
    for s in parsed("noscript"):
        s.decompose()
    for s in parsed("style"):
        s.decompose()

    return parsed.text


# returns a list of all filepaths
def get_filepaths():
    base_dir = "./PA3-data"
    filepath_list = []

    for root, dirs, files in os.walk(base_dir):
        filepath_list.extend(os.path.join(root, x) for x in files if x.endswith(".html"))

    return filepath_list


# just a demo, how to call functions above
def main():

    paths = get_filepaths()

    for p in paths:
        text = get_text(p)

    pass









if __name__ == "__main__":
    main()