count = 64620
root_dir = '.\\data\\data_cut\\'

def numberToStr3(n):
	return '%03d' % n

def getFilenameByNumber(n):
	return root_dir + numberToStr3(n // 300) + '\\' + numberToStr3(n % 300)

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

def getWords(n):
	if n >= count:
		return None
	fp = open(getFilenameByNumber(n), encoding='utf-8')
	words = filterCharacter(fp.read()).split(' ')
	words = [word for word in words if not word == '']
	return words
