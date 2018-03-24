from trainmodel import Model
import filereader as fr
import math

#判断第n封邮件是否垃圾邮件。 model-所选用的训练好的分类器。 use_postfix-是否使用发件人邮箱后缀信息。 alpha-阈值
def classify(n, model, use_postfix, alpha):
	words = fr.getWords(n)
	postfix = fr.getPostfix(n)
	diff = model.p_spam - model.p_ham + model.diff
	for word in words:
		diff += model.p_w_spam[word]
		diff -= model.p_w_ham[word]
	if use_postfix == True:
		#postfix = postfix if postfix in model.p_p_ham.keys() else None
		diff += (model.p_p_spam[postfix] - model.p_p_ham[postfix])
	if diff >= alpha:
		return True
	return False
