import urllib, urllib.request
import xml.etree.ElementTree as ET
from ratelimit import limits, sleep_and_retry


_THREE_SECONDS = 3

@sleep_and_retry
@limits(calls=1, period=_THREE_SECONDS)
def get_abstract_arxiv(url: str) -> str:
   
    try: 
        data = urllib.request.urlopen(url)
    except Exception as e:
        print(e)
        return ''

    try:
        xml_str = data.read().decode('utf-8')

    except ET.ParseError as e:
        print(e)
        return ''
   
    root = ET.fromstring(xml_str)
    abstract = root.find('./{*}entry/{*}summary').text

    return abstract


if __name__ == '__main__':
    print(get_abstract_arxiv('http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'))
