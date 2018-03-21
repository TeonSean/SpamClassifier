count = 64620
root_dir = '.\\data\\data_cut\\'

def numberToStr3(n):
	if n < 10:
		n = '00' + str(n)
	elif n < 100:
		n = '0' + str(n)
	else:
		n = str(n)
	return n

def getFilenameByNumber(n):
	if n >= count:
		return
	level_1 = n // 300
	level_2 = n % 300
	return root_dir + numberToStr3(level_1) + '\\' + numberToStr3(level_2)

