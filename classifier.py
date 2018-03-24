from trainmodel import Model
import filereader as fr
import math

#判断第n封邮件是否垃圾邮件。 model-所选用的训练好的分类器。 use_postfix-是否使用发件人邮箱后缀信息。 alpha-阈值
def classify(n, model, use_postfix, alpha):
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
