import requests
import csv
from bs4 import BeautifulSoup
import re
import os
from pathlib import Path
from urllib.parse import urljoin
import time 

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
print ("extraire les information d'un livre de la rubrique Sequential Art")
print("Titre du livre :  Scott Pilgrim's Precious Little Life")
url = "https://books.toscrape.com/catalogue/scott-pilgrims-precious-little-life-scott-pilgrim-1_987/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
if response.ok:
    product_page_url = url
    product_information = soup.find_all("td")
    p = soup.find_all("p")
    title = soup.find("h1").text
    p_all = soup.find_all("p")
    upc = product_information[0].text
    title = soup.find("h1").text
    price_including_tax = product_information[2].text
    price_excluding_tax = product_information[3].text
    prod_avail = product_information[5].text
    number_available = prod_avail.replace(" (", " ").replace(")", "")
    product_description = (soup.find("div", {"id": "product_description"}).find_next("p").text)
    category = soup.find_all("a")[3].text
    review_rating = f"{p[2]['class'][-1]} stars"
    picture_url = soup.find("img")["src"]
    image_url = "https://books.toscrape.com/" + picture_url.replace("../../", "")
    
    print(f"///////////// LIVRE : {title}//////////////////////////// ")
    print(f"URL: {url}")
    print(f"UPC:{upc} , Catégorie: {category} ,Titre: {title}")
    print(f"Prix TTC: {price_including_tax}  , Prix HT:{price_excluding_tax} , Reste en stock : {number_available}")
    print(f" Catégorie:  {category} , Score: {review_rating}")
    print(f"Réference de l'image:{image_url}")
    print(f"product description : {product_description}")
    print(f"///////////////////////////////////////////////////////////////////////////////////////////")
    print(f" Catégorie:  {category} , Score: {review_rating}")
    

        
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# recuperer toutes les urls de la catégorie sequential art sur 4 pages et ses eléments
main_url = "https://books.toscrape.com/"
catalog_url = "http://books.toscrape.com/catalogue/"
index = requests.get(main_url)
categories_links = []
if index.ok:
    soup = BeautifulSoup(index.text, "html.parser")
    category_list = soup.find("div", {"class": "side_categories"}).find_all("li")
    for rech_list in category_list:
        a = rech_list.find("a")
        categs = a["href"]
        categories_links.append(main_url + categs)
links = []
link_to_category = categories_links[4]
page = requests.get(link_to_category)    
# Trouver la page de chaque livre dans une categorie
url = link_to_category
bNext = True
while bNext:
    response = requests.get(url)
    # Vérifier si la page existe (statut 200) si non on stop le programme
    if response.status_code != 200:
        break
    # Parser le contenu de la page
    soup = BeautifulSoup(response.text, "html.parser")
    book_title = soup.find_all("article", class_="product_pod")
    for book in book_title:
        bouquin = book.h3.a["href"]
        full_book_url = catalog_url + bouquin.replace("../../../", "")
        links.append(full_book_url)
        #Existe t'il une page suivante pour les catégories scrappées?
    bouton_next = soup.find("li", class_="next")
    if bouton_next:
        url_next = bouton_next.find("a")["href"]
        url = link_to_category.replace("index.html", "") + url_next
    else:
        bNext = False
    #Boucle pour extraire les données de chaque livre
    """
for urls in links:
    time.sleep(1)       
    print(urls)
    """
    
    

# print("*****************Je recupere les url des livres de chaque categorie******************")
main_url = "https://books.toscrape.com/"
catalog_url = "http://books.toscrape.com/catalogue/"
# Gestion de la reponse par requests
answer = requests.get(main_url)
categ_links = []
# Le dictionnaire a_books_dict stockera les liens des livres associés à chaque catégorie.
a_books_dict = {}
if not os.path.exists('csv_categories'):
    os.makedirs('csv_categories')
if answer.ok:
    # Extraction du contenu et transformation en liste grace à BeautifulSoup
    soup = BeautifulSoup(answer.text, "html.parser")
    # On ignore le premier lien "Books" pour y parvenir j'extrais à partir d'une tranche de ma liste
    categ_list = soup.find("div", {"class": "side_categories"}).find_all("a")[1:]
    for category in categ_list:
        categs = category["href"].strip()
        # Je joins url relative et absolue
        full_category_url = urljoin(main_url, categs)
        categ_links.append((category.text.strip(), full_category_url))
