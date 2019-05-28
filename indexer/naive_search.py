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
query4 = "okoljevarstveno dovoljenje"
query5 = "stanovanjski objekt"
query6 = "registracija samostojnega podjetnika"


def main():

    import time
    start = time.time()

    paths = get_filepaths()

    # get stopwords only once
    slovene_stopwords = get_stopwords()

    # process the query
    text_for_query = get_text(query4)
    all_tokens_for_query = nltk.word_tokenize(text_for_query)

    print("q1 text", text_for_query)
    print("q1 tokens", all_tokens_for_query)

    print("Results for a query: \"", text_for_query, "\"", "\n")

    results = []
    for filePath in paths:
        original_text_for_doc = get_text(filePath)
        all_tokens_for_doc = nltk.word_tokenize(original_text_for_doc)
        postings_for_doc = get_postings(all_tokens_for_doc, slovene_stopwords)

        all_snippets = ""
        frequencies = 0

        for word in all_tokens_for_query:
            if word in postings_for_doc:
                frequencies += postings_for_doc[word]["frequency"]

                snippet = ""
                for index in postings_for_doc[word]["indexes"]:
                    if index > 3:
                        snippet += "... "
                    if index > 2:
                        snippet = snippet + all_tokens_for_doc[index-3] + " "
                    if index > 1:
                        snippet = snippet + all_tokens_for_doc[index-2] + " "
                    if index > 0:
                        snippet += all_tokens_for_doc[index-1] + " "

                    snippet += all_tokens_for_doc[index] + " "

                    if index < len(all_tokens_for_doc) - 1:
                        snippet += all_tokens_for_doc[index+1] + " "
                    if index < len(all_tokens_for_doc) - 2:
                        snippet = snippet + all_tokens_for_doc[index+2] + " "
                    if index < len(all_tokens_for_doc) - 3:
                        snippet = snippet + all_tokens_for_doc[index+3] + " "
                    if index < len(all_tokens_for_doc) - 4:
                        snippet += "... "

                all_snippets += snippet

        if frequencies > 0:
            results.append({"frequency": frequencies, "snippets": all_snippets[0:200], "path": filePath})

    end = time.time()
    print("Results found in", end - start, "\n")

    print("Frequencies Document                                  Snippet")
    print(
        "----------- ----------------------------------------- -----------------------------------------------------------")

    results_sorted = sorted(results, key=lambda x: x["frequency"], reverse=True)

    for res in results_sorted:
        print(res["frequency"], "\t", res["path"], "\t", res["snippets"])



if __name__ == "__main__":
    main()