import sys
import pynotify
import requests
from bs4 import BeautifulSoup as b
#####
la_liga= "http://www.livescore.com/soccer/spain/primera-division/"
bpl = "http://www.livescore.com/soccer/england/premier-league/"
bundesliga="http://www.livescore.com/soccer/germany/bundesliga/"

url=bundesliga


soup=b(requests.get(url).content,"lxml")

current_match = soup.findAll("div",{"class":"row-gray even"})[0]

pynotify.init ("icon-summary-body")

if current_match.find("img"):

	time = current_match.findAll("div")[0].text

	home_team = current_match.findAll("div")[1].text

	score = current_match.findAll("div")[2]

	details ="http://www.livescore.com/"+ score.find('a').get('href')

	details_soup = b(requests.get(details).content,"lxml")
	

	away_team = current_match.findAll("div")[3].text
	 
	icon  = "/home/varun/Desktop/live-football-update/football.png"

	notification = pynotify.Notification(	home_team + ' vs ' + away_team, score.text + " in "+ time , icon	)
	notification.show()





else:
	notification = pynotify.Notification(	"La Liga" , "No live match going on"	)
	notification.show()