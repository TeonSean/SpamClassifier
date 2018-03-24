from trainmodel import Model
import filereader as fr
import math

threshold = 0.5
alpha = math.log(threshold / (1 - threshold))

def classify(n, model, use_postfix):
	words = fr.getWords(n)
	postfix = fr.getPostfix(n)
	spam = model.p_spam
	ham = model.p_ham
	for word in words:
		spam += model.p_w_spam[word]
		ham += model.p_w_ham[word]
	if use_postfix == True:
		spam += model.p_p_spam[postfix]
		ham += model.p_p_ham[postfix]
	if spam - ham >= alpha:
		return True
	return False
