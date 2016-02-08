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


