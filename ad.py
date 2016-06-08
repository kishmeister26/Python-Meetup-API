import pandas as pd
import matplotlib.pyplot as plt
import urllib.request as ur
import json
from geopy.geocoders import Nominatim
geolocator = Nominatim()

places = ["san fransisco", "los angeles", "san diego"]
urls = [] #url lists
radius = 50.0
data_format = "json"
topic = "Python"
sig_id = "191677190"
sig = "07e55c2b34502597032d3cb73f333558b29789d2"

for place in places:
    location = geolocator.geocode(place)
    urls.append("https://api.meetup.com/2/groups?offset=0&format="+data_format+
    "&lon=" + str(location.longitude) + 
    "&topic="+ topic + 
    "&photo-host=public&page=500&radius=" + str(radius) +
    "&fields=&lat=" + str(location.latitude) + 
    "&order=id&desc=false&sig_id=" + sig_id + 
    "&sig=" +sig)
    
city,country,rating,name,members = [],[],[],[],[]
for url in urls:
    response = ur.urlopen(url)
    data = json.loads(response.read())
    data =data["results"]
    
for i in data :
 city.append(i['city'])
 country.append(i['country'])
 rating.append(i['rating'])
 name.append(i['name'])
 members.append(i['members']) 
 
df = pd.DataFrame([city,country,rating,name,members]).T
df.columns=['city','country','rating','name','members']
df.sort(['members','rating'], ascending=[False, False])

freq = df.groupby('country').city.count()
fig = plt.figure(figsize=(8,4))
ax1 = fig.add_subplot(121)
ax1.set_xlabel('Country')
ax1.set_ylabel('Count of Groups')
ax1.set_title("Number of Python Meetup Groups")
freq.plot(kind='bar')

freq = df.groupby('country').members.sum()/df.groupby('country').members.count()
ax1.set_xlabel('Country')
ax1.set_ylabel('Average Members in each group')
ax1.set_title("Python Meetup Groups")
freq.plot(kind='bar')

freq = df.groupby('country').rating.sum()/df.groupby('country').rating.count()
ax1.set_xlabel('Country')
ax1.set_ylabel('Average rating')
ax1.set_title("Python Meetup Groups")
freq.plot(kind='bar')

df=df.sort(['country','members'], ascending=[False,False])
df.groupby('country').head(2)
