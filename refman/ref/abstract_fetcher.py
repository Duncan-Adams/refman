import urllib, urllib.request
import xml.etree.ElementTree as ET

def get_abstract_arxiv(url: str) -> str:
   
    try: 
        data = urllib.request.urlopen(url)
    except Exception as e:
        print(e)
        return ''

    try:
        xml_str = data.read().decode('utf-8')

    except xml.etree.ElementTree.ParseError as e:
        print(e)
        return ''
   
    root = ET.fromstring(xml_str)
    abstract = root.find('./{*}entry/{*}summary').text

    return abstract


if __name__ == '__main__':
    print(get_abstract_arxiv('http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'))
