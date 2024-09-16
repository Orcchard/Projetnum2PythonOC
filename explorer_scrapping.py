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
    review_rating = f"{p[-1]['class'][-1]} stars"
    picture = soup.find("img")
    picture_url = picture["src"]
    print(picture_url)
    image_url = "https://books.toscrape.com/" + picture_url.replace("../../", "")

    print(f"url : {url}")
    print(f"UPC : {upc}")
    print(f"Titre : {title}")
    print(f"price_including_tax : {price_including_tax}")
    print(f"price_excluding_tax : {price_excluding_tax}")
    #print(f"Prod avail : {prod_avail}")
    print(f"number available : {number_available}")
    print(f"product description : {product_description}")
    print(f"category: {category}")
    print(f"review rating : {review_rating}")
    print(f"image url : {image_url}")
    
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
        "image_url" : image_url, 
    }
#ecrire les data dans un fichier csv
with open('product_information.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file ,fieldnames=data_produit.keys())
        writer.writeheader()
        writer.writerow(data_produit)
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#recuperer toutes les urls de la catégorie sequential art sur 4 pages et ses elements
#je créé une variable
sequential_links =[]
#la category sequential art a 4 pages

for i in range(5):
    c = (f"page-{str(i)}.html" )
    print(c)

    #je recupere les infos des pages
    url ="https://books.toscrape.com/catalogue/category/books/sequential-art_5/"+ c
    response = requests.get(url)
    if response.ok:
        print(f"response est de type: {type(response)}")
        print(response) 
        print(url)
        soup =  BeautifulSoup(response.content, 'lxml')
        print(f"soup est de type: {type(soup)}")
#on search les elements h3 à inside la page 
        tds = soup.find_all('h3') 
        print(f"h3 est de type: {type('h3')}")
#pour each element td on va search le a
        for h3 in tds :
            a = h3.find('a')
            link = a['href']
#on reconstitute le lien à link created en amont
            sequential_links.append('https://books.toscrape.com/' + link.replace("../../.." , "catalogue"))
            
            time.sleep(2)

            with open('results_url.txt', 'w') as file:
                for uerl in sequential_links:
                    file.write(uerl+'\n')
                    print(f"Titre de livre:{uerl}")