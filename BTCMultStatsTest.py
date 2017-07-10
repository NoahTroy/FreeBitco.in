#Noah Troy
#FreeBitCo.in Strategy Script


#w = percent chance of winning
#x = payout

#(100/x) - ((100/x)/20) = w
#x = (95/w)

#Bet 0dds = (95/w)






import random , time , math

#Declare starting values:
startingMoney = 0.000005
currentMoney = startingMoney
targetAmount = 0.0003
percentChance = 1.0
percentIncrease = 0.0
currentBet = 0.00000001
success = True
timeout = 1200000 #600,000 = about 24 hours-worth of rolls on freebitco.in
iterationCounter = 0
startTime = 0
endTime = 0
averageTime = 0
timeLeft = 0
oldPercentageInterval = 0
maxBet = 0
maxBetSatoshi = 0
score = 0


#Define a function to place bets:
def bet(amount , odds):
	if (odds > 94.06):
		print('\n\nError!\nImpossible Odds!')
		exit()

	#Use the random package to determine if the roll would have won, using the designated odds:
	win = (random.random() < (odds / 100.0))

	if (win):
		payout = (math.floor(amount * (95.0/odds)))
		return payout
	else:
		payout = (0.0 - amount)
		return payout

#Define a function to increment the default values a specific number of times, and then reset them:
def increment():
	global percentIncrease
	global percentChance
	if (percentIncrease < 10000.0):
		percentIncrease += 5.0
		return True
	else:
		if (percentChance < 94.00):
			percentIncrease = 0.0
			percentChance += 1.0
			print('Current Percentage:\t' , str(percentChance) , '\n' , 'Time Remaining:\t\t' , str((9400 - (percentChance * 100)) * averageTime) , sep = '')

			return True
		else:
			return False

def writeProgress(points , percent1 , percent2 , counter , biggestBet):
	writeString = ('Score: ' + str(points) + '\t\tChance Of Winning: ' + str(percent1) + '\t\tPayout: ' + str((100 / percent1)) + '\t\tCurrent Amount To Increase Bet By: ' + str(percent2) + '\t\tNumber Of Iterations: ' + str(counter) + '\t\tMaximum Bet In Satoshi: ' + str(biggestBet) + '\n')

	with open('Success List.txt' , 'a') as file:
		file.write(writeString)


#A loop to cycle through all possibilities until the maximum paremeters are met:
while (True):
	if (percentIncrease == 0.0):
		startTime = time.time()

	success = True
	#Test each condition a set number of times, to help eliminate luck:
	for i in range(0 , 2):
		#Break out of the loop as soon as it doesn't work; saves lots of time:
		if (not success):
			break

		#reset the amount of money before each new test:
		currentMoney = startingMoney
		currentBet = 0.00000001
		iterationCounter = 0
		maxBet = 0
		score = 0

		while (True):
			if (iterationCounter > timeout):
				success = False
				break
			else:
				iterationCounter += 1

			if (currentBet > maxBet):
				maxBetSatoshi = math.ceil((currentBet * 100000000))
				maxBet = currentBet

			result = bet(currentBet , percentChance)
			currentMoney += result

			if (result <= 0.0):
				if (not(percentIncrease == 0)):
					currentBet += (currentBet * (percentIncrease / 100.0))
				if ((currentBet > currentMoney) and (currentMoney >= 0.00000001)):
					currentBet = 0.00000001
				if ((currentBet > currentMoney) and (currentMoney < 0.00000001)):
					success = False
					break
					
			else:
				currentBet = 0.00000001

			if (currentMoney >= targetAmount):
				success = True
				break

	if (percentIncrease == 10000.0):
		endTime = time.time()

		if (oldPercentageInterval != (math.floor(percentChance))):
			averageTime = 0

		if (averageTime == 0):
			averageTime = (endTime - startTime)
		else:
			averageTime = ((averageTime + (endTime - startTime))/2)

	if (success):
		print('Hello')
		#Each success gets scored in different categories, each having a range of 0-1000 possible points. This helps to choose the best of the best results:
		divideTo1000 = (timeout / 1000.0)
		divideTo10002 = (targetAmount / 1000.0)
		score += math.floor((((timeout - iterationCounter) / divideTo1000) + ((targetAmount - maxBet) / divideTo10002)))
		
		writeProgress(score , percentChance , percentIncrease , iterationCounter , maxBetSatoshi)


	keepGoing = increment()

	if (not keepGoing):
		break

topResult = 0
top10Results = []

try:
	mainFile = open('Success List.txt' , 'r')
	for result in mainFile.readlines():
		newResult = int(result[7:11])

		if (newResult > topResult):
			topResult = newResult

			top10Results.insert(0 , result)
	mainFile.close()


	topResultsFile = open('Top 10.txt' , 'w')

	counter = 0
	writeString = ''

	for item in top10Results:
		if (counter == 10):
			break
		else:
			writeString += (item + '\n')
			counter += 1

	topResultsFile.write(writeString)
	topResultsFile.close()
except:
	print('There Were No Successful Results.')	