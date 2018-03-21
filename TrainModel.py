import FileReader as fr
import pickle

class Model:
	p_w_ham = dict()
	p_w_spam = dict()
	p_ham = float()
	p_spam = float()
	__id = str()


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
		return n_ham, n_spam


	def initDicts(self):
		fp = open('words.dat', 'rb')
		words = pickle.load(fp)
		for word in words:
			self.p_w_ham[word] = 0
			self.p_w_spam[word] = 0
		fp.close()


	def computePostProb(self, trainingSet, n_ham, n_spam):
		for i in trainingSet:
			#print('learning file#%d' % i)
			words = fr.getWords(i)
			counts = self.p_w_spam if fr.is_spam(i) else self.p_w_ham
			for word in words:
				counts[word] += 1
		for key in self.p_w_ham:
			self.p_w_ham[key] += 1
			self.p_w_ham[key] /= (n_ham + 2)
		for key in self.p_w_spam:
			self.p_w_spam[key] += 1
			self.p_w_spam[key] /= (n_spam + 2)


	def train(self, trainingSet):
		n_ham, n_spam = self.computePriorProb(trainingSet)
		self.initDicts()
		self.computePostProb(trainingSet, n_ham, n_spam)
		print(self.p_w_spam)
		print(self.p_w_ham)


	def __init__(self, id, trainingSet):
		self.__id = id
		self.train(trainingSet)
