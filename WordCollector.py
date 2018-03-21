count = 64620
root_dir = '.\\data\\data_cut\\'

def numberToStr3(n):
	return '%03d' % n

def getFilenameByNumber(n):
	if n >= count:
		return
	level_1 = n // 300
	level_2 = n % 300
	return root_dir + numberToStr3(level_1) + '\\' + numberToStr3(level_2)