import requests
import csv
from bs4 import BeautifulSoup
import time
#import string
links =[]
#la category sequential art a 4 pages
for i in range(5):
    c = (f"page-{str(i)}.html" )
    print(c)
    url ="https://books.toscrape.com/catalogue/category/books/sequential-art_5/"+ c
    response = requests.get(url)
    if response.ok:
        print(f"response est de type: {type(response)}")
    print(response) 
    print(url)
    soup =  BeautifulSoup(response.content, 'lxml')
    print(f"soup est de type: {type(soup)}")
#on search les elements h3 à inside la page 
tds = soup.findAll('h3') 
print(f"h3 est de type: {type('h3')}")
#pour each element td on va search le a
for h3 in tds :
    a = h3.find('a')
    link = a['href']
#on reconstitute le lien à link created en amont
    links.append('https://books.toscrape.com/' + link.replace("../../.." , "catalogue"))
time.sleep(2)

for url in links:
    print(url)
    #print(f"url est de type: {type(url)}")          
    with open('results_url.txt', 'w') as file:
        file.write(url+'\n')
        