#!/usr/bin/python

from glob import iglob
import os
from collections import defaultdict

class WordCount:

	datastore = defaultdict(int)

	def files(self, dir='wc_input'):
		'''
			lists files one by one
			returns an iterator and does not store huge values in memory
		'''
		for eachfile in iglob(os.path.join(dir,'*')):
			yield eachfile


	def words(self, file_name):
		'''
			reads word by word from a file.
			reads a fixed buffer from a file. Does not store more than 10240 bytes in the memory
		'''
		last = ""
		with open(file_name) as inp:
			while True:
				buf = inp.read(10240)
				if not buf:
					break
				words = (last+buf).replace("\n"," ").split()
				last = words.pop()
				for word in words:
					yield word
			yield last


	def sanitize(self, word):
		'''
			removes garbage from around the word AND converts word to lower
			add more alphabets or words to remove from around the words
		'''
		toremove = [' ', '"', ",", "'", ".", "?", "-", "=", "|", "\r", \
					"\r\n", "\n", "_", ";", ":", "!", "(", ")", "*"] 
		word = word.strip("".join(toremove))
		return word.lower()


	def countit(self, word):
		'''
			Counts the word in the datastore
		'''
		self.datastore[word] += 1


	def writeresults(self, outputfilename=os.path.join("wc_output", "wc_result.txt")):
		'''
			writes the counted words to the output file
		'''
		with open(outputfilename, 'w+') as f:
			for i in self.datastore:
				f.write(i + " " + str(self.datastore[i]) + "\n")


	def runner(self):
		for f in self.files():
			for word in self.words(f):
				word = self.sanitize(word)
				if word!="":
					self.countit(word)

	def __init__(self):
		self.runner()
		self.writeresults()

if __name__ == "__main__":
	wc=WordCount()
