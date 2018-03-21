import FileReader as fr
import pickle

def collectWords(n):
	words = set()
	for i in range(n):
		print("Processing file#%d..." % i)
		candidates = fr.getWords(i)
		words = words.union(set(candidates))
	print('Processed %d files successfully.' % n)
	return list(words)

def collectAllWords():
	fp = open('words.dat', 'wb')
	pickle.dump(collectWords(fr.count), fp)

collectAllWords()
