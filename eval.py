import os
import string
import sys

class EvalClass:
	'''
	eval class analyzes a text file and returns:
	the letter frequency analysis
	'''
	def __init__(self,target):
		'''initializes the  evaluation class'''
		self.target=target	#the name of the target file to be evaluated
		self.letter_frequency={}	#dictionary which will hold the frequency of each letter
		self.letter_count={}		#a dictionary which will hold the total of each letter
		self.total_letters=0		#the total letters in the cypher
		
		'''
			build our dicts and set the values to 0
		'''
		for letter in string.ascii_lowercase:
			self.letter_frequency[letter]=0.0
			self.letter_count[letter]=0
		

	def freq_analysis(self):
		'''
			does a frequency analysis on a string 
			and comes up wtih the percentage of letters
		'''

		letters=string.ascii_lowercase	#just holds the string of lowercase letters
		
		'''
		open the target file
		for each letter in the file, count the number of times the letter occurs 
		and the total letters in the file
		'''
		file=open(self.target,"r")	#file contianing the encoded text
		lines=file.readlines()	#hodls all the lines in the file
		for line in lines:
			for letter in line:
				if letter in letters:
					self.letter_count[letter]+=1
					self.total_letters+=1
		'''
		for each possible letter, calculate the frequency based on the total number of letters
		'''
		for letter in letters:
			self.letter_frequency[letter]=self.letter_count[letter]/self.total_letters
		
		'''
		output the frequqency, testing purposes only
	
		for letter in letters:
			print(letter,"|",self.letter_count[letter],"|",self.letter_frequency[letter])
	'''	
	def find_one_letters(self):
		'''
		first part of our analysis, we will find all the single letters
		rule: there can only be 2 (I,A)
		if we find 1 it is a/i
		if we find 2, they are a/i and the rest are removed
		'''
		file=open(self.target,'r')
		lines=file.readlines()
		single=[]
		for line in lines:
			words=line.split()
			for word in words:
				if len(word)==1 and single.count(word)==0:
					single.append(word)
				if len(single)==2:
					break
			if len(single)==2:
				break
					
		self.fake[single[0]]=const.oneLetter
		self.fake[single[1]]=const.oneLetter
		##remove a/i from remainder of items if 2 have been found
		if len(single)==2:
			for letter in string.ascii_lowercase:
				if (letter!=single[0]) & (letter!=single[1]):
					self.fake[letter].remove(const.oneLetter[0])
					self.fake[letter].remove(const.oneLetter[1])
	