import requests
import csv
from bs4 import BeautifulSoup
import re
import os 
from pathlib import Path
import time
# URL du site  de vente en ligne books.toscrap 
start_time = time.perf_counter()
depart_url = "https://books.toscrape.com/"
catalog_url = "http://books.toscrape.com/catalogue/"
# Variable  pour stocker les URLs récupérées sous forme de liste
links_categ = []
response = requests.get(depart_url)
if response.ok:   
# Parser le contenu HTML de la result
    soup =  BeautifulSoup(response.content, 'lxml')
#print(f"soup est de type: {type(soup)}") test comprehension
# chargement ds variable ldu resultat de find
    list_categ = soup.find('div', {'class': 'side_categories'}).find_all('li')
    for little_a in list_categ:
        a = little_a.find('a')
        linka = a['href']
#on reconstitute la liste des urls de toutes les categories
        links_categ.append(depart_url + linka)    
#Note: le [1:] permet de commencer les categories du site par la première visible dans la liste (Travel)
for by_category in links_categ[1:]:
    result = requests.get(by_category)
    all_categories = by_category
    #time.sleep(2) 
    links = []
#Permet de retrouver plus finement chaque catégorie
    if result.ok:
        soup = BeautifulSoup(result.content, 'lxml')
        which_category = soup.find('li', class_="active").text
        #print(f"The category is : {which_category}")
    #On recherche si le nombre de pages ets superieur à une page
    #if result.ok:
        #soup = BeautifulSoup(result.text, 'html.parser')
        # Recherche de la page suivante
        next_page = soup.find_all('ul', class_="pager")
        #print(next_page)
    #more than one result  
        if len(next_page)>=1:
            for page_num in next_page:
                page_num_suiv = page_num.find('li' , class_="current").text
                #print(len(page_num_suiv))
                #print(page_num_suiv)
                #Permet d'extraire le nombre de pages de la catégorie à partir du 10 eme caratère de la liste
                choice = page_num_suiv.strip()[10:]
                #print(choice)
                choice_suiv = int(choice)+1
                #print(f"choice_suiv : {choice_suiv} alors que choice : {choice}")
                #print(f"This category has {choice_suiv-1} pages in total.")
                #Boucle sur le nombre de pages entre 1 et dernière page + 1 et extraction de toutes les url des pages de chaque categorie
                for i in range(1, choice_suiv):
                    url_page = all_categories.replace('index.html', '') + f"page-{str(i)}.html"
                    page_after = requests.get(url_page)
                    #print(f"page_after : {page_after}")
                    #print(f"url_page  : {url_page}")
                    
                    if page_after.ok:
                        #print("result: " + str(i))
                        soup = BeautifulSoup(page_after.content, 'lxml')
                        book_title = soup.find_all('article', class_="product_pod")
                        for titlelink in book_title:
                            a = titlelink.find('a')
                            book_link = a['href']
                            
                            links.append(catalog_url + book_link[9:]+ '\n' )
                            print(links)








"""

        rev_rating = soup.find("p", class_= "star-rating").get("class")[-1]
        table = soup.find('table', class_="table table-striped")
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