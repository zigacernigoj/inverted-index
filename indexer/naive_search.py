import re
import nltk
import time

from data_processor import get_filepaths
from data_processor import get_stopwords
from data_processor import get_text
from data_processor import get_postings


query1 = "predelovalne dejavnosti"
query2 = "trgovina"
query3 = "social services"


def main():

    import time
    start = time.time()

    paths = get_filepaths()

    # get stopwords only once
    slovene_stopwords = get_stopwords()

    # process the query
    text_for_query = get_text(query1)
    all_tokens_for_query = nltk.word_tokenize(text_for_query)

    print("q1 text", text_for_query)
    print("q1 tokens", all_tokens_for_query)

    print("Results for a query: \"", text_for_query, "\"", "\n")

    print("Frequencies Document                                  Snippet")
    print("----------- ----------------------------------------- -----------------------------------------------------------")

    for filePath in paths:
        original_text_for_doc = get_text(filePath)
        all_tokens_for_doc = nltk.word_tokenize(original_text_for_doc)
        postings_for_doc = get_postings(all_tokens_for_doc, slovene_stopwords)

        if all_tokens_for_query[0] in postings_for_doc:

            snippet = ""
            for index in postings_for_doc[all_tokens_for_query[0]]["indexes"]:
                snippet = snippet + "..." \
                                    + all_tokens_for_doc[index-3] + " " \
                                    + all_tokens_for_doc[index-2] + " " \
                                    + all_tokens_for_doc[index-1] + " " \
                                    + all_tokens_for_doc[index] + " " \
                                    + all_tokens_for_doc[index+1] + " " \
                                    + all_tokens_for_doc[index+2] + " " \
                                    + all_tokens_for_doc[index+3] + "..."

            print(postings_for_doc[all_tokens_for_query[0]]["frequency"], "\t", filePath, "\t", snippet)

    end = time.time()
    print("Results found in", end - start)

if __name__ == "__main__":
    main()