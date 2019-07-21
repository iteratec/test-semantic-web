#!/home/dlade/anaconda3/bin/python

import bz2
import xml.etree.cElementTree as ET

import mwparserfromhell
from mwparserfromhell.wikicode import Wikicode
from mwparserfromhell.nodes import Template, Wikilink

class Parser:
    def __init__(self, word:str, kind:str):
        self.__data = {'word' : word, 'kind' : kind}
        self._parser:Wikicode = None
        
    def collect_links_at(self, template):
        links = set()
        idx = self._parser.index(template)
        while True:
            idx += 1
            node = self._parser.get(idx)
            if isinstance(node, Template):
                break
            elif not isinstance(node, Wikilink):
                continue
            links.add(str(node.title))
            
        return list(links)

    def parse(self, text:str):
        self._parser:Wikicode = mwparserfromhell.parse(text, skip_style_tags=True)
        
        for template in self._parser.ifilter_templates():
            name = str(template.name).strip()
            if (name == 'Synonyme'):
                self.data['synonyme'] = self.collect_links_at(template)
            elif (name == 'Oberbegriffe'):
                self.data['oberbegriffe'] = self.collect_links_at(template)
            elif (name == 'Gegenwörter'):
                self.data['gegenwoerter'] = self.collect_links_at(template)
            elif (name == 'Abkürzungen'):
                self.data['abkuerzungen'] = self.collect_links_at(template)

    @property
    def data(self):
        return self.__data


class SubstantivParser(Parser):
    def __init__(self, word):
        super().__init__(word, 'substantiv')

    def parse(self, text:str):
        super().parse(text)

        def parse_gender(template):
            return template.get('Genus').value.strip()
            
        def parse_variations(template):
            variations = set()
            for param in template.params:
                if str(param.name) in set((
                        'Nominativ Singular', 'Nominativ Plural', 
                        'Genitiv Singular'  , 'Genitiv Plural',
                        'Dativ Singular'    ,'Dativ Plural',
                        'Akkusativ Singular','Akkusativ Plural')):
                    variations.add(param.value.strip())
                    
            variations.discard(self.data['word'])                
            return list(variations)
        
        for template in self._parser.ifilter_templates():
            name = str(template.name).strip()
            if (name == 'Deutsch Substantiv Übersicht'):
                self.data['gender'] = parse_gender(template)
                self.data['variations'] = parse_variations(template)
                
                
class VerbParser(Parser):
    def __init__(self, word):
        super().__init__(word, 'verb')

    def parse(self, text:str):
        super().parse(text)

        def parse_variations(template):
            variations = set()
            for param in template.params:
                if str(param.name) in set((
                        'Präsens_ich'       , 'Präsens_du'     , 'Präsens_er, sie, es', 
                        'Präteritum_ich'    , 'Präteritum_ich*',
                        'Partizip II'       , 'Partizip II*',
                        'Konjunktiv II_ich' , 'Konjunktiv II_ich*',
                        'Imperativ Singular', 'Imperativ Plural')):
                    variations.add(param.value.strip())
                    
            variations.discard(self.data['word'])                
            return list(variations)
        
        for template in self._parser.ifilter_templates():
            name = str(template.name).strip()
            if (name == 'Deutsch Verb Übersicht'):
                self.data['variations'] = parse_variations(template)
               

class AdjektivParser(Parser):
    def __init__(self, word):
        super().__init__(word, 'adjektiv')

    def parse(self, text:str):
        super().parse(text)

        def parse_variations(template):
            variations = set()
            for param in template.params:
                if str(param.name) in set((
                        'Positiv', 'Komparativ', 'Superlativ'
                    )):
                    variations.add(param.value.strip())
                    
            variations.discard(self.data['word'])                
            return list(variations)
        
        for template in self._parser.ifilter_templates():
            name = str(template.name).strip()
            if (name == 'Deutsch Adjektiv Übersicht'):
                self.data['variations'] = parse_variations(template)
                

def get_parser(kind, word):
    if kind == 'substantiv':
        return SubstantivParser(word)
    elif kind == 'verb':
        return VerbParser(word)
    elif kind == 'adjektiv':
        return AdjektivParser(word)
    elif kind == 'adverb':
        return Parser(word, 'adverb')
    elif kind == 'abkürzung':
        return Parser(word, 'abkürzung')
    
    print('Unknown word kind: {}'.format(kind))
    return None
    
import json

with bz2.open('/home/dlade/Downloads/TBA.xml.bz2', "rb") as f:
    for event, element in ET.iterparse(f, ('start','end')):
        if event == 'start':
            kind = str(element.tag)
            word = element.attrib['word']

            # get parser and ignore unknown type            
            parser = get_parser(kind, word)
            if not parser:
                continue
            
            # get all text, ignoring children but add were tails
            text = str(element.text)
            for child in element:
                text += str(child.tail)
                
            parser.parse(text)
            
            print(json.dumps(parser.data))
            break
