from flask import Flask, render_template
from flask import request
from datetime import datetime
from textblob import TextBlob
import random
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
	timeNow = datetime.now()
	year = str(timeNow.year)
	#removeFromFile(str(timeNow))
	fileItself = readFile()
	if request.method == "POST":
		theMessage = request.form["theActPost"].strip()
		errMess = ""
		if sentiment(theMessage)==False:
			errMess = "ERROR: Your message was not positive enough. Refrain from using words such as 'not', 'don't', etc."
		elif spacingFilter(theMessage)==False:
			errMess = "ERROR: Please check the spacing in your message."
		if errMess!="":
			newestFile = random.sample(fileItself, 3)
			if fileItself[0] not in newestFile:
				newestFile.append(fileItself[0])
			return render_template("index.html", messageList = newestFile, listLen = len(fileItself), year=year, errMess=errMess)
		addToFile(theMessage, timeNow)
		newFile = readFile()
		newestFile = random.sample(newFile, 3)
		if newFile[0] not in newestFile:
			newestFile.append(newFile[0])
		print(newestFile)
		return render_template("index.html", messageList = newestFile, listLen = 4, year=year, errMess='')
	else:
		newestFile = random.sample(fileItself, 3)
		if fileItself[0] not in newestFile:
			newestFile.append(fileItself[0])
		return render_template("index.html", messageList = newestFile, listLen = 4, year=year, errMess='')

def sentiment(text):
	inst = TextBlob(text)
	pol = inst.sentiment.polarity
	"""
	if pol<0 or pol==0:
		return False
	elif pol>0 and pol<=1:
		return True
	"""
	if pol<0.25:
		return False
	if "not" in text:
		return False
	return True

def spacingFilter(text):
	textList = text.split()
	for element in textList:
		if len(element)==1 and textList.index(element)<=len(textList)-3:
			if len(textList[textList.index(element)+1])==1:
				if len(textList[textList.index(element)+2])==1:
					return False
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
"""
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
"""
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
	#app.run(debug=True)
	app.run(port=80, host="0.0.0.0")