for categ_name, link_to_category in categ_links:
    page = requests.get(link_to_category)
    if page.ok:
        # Trouver l'url de chaque livre pour chaque categorie
        url = link_to_category
        # toutes les url retourne la page de la categorie: https://books.toscrape.com/catalogue/category/books/crime_51/index.html
        b_next = True
        category_books_l = []
        # Creation d'une boucle while
        while b_next:
            # Tentative d'intercepter une exeption
            try:
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la récupération de {url}: {e}")
                break
            # recuperation des titres de la page et de son
            soup = BeautifulSoup(response.text, "html.parser")
            book_title = soup.find_all("article", class_="product_pod")
            for book in book_title:
                bouquin = book.h3.a["href"]
                full_book_url = urljoin(catalog_url, bouquin.replace("../../../", ""))
        #Récuperation de l'URL de la couverture
                image_cover =book.find("img")
                image_url = urljoin(main_url, image_cover["src"])
        #Affichage à l'écran de la catégorie de l'URL du livre
        #Requests sur l'URL de chaque page de livre
                page_book = requests.get(full_book_url)
                if page_book.ok:
                    page_book_soup = BeautifulSoup(page_book.text, 'html.parser')
                    # Definition des elements
                    product_page_url = full_book_url
                    product_table = page_book_soup.find("table", class_="table table-striped")
                    upc = product_table.find("th", string="UPC").find_next_sibling("td").text 
                    title = page_book_soup.find("h1").text
                    price_including_tax = page_book_soup.find('th', string='Price (incl. tax)').find_next_sibling("td").text 
                    price_excluding_tax = page_book_soup.find('th', string='Price (excl. tax)').find_next_sibling("td").text
                    prod_avail = page_book_soup.find('th', string="Availability").find_next_sibling("td").text 
                    number_available = prod_avail.replace(" (", " ").replace(")", "")
                    product_description = page_book_soup.find('meta', {'name':'description'})['content'].strip()
                    category = categ_name
                    rating_element = page_book_soup.find("p", class_="star-rating")
                    if rating_element: 
                # Extraire la classe qui indique le nombre d'étoiles (par exemple "One", "Two", etc.) 
                        rating_class = rating_element["class"] 
                        rating = rating_class[1]  
                        # La deuxième classe correspond à la note 
                    else: 
                        rating = "N/A"
                #Ajout des informations du livre dans dictionnaire
                data_produit = {
                    "Product_page_url": product_page_url,
                    "Universal_product_code": upc,
                    "Titre": title,
                    "Price_including_tax": price_including_tax,
                    "Price_excluding_price": price_excluding_tax,
                    "Number_available": number_available,
                    "Product description": product_description,
                    "Category": category,
                    "Review_rating": rating,
                    "Image_url": image_url,
                }
                category_books_l.append(data_produit)
            # Vérifier s'il y a une page suivante
            bouton_next = soup.find("li", class_="next")
            if bouton_next:
                url_next = bouton_next.find("a")["href"]
                url = urljoin(link_to_category, url_next)
            else:
                b_next = False
     #liste introduite dans le dictionnaire
        if category_books_l:
            a_books_dict[categ_name] = category_books_l
    # Sauvegarder les livres dans un fichier CSV pour chaque catégorie
for categ_name, books in a_books_dict.items():       
    csv_file = f"csv_categories/{categ_name}.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["Product_page_url", "Universal_product_code", "Titre", "Price_including_tax", "Price_excluding_price", "Number_available", "Product description", "Category", "Review_rating", "Image_url"]
    #ecriture des noms des colonnes            
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(books)
    print(f"Fichier CSV créé pour la catégorie : {categ_name}")
print("Processus terminé.")
"""
for urls in full_book_url:
    time.sleep(1)
    print(f"Nom de la catégorie : {categ_name}")
    print(f"url du livre : {urls}")
"""