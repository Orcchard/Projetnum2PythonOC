import requests
#import csv
from bs4 import BeautifulSoup
import string
url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
response = requests.get(url)
if response.ok:
    print(response)
#links[]
soup = BeautifulSoup(response.content, 'lxml')
# find Book title
"""
titre= soup.find('h1').text
print(titre)
#Find Review_rating
#review_rating= soup.find('p',class_='star-rating')['class'][1]
"""
review_element = soup.select_one('p.star-rating.Three')
if review_element.ok :
    print("how many stars :")
    print(review_element.get_text(strip=True))
else:
    print("Nothing found")
print(review_element)

"""
ths= soup.findAll('th')
print(len(ths)) 
[print(str(th) + '\n\n') for th in ths]

trs= soup.findAll('tr')
print(len(trs)) 
[print(str(tr) + '\n\n') for tr in trs]

   """
#with open('exploration.txt', 'w') as file:
    #file.write(str(tds)+ '\n')
               # file.write(str(ths))
                
                #file.write(str(trs)+ '\n')
             