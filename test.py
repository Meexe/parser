from requests import get
from bs4 import BeautifulSoup
from re import compile


TAGS = ['h1', 'h2', 'h3', 'p']
URLS = [
    'https://www.google.com/recaptcha/api2/demo',
    'https://www.google.com/recaptcha/api2/demo?invisible=true',
    'https://recaptcha-demo.appspot.com/',
    'https://recaptcha-demo.appspot.com/'
]
result = {
                'count': 0,
                'sites': []
        }

for url in URLS:
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

    if subsoup.find(id=compile("captcha")):
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

for site in result['sites']:
    print(site['text'])
