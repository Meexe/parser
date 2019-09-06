from math import ceil
from json import dumps
from requests import get
from bs4 import BeautifulSoup
import re


URL = 'https://yandex.com/search/xml'
TAGS = ['h1', 'h2', 'h3', 'p', 'article']


def parser(request, count):
        
        result = {
                'count': 0,
                'sites': []
        }
        
        for page in range(ceil(count/10)):
                params = {
                        'query': request,
                        'page': page,
                        'user': 'uid-dw6thucr',
                        'key': '03.565368559:46c785521335d531668b6879416b9d08',
                        'l10n': 'en'
                }
                xml = get(URL, params=params)
                soup = BeautifulSoup(xml.text, 'xml')

                for link in soup.find_all('doc'):
                        url = link.url.string
                        html = get(url)

                        if html.status_code != 200:
                                result['sites'].append({
                                        'status': 'Error' + str(html.status_code),
                                        'url': url,
                                        'text': None
                                })
                                result['count'] += 1
                                continue

                        subsoup = BeautifulSoup(html.text, 'html.parser')

                        if subsoup.find(id=re.compile("captcha")):
                                result['sites'].append({
                                        'status': 'CAPTCHA',
                                        'url': url,
                                        'text': None
                                })
                                result['count'] += 1
                                continue

                        tags = subsoup.find_all(TAGS)
                        text = '\n'.join(tag.text for tag in tags)


                        result['sites'].append({
                                'status': 'Available',
                                'url': url,
                                'text': text
                        })
                        result['count'] += 1
        return dumps(result)


if __name__ == "__main__":
        # request = 'yandex search api'
        # count = 5
        
        request = input('Request: ')
        count = int(input('Number of sites: '))

        result = parser(request, count)
        print(result)
    