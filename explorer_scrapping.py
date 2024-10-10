import requests
import csv
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from word2number import w2n
import re

# print("*****************Je recupere les url des livres de chaque categorie******************")
main_url = "https://books.toscrape.com/"
catalog_url = "http://books.toscrape.com/catalogue/"
categ_links = []
# Le dictionnaire a_books_dict stockera les liens des livres associés à chaque catégorie.
#a_books_dict = {}

#Effacement des caractere spéciaux pour les champs price_including_tax & price_excluding_tax
def clean_text(text):
    if isinstance(text, str):
        return text.replace('Â', '').replace('â', '')
    return text
# Gestion de la reponse par requests
answer = requests.get(main_url)
if answer.ok:
    # Extraction du contenu et transformation en liste grace à BeautifulSoup
    soup = BeautifulSoup(answer.text, "html.parser")
    # On ignore le premier lien "Books" pour y parvenir j'extrais à partir de la premiere catégorie: Travel
    categ_list = soup.find("div", {"class": "side_categories"}).find_all("a")[1:]
    for category in categ_list:
        categs = category["href"].strip()
    # Je joins url relative et absolue pour obtenir l'url de chaque categorie
        full_category_url = urljoin(main_url, categs)
        categ_links.append((category.text.strip(), full_category_url))
    #Je crée le dossier categorie qui contiendra l'extraction du fichier .csv par nom de catégorie
if not os.path.exists('categorie'):
    os.makedirs('categorie')
#Impression à l'écran du nom de la catégorie
for categ_name, link_to_category in categ_links:
    page = requests.get(link_to_category)
    if page.ok:
        soup = BeautifulSoup(page.text, 'html.parser')
        print("**********************************************************")
        print(f" La catégories est : {categ_name}")
        print("**********************************************************")
        url = link_to_category
        b_next = True
        
        
#Création d'un chemin vers le dossier catégorie ce sous repertoire portera le nom de chaque catégorie et 
# contiendra le fichier.csv et le dossier couverture_livre 
        category_folder = os.path.join('categorie', categ_name)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder) 
    # Je nomme un autre  sous repertoire "couverture-livre" qui contiendra  les images
        cover_folder = os.path.join(category_folder, 'couverture-livre')
        if not os.path.exists(cover_folder):
            os.makedirs(cover_folder)
           
        #Scrapping du nombre de livres de la catégorie sur  la premiere url de la catégorie  (select.one)
        number_books = soup.select_one("form", {"class": "form-horizontal"}).find("strong")
        if number_books:
            number_of_books = int(number_books.text.strip())
            print(f"Le nombre de livre(s) est {number_of_books}")
            
            #création du fichier csv et son en tête pour chaque catégorie
            csv_file = os.path.join(category_folder, f"{categ_name}.csv")
            fieldnames = ["Product_page_url", "Universal_product_code", "Titre", "Price_including_tax", "Price_excluding_price", "Number_available", "Category", "Review_rating", "Image_url", "Product description"]
             
             
             #ecriture des noms des colonnes            
            #writer = csv.DictWriter(file, fieldnames=fieldnames)
            #writer.writeheader()
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
            
            # recuperation de l'url  des livres de chaque page (full_book_url)
                soup = BeautifulSoup(response.text, "html.parser")
                book_title = soup.find_all("article", class_="product_pod")
                for book in book_title:
                    bouquin = book.h3.a["href"]
                    full_book_url = urljoin(catalog_url, bouquin.replace("../../../", ""))
        
            # Ajout des informations de chaque livre
            #Affichage à l'écran de la catégorie de l'URL du livre
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
                        number_available = prod_avail.replace("In stock (", "").replace(" available)", "")
                        category = categ_name
                        rating_element = page_book_soup.find("p", class_="star-rating")
                        product_description = page_book_soup.find('meta', {'name':'description'})['content'].strip()
                        if rating_element:
                    # Extraire la classe qui indique le nombre d'étoiles (par exemple "One", "Two", etc.) et la traduire en numérique
                            rating_class = rating_element["class"] 
                            rating = w2n.word_to_num(rating_class[1])
                            
                        else: 
                            rating = "N/A"
                        #Récuperation de l'URL de la couverture DU LIVRE
                        image_cover =book.find("img")
                        image_url = urljoin(main_url, image_cover["src"])
#j'utilise la f-string pour inserer la variable titre titre du livre
                        image_name = f"{title}.jpg"
                        image_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', image_name) 
                
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
                            "Titre": title,
                            "Price_including_tax": clean_text(price_including_tax),
                            "Price_excluding_price": clean_text(price_excluding_tax),
                            "Number_available": number_available,
                            "Category": category,
                            "Review_rating": rating, 
                            "Image_url": image_url,
                            "Product description": clean_text(product_description),
                        }
                        
                        # Écriture des données dans le fichier CSV au fur et à mesure
                        file_exists = os.path.isfile(csv_file)
                        with open(csv_file, mode='a', newline='', encoding='utf-8_sig') as file:
                            writer = csv.DictWriter(file, fieldnames=fieldnames)
                            if not file_exists:
                        # Écrire les en-têtes seulement si le fichier est nouveau
                                writer.writeheader()  
                        # Écrire la ligne du livre
                            writer.writerow(data_produit)
                             
                        print(f"Fichier CSV créé pour la catégorie : {categ_name}")
                    # Vérifier s'il y a une page suivante
                    bouton_next = soup.find("li", class_="next")
                    if bouton_next:
                        url_next = bouton_next.find("a")["href"]
                        url = urljoin(link_to_category, url_next)
                    else:
                        b_next = False
    
print("Processus terminé.")
