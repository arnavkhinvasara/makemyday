from flask import Flask, render_template, request, send_from_directory
from datetime import datetime
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
	timeNow = datetime.now()
	year = str(timeNow.year)
	removeFromFile(timeNow)
	fileItself = readFile()
	if request.method == "POST":
		theMessage = request.form["theActPost"].strip()
		if theMessage in fileItself:
			return render_template("index.html", messageList = fileItself, listLen = len(fileItself), year=year)
		addToFile(theMessage, timeNow)
		newFile = readFile()
		return render_template("index.html", messageList = newFile, listLen = len(newFile), year=year)
	else:
		return render_template("index.html", messageList = fileItself, listLen = len(fileItself), year=year)

def dbCommand():
	with open("database.txt") as db:
		dbLines = db.readlines()
		allMessages = []
		for line in dbLines:
			allMessages.append(line.strip())
	return allMessages

def removeFromFile(time):
	allMessages = dbCommand()
	dataDict = {}
	for message in allMessages:
		firstPart = message.split(" ---- ")[0]
		secondPart = message.split(" ---- ")[1]
		dataDict[secondPart] = firstPart
	allTimes = list(dataDict.keys())
	print(allTimes)
	for aTime in allTimes:
		if (time - datetime.fromisoformat(aTime)).days >= 1:
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