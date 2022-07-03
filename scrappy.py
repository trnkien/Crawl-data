
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

baseurl = 'https://www.thewhiskyexchange.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0'
}

productlinks = []
for x in range(1,5):
    #get request
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/639/bourbon-whiskey?pg={x}')
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/637/corn-american-whiskey?pg={x}')
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/784/american-malt-whiskey?pg={x}')
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/328/rye-american-whiskey?pg={x}')
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/327/tennessee-whiskey?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/638/wheat-american-whiskey?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/640/white-dog-american-whiskey?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/35/japanese-whisky?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/34/canadian-whisky?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/493/english-whisky?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/352/vs-cognac?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/354/vsop-cognac?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/433/xo-and-napoleon-cognac?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/340/white-rum?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/518/golden-rum?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/342/dark-rum?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/692/london-dry-gin?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/854/old-tom-gin?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/862/english-gin?pg={x}')  
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/331/non-vintage-champagne?pg={x}')  
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/332/vintage-champagne?pg={x}')   
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/333/rose-champagne?pg={x}')   
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/1094/white-wine?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/465/red-wine?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/1095/orange-wine?pg={x}') 
    #r = requests.get(f'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?bottlingstatus=Discontinued&pg={x}') 
    #   r = requests.get(f'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?bottlingstatus=Discontinued&subcategory=Islay&pg={x}') 
    r = requests.get(f'https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?bottlingstatus=Discontinued&bottler=Independent%2bBottling&pg={x}') 
    
 
    soup = BeautifulSoup(r.content, 'lxml')
    #get product lis}
    productlist = soup.find_all('li', class_='product-grid__item')
    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(baseurl + link['href'])

#testlink = 'https://www.thewhiskyexchange.com/p/35027/ezra-brooks-7-year-old-bourbon'

whiskylist = []
for link in productlinks:  
    r = requests.get(link, headers=headers)
    #get src image
    soup = BeautifulSoup(r.content, 'lxml') 
    #product's id
    try:
        id = soup.find('input', id='productID')['value']
    except:
        id = ''

    #product's main
    try: 
        name = soup.find('h1', class_= 'product-main__name').text.strip()
    except:
        name = ''
    #product's prices
    try:
        price = soup.find('p', class_ = 'product-action__price').text.strip()
    except:
        price = ''
    #product's image-main
    try:
        images = soup.find('img', class_= ['product-main__image','product-slider__image'])['src']
    except:
        images = ''
    #product's description
    try:
        description = soup.find('div', class_= 'product-main__description').text.strip()
    except:
        description = ''
    #product's short description
    try: 
        short_description = soup.find('p', class_='product-main__data').text.strip()
    except:
        short_description = ''
    #product's meta data
    try:
        meta_data = soup.find('ul', class_= 'product-main__meta').text.strip()
    except:
         meta_data = ''
    whisky = {
        'id': id,
        'name': name,
        'price': price,
        'Images': images,
        'description': description,
        'Import as meta data': meta_data,
        'short description': short_description
    }
    whiskylist.append(whisky)

df = pd.DataFrame(whiskylist)
df.to_csv('Indie Bottling.csv')
