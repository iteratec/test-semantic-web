#!/home/dlade/anaconda3/bin/python

import re
import bz2
import xml.etree.cElementTree as ET

ART_FILTER = set(('Substantiv','Adjektiv','Verb','Adverb','Abkürzung'))
ART_MATCHER = re.compile('Wortart\|(\w+)\|Deutsch.+')

def get_art(text):
  match_art = ART_MATCHER.search(text)
  if not match_art:
      return None
  return match_art.group(1)
    
with bz2.open('/home/dlade/Downloads/dewiktionary-latest-pages-articles.xml.bz2', "rb") as f:
    for event, element in ET.iterparse(f, ('start','end')):
      if event == 'start' and element.tag.endswith('}text'):
        text = str(element.text).strip()
        art = get_art(text)
        if art in ART_FILTER:
            print(text)
            print('-' * 100)
            print()
'''
  84179 Substantiv
  11441 Adjektiv
  10136 Verb
   5036 Komparativ - Form von Adjektiv
   4967 Superlativ - Form von Adjektiv
   4319 Abkürzung
   2193 Redewendung
   1134 Adverb
   1133 Wortverbindung
    242 Interjektion
    160 Präposition
    152 Suffix
    152 Sprichwort
    139 Präfix
    121 Numerale
     93 Ortsnamengrundwort
     61 Indefinitpronomen
     51 Lokaladverb
     49 Konjunktion
     47 Subjunktion
     42 Kontraktion
     38 Eigenname
     36 Personalpronomen
     35 Demonstrativpronomen
     34 Straßenname
     30 Partikel
     27 Präfixoid
     19 Pronominaladverb
     16 Toponym
     16 Grußformel
     15 Artikel
     14 Pronomen
     11 Gradpartikel
     10 Zahlzeichen
     10 Antwortpartikel
'''