import requests
import csv
from bs4 import BeautifulSoup
import re
import os 
from pathlib import Path
import time

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#extraire les information d'un livre de la rubrique Sequential Art
links =[]
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
#je créé une variable
"""
#la category sequential art a 4 pages
for i in range(5):
    c = (f"page-{str(i)}.html" )
    print(c)
    #je recupere les infos des pages
"""
sequential_url ="https://books.toscrape.com/catalogue/category/books/sequential-art_5/"
response = requests.get(sequential_url)
sequential_link = []
if response.ok:
    print(response) 
    soup =  BeautifulSoup(response.content, 'lxml')
    #bnext = soup.find_all('li', class_="next")
    next_page = True
    while(next_page):
    #print(f"soup est de type: {type(soup)}")
    #on search les elements h3 à inside la page 
        tds = soup.find_all('h3') 
        for h3 in tds:
            a = h3.find('a')
            links = a['href']
            sequential_link.append('https://books.toscrape.com/' + links.replace("../../.." , "catalogue"))
            for sequential_row in sequential_link:
                print(sequential_row)
                print("il y a un next")
        else:
            print("vous avez attent la dernière page")
            next_page = False

#ecrire les données dans un dictionnaire
    data_produit = {
        "product_page_url" : url ,
        "universal_product_code" : upc,
        "title" : title,
        "price_including_tax" : price_including_tax, 
        "price_excluding_price" : price_excluding_tax, 
        "number_available" : number_available, 
        "product description" : product_description, 
        "category" : category, 
        "review_rating" : review_rating, 
        "image_url" : image_url, }
#écrire les data dans un fichier csv
    with open('product_information.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file ,fieldnames=data_produit.keys())
            writer.writeheader()
            for sequential_row in sequential_link:
                writer.writerow(data_produit)
"""
            with open('results_url.txt', 'w') as file:
                for uerl in sequential_links:
                    file.write(uerl+'\n')
                    print(f"Titre de livre:{uerl}")
                    #ecrire les data dans un fichier csv

"""