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


def get_stopwords():
    # load stopwords
    # used ajdapretnar's list (available in file 'slovenian', https://github.com/nltk/nltk_data/issues/54)
    # plus provided stopwords (http://zitnik.si/teaching/wier/data/pa3/stopwords.py)
    stop_words_slovene = {"ter", "nov", "novo", "nova", "zato", "še", "zaradi", "a", "ali", "april", "avgust", "b",
                          "bi", "bil", "bila", "bile", "bili", "bilo", "biti", "blizu", "bo", "bodo", "bojo", "bolj",
                          "bom", "bomo", "boste", "bova", "boš", "brez", "c", "cel", "cela", "celi", "celo", "d", "da",
                          "daleč", "dan", "danes", "datum", "december", "deset", "deseta", "deseti", "deseto", "devet",
                          "deveta", "deveti", "deveto", "do", "dober", "dobra", "dobri", "dobro", "dokler", "dol",
                          "dolg", "dolga", "dolgi", "dovolj", "drug", "druga", "drugi", "drugo", "dva", "dve", "e",
                          "eden", "en", "ena", "ene", "eni", "enkrat", "eno", "etc.", "f", "februar", "g", "g.", "ga",
                          "ga.", "gor", "gospa", "gospod", "h", "halo", "i", "idr.", "ii", "iii", "in", "iv", "ix",
                          "iz", "j", "januar", "jaz", "je", "ji", "jih", "jim", "jo", "julij", "junij", "jutri", "k",
                          "kadarkoli", "kaj", "kajti", "kako", "kakor", "kamor", "kamorkoli", "kar", "karkoli",
                          "katerikoli", "kdaj", "kdo", "kdorkoli", "ker", "ki", "kje", "kjer", "kjerkoli", "ko",
                          "koder", "koderkoli", "koga", "komu", "kot", "kratek", "kratka", "kratke", "kratki", "l",
                          "lahka", "lahke", "lahki", "lahko", "le", "lep", "lepa", "lepe", "lepi", "lepo", "leto", "m",
                          "maj", "majhen", "majhna", "majhni", "malce", "malo", "manj", "marec", "me", "med", "medtem",
                          "mene", "mesec", "mi", "midva", "midve", "mnogo", "moj", "moja", "moje", "mora", "morajo",
                          "moram", "moramo", "morate", "moraš", "morem", "mu", "n", "na", "nad", "naj", "najina",
                          "najino", "najmanj", "naju", "največ", "nam", "narobe", "nas", "nato", "nazaj", "naš", "naša",
                          "naše", "ne", "nedavno", "nedelja", "nek", "neka", "nekaj", "nekatere", "nekateri",
                          "nekatero", "nekdo", "neke", "nekega", "neki", "nekje", "neko", "nekoga", "nekoč", "ni",
                          "nikamor", "nikdar", "nikjer", "nikoli", "nič", "nje", "njega", "njegov", "njegova",
                          "njegovo", "njej", "njemu", "njen", "njena", "njeno", "nji", "njih", "njihov", "njihova",
                          "njihovo", "njiju", "njim", "njo", "njun", "njuna", "njuno", "no", "nocoj", "november",
                          "npr.", "o", "ob", "oba", "obe", "oboje", "od", "odprt", "odprta", "odprti", "okoli",
                          "oktober", "on", "onadva", "one", "oni", "onidve", "osem", "osma", "osmi", "osmo", "oz.", "p",
                          "pa", "pet", "peta", "petek", "peti", "peto", "po", "pod", "pogosto", "poleg", "poln",
                          "polna", "polni", "polno", "ponavadi", "ponedeljek", "ponovno", "potem", "povsod",
                          "pozdravljen", "pozdravljeni", "prav", "prava", "prave", "pravi", "pravo", "prazen", "prazna",
                          "prazno", "prbl.", "precej", "pred", "prej", "preko", "pri", "pribl.", "približno", "primer",
                          "pripravljen", "pripravljena", "pripravljeni", "proti", "prva", "prvi", "prvo", "r", "ravno",
                          "redko", "res", "reč", "s", "saj", "sam", "sama", "same", "sami", "samo", "se", "sebe",
                          "sebi", "sedaj", "sedem", "sedma", "sedmi", "sedmo", "sem", "september", "seveda", "si",
                          "sicer", "skoraj", "skozi", "slab", "smo", "so", "sobota", "spet", "sreda", "srednja",
                          "srednji", "sta", "ste", "stran", "stvar", "sva", "t", "ta", "tak", "taka", "take", "taki",
                          "tako", "takoj", "tam", "te", "tebe", "tebi", "tega", "težak", "težka", "težki", "težko",
                          "ti", "tista", "tiste", "tisti", "tisto", "tj.", "tja", "to", "toda", "torek", "tretja",
                          "tretje", "tretji", "tri", "tu", "tudi", "tukaj", "tvoj", "tvoja", "tvoje", "u", "v", "vaju",
                          "vam", "vas", "vaš", "vaša", "vaše", "ve", "vedno", "velik", "velika", "veliki", "veliko",
                          "vendar", "ves", "več", "vi", "vidva", "vii", "viii", "visok", "visoka", "visoke", "visoki",
                          "vsa", "vsaj", "vsak", "vsaka", "vsakdo", "vsake", "vsaki", "vsakomur", "vse", "vsega", "vsi",
                          "vso", "včasih", "včeraj", "x", "z", "za", "zadaj", "zadnji", "zakaj", "zaprta", "zaprti",
                          "zaprto", "zdaj", "zelo", "zunaj", "č", "če", "često", "četrta", "četrtek", "četrti",
                          "četrto", "čez", "čigav", "š", "šest", "šesta", "šesti", "šesto", "štiri", "ž", "že", "svoj",
                          "jesti", "imeti", "\u0161e", "iti", "kak", "www", "km", "eur", "pač", "del", "kljub", "šele",
                          "prek", "preko", "znova", "morda", "kateri", "katero", "katera", "ampak", "lahek", "lahka",
                          "lahko", "morati", "torej", "ali", "ampak", "bodisi", "in", "kajti", "marveč", "namreč", "ne",
                          "niti", "oziroma", "pa", "saj", "sicer", "temveč", "ter", "toda", "torej", "vendar",
                          "vendarle", "zakaj", "če", "čeprav", "čeravno", "četudi", "čim", "da", "kadar", "kakor",
                          "ker", "ki", "ko", "kot", "naj", "najsi", "odkar", "preden", "dve", "dvema", "dveh", "šest",
                          "šestdeset", "šestindvajset", "šestintrideset", "šestnajst", "šeststo", "štiri", "štirideset",
                          "štiriindvajset", "štirinajst", "štiristo", "deset", "devet", "devetdeset", "devetintrideset",
                          "devetnajst", "devetsto", "dvainšestdeset", "dvaindvajset", "dvajset", "dvanajst", "dvesto",
                          "enaindvajset", "enaintrideset", "enajst", "nič", "osem", "osemdeset", "oseminštirideset",
                          "osemindevetdeset", "osemnajst", "pet", "petdeset", "petinštirideset", "petindevetdeset",
                          "petindvajset", "petinosemdeset", "petinpetdeset", "petinsedemdeset", "petintrideset",
                          "petnajst", "petsto", "sedem", "sedemdeset", "sedeminšestdeset", "sedemindvajset",
                          "sedeminpetdeset", "sedemnajst", "sedemsto", "sto", "tisoč", "tri", "trideset",
                          "triinšestdeset", "triindvajset", "triinpetdeset", "trinajst", "tristo", "šestdesetim",
                          "šestim", "šestindvajsetim", "šestintridesetim", "šestnajstim", "šeststotim", "štiridesetim",
                          "štiriindvajsetim", "štirim", "štirinajstim", "štiristotim", "desetim", "devetdesetim",
                          "devetim", "devetintridesetim", "devetnajstim", "devetstotim", "dvainšestdesetim",
                          "dvaindvajsetim", "dvajsetim", "dvanajstim", "dvestotim", "enaindvajsetim", "enaintridesetim",
                          "enajstim", "osemdesetim", "oseminštiridesetim", "osemindevetdesetim", "osemnajstim", "osmim",
                          "petdesetim", "petim", "petinštiridesetim", "petindevetdesetim", "petindvajsetim",
                          "petinosemdesetim", "petinpetdesetim", "petinsedemdesetim", "petintridesetim", "petnajstim",
                          "petstotim", "sedemdesetim", "sedeminšestdesetim", "sedemindvajsetim", "sedeminpetdesetim",
                          "sedemnajstim", "sedemstotim", "sedmim", "stotim", "tisočim", "trem", "tridesetim",
                          "triinšestdesetim", "triindvajsetim", "triinpetdesetim", "trinajstim", "tristotim",
                          "šestdesetih", "šestih", "šestindvajsetih", "šestintridesetih", "šestnajstih", "šeststotih",
                          "štiridesetih", "štirih", "štiriindvajsetih", "štirinajstih", "štiristotih", "desetih",
                          "devetdesetih", "devetih", "devetintridesetih", "devetnajstih", "devetstotih",
                          "dvainšestdesetih", "dvaindvajsetih", "dvajsetih", "dvanajstih", "dvestotih",
                          "enaindvajsetih", "enaintridesetih", "enajstih", "osemdesetih", "oseminštiridesetih",
                          "osemindevetdesetih", "osemnajstih", "osmih", "petdesetih", "petih", "petinštiridesetih",
                          "petindevetdesetih", "petindvajsetih", "petinosemdesetih", "petinpetdesetih",
                          "petinsedemdesetih", "petintridesetih", "petnajstih", "petstotih", "sedemdesetih",
                          "sedeminšestdesetih", "sedemindvajsetih", "sedeminpetdesetih", "sedemnajstih", "sedemstotih",
                          "sedmih", "stotih", "tisočih", "treh", "tridesetih", "triinšestdesetih", "triindvajsetih",
                          "triinpetdesetih", "trinajstih", "tristotih", "šestdesetimi", "šestimi", "šestindvajsetimi",
                          "šestintridesetimi", "šestnajstimi", "šeststotimi", "štiridesetimi", "štiriindvajsetimi",
                          "štirimi", "štirinajstimi", "štiristotimi", "desetimi", "devetdesetimi", "devetimi",
                          "devetintridesetimi", "devetnajstimi", "devetstotimi", "dvainšestdesetimi", "dvaindvajsetimi",
                          "dvajsetimi", "dvanajstimi", "dvestotimi", "enaindvajsetimi", "enaintridesetimi", "enajstimi",
                          "osemdesetimi", "oseminštiridesetimi", "osemindevetdesetimi", "osemnajstimi", "osmimi",
                          "petdesetimi", "petimi", "petinštiridesetimi", "petindevetdesetimi", "petindvajsetimi",
                          "petinosemdesetimi", "petinpetdesetimi", "petinsedemdesetimi", "petintridesetimi",
                          "petnajstimi", "petstotimi", "sedemdesetimi", "sedeminšestdesetimi", "sedemindvajsetimi",
                          "sedeminpetdesetimi", "sedemnajstimi", "sedemstotimi", "sedmimi", "stotimi", "tisočimi",
                          "tremi", "tridesetimi", "triinšestdesetimi", "triindvajsetimi", "triinpetdesetimi",
                          "trinajstimi", "tristotimi", "eno", "eni", "ene", "ena", "dva", "štirje", "trije", "en",
                          "enega", "enemu", "enim", "enem", "eden", "dvojni", "trojni", "dvojnima", "trojnima",
                          "dvojnih", "trojnih", "dvojne", "trojne", "dvojnim", "trojnim", "dvojnimi", "trojnimi",
                          "dvojno", "trojno", "dvojna", "trojna", "dvojnega", "trojnega", "dvojen", "trojen",
                          "dvojnemu", "trojnemu", "dvojnem", "trojnem", "četrti", "šestdeseti", "šesti", "šestnajsti",
                          "štirideseti", "štiriindvajseti", "štirinajsti", "deseti", "devetdeseti", "deveti",
                          "devetnajsti", "drugi", "dvaindevetdeseti", "dvajseti", "dvanajsti", "dvestoti",
                          "enaindvajseti", "enajsti", "osemdeseti", "osemnajsti", "osmi", "petdeseti", "peti",
                          "petinštirideseti", "petindvajseti", "petinosemdeseti", "petintrideseti", "petnajsti", "prvi",
                          "sedemdeseti", "sedemindvajseti", "sedemnajsti", "sedmi", "stoti", "tisoči", "tretji",
                          "trideseti", "triindvajseti", "triintrideseti", "trinajsti", "tristoti", "četrtima",
                          "šestdesetima", "šestima", "šestnajstima", "štiridesetima", "štiriindvajsetima",
                          "štirinajstima", "desetima", "devetdesetima", "devetima", "devetnajstima", "drugima",
                          "dvaindevetdesetima", "dvajsetima", "dvanajstima", "dvestotima", "enaindvajsetima",
                          "enajstima", "osemdesetima", "osemnajstima", "osmima", "petdesetima", "petima",
                          "petinštiridesetima", "petindvajsetima", "petinosemdesetima", "petintridesetima",
                          "petnajstima", "prvima", "sedemdesetima", "sedemindvajsetima", "sedemnajstima", "sedmima",
                          "stotima", "tisočima", "tretjima", "tridesetima", "triindvajsetima", "triintridesetima",
                          "trinajstima", "tristotima", "četrtih", "drugih", "dvaindevetdesetih", "prvih", "tretjih",
                          "triintridesetih", "četrte", "šestdesete", "šeste", "šestnajste", "štiridesete",
                          "štiriindvajsete", "štirinajste", "desete", "devetdesete", "devete", "devetnajste", "druge",
                          "dvaindevetdesete", "dvajsete", "dvanajste", "dvestote", "enaindvajsete", "enajste",
                          "osemdesete", "osemnajste", "osme", "petdesete", "pete", "petinštiridesete", "petindvajsete",
                          "petinosemdesete", "petintridesete", "petnajste", "prve", "sedemdesete", "sedemindvajsete",
                          "sedemnajste", "sedme", "stote", "tisoče", "tretje", "tridesete", "triindvajsete",
                          "triintridesete", "trinajste", "tristote", "četrtim", "drugim", "dvaindevetdesetim", "prvim",
                          "tretjim", "triintridesetim", "četrtimi", "drugimi", "dvaindevetdesetimi", "prvimi",
                          "tretjimi", "triintridesetimi", "četrto", "šestdeseto", "šestnajsto", "šesto", "štirideseto",
                          "štiriindvajseto", "štirinajsto", "deseto", "devetdeseto", "devetnajsto", "deveto", "drugo",
                          "dvaindevetdeseto", "dvajseto", "dvanajsto", "dvestoto", "enaindvajseto", "enajsto",
                          "osemdeseto", "osemnajsto", "osmo", "petdeseto", "petinštirideseto", "petindvajseto",
                          "petinosemdeseto", "petintrideseto", "petnajsto", "peto", "prvo", "sedemdeseto",
                          "sedemindvajseto", "sedemnajsto", "sedmo", "stoto", "tisočo", "tretjo", "trideseto",
                          "triindvajseto", "triintrideseto", "trinajsto", "tristoto", "četrta", "šesta", "šestdeseta",
                          "šestnajsta", "štirideseta", "štiriindvajseta", "štirinajsta", "deseta", "deveta",
                          "devetdeseta", "devetnajsta", "druga", "dvaindevetdeseta", "dvajseta", "dvanajsta",
                          "dvestota", "enaindvajseta", "enajsta", "osemdeseta", "osemnajsta", "osma", "peta",
                          "petdeseta", "petinštirideseta", "petindvajseta", "petinosemdeseta", "petintrideseta",
                          "petnajsta", "prva", "sedemdeseta", "sedemindvajseta", "sedemnajsta", "sedma", "stota",
                          "tisoča", "tretja", "trideseta", "triindvajseta", "triintrideseta", "trinajsta", "tristota",
                          "četrtega", "šestdesetega", "šestega", "šestnajstega", "štiridesetega", "štiriindvajsetega",
                          "štirinajstega", "desetega", "devetdesetega", "devetega", "devetnajstega", "drugega",
                          "dvaindevetdesetega", "dvajsetega", "dvanajstega", "dvestotega", "enaindvajsetega",
                          "enajstega", "osemdesetega", "osemnajstega", "osmega", "petdesetega", "petega",
                          "petinštiridesetega", "petindvajsetega", "petinosemdesetega", "petintridesetega",
                          "petnajstega", "prvega", "sedemdesetega", "sedemindvajsetega", "sedemnajstega", "sedmega",
                          "stotega", "tisočega", "tretjega", "tridesetega", "triindvajsetega", "triintridesetega",
                          "trinajstega", "tristotega", "četrtemu", "šestdesetemu", "šestemu", "šestnajstemu",
                          "štiridesetemu", "štiriindvajsetemu", "štirinajstemu", "desetemu", "devetdesetemu",
                          "devetemu", "devetnajstemu", "drugemu", "dvaindevetdesetemu", "dvajsetemu", "dvanajstemu",
                          "dvestotemu", "enaindvajsetemu", "enajstemu", "osemdesetemu", "osemnajstemu", "osmemu",
                          "petdesetemu", "petemu", "petinštiridesetemu", "petindvajsetemu", "petinosemdesetemu",
                          "petintridesetemu", "petnajstemu", "prvemu", "sedemdesetemu", "sedemindvajsetemu",
                          "sedemnajstemu", "sedmemu", "stotemu", "tisočemu", "tretjemu", "tridesetemu",
                          "triindvajsetemu", "triintridesetemu", "trinajstemu", "tristotemu", "četrtem", "šestdesetem",
                          "šestem", "šestnajstem", "štiridesetem", "štiriindvajsetem", "štirinajstem", "desetem",
                          "devetdesetem", "devetem", "devetnajstem", "drugem", "dvaindevetdesetem", "dvajsetem",
                          "dvanajstem", "dvestotem", "enaindvajsetem", "enajstem", "osemdesetem", "osemnajstem",
                          "osmem", "petdesetem", "petem", "petinštiridesetem", "petindvajsetem", "petinosemdesetem",
                          "petintridesetem", "petnajstem", "prvem", "sedemdesetem", "sedemindvajsetem", "sedemnajstem",
                          "sedmem", "stotem", "tisočem", "tretjem", "tridesetem", "triindvajsetem", "triintridesetem",
                          "trinajstem", "tristotem", "deseteri", "dvakratni", "dvoji", "enkratni", "peteri", "stoteri",
                          "tisočeri", "trikratni", "troji", "deseterima", "dvakratnima", "dvojima", "enkratnima",
                          "peterima", "stoterima", "tisočerima", "trikratnima", "trojima", "deseterih", "dvakratnih",
                          "dvojih", "enkratnih", "peterih", "stoterih", "tisočerih", "trikratnih", "trojih", "desetere",
                          "dvakratne", "dvoje", "enkratne", "petere", "stotere", "tisočere", "trikratne", "troje",
                          "deseterim", "dvakratnim", "dvojim", "enkratnim", "peterim", "stoterim", "tisočerim",
                          "trikratnim", "trojim", "deseterimi", "dvakratnimi", "dvojimi", "enkratnimi", "peterimi",
                          "stoterimi", "tisočerimi", "trikratnimi", "trojimi", "desetero", "dvakratno", "dvojo",
                          "enkratno", "petero", "stotero", "tisočero", "trikratno", "trojo", "desetera", "dvakratna",
                          "dvoja", "enkratna", "petera", "stotera", "tisočera", "trikratna", "troja", "deseterega",
                          "dvakratnega", "dvojega", "enkratnega", "peterega", "stoterega", "tisočerega", "trikratnega",
                          "trojega", "deseter", "dvakraten", "dvoj", "enkraten", "peter", "stoter", "tisočer",
                          "trikraten", "troj", "deseteremu", "dvakratnemu", "dvojemu", "enkratnemu", "peteremu",
                          "stoteremu", "tisočeremu", "trikratnemu", "trojemu", "deseterem", "dvakratnem", "dvojem",
                          "enkratnem", "peterem", "stoterem", "tisočerem", "trikratnem", "trojem", "le-onega",
                          "le-tega", "le-tistega", "le-toliko", "onega", "tega", "tistega", "toliko", "le-oni",
                          "le-takšni", "le-taki", "le-te", "le-ti", "le-tisti", "oni", "takšni", "taki", "te", "ti",
                          "tisti", "le-onima", "le-takšnima", "le-takima", "le-tema", "le-tistima", "onima", "takšnima",
                          "takima", "tema", "tistima", "le-onih", "le-takšnih", "le-takih", "le-teh", "le-tistih",
                          "onih", "takšnih", "takih", "teh", "tistih", "le-one", "le-takšne", "le-take", "le-tiste",
                          "one", "takšne", "take", "tiste", "le-onim", "le-takšnim", "le-takim", "le-tem", "le-tistim",
                          "onim", "takšnim", "takim", "tem", "tistim", "le-onimi", "le-takšnimi", "le-takimi",
                          "le-temi", "le-tistimi", "onimi", "takšnimi", "takimi", "temi", "tistimi", "le-ono",
                          "le-takšno", "le-tako", "le-tisto", "le-to", "ono", "takšno", "tako", "tisto", "to", "le-tej",
                          "tej", "le-ona", "le-ta", "le-takšna", "le-taka", "le-tista", "ona", "ta", "takšna", "taka",
                          "tista", "le-tak", "le-takšen", "tak", "takšen", "le-takšnega", "le-takega", "takšnega",
                          "takega", "le-onemu", "le-takšnemu", "le-takemu", "le-temu", "le-tistemu", "onemu",
                          "takšnemu", "takemu", "temu", "temuintemu", "tistemu", "le-onem", "le-takšnem", "le-takem",
                          "le-tistem", "onem", "takšnem", "takem", "tistem", "vsakogar", "vsakomur", "vsakomer",
                          "vsakdo", "obe", "vsaki", "vsakršni", "vsi", "obema", "vsakima", "vsakršnima", "vsema",
                          "obeh", "vsakih", "vsakršnih", "vseh", "vsake", "vsakršne", "vse", "vsakim", "vsakršnim",
                          "vsem", "vsakimi", "vsakršnimi", "vsemi", "vsako", "vsakršno", "vso", "vsej", "vsa", "vsaka",
                          "vsakršna", "oba", "ves", "vsak", "vsakršen", "vsakega", "vsakršnega", "vsega", "vsakemu",
                          "vsakršnemu", "vsemu", "vsakem", "vsakršnem", "enako", "istega", "koliko", "mnogo", "nekoga",
                          "nekoliko", "precej", "kaj", "koga", "marsikaj", "marsikoga", "nekaj", "čemu", "komu",
                          "marsičemu", "marsikomu", "nečemu", "nekomu", "česa", "marsičesa", "nečesa", "kom",
                          "marsičim", "marsikom", "nečim", "nekom", "čem", "marsičem", "nečem", "kdo", "marsikdo",
                          "nekdo", "čigavi", "drugačni", "enaki", "isti", "kakšni", "kaki", "kakršnikoli", "kateri",
                          "katerikoli", "kolikšni", "koliki", "marsikateri", "nekakšni", "nekaki", "nekateri", "neki",
                          "takile", "tele", "tile", "tolikšni", "toliki", "čigavima", "drugačnima", "enakima", "enima",
                          "istima", "kakšnima", "kakima", "kakršnimakoli", "katerima", "katerimakoli", "kolikšnima",
                          "kolikima", "marsikaterima", "nekakšnima", "nekakima", "nekaterima", "nekima", "takimale",
                          "temale", "tolikšnima", "tolikima", "čigavih", "drugačnih", "enakih", "enih", "istih",
                          "kakšnih", "kakih", "kakršnihkoli", "katerih", "katerihkoli", "kolikšnih", "kolikih",
                          "marsikaterih", "nekakšnih", "nekakih", "nekaterih", "nekih", "takihle", "tehle", "tolikšnih",
                          "tolikih", "čigave", "drugačne", "enake", "iste", "kakšne", "kake", "kakršnekoli", "katere",
                          "katerekoli", "kolikšne", "kolike", "marsikatere", "nekakšne", "nekake", "nekatere", "neke",
                          "takele", "tolikšne", "tolike", "čigavim", "drugačnim", "enakim", "istim", "kakšnim", "kakim",
                          "kakršnimkoli", "katerim", "katerimkoli", "kolikšnim", "kolikim", "marsikaterim", "nekakšnim",
                          "nekakim", "nekaterim", "nekim", "takimle", "temle", "tolikšnim", "tolikim", "čigavimi",
                          "drugačnimi", "enakimi", "enimi", "istimi", "kakšnimi", "kakimi", "kakršnimikoli", "katerimi",
                          "katerimikoli", "kolikšnimi", "kolikimi", "marsikaterimi", "nekakšnimi", "nekakimi",
                          "nekaterimi", "nekimi", "takimile", "temile", "tolikšnimi", "tolikimi", "čigavo", "drugačno",
                          "isto", "kakšno", "kako", "kakršnokoli", "katero", "katerokoli", "kolikšno", "marsikatero",
                          "nekakšno", "nekako", "nekatero", "neko", "takole", "tole", "tolikšno", "tejle", "čigava",
                          "drugačna", "enaka", "ista", "kakšna", "kaka", "kakršnakoli", "katera", "katerakoli",
                          "kolikšna", "kolika", "marsikatera", "neka", "nekakšna", "nekaka", "nekatera", "takale",
                          "tale", "tolikšna", "tolika", "čigav", "drug", "drugačen", "enak", "kak", "kakšen",
                          "kakršenkoli", "kakršnegakoli", "kateregakoli", "kolik", "kolikšen", "nek", "nekak",
                          "nekakšen", "takegale", "takle", "tegale", "tolik", "tolikšen", "čigavega", "drugačnega",
                          "enakega", "kakšnega", "kakega", "katerega", "kolikšnega", "kolikega", "marsikaterega",
                          "nekakšnega", "nekakega", "nekaterega", "nekega", "tolikšnega", "tolikega", "čigavemu",
                          "drugačnemu", "enakemu", "istemu", "kakšnemu", "kakemu", "kakršnemukoli", "kateremu",
                          "kateremukoli", "kolikšnemu", "kolikemu", "marsikateremu", "nekakšnemu", "nekakemu",
                          "nekateremu", "nekemu", "takemule", "temule", "tolikšnemu", "tolikemu", "čigavem",
                          "drugačnem", "enakem", "istem", "kakšnem", "kakem", "kakršnemkoli", "katerem", "kateremkoli",
                          "kolikšnem", "kolikem", "marsikaterem", "nekakšnem", "nekakem", "nekaterem", "nekem",
                          "takemle", "tolikšnem", "tolikem", "naju", "nama", "midva", "nas", "nam", "nami", "mi",
                          "mene", "me", "meni", "mano", "menoj", "jaz", "vaju", "vama", "vidva", "vas", "vam", "vami",
                          "vi", "tebe", "tebi", "tabo", "teboj", "njiju", "jih", "ju", "njima", "jima", "onedve",
                          "onidve", "nje", "njih", "njim", "jim", "njimi", "njo", "jo", "njej", "nji", "ji", "je",
                          "onadva", "njega", "ga", "njemu", "mu", "njem", "on", "čigar", "kolikor", "kar", "karkoli",
                          "kogar", "kogarkoli", "čemur", "čemurkoli", "komur", "komurkoli", "česar", "česarkoli",
                          "čimer", "čimerkoli", "komer", "komerkoli", "čemer", "čemerkoli", "kdor", "kdorkoli",
                          "kakršni", "kakršnima", "kakršnih", "kakršne", "kakršnim", "kakršnimi", "kakršno", "kakršna",
                          "kakršen", "kakršnega", "kakršnemu", "kakršnem", "najini", "naši", "moji", "najinima",
                          "našima", "mojima", "najinih", "naših", "mojih", "najine", "naše", "moje", "najinim", "našim",
                          "mojim", "najinimi", "našimi", "mojimi", "najino", "našo", "mojo", "najina", "naša", "moja",
                          "najin", "najinega", "naš", "našega", "moj", "mojega", "najinemu", "našemu", "mojemu",
                          "najinem", "našem", "mojem", "vajini", "vaši", "tvoji", "vajinima", "vašima", "tvojima",
                          "vajinih", "vaših", "tvojih", "vajine", "vaše", "tvoje", "vajinim", "vašim", "tvojim",
                          "vajinimi", "vašimi", "tvojimi", "vajino", "vašo", "tvojo", "vajina", "vaša", "tvoja",
                          "vajin", "vajinega", "vaš", "vašega", "tvoj", "tvojega", "vajinemu", "vašemu", "tvojemu",
                          "vajinem", "vašem", "tvojem", "njuni", "njihovi", "njeni", "njegovi", "njunima", "njihovima",
                          "njenima", "njegovima", "njunih", "njihovih", "njenih", "njegovih", "njune", "njihove",
                          "njene", "njegove", "njunim", "njihovim", "njenim", "njegovim", "njunimi", "njihovimi",
                          "njenimi", "njegovimi", "njuno", "njihovo", "njeno", "njegovo", "njuna", "njihova", "njena",
                          "njegova", "njun", "njunega", "njihov", "njihovega", "njen", "njenega", "njegov", "njegovega",
                          "njunemu", "njihovemu", "njenemu", "njegovemu", "njunem", "njihovem", "njenem", "njegovem",
                          "se", "si", "sebe", "sebi", "sabo", "seboj", "svoji", "svojima", "svojih", "svoje", "svojim",
                          "svojimi", "svojo", "svoja", "svoj", "svojega", "svojemu", "svojem", "nikogar", "noben",
                          "ničemur", "nikomur", "ničesar", "ničimer", "nikomer", "ničemer", "nihče", "nikakršni",
                          "nobeni", "nikakršnima", "nobenima", "nikakršnih", "nobenih", "nikakršne", "nobene",
                          "nikakršnim", "nobenim", "nikakršnimi", "nobenimi", "nikakršno", "nobeno", "nikakršna",
                          "nobena", "nikakršen", "nikakršnega", "nobenega", "nikakršnemu", "nobenemu", "nikakršnem",
                          "nobenem", "še", "šele", "žal", "že", "baje", "bojda", "bržčas", "bržkone", "celo",
                          "dobesedno", "domala", "edinole", "gotovo", "itak", "ja", "kajne", "kajpada", "kajpak",
                          "koli", "komaj", "le", "malone", "mar", "menda", "morda", "morebiti", "nadvse", "najbrž",
                          "nemara", "nerad", "neradi", "nikar", "pač", "pogodu", "prav", "pravzaprav", "predvsem",
                          "preprosto", "rad", "rada", "rade", "radi", "ravno", "res", "resda", "samo", "seveda",
                          "skoraj", "skorajda", "spet", "sploh", "tudi", "všeč", "verjetno", "vnovič", "vred", "vsaj",
                          "zadosti", "zapored", "zares", "zgolj", "zlasti", "zopet", "čezenj", "čeznje", "mednje",
                          "mednju", "medse", "nadenj", "nadme", "nadnje", "name", "nanj", "nanje", "nanjo", "nanju",
                          "nase", "nate", "obenj", "podnjo", "pome", "ponj", "ponje", "ponjo", "pote", "predenj",
                          "predme", "prednje", "predse", "skozenj", "skoznje", "skoznjo", "skozte", "vame", "vanj",
                          "vanje", "vanjo", "vanju", "vase", "vate", "zame", "zanj", "zanje", "zanjo", "zanju", "zase",
                          "zate", "čez", "med", "na", "nad", "ob", "po", "pod", "pred", "raz", "skoz", "skozi", "v",
                          "za", "zoper", "h", "k", "kljub", "nasproti", "navkljub", "navzlic", "proti", "ž", "blizu",
                          "brez", "dno", "do", "iz", "izmed", "iznad", "izpod", "izpred", "izven", "izza", "krog",
                          "mimo", "namesto", "naokoli", "naproti", "od", "okoli", "okrog", "onkraj", "onstran", "poleg",
                          "povrh", "povrhu", "prek", "preko", "razen", "s", "spod", "spričo", "sredi", "vštric",
                          "vpričo", "vrh", "vrhu", "vzdolž", "z", "zaradi", "zavoljo", "zraven", "zunaj", "o", "pri",
                          "bi", "bova", "bomo", "bom", "bosta", "boste", "boš", "bodo", "bojo", "bo", "sva", "nisva",
                          "smo", "nismo", "sem", "nisem", "sta", "nista", "ste", "niste", "nisi", "so", "niso", "ni",
                          "bodiva", "bodimo", "bodita", "bodite", "bodi", "biti", "bili", "bila", "bile", "bil", "bilo",
                          "želiva", "dovoliva", "hočeva", "marava", "morava", "moreva", "smeva", "zmoreva", "nočeva",
                          "želimo", "dovolimo", "hočemo", "maramo", "moramo", "moremo", "smemo", "zmoremo", "nočemo",
                          "želim", "dovolim", "hočem", "maram", "moram", "morem", "smem", "zmorem", "nočem", "želita",
                          "dovolita", "hočeta", "marata", "morata", "moreta", "smeta", "zmoreta", "nočeta", "želite",
                          "dovolite", "hočete", "marate", "morate", "morete", "smete", "zmorete", "nočete", "želiš",
                          "dovoliš", "hočeš", "maraš", "moraš", "moreš", "smeš", "zmoreš", "nočeš", "želijo",
                          "dovolijo", "hočejo", "marajo", "morajo", "morejo", "smejo", "zmorejo", "nočejo", "želi",
                          "dovoli", "hoče", "mara", "mora", "more", "sme", "zmore", "noče", "hotiva", "marajva",
                          "hotimo", "marajmo", "hotita", "marajta", "hotite", "marajte", "hoti", "maraj", "želeti",
                          "dovoliti", "hoteti", "marati", "moči", "morati", "smeti", "zmoči", "želeni", "dovoljeni",
                          "želena", "dovoljena", "želene", "dovoljene", "želen", "dovoljen", "želeno", "dovoljeno",
                          "želeli", "dovolili", "hoteli", "marali", "mogli", "morali", "smeli", "zmogli", "želela",
                          "dovolila", "hotela", "marala", "mogla", "morala", "smela", "zmogla", "želele", "dovolile",
                          "hotele", "marale", "mogle", "morale", "smele", "zmogle", "želel", "dovolil", "hotel",
                          "maral", "mogel", "moral", "smel", "zmogel", "želelo", "dovolilo", "hotelo", "maralo",
                          "moglo", "moralo", "smelo", "zmogl"}

    return stop_words_slovene


# returns a list of all filepaths
def get_filepaths():
    base_dir = "./PA3-data"
    filepath_list = []

    for root, dirs, files in os.walk(base_dir):
        filepath_list.extend(os.path.join(root, x).replace("\\", "/") for x in files if x.endswith(".html"))

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

    conn = create_connection('../inverted-index.db')

    sql = 'CREATE TABLE IF NOT EXISTS IndexWord (  word TEXT PRIMARY KEY );'
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

    # postings
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
