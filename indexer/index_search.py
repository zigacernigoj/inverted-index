import collections
import operator
import re
import time

import nltk

from indexer.data_processor import get_text
from indexer.sqlite import create_connection, close_connection, select_sql

query1 = "predelovalne dejavnosti"
query2 = "trgovina"
query3 = "social services"


def main():
    # get stopwords only once
    # slovene_stopwords = get_stopwords()
    started = time.time()
    conn = create_connection('../inverted-index.db')

    # process the query
    text_for_query = get_text(query3)
    # print("q1 text", text_for_query)

    tokens_for_query = nltk.word_tokenize(text_for_query)

    # tokens_for_query = get_tokens(text_for_query, slovene_stopwords)
    # print("q1 tokens", tokens_for_query)

    sql = "SELECT word, documentName, frequency, indexes FROM Posting WHERE word IN ({seq})" \
        .format(seq=','.join(['?'] * len(tokens_for_query)))
    # values = ','.join(tokens_for_query)
    # print(sql)
    results = select_sql(conn, sql, tokens_for_query)
    # print(results)
    documents = {}
    for item in results:
        document = item[1]
        if document not in documents:
            documents[document] = {}
        indexes = item[3].split(",")
        for index in indexes:
            documents[document][int(index)] = item[0]
        # print(item[0], item)

    length = len(tokens_for_query)
    results = {}
    matches = {}
    for document in documents:
        if document not in results:
            results[document] = 0
        compare = 0
        total_length = 0
        start = 0
        words = 0
        # print(document, documents[document])
        for item in sorted(documents[document]):
            word = documents[document][item]
            # print("BBB", word, item, compare)
            reset = False
            add_document = False
            print(compare, length)
            if word == tokens_for_query[compare]:
                if compare == 0:
                    start = item
                elif start + total_length <= item:
                    reset = True
                if not reset:
                    compare += 1
                    total_length += 2
                    words += 1
            else:
                if start == 0:
                    start = item
                    words = 1
                add_document = True
                reset = True

            if compare == length:
                add_document = True
                reset = True

            if add_document:
                # print("CCC", compare, length, start, words)
                if document not in matches:
                    matches[document] = []
                matches[document].append({'from': start, 'to': item, 'words': words})
                if words > 0:
                    results[document] += words
                else:
                    results[document] += 1

                if compare == 1 and (word != tokens_for_query[0] or length == 1):
                    # print("FFF", compare, length, item, words, word, tokens_for_query[0])
                    matches[document].append({'from': item, 'to': item, 'words': words})
                    results[document] += 1
                    reset = True
                if compare == 1 and word != tokens_for_query[0] and length != 1:
                    start = item
                    reset = False

            if reset:
                words = 0
                start = 0
                compare = 0
                total_length = 0

        if compare > 0:
            # print("CCC", compare, length, start, words)
            if document not in matches:
                matches[document] = []
            matches[document].append({'from': start, 'to': item, 'words': words})
            """
            reset = False
            if word == tokens_for_query[compare]:
                if compare == 0:
                    start = item
                elif start + total_length <= item:
                    reset = True
                if not reset:
                    compare += 1
                    total_length += len(word) + 2
            else:
                reset = True

            if compare == length:
                print("CCC", compare, length)
                if document not in matches:
                    matches[document] = []
                matches[document].append({'from': start, 'to': item + len(word)})
                reset = True

            if reset:
                compare = 0
                total_length = 0
                
            """

    # print("MMM:", matches)

    # print("AAAAAA", sorted(results.items(), reverse=True, key=operator.itemgetter(1)))
    # exit(0)
    ended = time.time()
    print("Results for a query: \"", text_for_query, "\"", "\n")

    print("Results found in", ended - started)

    print("Frequencies Document                                  Snippet")
    print(
        "----------- ----------------------------------------- -----------------------------------------------------------")

    for document in sorted(results.items(), reverse=True, key=operator.itemgetter(1)):
        # TODO format print
        freq = document[1]
        document = document[0]
        frequency = len(matches[document])
        if frequency < freq:
            frequency = freq
        # print("DDDD", document, frequency, results[document])
        original_text_for_doc = get_text(document.replace("\\", "/"))
        all_tokens_for_doc = nltk.word_tokenize(original_text_for_doc)
        snippet = ""
        for match in matches[document]:
            index = match['from']
            snippet += "..." \
                      + all_tokens_for_doc[index - 3] + " " \
                      + all_tokens_for_doc[index - 2] + " " \
                      + all_tokens_for_doc[index - 1] + " "
            maximum = 3 + match['words']
            i = 0
            while i < maximum:
                snippet += all_tokens_for_doc[index + i] + " "
                i += 1
            snippet += "... "
            # print(match, snippet)
            # print(snippet)
        print(frequency, "\t", document, "\t", snippet[0:200])

    close_connection(conn)


if __name__ == "__main__":
    main()
