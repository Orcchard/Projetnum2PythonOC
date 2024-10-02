Book Scraper - Books to Scrape
Description
Ce programme est un scraper web qui extrait les informations des livres à partir du site Books to Scrape. Pour chaque catégorie de livres, il permet d'extraire les informationssuivantes pour chacun :

Titre 
URL du livre
URL de la couverturePrix incluant la taxe
Category (du livre)
Description du produit
UPC (Code unique identifiant le produit)
Prix incluant la taxe
Prix excluant la taxe
Number available (Nombre en stock
Review_rating (Note attribuée pour chaque livre

Fonctionnalités

Scrape toutes les catégories de livres du site Books to Scrape.
Récupère des informations détaillées pour chaque livre.
Enregistre les résultats sous forme de fichiers CSV, un fichier par catégorie.
Affiche en temps réel les catégories et les URL des livres en cours d'extraction.
Prérequis

Avant d'exécuter ce programme, vous devez installer les bibliothèques Python suivantes :

requests : pour envoyer des requêtes HTTP au site.
BeautifulSoup (à travers bs4) : pour parser le HTML et extraire les données.
csv : Permet de créer modifier lire fichiers csv
os : Permet decréer, manipuler des repertoires
pathlib  Path
urljoin
time 
Bibliothèques installées en utilisant pip :
pip install requests
pip install beautifulsoup4



Exécutez le script Python : Assurez-vous que vous avez Python installé, puis exécutez le script :

explorer_scrapping.py
Vérifiez les résultats : Après l'exécution, un dossier categories sera créé dans le répertoire du projet. Ce dossier contiendra un fichier CSV pour chaque catégorie de livres. Chaque fichier CSV inclura les informations détaillées pour les livres de la catégorie correspondante.
Ce dossier contiendra également un sous dossier couverture_livre Les couvertures des livres sont enregistrés en format JPEG pour sa catégorie.

Chaque fichier CSV aura le format suivant :
Titre URL du livre  URL de la couverture Description du produit UPC Prix incluant la taxe
Product_page_url
Universal_product_code
Titre
Price_including_tax
Price_excluding_price
Number_available
Category
Review_rating
Image_url
Product description




