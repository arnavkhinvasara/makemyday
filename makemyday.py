from flask import Flask, render_template, request, send_from_directory
from datetime import datetime
from textblob import TextBlob
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
	timeNow = datetime.now()
	year = str(timeNow.year)
	removeFromFile(str(timeNow))
	fileItself = readFile()
	if request.method == "POST":
		theMessage = request.form["theActPost"].strip()
		if theMessage in fileItself or sentiment(theMessage)==False:
			if theMessage in fileItself:
				errMess = "Your message already exists."
			else:
				errMess = "Your message was not positive. It was either negative or neutral."
			return render_template("index.html", messageList = fileItself, listLen = len(fileItself), year=year, errMess=errMess)
		addToFile(theMessage, timeNow)
		newFile = readFile()
		return render_template("index.html", messageList = newFile, listLen = len(newFile), year=year, errMess='')
	else:
		return render_template("index.html", messageList = fileItself, listLen = len(fileItself), year=year, errMess='')

def sentiment(text):
	inst = TextBlob(text)
	pol = inst.sentiment.polarity
	if pol<0 or pol==0:
		return False
	elif pol>0 and pol<=1:
		return True

def dbCommand():
	with open("database.txt") as db:
		dbLines = db.readlines()
		allMessages = []
		for line in dbLines:
			allMessages.append(line.strip())
	return allMessages

def slicer(aString):
	if aString[0]=="0":
		newString = aString[1:]
		return newString
	else:
		return aString

def timeDiff(current, past):
	currentFirst, currentSecond = current.split(" ")[0], current.split(" ")[1]
	currentYear, currentMonth, currentDay = currentFirst.split("-")[0], currentFirst.split("-")[1], currentFirst.split("-")[2]
	currentHour = currentSecond.split(":")[0]
	pastFirst, pastSecond = past.split(" ")[0], past.split(" ")[1]
	pastYear, pastMonth, pastDay = pastFirst.split("-")[0], pastFirst.split("-")[1], pastFirst.split("-")[2]
	pastHour = pastSecond.split(":")[0]
	currentMonth, currentDay, currentHour = slicer(currentMonth), slicer(currentDay), slicer(currentHour)
	pastMonth, pastDay, pastHour = slicer(pastMonth), slicer(pastDay), slicer(pastHour)
	if int(currentYear)==int(pastYear) and int(currentMonth)==int(pastMonth):
		if int(currentDay)==int(pastDay)+1 and currentHour<pastHour:
			return True
		elif int(currentDay)==int(pastDay):
			return True
	return False

def removeFromFile(time):
	allMessages = dbCommand()
	dataDict = {}
	for message in allMessages:
		firstPart = message.split(" ---- ")[0]
		secondPart = message.split(" ---- ")[1]
		dataDict[secondPart] = firstPart
	allTimes = list(dataDict.keys())
	for aTime in allTimes:
		strATime = str(aTime)
		if timeDiff(time, strATime)==False:
			del dataDict[aTime]
	with open("database.txt", "w") as db:
		dataList = list(dataDict.keys())
		for timePart in dataList:
			messagePart = dataDict[timePart]
			db.write(messagePart+" ---- "+timePart+"\n")

def addToFile(message, time):
	with open("database.txt", "a") as db:
		db.write(message+" ---- "+str(time)+"\n")

def readFile():
	allMessages = dbCommand()
	messagesThemselves = []
	for message in allMessages:
		splittedMessage = message.split(" ---- ")
		messagesThemselves.append(splittedMessage[0])
	messagesThemselves.reverse()
	return messagesThemselves

@app.route("/favicon.ico")
def favicon():
	return send_from_directory(app.root_path+'/static','favicon.ico',mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
	app.run(debug=True)
	#app.run(port=80, host="0.0.0.0")
