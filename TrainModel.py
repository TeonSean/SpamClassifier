import filereader as fr
import math
import pickle
import sys

class Model:
	p_w_ham = dict()
	p_w_spam = dict()
	p_p_ham = dict()
	p_p_spam = dict()
	p_ham = float()
	p_spam = float()


	#计算先验概率
	def computePriorProb(self, trainingSet):
		total = len(trainingSet)
		n_ham = 0
		n_spam = 0
		for i in trainingSet:
			if fr.is_spam(i):
				n_spam += 1
			else:
				n_ham += 1
		self.p_ham = (n_ham + 1) / (total + 2)
		self.p_spam = (n_spam + 1) / (total + 2)
		self.p_ham = math.log(self.p_ham)
		self.p_spam = math.log(self.p_spam)
		return n_ham, n_spam


	def initDicts(self):
		fp = open('words.dat', 'rb')
		words = pickle.load(fp)
		for word in words:
			self.p_w_ham[word] = 0
			self.p_w_spam[word] = 0
		fp.close()
		fp = open('postfixes.dat', 'rb')
		postfixes = pickle.load(fp)
		for postfix in postfixes:
			self.p_p_ham[postfix] = 0
			self.p_p_spam[postfix] = 0
		fp.close()


	#计算后验概率
	def computePostProb(self, trainingSet, n_ham, n_spam):
		for k in range(len(trainingSet)):
			i = trainingSet[k]
			words = fr.getWords(i)
			counts = self.p_w_spam if fr.is_spam(i) else self.p_w_ham
			for word in words:
				counts[word] += 1
			counts = self.p_p_spam if fr.is_spam(i) else self.p_p_ham
			counts[fr.getPostfix(i)] += 1
			sys.stdout.write("\rTraining progress: %d/%d" % (k + 1, len(trainingSet)))
			sys.stdout.flush()
		print('\nprocessing...')
		for key in self.p_w_ham:
			self.p_w_ham[key] += 1
			self.p_w_ham[key] /= (n_ham + 2)
			self.p_w_ham[key] = math.log(self.p_w_ham[key])
		for key in self.p_w_spam:
			self.p_w_spam[key] += 1
			self.p_w_spam[key] /= (n_spam + 2)
			self.p_w_spam[key] = math.log(self.p_w_spam[key])
		for key in self.p_p_ham:
			self.p_p_ham[key] += 1
			self.p_p_ham[key] /= (n_ham + 2)
			self.p_p_ham[key] = math.log(self.p_p_ham[key])
		for key in self.p_p_spam:
			self.p_p_spam[key] += 1
			self.p_p_spam[key] /= (n_spam + 2)
			self.p_p_spam[key] = math.log(self.p_p_spam[key])


	def train(self, trainingSet):
		n_ham, n_spam = self.computePriorProb(trainingSet)
		self.initDicts()
		self.computePostProb(trainingSet, n_ham, n_spam)


	#从文件中还原model
	def restore(self, p_ham, p_spam, p_w_ham, p_w_spam, p_p_ham, p_p_spam):
		self.p_ham = p_ham
		self.p_spam = p_spam
		self.p_w_ham = p_w_ham
		self.p_w_spam = p_w_spam
		self.p_p_ham = p_p_ham
		self.p_p_spam = p_p_spam
