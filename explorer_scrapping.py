import requests
#import csv
from bs4 import BeautifulSoup
import string
url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

response = requests.get(url)
#links[]
soup = BeautifulSoup(response.content, 'lxml')

tds= soup.findAll('td')
print(len(tds)) 
[print(str(td) + '\n\n') for td in tds]

"""
ths= soup.findAll('th')
print(len(ths)) 
[print(str(th) + '\n\n') for th in ths]

trs= soup.findAll('tr')
print(len(trs)) 
[print(str(tr) + '\n\n') for tr in trs]

   """
with open('exploration.txt', 'w') as file:
    file.write(str(tds)+ '\n')
               # file.write(str(ths))
                
                #file.write(str(trs)+ '\n')
             