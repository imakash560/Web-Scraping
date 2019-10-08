import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

response = requests.get('https://naadyogacouncil.com/events/list/?tribe_paged=1&tribe_event_display=past&tribe-bar-date=2019-10-05')
soup = BeautifulSoup(response.text,'html.parser')
names = soup.findAll('h3', attrs={'class':'tribe-events-list-event-title'})
details = soup.findAll('div', attrs={'class':'tribe-events-event-meta'})

name =[]
location =[]
date =[]
url = []

name1 = []
location1 = []
date1 = []
url1 = []

name2 = []
location2 = []
date2 = []
url2 =[]

t=1
k=1

for n in names:
    if t<=10:
        title = n.find('a', attrs={'class':'tribe-event-url'})
        urls = n.find('a')['href']
        name.append(title.text)
        url.append(urls)
        t=t+1
for d in details:
    if k<=10:
        locations = d.find('div', attrs={'class':'tribe-events-venue-details'})
        location.append(locations.text.replace('\n',''))
        k=k+1
        dates = d.find('div', attrs={'class':'tribe-event-schedule-details'})
        date.append(dates.text.replace('\n',''))

j=0
l=0
k=0

df = pd.DataFrame({'Name':name,'Location':location,'Date':date,'URL':url})

for i in range(0,10):
    print(df.iloc[[i]])
    ch = int(input("If you wish to scrap this event enter '1' and if not enter then enter '2' :"))
    if ch == 1:
        name1.append(name[j])
        location1.append(location[j])
        date1.append(date[j])
        url1.append(url[j])
        j+=1
    elif ch == 2:
        name2.append(name[k])
        location2.append(location[k])
        date2.append(date[k])
        url2.append(url[k])

        k+=1

df1 = pd.DataFrame({'Name':name1,'Location':location1,'Date':date1,'URL':url1})
df2 = pd.DataFrame({'Name':name2,'Location':location2,'Date':date2,'URL':url2})

engine = create_engine("mysql+pymysql://root:Ayush@900@localhost:3306/scrap")
df1.to_sql(name ='interesting_url', con=engine, index = False , if_exists = "replace")
df2.to_sql(name ='non_interesting_url', con=engine, index = False , if_exists = "replace")

print('interesting_url table:')
print(engine.execute("SELECT * FROM interesting_url").fetchall())
print('non_interesting_url table:')
print(engine.execute("SELECT * FROM non_interesting_url").fetchall())
