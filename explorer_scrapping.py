import requests
import csv
from bs4 import BeautifulSoup
import re
import os 
from pathlib import Path
import time
# URL de la première page de la catégorie "Sequential Art"
start_time = time.perf_counter()
depart_url = "https://books.toscrape.com/"
catalog_url = "http://books.toscrape.com/catalogue/"
# Variable pour stocker les URLs récupérées
links_categ = []
response = requests.get(depart_url)
if response.ok:   
# Parser le contenu HTML de la page
    soup =  BeautifulSoup(response.content, 'lxml')
#print(f"soup est de type: {type(soup)}")
#on search les elements  à inside la page 
    list_categ = soup.find('div', {'class': 'side_categories'}).find_all('li')
    for little_a in list_categ:
        a = little_a.find('a')
        linka = a['href']
#on reconstitute le lien à link created en amont
        links_categ.append(depart_url + linka)
    time.sleep(2)          
    with open('results_url.txt', 'w') as file:
        for uerl in links_categ:
            file.write(uerl+'\n')
"""
        rev_rating = soup.find("p", class_= "star-rating").get("class")[-1]
        table = soup.find('table', class_='table table-striped')
        upc= []
        upc_row = table.find('th', string='UPC')
# Extraire le texte de la cellule linked
        upc = upc_row.find_next_sibling('td').text
    for row in file:
        url = row.strip()
        print(url + ' , ' + rev_rating + ' , '+ upc_row)
# response = requests.url
        #if response.ok:         
        #rev_rating = soup.find("p", class_= "star-rating").get("class")[-1] 
        if rev_rating == "One":  # on adapte le chiffre obtenu avec une note sur cinq en string.
            rev_rating = "1 / 5"
        elif rev_rating == "Two":
            rev_rating = "2 / 5"
        elif rev_rating == "Three":
            rev_rating = "3 / 5"
        elif rev_rating == "Four":
            rev_rating = "4 / 5"    
        elif rev_rating == "Five":
                rev_rating = "5 / 5"
        else:
            rev_rating = "0 / 5"
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
#url_category= url
#print(url_category)
#recuperer le prix hors taxe puis TTC
#price_ht = soup.find('th', string = "Price (excl. tax)").find('td').string
#price_ttc = soup.find('th',string="Price (incl. tax)").find_next_sibling("td").string
#print(price_ht)
#print(price_ttc)
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
data_produit = {"product_page_url" : row,
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