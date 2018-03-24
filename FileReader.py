import re

count = 64620
root_dir = '.\\data\\data_cut\\'
labels = list()
fp = open('data\\label\\index', 'r')
#获取label文件夹中的数据
for line in fp.readlines():
	if line[0] == 's':
		labels.append(True)
	else:
		labels.append(False)
fp.close()

#根据label文件夹的内容判断某邮件是否垃圾邮件
def is_spam(n):
	if n >= count:
		return None
	return labels[n]

#格式化数字
def numberToStr3(n):
	return '%03d' % n

#根据0~64619的数字id获取文件路径
def getFilenameByNumber(n):
	return root_dir + numberToStr3(n // 300) + '\\' + numberToStr3(n % 300)

#获取某一邮件的发件人的邮箱后缀
def getPostfix(n):
	if n >= count:
		return None
	fp = open(getFilenameByNumber(n), encoding='utf-8')
	lines = fp.readlines()
	for line in lines:
		if not line[:4] == 'From':
			continue
		postfix = re.search(r'@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+', line)
		if not postfix == None:
			postfix = postfix.group()
		return postfix
	return None

#筛去邮件中的非中文字符
def filterCharacter(content):
	re = ''
	has_space = False
	for i in range(len(content)):
		uchar = content[i]
		if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
			re = re + uchar
			has_space = False
		elif not has_space:
			re = re + u' '
			has_space = True
	return re

#获取邮件中出现的中文词语的列表
def getWords(n):
	if n >= count:
		return None
	fp = open(getFilenameByNumber(n), encoding='utf-8')
	words = filterCharacter(fp.read()).split(' ')
	words = list(set([word for word in words if not word == '']))
	return words
