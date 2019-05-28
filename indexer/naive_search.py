import re

from indexer.data_processor import get_filepaths, get_stopwords, get_text, get_tokens
from indexer.sqlite import create_connection, close_connection, select_sql

query1 = "predelovalne dejavnosti"
query2 = "trgovina"
query3 = "social services"


def main():
    paths = get_filepaths()

    # get stopwords only once
    slovene_stopwords = get_stopwords()

    conn = create_connection('db.db')

    # process the query
    text_for_query = get_text('evidenca trga')
    print("q1 text", text_for_query)

    tokens_for_query = get_tokens(text_for_query, slovene_stopwords)
    print("q1 tokens", tokens_for_query)

    sql = "SELECT word, documentName, frequency, indexes FROM Posting WHERE word IN ({seq})" \
        .format(seq=','.join(['?'] * len(tokens_for_query)))
    # values = ','.join(tokens_for_query)
    print(sql)
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
        print(item[0], item)

    length = len(tokens_for_query)
    matches = {}
    for document in documents:
        compare = 0
        total_length = 0
        start = 0
        print(document, documents[document])
        for item in sorted(documents[document]):
            word = documents[document][item]
            print(word, item, compare)
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
                if document not in matches:
                    matches[document] = []
                matches[document].append({'from': start, 'to': item + len(word)})
                reset = True

            if reset:
                compare = 0
                total_length = 0

    print(matches)

    for document in matches:
        # TODO format print
        # TODO get snippet from document in 3 words + from : to + 3 words
        frequency = len(matches[document])
        print(document, frequency)
        original_text_for_doc = get_text(document)
        for match in matches[document]:
            to = original_text_for_doc.find(' ', match['to'] + 1)
            to = original_text_for_doc.find(' ', to + 1)
            to = original_text_for_doc.find(' ', to + 1)
            print(match, original_text_for_doc[match['from']:to], to)

    return

    for filePath in paths:
        original_text_for_doc = get_text(filePath)
        indexes_of_occurrences = [m.start() for m in re.finditer(re.escape(tokens_for_query[0]), original_text_for_doc,
                                                                 flags=re.IGNORECASE)]

        if len(indexes_of_occurrences) > 0:
            print("file", filePath, "count", len(indexes_of_occurrences), "indexes", indexes_of_occurrences)

    close_connection(conn)


if __name__ == "__main__":
    main()
