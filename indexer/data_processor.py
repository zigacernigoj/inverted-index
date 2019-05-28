# DATA PROCESSOR:
# read HTML files
# get text from HTML files

import os
from os.path import isfile
from bs4 import BeautifulSoup
import re
import string

import nltk

from indexer.sqlite import create_connection, create_table, insert_sql, bulk_insert_postings_sql, bulk_insert_words_sql, close_connection

nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import stopwords


def get_stopwords():
    # load stopwords
    # used ajdapretnar's list - manually added to .../nltk_data/corpora/stopwords
    # (https://github.com/nltk/nltk_data/issues/54)
    # plus provided stopwords (http://zitnik.si/teaching/wier/data/pa3/stopwords.py)
    stop_words_slovene = set(stopwords.words("slovenian")).union(
        {"ter", "nov", "novo", "nova", "zato", "še", "zaradi", "a", "ali", "april", "avgust", "b", "bi", "bil", "bila",
         "bile",
         "bili", "bilo", "biti", "blizu", "bo", "bodo", "bojo", "bolj", "bom", "bomo", "boste", "bova", "boš", "brez",
         "c",
         "cel", "cela", "celi", "celo", "d", "da", "daleč", "dan", "danes", "datum", "december", "deset", "deseta",
         "deseti",
         "deseto", "devet", "deveta", "deveti", "deveto", "do", "dober", "dobra", "dobri", "dobro", "dokler", "dol",
         "dolg",
         "dolga", "dolgi", "dovolj", "drug", "druga", "drugi", "drugo", "dva", "dve", "e", "eden", "en", "ena", "ene",
         "eni",
         "enkrat", "eno", "etc.", "f", "februar", "g", "g.", "ga", "ga.", "gor", "gospa", "gospod", "h", "halo", "i",
         "idr.",
         "ii", "iii", "in", "iv", "ix", "iz", "j", "januar", "jaz", "je", "ji", "jih", "jim", "jo", "julij", "junij",
         "jutri",
         "k", "kadarkoli", "kaj", "kajti", "kako", "kakor", "kamor", "kamorkoli", "kar", "karkoli", "katerikoli",
         "kdaj",
         "kdo", "kdorkoli", "ker", "ki", "kje", "kjer", "kjerkoli", "ko", "koder", "koderkoli", "koga", "komu", "kot",
         "kratek", "kratka", "kratke", "kratki", "l", "lahka", "lahke", "lahki", "lahko", "le", "lep", "lepa", "lepe",
         "lepi",
         "lepo", "leto", "m", "maj", "majhen", "majhna", "majhni", "malce", "malo", "manj", "marec", "me", "med",
         "medtem",
         "mene", "mesec", "mi", "midva", "midve", "mnogo", "moj", "moja", "moje", "mora", "morajo", "moram", "moramo",
         "morate", "moraš", "morem", "mu", "n", "na", "nad", "naj", "najina", "najino", "najmanj", "naju", "največ",
         "nam",
         "narobe", "nas", "nato", "nazaj", "naš", "naša", "naše", "ne", "nedavno", "nedelja", "nek", "neka", "nekaj",
         "nekatere", "nekateri", "nekatero", "nekdo", "neke", "nekega", "neki", "nekje", "neko", "nekoga", "nekoč",
         "ni",
         "nikamor", "nikdar", "nikjer", "nikoli", "nič", "nje", "njega", "njegov", "njegova", "njegovo", "njej",
         "njemu",
         "njen", "njena", "njeno", "nji", "njih", "njihov", "njihova", "njihovo", "njiju", "njim", "njo", "njun",
         "njuna",
         "njuno", "no", "nocoj", "november", "npr.", "o", "ob", "oba", "obe", "oboje", "od", "odprt", "odprta",
         "odprti",
         "okoli", "oktober", "on", "onadva", "one", "oni", "onidve", "osem", "osma", "osmi", "osmo", "oz.", "p", "pa",
         "pet",
         "peta", "petek", "peti", "peto", "po", "pod", "pogosto", "poleg", "poln", "polna", "polni", "polno",
         "ponavadi",
         "ponedeljek", "ponovno", "potem", "povsod", "pozdravljen", "pozdravljeni", "prav", "prava", "prave", "pravi",
         "pravo",
         "prazen", "prazna", "prazno", "prbl.", "precej", "pred", "prej", "preko", "pri", "pribl.", "približno",
         "primer",
         "pripravljen", "pripravljena", "pripravljeni", "proti", "prva", "prvi", "prvo", "r", "ravno", "redko", "res",
         "reč",
         "s", "saj", "sam", "sama", "same", "sami", "samo", "se", "sebe", "sebi", "sedaj", "sedem", "sedma", "sedmi",
         "sedmo",
         "sem", "september", "seveda", "si", "sicer", "skoraj", "skozi", "slab", "smo", "so", "sobota", "spet", "sreda",
         "srednja", "srednji", "sta", "ste", "stran", "stvar", "sva", "t", "ta", "tak", "taka", "take", "taki", "tako",
         "takoj", "tam", "te", "tebe", "tebi", "tega", "težak", "težka", "težki", "težko", "ti", "tista", "tiste",
         "tisti",
         "tisto", "tj.", "tja", "to", "toda", "torek", "tretja", "tretje", "tretji", "tri", "tu", "tudi", "tukaj",
         "tvoj",
         "tvoja", "tvoje", "u", "v", "vaju", "vam", "vas", "vaš", "vaša", "vaše", "ve", "vedno", "velik", "velika",
         "veliki",
         "veliko", "vendar", "ves", "več", "vi", "vidva", "vii", "viii", "visok", "visoka", "visoke", "visoki", "vsa",
         "vsaj",
         "vsak", "vsaka", "vsakdo", "vsake", "vsaki", "vsakomur", "vse", "vsega", "vsi", "vso", "včasih", "včeraj", "x",
         "z",
         "za", "zadaj", "zadnji", "zakaj", "zaprta", "zaprti", "zaprto", "zdaj", "zelo", "zunaj", "č", "če", "često",
         "četrta",
         "četrtek", "četrti", "četrto", "čez", "čigav", "š", "šest", "šesta", "šesti", "šesto", "štiri", "ž", "že",
         "svoj",
         "jesti", "imeti", "\u0161e", "iti", "kak", "www", "km", "eur", "pač", "del", "kljub", "šele", "prek", "preko",
         "znova", "morda", "kateri", "katero", "katera", "ampak", "lahek", "lahka", "lahko", "morati", "torej"})

    return stop_words_slovene


