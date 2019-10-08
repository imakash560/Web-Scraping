import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

response = requests.get('https://insider.in/all-events-in-noida')
soup = BeautifulSoup(response.text,'html.parser')
events = soup.findAll('li', attrs={'class':'card-list-item'})

name1 = []
location1 = []
date1 = []
url1 = []
name2 = []
location2 = []
date2 = []
url2 = []
t=1

for event in events:
    if t<=10:
        title = event.find('div', attrs={'class':'event-card-name'})
        locations = event.find('span', attrs={'class':'event-card-venue'})
        dates = event.find('span', attrs={'class':'event-card-date'})
        urls = event.find('a')['href']
        url = 'https://insider.in'+urls
        df = pd.DataFrame({'Name':[title.text],'Location':[locations.text],'Date':[dates.text],'URL':[url]})
        print(df)
        t=t+1
        ch = int(input("If you wish to scrap this event enter '1' and if not enter then enter '2' :"))
        if ch == 1:
             name1.append(title.text)
             location1.append(locations.text)
             date1.append(dates.text)
             url1.append(url)
        elif ch == 2:
             name2.append(title.text)
             location2.append(locations.text)
             date2.append(dates.text)
             url2.append(url)

df1 = pd.DataFrame({'Name':name1,'Location':location1,'Date':date1,'URL':url1})
df2 = pd.DataFrame({'Name':name2,'Location':location2,'Date':date2,'URL':url2})

engine = create_engine("mysql+pymysql://root:Ayush@900@localhost:3306/scrap")
df1.to_sql(name ='interesting_url', con=engine, index = False , if_exists="append")
df2.to_sql(name ='non_interesting_url', con=engine, index = False , if_exists="append")

print('interesting_url table:')
print(engine.execute("SELECT * FROM interesting_url").fetchall())
print('non_interesting_url table:')
print(engine.execute("SELECT * FROM non_interesting_url").fetchall())
