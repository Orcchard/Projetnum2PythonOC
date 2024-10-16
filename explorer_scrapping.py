import requests
import csv
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from word2number import w2n
import re


main_url = "https://books.toscrape.com/"
catalog_url = "http://books.toscrape.com/catalogue/"
categ_links = []

# nettoyage caractères spéciaux
def clean_text(text):
    if isinstance(text, str):
        return text.replace('Â', '').replace('â', '').replace('©', '')
    return text
# Gestion de la reponse via requests
answer = requests.get(main_url)
if answer.ok:
    soup = BeautifulSoup(answer.text, "html.parser")
    # On ignore le premier lien "Books" pour y parvenir j'extrais à partir de la premiere catégorie: Travel
    categ_list = soup.find("div", {"class": "side_categories"}).find_all("a")[1:]
    for category in categ_list:
        categs = category["href"].strip()
        # Je joins url relative et absolue pour obtenir l'url de chaque categorie
        full_category_url = urljoin(main_url, categs)
        categ_links.append((category.text.strip(), full_category_url))
#Création du dossier Data-categorie 
if not os.path.exists('Data-categorie'):
    os.makedirs('Data-categorie')
#Impression à l'écran du nom de la catégorie
for categ_name, link_to_category in categ_links:
    page = requests.get(link_to_category)

    if page.ok:
        soup = BeautifulSoup(page.text, 'html.parser')

        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print(f" La catégories est : {categ_name}")
        
        category_books_link = []
        url = link_to_category

        # Créer un dossier par catégorie
        category_folder = os.path.join('Data-categorie', categ_name)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder) 

        # Créer un sous-dossier pour les images
        cover_folder = os.path.join(category_folder, 'couverture-livre')
        if not os.path.exists(cover_folder):
            os.makedirs(cover_folder)
           
        # Scraper le nombre de livres de la catégorie
        number_books = soup.select_one("form", {"class": "form-horizontal"}).find("strong")
        if number_books:
            number_of_books = int(number_books.text.strip())
            print(f"Le nombre de livre(s) est {number_of_books}")
            # Creation d'une boucle while
            b_next = True
            while b_next: 
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code != 200:
                        break
                except requests.exceptions.RequestException as e:
                    print(f"Erreur lors de la récupération de {url}: {e}")
                    break
            
                # reconstitution de l'url  des livres de chaque page
                soup = BeautifulSoup(response.text, "html.parser")
                book_title = soup.find_all("article", class_="product_pod")

                for book in book_title:
                    bouquin = book.h3.a["href"]
                    full_book_url = urljoin(catalog_url, bouquin.replace("../../../", ""))

                #Affichage à l'écran de la catégorie de l'URL du livre
                    page_book = requests.get(full_book_url)
                    if page_book.ok:
                        page_book_soup = BeautifulSoup(page_book.text, 'html.parser')
                        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
                        print(f"URL du livre :{full_book_url}")

                        # Definition des élements
                        product_page_url = full_book_url
                        product_table = page_book_soup.find("table", class_="table table-striped")
                        upc = product_table.find("th", string="UPC").find_next_sibling("td").text 
                        title = page_book_soup.find("h1").text
                        price_including_tax = page_book_soup.find('th', string='Price (incl. tax)').find_next_sibling("td").text 
                        price_excluding_tax = page_book_soup.find('th', string='Price (excl. tax)').find_next_sibling("td").text
                        prod_avail = page_book_soup.find('th', string="Availability").find_next_sibling("td").text 
                        number_available = prod_avail.replace("In stock (", "").replace(" available)", "")
                        category = categ_name
                        product_description = page_book_soup.find('meta', {'name':'description'})['content'].strip()
                        rating_element = page_book_soup.find("p", class_="star-rating")
                        if rating_element:
                            # Extraire la classe qui indique le nombre d'étoiles
                            rating_class = rating_element["class"][1]
                        rating_tuple = [("One", 1), ("Two", 2), ("Three", 3), ("Four", 4), ("Five", 5)]
                        rating ="N/A"
                        for lettre, val_num in rating_tuple:
                            if rating_class == lettre:
                                rating = val_num
                                break
                        print(f"Le nom du livre extrait: {title}")
                        #Récuperation de l'URL de la couverture DU LIVRE
                        image_cover =book.find("img")
                        image_url = urljoin(main_url, image_cover["src"])
                        # titre du livre pour la couverture du livre
                        image_name = f"{title}.jpg"
                        image_name = re.sub(r'[^a-zA-Z0-9_\-\.]+', '', image_name)                       
                        image_path = os.path.join(cover_folder, image_name)
                        try:
                            img_data = requests.get(image_url).content
                            with open(image_path, 'wb') as handler:
                                handler.write(img_data)
                        except Exception as e:
                            print(f"Erreur lors du téléchargement de l'image {image_url}: {e}")  
                                          
                        #Ajout des informations du livre dans dictionnaire
                        data_produit = {
                            "Product_page_url": product_page_url,
                            "Universal_product_code": upc,
                            "Titre": clean_text(title),
                            "Price_including_tax": clean_text(price_including_tax),
                            "Price_excluding_price": clean_text(price_excluding_tax),
                            "Number_available": number_available,
                            "Category": category,
                            "Review_rating": rating, 
                            "Image_url": image_url,
                            "Product description": clean_text(product_description),
                        }
                        category_books_link.append(data_produit)  

                # Vérifier s'il y a une page suivante
                bouton_next = soup.find("li", class_="next")
                if bouton_next:
                    url_next = bouton_next.find("a")["href"]
                    url = urljoin(link_to_category, url_next)
                else:
                    b_next = False

    # Créer le fichier CSV pour la catégorie           
    if category_books_link:               
        csv_file = os.path.join(category_folder, f"{categ_name}.csv")
        with open(csv_file, mode='w', newline='', encoding='utf-8_sig') as file:
            fieldnames = ["Product_page_url", "Universal_product_code", "Titre", "Price_including_tax", "Price_excluding_price", "Number_available", "Category", "Review_rating", "Image_url", "Product description"]
            #ecriture des noms des colonnes            
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(category_books_link)
        print(f"Fichier CSV créé pour la catégorie : {categ_name}")               
print("Processus terminé.")
