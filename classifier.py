from trainmodel import Model
import filereader as fr
import math

threshold = 0.5
alpha = math.log(threshold / (1 - threshold))

def classify(n, model):
	words = fr.getWords(n)
	spam = model.p_spam
	ham = model.p_ham
	for word in words:
		spam += model.p_w_spam[word]
		ham += model.p_w_ham[word]
	if spam - ham >= alpha:
		return True
	return False
