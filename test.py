
def fileCompare(fileName1,fileName2):
	f1 = open(fileName1,'r')
	f2 = open(fileName2,'r')

	f1string = f1.readline().strip()
	flag = True
	while f1string:
		f2string = f2.readline().strip()
		print f1string+"   "+f2string
		if f1string != f2string:
			print "They are not the same in the above line.********************************"
			flag = False
		f1string = f1.readline().strip()
	f1.close()
	f2.close()

	if flag == True:
		print "They are exactly the same with each other!"
	else:
		print "They are different in place with '********************************'."

# Test case 1 Greedy First Search
# fileCompare('./1/next_state.txt',"./1/GreedyFirst_nextstate.txt")

# Test case 2 MiniMax Search cutoff=1
# next state test
# fileCompare('./2/next_state.txt','./2/Minimax_nextState.txt')
# log test 
# fileCompare('./2/traverse_log.txt','./2/Minimax_log.txt')

# Test case 3 MiniMax Search cutoff=2
# next state test
# fileCompare('./3/next_state.txt','./3/Minimax_nextState.txt')
# log test 
# fileCompare('./3/traverse_log.txt','./3/Minimax_log.txt')

# Test case 4 Alpha-Beta Search cutoff=2
# next state test
# fileCompare('./4/next_state.txt','./4/AlphaBeta_nextState.txt')
# log test 
# fileCompare('./4/traverse_log.txt','./4/AlphaBeta_log.txt')

# Test case 5 Battle Simulation
# fileCompare('./5/trace_state.txt','./5/BATTLESIMULATION.txt')