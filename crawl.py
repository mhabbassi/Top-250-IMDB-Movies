import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import json



headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept-Language': 'en-US,en;q=0.5'}
url='https://www.imdb.com/chart/top/?ref_=nv_mv_250'
page = requests.get(url,headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')




films = soup.select('.ipc-metadata-list-summary-item__c')

films_url=[]
for film in films:

    films_url.append('https://www.imdb.com'+film.find('a').get('href'))



    film_collect=[]
count=0

for film_url in films_url:
         count+=1
         
         try:
            s = requests.Session()
            film_page = s.get(film_url,headers=headers,timeout =20)
            film_soup=BeautifulSoup(film_page.content, 'html.parser')



            result = {}

            result['Movie_id']=film_url.split("/")[4][2:]

            result['Title']=film_soup.find('h1').get_text()

            result['Year']=film_soup.find(class_='sc-69e49b85-0').select('a')[0].get_text()

            a=film_soup.find(class_='sc-69e49b85-0').select('a')
            if len(a)==1 :
                result['Parental_Guide']=None
            else: 
                result['Parental_Guide']=a[1].get_text()
 
            b=film_soup.find(class_='sc-69e49b85-0').find_all(class_='ipc-inline-list__item')
            if len(b)==2 :
                result['Runtime']=b[1].get_text()
            else: 
                result['Runtime']=b[2].get_text()

            genres=film_soup.find(class_='sc-69e49b85-4').find_all(class_='ipc-chip__text')
            result['Genre']=[genre.get_text() for genre in genres]

            directors=film_soup.find(class_='sc-69e49b85-2').find_all(class_='ipc-metadata-list-item__content-container')[0].find_all('a')
            result['Director']=[(director.get('href').split('/')[2][2:],director.get_text()) for director in directors]
 
            writers=film_soup.find(class_='sc-69e49b85-2').find_all(class_='ipc-metadata-list-item__content-container')[1].find_all('a')
            result['Writer']=[(writer.get('href').split('/')[2][2:],writer.get_text()) for writer in writers]

            stars=film_soup.find(class_='sc-69e49b85-2').find_all(class_='ipc-metadata-list-item__content-container')[2].find_all('a')
            result['Star']=[(star.get('href').split('/')[2][2:],star.get_text()) for star in stars]

            g=film_soup.find_all(class_='sc-f65f65be-0 bBlII')
            result['Gross_US_Canada']=None
            for i in range(len(g)):
                   c=g[i].find_all('span')
                   for j in range(len(c)):
                        if c[j].get_text()=='Gross US & Canada':
                              result['Gross_US_Canada']=c[j+1].get_text()

            film_collect.append(result)
         except Exception as e:
              print(count,e)
      

with open("imdb-scraped.json", "w") as file:
    json.dump(film_collect, file)