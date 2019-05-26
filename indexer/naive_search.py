import data_processor
import re

from data_processor import get_filepaths
from data_processor import get_stopwords
from data_processor import get_text
from data_processor import get_tokens


query1 = "predelovalne dejavnosti"
query2 = "trgovina"
query3 = "social services"


def main():

    paths = get_filepaths()

    # get stopwords only once
    slovene_stopwords = get_stopwords()


    # process the query
    text_for_query = get_text(query1)
    print("q1 text", text_for_query)

    tokens_for_query = get_tokens(text_for_query, slovene_stopwords)
    print("q1 tokens", tokens_for_query)

    for filePath in paths:
        original_text_for_doc = get_text(filePath)
        indexes_of_occurrences = [m.start() for m in re.finditer(re.escape(tokens_for_query[0]), original_text_for_doc, flags=re.IGNORECASE)]

        if len(indexes_of_occurrences) > 0:
            print("file", filePath, "count", len(indexes_of_occurrences), "indexes",  indexes_of_occurrences)


if __name__ == "__main__":
    main()