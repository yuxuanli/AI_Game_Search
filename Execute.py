from Board import Board
from sys import maxint

MAX_INT = maxint
MIN_INT = -maxint-1

board= Board()

f = open('./5/input.txt','r')
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

	if task == "1":# Greedy-Best-First-Search
		nextMove = board.GreedyFirstSearch(myplayer)
		# write into the file
		nextState = open('./1/GreedyFirst_nextstate.txt','w')
		nextState.write(board.makeAction(nextMove,myplayer).textBoard())
		nextState.close()
	elif task =="2":# MiniMaxSearch
		log = open('./3/Minimax_log.txt','w')
		log.write("Node,Depth,Value\n")
		currentDepth = 0
		nextMove = board.MiniMaxSearch("root",currentDepth+1,cutoffDepth,myplayer,log)
		log.close()

		nextState = open("./3/Minimax_nextState.txt","w")
		nextState.write(board.makeAction(nextMove,myplayer).textBoard())
		nextState.close()
	elif task =="3":# Alpha-Beta-Search
		log = open('./4/AlphaBeta_log.txt','w')
		log.write("Node,Depth,Value,Alpha,Beta\n")
		currentDepth = 0
		alpha = MIN_INT
		beta = MAX_INT
		nextMove = board.AlphaBetaSearch(alpha,beta,"root",currentDepth+1,cutoffDepth,myplayer,log)
		log.close()

		nextState = open("./4/AlphaBeta_nextState.txt","w")
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

	#print board.nofile_AlphaBetaSearch(MIN_INT,MAX_INT,1,2,"O")
	#print board.nofile_MiniMaxSearch(1,2,"O")

	while not board.terminal_test():
		board = board.BattleSimulation(firstplayer,firstplayerAlg,firstplayerCutoffDepth)
		battleText += board.textBoard()
		if not board.terminal_test():
			board = board.BattleSimulation(secondplayer,secondplayerAlg,secondplayerCutoffDepth)
			battleText += board.textBoard()
		else:
			break
	f = open('./5/BATTLESIMULATION.txt','w')
	f.write(battleText)
	f.close()









