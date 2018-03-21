import FileReader as fr
import random
import math
import pickle
from TrainModel import Model

trainingSet = list()
testSet = list()

def divideDataSet(pct):
	global trainingSet, testSet
	n = math.ceil(fr.count * pct / 100)
	numbers = list(range(fr.count))
	random.shuffle(numbers)
	trainingSet = numbers[:n]
	testSet = numbers[n:]

divideDataSet(25)
test = Model('test', trainingSet)