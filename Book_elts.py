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
title = soup.find('h1').text.strip()
print(str(title))
#récuperer l'url ou figure le livre selectionné
url_category= url
print(url_category)
#recuperer le prix hors taxe puis TTC
price_ht = soup.find('th',string="Price (excl. tax)").find_next_sibling("td").string
price_ttc = soup.find('th',string="Price (incl. tax)").find_next_sibling("td").string
print(price_ht)
print(price_ttc)
#extraire Number available
product_avaib = soup.find('th',string="Availability").find_next_sibling("td").string
print(product_avaib.replace("(" , ":"))
#extraire la catégorie
breadcrumb =soup.find('ul', class_="breadcrumb")

#print(breadcrumb)
category = breadcrumb.find_all('a')
categorie=category[-1].text.strip()
print(len('categorie'))
print(categorie)
#créer l'url de l' image du livre selectionné
picture = soup.find("img")
picture_url = picture["src"]
print(picture_url)
image_url = "https://books.toscrape.com/" + picture_url.replace("../../", "")
print(image_url)
#création d'un dictionnaire pour stocker les données du livre sélectionné
data_produit = {"product_page_url" : url_category,
                "universal_product_code" : upc,
                "title" : title,
                "price_including_tax" : price_ttc,
                "price_excluding_price" : price_ht,
                "number_available" : product_avaib,
                "category" : categorie,
                "review_rating" : rev_rating,
                "image_url" : image_url,
                }
#ecrire les data dans un fichier csv
with open('product_information.csv', 'w') as file:
        writer = csv.DictWriter(file , fieldnames=data_produit.keys())
        writer.writeheader()
        writer.writerow(data_produit)
        
    















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
             