Book Scraper - Books to Scrape
Description
Ce programme est un scraper web qui extrait les informations des livres à partir du site Books to Scrape. Pour chaque catégorie de livres, il collecte les détails suivants :

Titre
URL du livre
URL de la couverture
Description du produit
UPC (Identifiant unique du produit)
Prix incluant la taxe
Les informations de chaque catégorie sont ensuite enregistrées dans des fichiers CSV séparés, placés dans un dossier csv_categories.

Fonctionnalités

Scrape toutes les catégories de livres du site Books to Scrape.
Récupère des informations détaillées pour chaque livre.
Enregistre les résultats sous forme de fichiers CSV, un fichier par catégorie.
Affiche en temps réel les catégories et les URL des livres en cours d'extraction.
Prérequis

Avant d'exécuter ce programme, vous devez installer les bibliothèques Python suivantes :

requests : pour envoyer des requêtes HTTP au site.
BeautifulSoup (à travers bs4) : pour parser le HTML et extraire les données.
csv
re
os
pathlib  Path
urljoin
time 
Bibliothèques installées en utilisant pip :
pip install requests
pip install beautifulsoup4
cd book-scraper
Exécutez le script Python : Assurez-vous que vous avez Python installé, puis exécutez le script :

explorer_scrapping.py
Vérifiez les résultats : Après l'exécution, un dossier csv_categories sera créé dans le répertoire du projet. Ce dossier contiendra un fichier CSV pour chaque catégorie de livres. Chaque fichier CSV inclura les informations détaillées pour les livres de la catégorie correspondante.
Structure du Projet
Exemple de Sortie CSV

Chaque fichier CSV aura le format suivant :

Titre URL du livre  URL de la couverture Description du produit UPC Prix incluant la taxe
Améliorations Futures

Ajouter la possibilité de scraper uniquement une ou plusieurs catégories spécifiques.
Optimiser la gestion des erreurs et des interruptions réseau.
Enrichir les données avec des informations supplémentaires (ex. : disponibilité des stocks, évaluations des livres).
Licence


