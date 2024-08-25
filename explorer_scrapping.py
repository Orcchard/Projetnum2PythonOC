import requests
#import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
#import string
"""
for books in bookshelf:
    # collect title of all books
    book_title = books.h3.a["title"]
     # collect book price of all books
    book_price = books.findAll("p", {"class": "price_color"})
    price = book_price[0].text.strip()
 
    print("Title of the book :" + book_title)
    print("Price of the book :" + price)
 
    f.write(book_title + "," + price+"\n")
f.close()

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
    """
links =[]
#la category sequential art a 4 pages
for i in range(5):
    url ='https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'+ str(i)
response = requests.get(url)
if response.ok:
    print(response)
soup =  BeautifulSoup(response.text, 'lxml')
#on search les elements h3 à inside la page
tds = soup.findAll('h3') 
#pour each element td on va search le a
for h3 in tds :
    a = h3.find('a')
    link = a['href']
#on reconstitute le lien à link created en amont
    links.append('https://books.toscrape.com/' + link)
print(links)
with open('results_url.csv', 'w') as file:
    file.write(links +'\n')    
"""
for full_url in links:
    full_url_replaced = full_url.replace("/../../../", "/catalogue/")     
    with open('results_url.csv', 'w') as file:
        file.write(full_url +'\n')    
print(full_url)
"""