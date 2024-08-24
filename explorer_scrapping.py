import requests
#import csv
from bs4 import BeautifulSoup
import string
url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'lxml')

tds= soup.findAll('td')
print(len(tds)) 
[print(str(td) + '\n\n') for td in tds]


ths= soup.findAll('th')
print(len(ths)) 
[print(str(th) + '\n\n') for th in ths]

trs= soup.findAll('tr')
print(len(trs)) 
[print(str(tr) + '\n\n') for tr in trs]

with open('exploration.txt', 'w') as file:
    file.write(str(tds)+ '\n')
    file.write(str(ths))
    file.write(str(trs)+ '\n')
links =[]
url ='https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'
response = requests.get(url)
if response.ok:
    print(response)
soup =  BeautifulSoup(response.text, 'lxml')
tds = soup.findAll('h3') 
for h3 in tds :
        a = h3.find('a')
        link = a['href']
        links.append('https://books.toscrape.com/' + link)
for full_url in links:  
    full_url_replaced = full_url.replace("/../../../", "/catalogue/")     
    with open('results_url.txt', 'w') as file:
        file.write(full_url_replaced +'\n')             