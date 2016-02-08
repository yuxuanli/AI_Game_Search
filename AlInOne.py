import copy
import sys
from sys import maxint
MAX_INT = maxint
MIN_INT = -maxint-1

class Cell:
	def __init__(self,x,y,value=0,state="*"):
		self.x = x
		self.y = y
		self.value = value
		self.state = state
		self.evaluatedValue = 0
		alphalist = ["","A","B","C","D","E"]
		self.name = alphalist[y]+str(x)

	def setValue(self,value):
		self.value = value

	def getValue(self):
		return self.value

	def setState(self,state):
		self.state = state

	def getState(self):
		return self.state

	def setEvaluatedValue(self,evaluatedValue):
		self.evaluatedValue = evaluatedValue

	def getEvaluatedValue(self):
		return self.evaluatedValue
	def getName(self):
		return self.name

	def printCell(self):
		print "["+ str(self.x)+","+str(self.y)+"]"+str(self.value)+self.state

	def printCellName(self):
		print self.name

class Board:
	def __init__(self):
		self.board = [[Cell(j,i) for i in range(1,6)] for j in range(1,6)]

	def print_board(self):
		for row in self.board:
			for cell in row:
				cell.printCell()

	def print_boardValue(self):
		for row in self.board:
			string = ""
			for cell in row:
				string += " "+ str(cell.getValue())
			print string 

	def print_boardState(self):
		for row in self.board:
			string = ""
			for cell in row:
				string += " "+ str(cell.getState())
			print string
	def print_boardName(self):
		for row in self.board:
			string = ""
			for cell in row:
				string += " "+ str(cell.getName())
			print string

	def print_boardEvaluatedValue(self):
		for row in self.board:
			string = ""
			for cell in row:
				string += " "+ str(cell.getEvaluatedValue())
			print string

	def getCell(self,x,y):
		return self.board[x][y];

	def textBoard(self):
		text =""
		for i in range(5):
			for j in range(5):
				text += self.getCell(i,j).getState() 
			text += "\n"
		return text

	def legalActions(self):
		result = []
		for i in range(0,5):
			for j in range(0,5):
				if self.getCell(i,j).getState()=="*":
					result.append([i,j])
		return result
	def terminal_test(self):
		for i in range(0,5):
			for j in range(0,5):
				if self.getCell(i,j).getState()=="*":
					return False
		return True

	def makeAction(self,index,myplayer):
		b = copy.deepcopy(self)
		if b.getCell(index[0],index[1]).getState()=="*":
			b.getCell(index[0],index[1]).setState(myplayer)
			#print b.getCell(index[0],index[1]).getName()
			x = index[0]
			y = index[1]
			adjacents = [[x-1,y],[x+1,y],[x,y-1],[x,y+1]]
			validAdjacents = filter(lambda x: x[0]>=0 and x[0]<5 and x[1]>=0 and x[1]<5,adjacents)
			#print validAdjacents
			for nearby in validAdjacents:
				i = nearby[0]
				j = nearby[1]
				if b.getCell(i,j).getState() == myplayer:#this is a grid
					for near in validAdjacents:
						tempCell = b.getCell(near[0],near[1])
						if tempCell.getState()!=myplayer and tempCell.getState()!="*":
							tempCell.setState(myplayer)
		return b
		
	def currentEvaluatedValue(self,myplayer):
		result = 0
		for i in range(5):
			for j in range(5):
				tempCell = self.getCell(i,j)
				if tempCell.getState()==myplayer:
					result+= tempCell.getValue()
				elif tempCell.getState()=="*":
					pass
				else:
					result -= tempCell.getValue()
		return result

	def GreedyFirstSearch(self,myplayer):
		nextMove = []
		maxUtility = MIN_INT
		if not self.terminal_test():
			for a in self.legalActions():
				currentValue = self.makeAction(a,myplayer).currentEvaluatedValue(myplayer)
				if currentValue>maxUtility:
					maxUtility = currentValue
					nextMove = a
			return nextMove

	def MiniMaxSearch(self,parentSquare,currentDepth,cutoffDepth,myplayer,f):
		nextMove = []
		yourplayer = "O" if myplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			f.write(parentSquare+","+str(currentDepth-1)+","+str(self.currentEvaluatedValue(myplayer))+"\n")
			return self.currentEvaluatedValue(myplayer)
		v = MIN_INT
		f.write(parentSquare+","+str(currentDepth-1)+ ","+convertInfinity(v)+"\n")
		for a in self.legalActions():
			squareName = self.getCell(a[0],a[1]).getName()
			currentValue = self.makeAction(a,myplayer).minValue(squareName,currentDepth+1,cutoffDepth,yourplayer,f)
			if currentValue>v:
				nextMove = a
			v = max(v,currentValue)
			f.write(parentSquare+","+str(currentDepth-1)+","+convertInfinity(v)+"\n")
		return nextMove

	def maxValue(self,parentSquare,currentDepth,cutoffDepth,myplayer,f):
		nextMove = []
		yourplayer = "O" if myplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			f.write(parentSquare+","+str(currentDepth-1)+","+str(self.currentEvaluatedValue(myplayer))+"\n")
			return self.currentEvaluatedValue(myplayer)
		v = MIN_INT
		f.write(parentSquare+","+str(currentDepth-1)+ ","+convertInfinity(v)+"\n")
		for a in self.legalActions():
			squareName = self.getCell(a[0],a[1]).getName()
			currentValue = self.makeAction(a,myplayer).minValue(squareName,currentDepth+1,cutoffDepth,yourplayer,f)
			v = max(v,currentValue)
			f.write(parentSquare+","+str(currentDepth-1)+","+convertInfinity(v)+"\n")
		return v

	def minValue(self,parentSquare,currentDepth,cutoffDepth,yourplayer,f):
		myplayer = "O" if yourplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			f.write(parentSquare+","+str(currentDepth-1)+","+str(self.currentEvaluatedValue(myplayer))+"\n")
			return self.currentEvaluatedValue(myplayer)
		v = MAX_INT
		f.write(parentSquare+","+str(currentDepth-1)+ ","+convertInfinity(v)+"\n")
		for a in self.legalActions():
			squareName = self.getCell(a[0],a[1]).getName()
			currentValue = self.makeAction(a,yourplayer).maxValue(squareName,currentDepth+1,cutoffDepth,myplayer,f)
			v = min(v,currentValue)
			f.write(parentSquare+","+str(currentDepth-1)+","+convertInfinity(v)+"\n")
		return v

	def AlphaBetaSearch(self,alpha,beta,parentSquare,currentDepth,cutoffDepth,myplayer,f):
		nextMove = []
		yourplayer = "O" if myplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			f.write(parentSquare+","+str(currentDepth-1)+","+str(self.currentEvaluatedValue(myplayer))+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
			return self.currentEvaluatedValue(myplayer)
		v = MIN_INT
		f.write(parentSquare+","+str(currentDepth-1)+ ","+convertInfinity(v)+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
		for a in self.legalActions():
			squareName = self.getCell(a[0],a[1]).getName()
			currentValue = self.makeAction(a,myplayer).AlphaBeta_minValue(alpha,beta,squareName,currentDepth+1,cutoffDepth,yourplayer,f)
			if currentValue>v:
				nextMove = a
			v = max(v,currentValue)
			if v>=beta:
				f.write(parentSquare+","+str(currentDepth-1)+","+convertInfinity(v)+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
				return v
			else:
				alpha = max(alpha,v)
				f.write(parentSquare+","+str(currentDepth-1)+","+convertInfinity(v)+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
		return nextMove

	def AlphaBeta_maxValue(self,alpha,beta,parentSquare,currentDepth,cutoffDepth,myplayer,f):
		nextMove = []
		yourplayer = "O" if myplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			f.write(parentSquare+","+str(currentDepth-1)+","+str(self.currentEvaluatedValue(myplayer))+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
			return self.currentEvaluatedValue(myplayer)
		v = MIN_INT
		f.write(parentSquare+","+str(currentDepth-1)+ ","+convertInfinity(v)+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
		for a in self.legalActions():
			squareName = self.getCell(a[0],a[1]).getName()
			currentValue = self.makeAction(a,myplayer).AlphaBeta_minValue(alpha,beta,squareName,currentDepth+1,cutoffDepth,yourplayer,f)
			if currentValue>v:
				nextMove = a
			v = max(v,currentValue)
			if v>=beta:
				f.write(parentSquare+","+str(currentDepth-1)+","+convertInfinity(v)+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
				return v
			else:
				alpha = max(alpha,v)
				f.write(parentSquare+","+str(currentDepth-1)+","+convertInfinity(v)+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
		return v

	def AlphaBeta_minValue(self,alpha,beta,parentSquare,currentDepth,cutoffDepth,yourplayer,f):
		myplayer = "O" if yourplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			f.write(parentSquare+","+str(currentDepth-1)+","+str(self.currentEvaluatedValue(myplayer))+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
			return self.currentEvaluatedValue(myplayer)
		v = MAX_INT
		f.write(parentSquare+","+str(currentDepth-1)+ ","+convertInfinity(v)+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
		for a in self.legalActions():
			squareName = self.getCell(a[0],a[1]).getName()
			currentValue = self.makeAction(a,yourplayer).AlphaBeta_maxValue(alpha,beta,squareName,currentDepth+1,cutoffDepth,myplayer,f)
			v = min(v,currentValue)
			if v<=alpha:
				f.write(parentSquare+","+str(currentDepth-1)+","+convertInfinity(v)+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
				return v
			else:
				beta = min(beta,v)
				f.write(parentSquare+","+str(currentDepth-1)+","+convertInfinity(v)+","+convertInfinity(alpha)+","+convertInfinity(beta)+"\n")
		return v

	def nofile_MiniMaxSearch(self,currentDepth,cutoffDepth,myplayer):
		nextMove = []
		yourplayer = "O" if myplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			return self.currentEvaluatedValue(myplayer)
		v = MIN_INT
		for a in self.legalActions():
			currentValue = self.makeAction(a,myplayer).nofile_minValue(currentDepth+1,cutoffDepth,yourplayer)
			if currentValue>v:
				nextMove = a
			v = max(v,currentValue)
		return nextMove

	def nofile_maxValue(self,currentDepth,cutoffDepth,myplayer):
		nextMove = []
		yourplayer = "O" if myplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			return self.currentEvaluatedValue(myplayer)
		v = MIN_INT
		for a in self.legalActions():
			currentValue = self.makeAction(a,myplayer).nofile_minValue(currentDepth+1,cutoffDepth,yourplayer)
			v = max(v,currentValue)
		return v

	def nofile_minValue(self,currentDepth,cutoffDepth,yourplayer):
		myplayer = "O" if yourplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			return self.currentEvaluatedValue(myplayer)
		v = MAX_INT
		for a in self.legalActions():
			currentValue = self.makeAction(a,yourplayer).nofile_maxValue(currentDepth+1,cutoffDepth,myplayer)
			v = min(v,currentValue)
		return v

	def nofile_AlphaBetaSearch(self,alpha,beta,currentDepth,cutoffDepth,myplayer):
		nextMove = []
		yourplayer = "O" if myplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			return self.currentEvaluatedValue(myplayer)
		v = MIN_INT
		for a in self.legalActions():
			squareName = self.getCell(a[0],a[1]).getName()
			currentValue = self.makeAction(a,myplayer).nofile_AlphaBeta_minValue(alpha,beta,currentDepth+1,cutoffDepth,yourplayer)
			if currentValue>v:
				nextMove = a
			v = max(v,currentValue)
			if v>=beta:
				return v
			else:
				alpha = max(alpha,v)
		return nextMove

	def nofile_AlphaBeta_maxValue(self,alpha,beta,currentDepth,cutoffDepth,myplayer):
		nextMove = []
		yourplayer = "O" if myplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			return self.currentEvaluatedValue(myplayer)
		v = MIN_INT
		for a in self.legalActions():
			squareName = self.getCell(a[0],a[1]).getName()
			currentValue = self.makeAction(a,myplayer).nofile_AlphaBeta_minValue(alpha,beta,currentDepth+1,cutoffDepth,yourplayer)
			if currentValue>v:
				nextMove = a
			v = max(v,currentValue)
			if v>=beta:
				return v
			else:
				alpha = max(alpha,v)
		return v

	def nofile_AlphaBeta_minValue(self,alpha,beta,currentDepth,cutoffDepth,yourplayer):
		myplayer = "O" if yourplayer=="X" else "X"
		if self.terminal_test() or currentDepth>cutoffDepth:
			return self.currentEvaluatedValue(myplayer)
		v = MAX_INT
		for a in self.legalActions():
			squareName = self.getCell(a[0],a[1]).getName()
			currentValue = self.makeAction(a,yourplayer).nofile_AlphaBeta_maxValue(alpha,beta,currentDepth+1,cutoffDepth,myplayer)
			v = min(v,currentValue)
			if v<=alpha:
				return v
			else:
				beta = min(beta,v)
		return v

	def BattleSimulation(self,player,alg,cutoff):
		nextMove = []
		# nextMove = self.GreedyFirstSearch(player)
		# return self.makeAction(nextMove,player)
		if alg == "1":
			nextMove = self.GreedyFirstSearch(player)
		elif alg == "2":
			nextMove = self.nofile_MiniMaxSearch(1,cutoff,player)
		elif alg == "3":
			nextMove = self.nofile_AlphaBetaSearch(MIN_INT,MAX_INT,1,cutoff,player)
		else:
			pass
		return self.makeAction(nextMove,player)

def convertInfinity(n):
	if n==MAX_INT:
		return "Infinity"
	elif n== MIN_INT:
		return "-Infinity"
	else:
		return str(n)

inputFile = ""
for i in range(len(sys.argv)):
	if sys.argv[i]=="-i":
		inputFile = sys.argv[i+1]
		break
board= Board()

f = open(inputFile,'r')
task = f.readline().strip()

if task =="1" or task =="2" or task == "3":
	myplayer = f.readline().strip()
	yourplayer = ""
	if myplayer =="X":
		yourplayer = "O"
	else:
		yourplayer = "X"
	cutoffDepth = int(f.readline().strip())


	for i in range(0,5):
		oneRow = f.readline()
		array = oneRow.strip().split(" ")
		for j in range(0,5):
			board.getCell(i,j).setValue(int(array[j]))

	for i in range(0,5):
		oneRow = f.readline()
		array = list(oneRow.strip())
		for j in range(0,5):
			board.getCell(i,j).setState(array[j])
	f.close()

	if task == "1":# Greedy-Best-First-Search
		nextMove = board.GreedyFirstSearch(myplayer)
		# write into the file
		nextState = open('next_state.txt','w')
		nextState.write(board.makeAction(nextMove,myplayer).textBoard())
		nextState.close()
	elif task =="2":# MiniMaxSearch
		log = open('traverse_log.txt','w')
		log.write("Node,Depth,Value\n")
		currentDepth = 0
		nextMove = board.MiniMaxSearch("root",currentDepth+1,cutoffDepth,myplayer,log)
		log.close()

		nextState = open("next_state.txt","w")
		nextState.write(board.makeAction(nextMove,myplayer).textBoard())
		nextState.close()
	elif task =="3":# Alpha-Beta-Search
		log = open('traverse_log.txt','w')
		log.write("Node,Depth,Value,Alpha,Beta\n")
		currentDepth = 0
		alpha = MIN_INT
		beta = MAX_INT
		nextMove = board.AlphaBetaSearch(alpha,beta,"root",currentDepth+1,cutoffDepth,myplayer,log)
		log.close()

		nextState = open("next_state.txt","w")
		nextState.write(board.makeAction(nextMove,myplayer).textBoard())
		nextState.close()
elif task == "4":# Battle simulation
	firstplayer = f.readline().strip()
	firstplayerAlg = f.readline().strip()
	firstplayerCutoffDepth = int(f.readline().strip())

	secondplayer = f.readline().strip()
	secondplayerAlg = f.readline().strip()
	secondplayerCutoffDepth = int(f.readline().strip())

	for i in range(0,5):# board grid value
		oneRow = f.readline()
		array = oneRow.strip().split(" ")
		for j in range(0,5):
			board.getCell(i,j).setValue(int(array[j]))

	for i in range(0,5): #current grid state
		oneRow = f.readline()
		array = list(oneRow.strip())
		for j in range(0,5):
			board.getCell(i,j).setState(array[j])
	f.close()

	battleText = ""

	while not board.terminal_test():
		board = board.BattleSimulation(firstplayer,firstplayerAlg,firstplayerCutoffDepth)
		battleText += board.textBoard()
		if not board.terminal_test():
			board = board.BattleSimulation(secondplayer,secondplayerAlg,secondplayerCutoffDepth)
			battleText += board.textBoard()
		else:
			break
	f = open('trace_state.txt','w')
	f.write(battleText)
	f.close()









