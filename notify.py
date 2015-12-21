import time
import pynotify
import requests
from bs4 import BeautifulSoup as b
######### club variables ################################################################
la_liga= "http://www.livescore.com/soccer/spain/primera-division/"						#
bpl = "http://www.livescore.com/soccer/england/premier-league/"							#
bundesliga="http://www.livescore.com/soccer/germany/bundesliga/"						#
serie_a = "http://www.livescore.com/soccer/italy/serie-a/"								#
######## notification refresh interval in seconds #######################################
seconds = 60																			#
######## change the url below to whatever league you want to follow #####################
url = bundesliga																			#
################################ CHANGE THIS VARIABLE V #################################
icon  = "/home/varun/live-football-update/images/"+ "bundesliga" +".png"					#
################################ CHANGE THIS VARIABLE ^ #################################
pynotify.init ("icon-summary-body")
count =0

def getdetails(content, count):
	a=[]
	while count != len(content):	
		for i in range(count,len(content)):
			if "match details" in content[i].text:
				continue
			if "venue" in content[i].text:
				break
			else:
				try:
					event_time = content[i].findAll("div")[0].text
					a.append(event_time)
					players =  content[i].findAll("span",{"class":"name"})
				
					for x in players:
						if x.text.strip():
							a.append(x.text.strip())
						
							if content[i].findAll("span",{"class":"inc redcard"}):
								a.append("Red Card")
							if content[i].findAll("span",{"class":"inc yellowcard"}):
								a.append("Yellow Card")
							if content[i].findAll("span",{"class":"inc goal"}):
								a.append("Goal")
							if content[i].findAll("span",{"class":"inc redyellowcard"}):
								a.append("Red Yellow Card")	
							if x.text.strip()==content[i].findAll("div",{"class":"ply tright"})[0].text.strip():
								a.append("home_team")
						else:
							a.append("away_team")
				except:
					pass
		count+=1
		print count
		print len(content)
		print 56565454654546
		return a,count
################################################################################################

while 1:
	soup=b(requests.get(url).content,"lxml")

	current_match = soup.findAll("div",{"class":"row-gray even"})[0]

	if current_match.find("img"):

		match_time = current_match.findAll("div")[0].text

		home_team = current_match.findAll("div")[1].text

		score = current_match.findAll("div")[2]
		
		away_team = current_match.findAll("div")[3].text

		if match_time=="HT":
			notification = pynotify.Notification(match_time+home_team+score.text.split("-")[0]+away_team+score.text.split("-")[1],"", icon)
			notification.show()
			time.sleep(300)

		elif match_time=="FT":
			notification = pynotify.Notification(match_time+home_team+score.text.split("-")[0]+away_team+score.text.split("-")[1],"", icon)
			notification.show()
			break

		else:
			notification = pynotify.Notification(match_time+home_team+score.text.split("-")[0]+away_team+score.text.split("-")[1],"", icon)
			notification.show()

		#############################################################################################
			details ="http://www.livescore.com/"+ score.find('a').get('href')						#
			details_soup = b(requests.get(details).content,"lxml")									#
			body = details_soup.findAll("div",{"data-id":"details"})								#
			#########################################################################################
			a,count=getdetails(body,count)															#
			try:																					#
				if a[len(a)-1]=="home_team":														#
					notification = pynotify.Notification(home_team,a[0] + " "+a[2]+" "+a[1],icon)	#
				else:																				#
					notification = pynotify.Notification(away_team,a[0] + " "+a[2]+" "+a[1],icon)	#
				notification.show()																	#
			except:																					#
				pass																				#
		#############################################################################################

			time.sleep(19)

	else:
		notification = pynotify.Notification(	 "No live match going on",'', icon	)
		notification.show()
		break