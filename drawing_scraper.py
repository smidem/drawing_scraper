from bs4 import BeautifulSoup
import requests
from shutil import copyfileobj
from urllib.request import urlopen
import os

if __name__ == '__main__':
    base = 'https://www.ercoupe.info'
    url = f'{base}/uploads/Main/drawings/'
    cwd = os.getcwd()
    drawings = os.path.join(cwd, 'drawings')

    print(f'Attempting to retrieve data from {url}...')
    get = requests.get(url)
    print('Data retrieved!')

    print('Attempting to parse data...')
    soup = BeautifulSoup(get.content, features='html.parser')
    links = soup.find_all('a', href=True)
    jpg_urls = [
        (f"{base}{a['href']}", a.next) for a in links if '.jpg' in str(a)
    ]
    print(f'Success! Found links for {len(jpg_urls)} drawings.')

    if not os.path.exists(drawings):
        os.makedirs(drawings)

    print(f'Downloading {len(jpg_urls)} drawings...')
    for jpg, filename in jpg_urls:
        path = os.path.join(cwd, 'drawings', filename)
        with urlopen(jpg) as link, open(path, 'wb') as file:
            copyfileobj(link, file)

    print(f'All done! Drawings saved to {drawings}')
