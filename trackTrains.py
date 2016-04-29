#!/usr/local/bin/python3
'''
CTA Train Tracker

By Max Thauer
'''

import requests, time
import xml.etree.ElementTree as ET

token = '' # Your key
myStation = str(00000) # Your station number, see reference documents
line = '' # Your line (Red, Blue, Brn, G, Org, P, Pink, Y)

i = 3
timeFormat = '%Y%m%d %H:%M:%S'
url = requests.get('http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx?key='+token+'&mapid='+myStation)
url = url.text
root = ET.fromstring(url)
ctaTime = root[0].text
ctaTimeEpoch = int(time.mktime(time.strptime(ctaTime, timeFormat)))

for train in root:
	try:
		station = root[i][2].text
		stationDesc = root[i][3].text
		trainNumber = root[i][4].text
		route = root[i][5].text  
		direction = root[i][7].text
		arrT = root[i][10].text
		isApp = root[i][11].text #boolean, 0 = due, 1 = approaching
		i = i + 2
		arrTEpoch = int(time.mktime(time.strptime(arrT, timeFormat)))

		if route == line:
			if route == "G":
				route = "Green"
			if route == "Brn":
				route = "Brown"	
			if route == "P":
				route == "Purple"
			if route == "Org":
				route = "Orange"
			if isApp == "0":
				isApp = "" #Due for arrival
			else:
				isApp = "Now Approaching"	

			print ("\nCTA Time: {}\nStation: {}, {}\n{} line, train number {} heading towards {}\nEstimated Arrival: {}\n{}\n".format(ctaTime,station,stationDesc,route,trainNumber,direction,arrT,isApp))
			
			timeDue = arrTEpoch - ctaTimeEpoch
			if timeDue < 60:
				print ("Train due in {} seconds".format(timeDue))
			else:
				timeDue = timeDue/60
				timeDue = round(timeDue,2)
				print ("Train due in {} minutes".format(timeDue))	
			print ("----------------------------------------------------")

	except IndexError:
		exit()
