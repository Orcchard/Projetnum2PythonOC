import requests
import csv
from bs4 import BeautifulSoup
import re
import os
from pathlib import Path
from urllib.parse import urljoin
import time 


    #Boucle pour extraire les données de chaque livre
# print("*****************Je recupere les url des livres de chaque categorie******************")
main_url = "https://books.toscrape.com/"
catalog_url = "http://books.toscrape.com/catalogue/"
# Gestion de la reponse par requests
answer = requests.get(main_url)
categ_links = []
# Le dictionnaire a_books_dict stockera les liens des livres associés à chaque catégorie.
a_books_dict = {}

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
        print("La catégories est : " + categ_name)
        #print(f"URL du livre :{full_book_url}")
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
            # recuperation des titres de la page et de son URL
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
                    print(f"URL du livre :{full_book_url}")
                    # Definition des élements
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
