import filereader as fr
import pickle

def collectPostfixes(n):
	postfixes = set()
	for i in range(n):
		print("Processing file#%d..." % i)
		postfixes.add(fr.getPostfix(i))
	print('Processed %d files successfully. Detected %d postfixes.' % (n, len(list(postfixes))))
	return list(postfixes)

def collectAllPostfixes():
	fp = open('postfixes.dat', 'wb')
	pickle.dump(collectPostfixes(fr.count), fp)

collectAllPostfixes()