# returns a list of all filepaths
def get_filepaths():
    base_dir = "./PA3-data"
    filepath_list = []

    for root, dirs, files in os.walk(base_dir):
        filepath_list.extend(os.path.join(root, x) for x in files if x.endswith(".html"))

    return filepath_list


# returns only a text from HTML document
# RETURNS BASE TEXT FOR ALL FURTHER WORK
def get_text(file_or_string):
    if isfile(file_or_string):

        # print(filepath)
        f = open(file_or_string, "r", encoding='utf-8', errors='ignore')
        content = f.read()
        f.close()

        # parse, prettify, parse again ... because of *** GOV code
        parsed = BeautifulSoup(BeautifulSoup(content, 'html.parser').prettify(), 'html.parser')

        # additional steps
        # TODO: describe in report
        for s in parsed("script"):
            s.decompose()
        for s in parsed("noscript"):
            s.decompose()
        for s in parsed("style"):
            s.decompose()

        return parsed.text

    elif type(file_or_string) is str:
        return file_or_string

    else:
        print("something wrong with input")
        raise Exception


def get_only_words(tokens, slovene_stopwords):
    return [token.lower() for token in tokens if token not in slovene_stopwords and token not in string.punctuation]


def get_postings(tokens, slovene_stopwords):

    postings_for_doc = {}

    for index, token in enumerate(tokens):
        token = token.lower()

        if token not in slovene_stopwords and token not in string.punctuation:
            if token in postings_for_doc:
                postings_for_doc[token]["indexes"].append(index)
                postings_for_doc[token]["frequency"] += 1
            else:
                postings_for_doc[token] = {"indexes": [index], "frequency": 1}

    return postings_for_doc


# just a demo, how to call functions above
def main():
    paths = get_filepaths()

    # get stopwords only once
    slovene_stopwords = get_stopwords()

    conn = create_connection('db.db')

    sql = 'CREATE TABLE IndexWord (  word TEXT PRIMARY KEY );'
    sql2 = 'CREATE TABLE Posting (' \
           '  word TEXT NOT NULL,' \
           '  documentName TEXT NOT NULL,' \
           '  frequency INTEGER NOT NULL,' \
           '  indexes TEXT NOT NULL,' \
           '  PRIMARY KEY(word, documentName),' \
           '  FOREIGN KEY (word) REFERENCES IndexWord(word)' \
           ');'

    create_table(conn, sql)
    create_table(conn, sql2)

    print("getting words")
    unique_words = []
    for filePath in paths:
        original_text_for_doc = get_text(filePath)
        all_tokens_for_doc = nltk.word_tokenize(original_text_for_doc)
        words_for_doc = get_only_words(all_tokens_for_doc, slovene_stopwords)
        print("got words for", filePath)
        unique_words.extend(words_for_doc)

    unique_words = set(unique_words)

    print("inserting words")
    try:
        bulk_insert_words_sql(conn, unique_words)
    except Exception as e:
        print(e)

    for filePath in paths:
        try:
            print("getting postings for", filePath)

            # get base text
            original_text_for_doc = get_text(filePath)

            # get tokens - separated WORDS, STOPWORDS AND PUNCTUATION
            # DO THIS SAME PROCEDURE WHEN SEARCHING !!!
            all_tokens_for_doc = nltk.word_tokenize(original_text_for_doc)
            # print(all_tokens_for_doc)

            postings_for_doc = get_postings(all_tokens_for_doc, slovene_stopwords)

            # print(filePath, postings_for_doc)

            print("inserting postings")
            postings_for_db = []
            for item in postings_for_doc:
                indexes = ','.join(str(e) for e in postings_for_doc[item]['indexes'])
                postings_for_db.append([item, filePath, postings_for_doc[item]['frequency'], indexes])

            bulk_insert_postings_sql(conn, postings_for_db)

            # break

        except Exception as e:
            print("DOC:", filePath, e)
            # break

    close_connection(conn)

    pass


if __name__ == "__main__":
    main()
