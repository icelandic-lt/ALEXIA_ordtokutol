from xml.etree import ElementTree as ET
from string import punctuation

def get_text_output(input):
    output = []
    with open('islensk_nutimamalsordabok.xml', 'r', encoding='utf-8') as content:
        tree = ET.parse(content)
        for element in tree.iter():
            for child in element:
                if child.tag == '{http://localhost/xmlschema}Lemma':
                    for element in child:
                        if element.attrib.get('val') not in output:
                            if ' ' in element.attrib.get('val'):
                                pass
                            elif '-' in element.attrib.get('val'):
                                pass
                            else:
                                output.append(element.attrib.get('val'))

    if input == 'eng':
        with open('dci_wordlist.txt', 'w', encoding='utf8') as out:
            out.write('lemma\n')
            for i in output:
                out.write(i+'\n')
    elif input == 'is':
        with open('nmo_ordalisti.txt', 'w', encoding='utf8') as out:
            out.write('lemma\n')
            for i in output:
                out.write(i+'\n')

if __name__ == '__main__':
    pass