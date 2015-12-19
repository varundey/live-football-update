import requests
from bs4 import BeautifulSoup as b
url = 'http://www.livescore.com/soccer/spain/primera-division/valencia-vs-getafe/1-2030235/'
soup = b(requests.get(url).content,"lxml")

content = soup.findAll("div",{"data-id":"details"})

count = 0

#while count!=len(content):
for i in content:
	a=[]
	if "match details" in i.text:
		continue
	if "venue" in i.text:
		break
	else:
		event_time = i.findAll("div")[0].text
		a.append(event_time)
		players =  i.findAll("span",{"class":"name"})
	for x in players:
		if x.text.strip():
			a.append(x.text.strip())
			
			if i.findAll("span",{"class":"inc redcard"}):
				a.append("Red Card")
			
			if i.findAll("span",{"class":"inc yellowcard"}):
				a.append("Yellow Card")
			if i.findAll("span",{"class":"inc goal"}):
				a.append("Goal")
			if x.text.strip()==i.findAll("div",{"class":"ply tright"})[0].text.strip():
				a.append("Home Team")
			else:
				a.append("Away Team")
	print a
	count+=1