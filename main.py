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

#划分训练集和测试集
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

#训练模型
def train(id, pct):
	divideDataSet(pct)
	print('Training model %s.' % id)
	model = Model()
	model.train(trainingSet)
	fp = open('models\\' + id + '.mdl', 'wb')
	pickle.dump(model.p_ham, fp)
	pickle.dump(model.p_spam, fp)
	pickle.dump(model.p_w_ham, fp)
	pickle.dump(model.p_w_spam, fp)
	pickle.dump(model.p_p_ham, fp)
	pickle.dump(model.p_p_spam, fp)
	pickle.dump(testSet, fp)
	fp.close()
	print('Training finished. %d files learned. Model saved.\n\n' % len(trainingSet))
	return model

#测试模型
def test(id, use_postfix, threshold):
	fp = open('models\\' + id + '.mdl', 'rb')
	model = Model()
	model.restore(pickle.load(fp), pickle.load(fp), pickle.load(fp), pickle.load(fp), pickle.load(fp), pickle.load(fp))
	testSet = pickle.load(fp)
	correct = 0
	incorrect = 0
	alpha = math.log(threshold / (1 - threshold))
	start = time.time()
	print('Testing model %s. Postfix%s considered. Threshold is %f.' % (id, ('' if use_postfix else ' not'), threshold))
	for k in range(len(testSet)):
		i = testSet[k]
		if fr.is_spam(i) == cf.classify(i, model, use_postfix, alpha):
			correct += 1
		else:
			incorrect += 1
		delta = time.time() - start
		sys.stdout.write("\rTesting progress: %d/%d. %d correctly and %d incorrectly classified. Elapsed time: %d.%03d seconds." \
			% (k + 1, len(testSet), correct, incorrect, delta, delta * 1000 % 1000))
		sys.stdout.flush()
	print('\n%d in %d files correctly classified. Accuracy %f.\n\n' % (correct, len(testSet), correct / len(testSet)))
	return correct / len(testSet)

#批量训练
def multitrain():
	percentage = [5, 20, 50, 80, 100]
	for p in percentage:
			id = 'model_%d' % (p)
			for k in range(10):
				train('%s_%d' % (id, k), p)

#批量测试
def multitest():
	percentage = [5, 20, 50, 80, 100]
	threshold = [0.3, 0.5, 0.7]
	acc = dict()
	for p in percentage:
		acc[p] = dict()
		for t in threshold:
			acc[p][t] = dict()
			acc[p][t][True] = dict()
			acc[p][t][False] = dict()
			id = 'model_%d' % (p)
			for k in range(10):
				acc[p][t][True][k] = test('%s_%d' % (id, k), True, t)
				acc[p][t][False][k] = test('%s_%d' % (id, k), False, t)
	for p in percentage:
		for t in threshold:
			print('Average accuracy of %d_%d_True is %f' % (p, t * 10, (sum(acc[p][t][True].values()) / 10)))
			print('Average accuracy of %d_%d_False is %f' % (p, t * 10, (sum(acc[p][t][False].values()) / 10)))

multitrain()
multitest()