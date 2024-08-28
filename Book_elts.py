import requests
import csv
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html'
response = requests.get(url)
if response.ok:
    print(response)
#links[]
soup = BeautifulSoup(response.content, 'lxml')
#review rating
rev_rating = soup.find("p", attrs={'class': 'star-rating'}).get("class")[1]
print(rev_rating)
#extraire l'UPC du livre de la catégorie
table = soup.find('table', class_='table table-striped')
if table: 
    upc= []
    upc_row = table.find('th', string='UPC')
# Extraire le texte de la cellule linked
    upc = upc_row.find_next_sibling('td').text
    print(upc)
    #extraire le titre du livre
title = soup.find('h1').text
print(str(title))
#récuperer l'url ou figure le livre selectionné
url_category='https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
print(url_category)
#recuperer le prix hors taxe puis TTC
price_ht = soup.find('th',string="Price (excl. tax)").find_next_sibling("td").string
price_ttc = soup.find('th',string="Price (incl. tax)").find_next_sibling("td").string
print(price_ht)
print(price_ttc)
#extraire Number available
product_avaib = soup.find('th',string="Availability").find_next_sibling("td").string
print(product_avaib)
#extraire la catégorie
breadcrumb =soup.find('ul', class_="breadcrumb")

print(breadcrumb)
category = breadcrumb.find_all('a')
categorie=category[-1].text.strip()
print(len('category'))
print(categorie)



"""
# find Book title
titre= soup.find('h1').text
print(titre)
#Find Review_rating

#review_rating= soup.find('p',class_='star-rating')['class'][1]
review_element = soup.select_one('p.star-rating.Three')
if review_element.ok :
    print("how many stars :")
    print(review_element.get_text(strip=True))
else:
    print("Nothing found")
print(review_element)
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
             