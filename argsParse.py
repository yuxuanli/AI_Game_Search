import sys
inputFile = ""
for i in range(len(sys.argv)):
	if sys.argv[i]=="-i":
		inputFile = sys.argv[i+1]
		print inputFile
		break