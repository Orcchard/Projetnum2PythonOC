Book Scraper - Books to Scrape

Description

Ce programme est un scraper web qui extrait les informations des livres à partir du site Books to Scrape. Pour chaque catégorie de livres, il permet d'extraire des données detaillées plus bas.

Fonctionnalités
Scrape toutes les catégories de livres du site Books to Scrape.
Récupère des informations détaillées pour chaque livre.
Enregistre les résultats sous forme de fichiers CSV, un fichier par catégorie.
Affiche en temps réel les catégories et les URL des livres en cours d'extraction.

Prérequis
- Vous devez installer l'application Python sur votre machine (Version du projet 3.12)
  
- Avant d'exécuter ce programme, vous devez installer les bibliothèques Python suivantes :
  Bibliothèques installées en utilisant pip install
  
  requests : pour envoyer des requêtes HTTP au site.
  
  BeautifulSoup (à travers bs4) : pour parser le HTML et extraire les données.
  
  csv : Permet de créer modifier lire fichiers csv
  
  os : Permet decréer, manipuler des repertoires
  
  pathlib  Path
  
  urljoin
  

  
- Création de l'environnement virtuel env à la commande :  python -m venv env
  
- Comment l'activer :
   la commande sera "source env/bin/activate" si vous etes sous Linux ou Apple
  
   la commande sera env\Scripts\activate.bat si vous êtes sous Windows
  
   la commande sera  env\Scripts\activate si vous utilisez PowerShell

  
Exécutez le script Python "explorer_scraping.py"
Vérifiez les résultats : 
Après l'exécution, si le programme fonctionne un dossier categorie sera créé dans le répertoire du projet. 
Ce dossier contiendra un fichier CSV pour chaque catégorie de livres. Chaque fichier CSV inclura les informations détaillées pour les livres de la catégorie correspondante.
Ce dossier contiendra également un sous dossier couverture_livre.Les couvertures des livres y sont enregistrées en format JPEG par nom de catégorie.

Chaque fichier CSV aura le format suivant  :
Product_page_url : l'URL du livre

Universal_product_code : Code unique identifiant le produit

Titre du livre

Price_including_tax

Price_excluding_price

Number_available : nombre de livres en stock

Category

Review_rating :Note attribuée pour chaque livre

Image_url

Product description




