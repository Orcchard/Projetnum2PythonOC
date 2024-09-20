import requests
import csv
from bs4 import BeautifulSoup
import re
import os 
from pathlib import Path
import time

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#extraire les information d'un livre de la rubrique Sequential Art

url ="https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')
if response.ok:
    product_page_url = url
    product_information = soup.find_all('td')
    p = soup.find_all('p')
    title = soup.find('h1').text
    p_all = soup.find_all('p')
    upc = product_information[0].text
    title = soup.find('h1').text
    price_including_tax = product_information[2].text
    price_excluding_tax = product_information[3].text
    prod_avail = product_information[5].text
    number_available = prod_avail.replace( ' (', ' ').replace(')', '')
    product_description = soup.find('div', {'id': 'product_description'}).find_next('p').text
    category = soup.find_all('a')[3].text
    review_rating = f"{p[2]['class'][-1]} stars"
    picture = soup.find("img")
    picture_url = picture["src"]
    print(picture_url)
    image_url = "https://books.toscrape.com/" + picture_url.replace("../../", "")
    print(f"///////////// LIVRE : {title}//////////////////////////// " )
    print(f"URL: {url}")
    print(f"UPC:{upc} , Catégorie: {category} ,Titre: {title}")
    print(f"Prix TTC: {price_including_tax}  , Prix HT:{price_excluding_tax} , Reste en stock : {number_available}")
    print(f" Catégorie:  {category} , Score: {review_rating}")
    print(f"Réference de l'image:{image_url}")
    print(f"product description : {product_description}")
    print(f"///////////////////////////////////////////////////////////////////////////////////////////")
    print(f" Catégorie:  {category} , Score: {review_rating}")

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#recuperer toutes les urls de la catégorie sequential art sur 4 pages et ses elements

main_url = "https://books.toscrape.com/"
catalog_url = "http://books.toscrape.com/catalogue/"


index = requests.get(main_url)
categories_links = []
links=[]
if index.ok:
    soup = BeautifulSoup(index.text, 'html.parser')
    category_list = soup.find('div', {'class': 'side_categories'}).find_all('li') 
    for rech_list in category_list:
        a = rech_list.find('a')
        categs = a['href']
        categories_links.append(main_url + categs)
    for link_to_category in categories_links[4:5]:
        page = requests.get(link_to_category)
    if page.ok:
        soup = BeautifulSoup(page.text, 'html.parser')
        categ_name = soup.find('li', class_='active').text
        print("Categorie en cours: " + categ_name)
        
# Trouver la page de chaque livre dans une categorie
url = link_to_category
bNext=True
while bNext:
    response = requests.get(url)
    # Vérifier si la page existe (statut 200)
    if response.status_code != 200:
        break
    # Parser le contenu de la page
    soup = BeautifulSoup(response.text, 'html.parser')
    book_title = soup.find_all('article', class_='product_pod')
    for book in book_title:
        bouquin = book.h3.a['href'] 
        full_book_url = catalog_url + bouquin.replace('../../../', '')
        links.append(full_book_url)
    bouton_next = soup.find('li', class_= "next")
    if bouton_next:
        url_next = bouton_next.find('a')['href']
        url = link_to_category.replace('index.html', '') + url_next
    else:
        print("pas de page suivante")
        bNext = False   
for urls in links:
    time.sleep(1)       
    print(urls)
   
#ecrire les données dans un dictionnaire
data_produit = {
    "product_page_url" : urls,
    "universal_product_code" : upc,
    "title" : title,
    "price_including_tax" : price_including_tax, 
    "price_excluding_price" : price_excluding_tax, 
    "number_available" : number_available, 
    "product description" : product_description, 
    "category" : category, 
    "review_rating" : review_rating, 
    "image_url" : image_url
    }

#écrire les data dans un fichier csv
with open('product_information.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file ,fieldnames=data_produit.keys())
    writer.writeheader()
    for uerl in links:
        writer.writerow(data_produit)
"""
with open('results_url.txt', 'w') as file:
    for uerl in links :
        file.write(uerl+'\n')


#je recupere les images  

img_cover = bouquin.find("img")['scr']
url_cover = "https://books.toscrape.com/" + cover.replace('../..','')
print(url_cover) 
""" 