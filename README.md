### Book Scraper - Books to Scrape (https://books.toscrape.com/index.html)

# Description

Ce programme est un scraper web qui extrait les informations des livres à partir du site Books to Scrape. Pour chaque catégorie de livres, il permet d'extraire des données detaillées plus bas dans le texte.

# Fonctionnalités
- Le programme scrape toutes les catégories de livres du site Books to Scrape
- Il récupère des informations détaillées de chaque livre
- Il enregistre les résultats des extractions sous forme de fichiers CSV, un fichier par catégorie
- Il enregistre les couvertures de livrespar catégorie en format jpeg dans un sous dossier couverture_livre
- Il affiche à l'écran en temps réel les catégories et les URL des livres en cours d'extraction

# Prérequis
- Vous devez installer l'application Python sur votre machine (Ce programme est developpé sous windows 11 avec la version Python 3.12)
  
## Avant d'exécuter ce programme, installez les bibliothèques Python suivantes : à l'aide pip install

- requests : pour envoyer des requêtes HTTP au site.
- BeautifulSoup (à travers bs4) : pour parser le HTML et extraire les données.
- csv : permet de créer modifier lire fichiers csv
- os : permet de créer, manipuler des repertoires
- Path pathlib: permet de créer des chemins d'accès, identifier des fichiers
- urljoin : utile pour construire des liens entre url de base et un chemin partiel
- re : permet de remplacer les caracteres non valides 

### Créez l'environnement virtuel env grace à la commande : python -m venv env
### Comment l'activer :
- la commande sera "source env/bin/activate" si vous êtes sous Linux ou Apple

- la commande sera env\Scripts\activate.bat si vous êtes sous Windows

- la commande sera  env\Scripts\activate si vous utilisez PowerShell

## Comment executer le programme
- Exécutez le script "python explorer_scraping.py"
- Vérifiez les résultats : 

### Après l'exécution, si le programme fonctionne un dossier nommé Data_categorie sera créé dans le répertoire du projet. 
- Ce dossier contiendra un fichier CSV pour chaque catégorie de livres.
- Chaque fichier CSV inclura les informations détaillées pour les livres de la catégorie correspondante.
- Ce dossier contiendra également un sous dossier couverture_livre. La couverture de chaque livre de la catégorie y     est enregistrée en format JPEG.

## Chaque fichier CSV au nom de la catégorie du livre aura le format suivant  :
- Product_page_url : l'URL du livre
- Universal_product_code : Code unique identifiant le produit
- Titre du livre
- Price_including_tax
- Price_excluding_price
- Number_available : nombre de livres en stock
- Category
- Review_rating :Note attribuée pour chaque livre
- Image_url
- Product description




