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

    def parse(self, text:str):
        self._parser:Wikicode = mwparserfromhell.parse(text, skip_style_tags=True)

    @property
    def data(self):
        return self.__data

class SubstantivParser(Parser):
    def __init__(self, word):
        super().__init__(word, 'substantiv')

    def parse(self, text:str):
        super().parse(text)

        def parse_gender(template):
            param = template.get('Genus')
            self.data['gender'] = param.value.strip()
            
        def parse_variations(template):
            variations = set()
            for param in template.params:
                if str(param.name) in set((
                        'Nominativ Singular', 'Nominativ Plural', 
                        'Genitiv Singular'  , 'Genitiv Plural',
                        'Dativ Singular'    ,'Dativ Plural',
                        'Akkusativ Singular','Akkusativ Plural')):
                    variations.add(param.value.strip())
                    
            variations.remove(self.data['word'])                
            self.data['variations'] = variations
        
        def collect_links_at(template):
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
                
            return links

        def parse_synonyme(template):
            self.data['synonyme'] = collect_links_at(template)
        
        def parse_oberbegriffe(template):
            self.data['oberbegriffe'] = collect_links_at(template)
            
        def parse_abkuerzungen(template):
            self.data['abkuerzungen'] = collect_links_at(template)
        
        for template in self._parser.ifilter_templates():
            name = str(template.name).strip()
            print(name)
            if (name == 'Deutsch Substantiv Übersicht'):
                parse_gender(template)
                parse_variations(template)
            elif (name == 'Synonyme'):
                parse_synonyme(template)
            elif (name == 'Oberbegriffe'):
                parse_oberbegriffe(template)
            elif (name == 'Abkürzungen'):
                parse_abkuerzungen(template)
                
                
               
# KIND_FILTER = set(('substantiv','adjektiv','verb','adverb','abkürzung'))
def get_parser(kind, word):
    if kind == 'substantiv':
        return SubstantivParser(word)
    
    print('Unknown word kind: {}'.format(kind))
    return None
    

with bz2.open('/home/dlade/Downloads/litschi.xml.bz2', "rb") as f:
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
                text += child.tail
                
            parser.parse(text)
            
            print('{}'.format(parser.data))
            break

#    print()
#    print(text)
