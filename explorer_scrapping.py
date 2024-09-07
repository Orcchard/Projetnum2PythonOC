import requests
from bs4 import BeautifulSoup
# URL de la première page de la catégorie "Sequential Art"
base_url = 'https://books.toscrape.com/catalogue/category/books/sequential-art_5/'
# Variable pour stocker les URLs récupérées
links = []
# Boucle sur les 4 premières pages
for page_num in range(1, 5):
    # Construire l'URL pour chaque page
    url = f"{base_url}page-{page_num}.html"
    print(url)
    response = requests.get(url)
    # Vérifier si la page existe
    if response.status_code != 200:
        print(f"Page {page_num} introuvable.")
        break
    # Parser le contenu HTML de la page#soup = BeautifulSoup(response.text, 'html.parser')
    soup =  BeautifulSoup(response.content, 'lxml')
#print(f"soup est de type: {type(soup)}")
#on search les elements h3 à inside la page 
    tds = soup.find_all('h3') 
#print(f"h3 est de type: {type('h3')}")
#pour each element td on va search le a
    for h3 in tds :
        a = h3.find('a')
        link = a['href']
#on reconstitute le lien à link created en amont
        links.append('https://books.toscrape.com/' + link.replace("../../.." , "catalogue"))
    #time.sleep(2)          
        with open('results_url.txt', 'w') as file:
            for uerl in links:
                file.write(uerl+'\n')