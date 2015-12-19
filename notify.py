import time
import pynotify
import requests
from bs4 import BeautifulSoup as b
######### club variables
la_liga= "http://www.livescore.com/soccer/spain/primera-division/"
bpl = "http://www.livescore.com/soccer/england/premier-league/"
bundesliga="http://www.livescore.com/soccer/germany/bundesliga/"
########notification refresh interval in seconds####
seconds = 60
########change the url below to whatever league you want to follow###
url = "http://www.livescore.com/soccer/bolivia/primera-division-apertura/"
######change the icon as well
icon  = "/home/varun/live-football-update/images/"+ "bundesliga" +".png"

soup=b(requests.get(url).content,"lxml")

current_match = soup.findAll("div",{"class":"row-gray even"})[0]

pynotify.init ("icon-summary-body")
count =0
######################################################################################
def getdetails(content, count):

	while count != len(url):	
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
						a.append("home_team")
					else:
						a.append("away_team")
		count+=1
	return a,count
################################################################################################
if current_match.find("img"):

	match_time = current_match.findAll("div")[0].text

	while match_time!="HT" or match_time!="FT":

		home_team = current_match.findAll("div")[1].text

		score = current_match.findAll("div")[2]
		
		away_team = current_match.findAll("div")[3].text

		notification = pynotify.Notification(	home_team + ' vs ' + away_team, score.text + " in "+ match_time , icon	)
		notification.show()

		################################################################################
		details ="http://www.livescore.com/"+ score.find('a').get('href')

		details_soup = b(requests.get(details).content,"lxml")

		body = details_soup.findAll("div",{"data-id":"details"})
		a,count=getdetails(body,count)

		if a[len(a)-1]=="home_team":
			notification = pynotify.Notification(home_team,a[0] + " "+a[2]+" "+a[1],icon)
		else:
			notification = pynotify.Notification(away_team,a[0] + " "+a[2]+" "+a[1],icon)
		notification.show()
		#############################################################################


		time.sleep(seconds)

else:
	notification = pynotify.Notification(	 "No live match going on",'', icon	)
	notification.show()