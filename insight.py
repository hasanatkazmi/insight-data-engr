#!/usr/bin/python

from glob import iglob
import os
from collections import defaultdict
import string 
from blist import sortedlist
import sys
import getopt

class Constant:
	EOF		=	0x1200
	EOL		=	0x1201
	EOW		=	0x1202

def files(dir='wc_input'):
	'''
		returns an iterator
		Running time: sorted will take O(nlogn) (Python uses tim sort that has better performace than quick sort on average cases)
		Space: iglob doesn't buffer but uses pointers, but sorting requires access to all elements, so at worst space required is O(n)
	'''
	for eachfile in sorted(iglob(os.path.join(dir,'*'))):
		yield eachfile

def aplhabets(file_name, buf=10240, ignore=[], enableEOW=True, enableEOL=True):
	'''
		returns:
		aplhabet or
		EOL	or # informs that end of line has occured
		EOW	# informs that end of word has occured
		Running time: constant operations on each aplhabet, O(1)
		Space: we buffer buf for performace (default 10KB). Its constant, O(1)
	'''
	with open(file_name, 'rb') as fp:
		for chunk in iter(lambda: fp.read(buf), ''):
			for apl in chunk:
				if apl.lower() in string.ascii_lowercase or apl in ignore:
					yield apl.lower()
				elif apl == " " and enableEOW:
					yield Constant.EOW
				elif apl == "\n" and enableEOL:
					yield Constant.EOL

def words(file_name, ignoreEOL=True):
	'''
		Reads words in the file. uses aplhabets function 
	'''
	word = ''
	for apl in aplhabets(file_name):
		if apl != Constant.EOW and apl!= Constant.EOL:
			word = word + apl
		else:
			if word != "":
				yield word	
				word = ''

				if apl == Constant.EOL and not ignoreEOL:
					yield Constant.EOL


def count_words_in_lines(file_name):
	'''
		Reads lines from the file. uses words function
	'''	
	count = 0
	for word in words(file_name, ignoreEOL=False):
		if word != Constant.EOL:
			count = count+1
		else:
			yield count
			count = 0	

def wordcount(inputdir='wc_input', outputfilename=os.path.join("wc_output", "wc_result.txt")):
	'''
		Uses words to count words in all files
	'''
	datastore = defaultdict(int)

	for f in files(dir=inputdir):
		for word in words(f):
			datastore[word] += 1
	
	with open(outputfilename, 'w+') as f:
		for i in sorted(datastore):
			f.write(i + "\t" + str(datastore[i]) + "\n")

def running_median(inputdir='wc_input', outputfilename=os.path.join("wc_output", "med_result.txt")):
	'''
		This function uses blist library. sortedlist in blist saves elements in binary tree struction making insertion and acess O(logn) 
	'''

	sl = sortedlist()

	with open(outputfilename, 'w+') as outfile:
		for f in files(dir=inputdir):
			for cur_count in count_words_in_lines(f):
				sl.add(cur_count) # O(logn)

				median = sl[len(sl)/2] # O(logn)
				if len(sl)%2==0: # O(1)
					median += sl[(len(sl)/2)-1] #O(logn)
					median /=2.0

				median = round(median, 1)
				outfile.write(str(median)+ "\n")

def main(argv):
	indir = ''
	outfile = ''
	function = ''

	try:
		opts, args = getopt.getopt(argv,"hi:o:f:",["indir=","outfile=","function="])
	except getopt.GetoptError:
		print 'test.py -i <inputdirectory> -o <outputfile> -f <function>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -i <inputdirectory> -o <outputfile> -f <function>'
			sys.exit()
		elif opt in ("-i", "--indir"):
			indir = arg
		elif opt in ("-o", "--outfile"):
			outfile = arg
		elif opt in ("-f", "--function"):
			function = arg

	if indir != '' and outfile != '' and function != '':
		if function == "wordcount":
			wordcount(inputdir=indir, outputfilename=outfile)
		elif function == "runningmedian":
			running_median(inputdir=indir, outputfilename=outfile)
		else:
			sys.exit("argument error")

if __name__ == "__main__":
	main(sys.argv[1:])

