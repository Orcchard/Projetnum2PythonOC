import requests
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import time
#import string
links =[]
#la category sequential art a 4 pages
for i in range(5):
    c = "page-" + str(i) + ".html" 
    url ="https://books.toscrape.com/catalogue/category/books/sequential-art_5/"+ c
    response = requests.get(url)
    if response.ok:
        print(response) 
        print(url)
        soup =  BeautifulSoup(response.text, 'lxml')
#on search les elements h3 à inside la page 
tds = soup.findAll('h3') 
#pour each element td on va search le a
for h3 in tds :
            a = h3.find('a')
            link = a['href']
#on reconstitute le lien à link created en amont
            links.append('https://books.toscrape.com/' + link.replace("../../.." , "catalogue"))
            time.sleep(2)
with open('results_url.txt', 'w') as file:
            file.write(links +'\n')