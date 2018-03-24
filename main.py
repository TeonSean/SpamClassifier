import filereader as fr
import random
import math
import pickle
from trainmodel import Model
import classifier as cf
import sys
import time

trainingSet = list()
testSet = list()

def divideDataSet(pct):
	global trainingSet, testSet
	n = math.ceil(fr.count * pct / 100)
	numbers = list(range(fr.count))
	random.shuffle(numbers)
	trainingSet = numbers[:n]
	trainingSet.sort()
	testSet = numbers[n:]
	if len(testSet) == 0:
		testSet = numbers
	testSet.sort()

def train(id, pct):
	divideDataSet(pct)
	print('Training model %s.' % id)
	model = Model()
	model.train(trainingSet)
	fp = open(id + '.mdl', 'wb')
	pickle.dump(model.p_ham, fp)
	pickle.dump(model.p_spam, fp)
	pickle.dump(model.p_w_ham, fp)
	pickle.dump(model.p_w_spam, fp)
	pickle.dump(model.p_p_ham, fp)
	pickle.dump(model.p_p_spam, fp)
	pickle.dump(testSet, fp)
	fp.close()
	print('Training finished. %d files learned. Model saved.' % len(trainingSet))
	return model

def test(id, use_postfix):
	fp = open(id + '.mdl', 'rb')
	model = Model()
	model.restore(pickle.load(fp), pickle.load(fp), pickle.load(fp), pickle.load(fp), pickle.load(fp), pickle.load(fp))
	testSet = pickle.load(fp)
	correct = 0
	incorrect = 0
	start = time.time()
	print('Using model %s.' % id)
	for k in range(len(testSet)):
		i = testSet[k]
		if fr.is_spam(i) == cf.classify(i, model, use_postfix):
			correct += 1
		else:
			incorrect += 1
		delta = time.time() - start
		sys.stdout.write("\rTesting progress: %d/%d. %d correctly and %d incorrectly classified. Elapsed time: %d.%d seconds." \
			% (k + 1, len(testSet), correct, incorrect, delta, delta * 1000 % 1000))
		sys.stdout.flush()
	print('\n%d in %d files correctly classified. Accuracy %f.' % (correct, len(testSet), correct / len(testSet)))
