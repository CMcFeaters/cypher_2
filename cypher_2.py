#cypher_2
'''
This library will be used to create a substituion cypher using a randomly generatred key, enocde the given text, and perfrom basic analysis on the encoded text.

Keys will be dicts where of the form {key:sub} where key is the character form teh text and sub is the character used as the substituion
There will be two keys.
Enconde key: used to encode the plain text.
decode key: used to decod the encoded text

Decode key is what our machine learning thing will try to predict

Encoded text will be an output format

Analysis will include:
letter frequency-% of time a letter appears int he encoded text
standalone frequency - %of standalone letters that this letter is (a/i)
start word freq - %of word starts this letter is
end word freq - %of time this letter ends a word
double freq - %of time a letter appears twice (dd) of all doubles


required file tree:
/source_data/	#where the source files are
//[whatever the file is]/ #container for all the subfolders created and teh output data
///blks/	#where all the blocks will be stored
///enc/		#where the encoded files are stored
///keys/	#where the keys are stored

'''


#python class that can perform basic cyphers

import string
import random
import os
import sys

class CypherClass:
	'''
		A class that will encode basic substituion cyphers
		stores the cypher and the key in separate text files in the folders described above
	'''
	def __init__(self,source,target):
		'''initializes the class'''
		self.source=source #this is the name of the source file, this is easier than having to worry about extracting it from the block name
		self.target=target	#name is the name of the plaintext orignal file that the cypher will work on
		self.name=self.target.split(".")[0]
		self.orig_path=os.path.join("./source_data/",self.source+"/blks/"+self.target)	#path to file we're reading from
		self.encode_path_dir=os.path.join("./source_data/",self.source+"/enc/")	#path to where we're storing the encoded files
		self.key_path_dir=os.path.join("./source_data/",self.source+"/keys/")	#path to where we're storing the keys
		
		self.encoder_dict={}	#the cypher is used to encode a message{real:fake}
		self.decoder_dict={}	#the cypher is used to decode a message{fake:real}
		self.key=""
		
	def encode(self):
		'''
			encodes the message with the encoder dict
		'''
	
		#open the files to be encoded and where the encoded text will be stored
		encode_dest=open(os.path.join(self.encode_path_dir,self.name+"_enc.txt"),"w+")	#where we're encoding to
		original=open(self.orig_path,"r")	#original file
		
		'''
		for each letter in the original, 
		write the encoded version to the encoded text
		'''
		orig=original.read()
		for thing in orig:
			if thing.lower() in self.encoder_dict:
				encode_dest.write(self.encoder_dict[thing.lower()])
			else:
				encode_dest.write(thing)
		encode_dest.close()
		original.close()
		
		return ("File encoded at: ",self.name,"_encode")
	
	'''
	def decode(self):

		#print("Origin file: ",self.original)
		
		decode_dest=open(self.name+"_decoded","w")
		decode_orig=open(self.name+"_encoded","r")
		
		orig=decode_orig.read()
		for thing in orig:
			if thing.lower() in self.decoder_dict:
				decode_dest.write(self.decoder_dict[thing.lower()])
			else:
				decode_dest.write(thing)
			
		decode_dest.close()
		decode_orig.close()
		
		return ("File decoded at: ",self.name,"_encode")
	'''
	
	def create_cypher_pair(self):
		'''
		creates a new cypher pair for encdoing/deconding
		stores in a file
		'''
		decoder_path=os.path.join(self.key_path_dir,self.name+"_key.txt")	#path to the decoder key file

		
		#two copies of the decoder 
		letters=[x for x in string.ascii_lowercase]	#used for popping off letters
		letters_copy=[x for x in string.ascii_lowercase]	#used as a whole list for indexing
		
		self.decoder_dict={}	#dict ot store the deocder
		self.encoder_dict={}	#dict to store the encoder
		i=0
		
		'''
		while there are letters in our original letters string
		pick a random letter
		pop it off the letters list
		our decoder will {random letter:letters_copy[i]}
		our encoder will contain {letters_copy[i]:random letter}
		'''
		while(len(letters)>0):

			index=random.randrange(0,len(letters))
			letter=letters.pop(index)
			self.decoder_dict[letter]=letters_copy[i]
			self.encoder_dict[letters_copy[i]]=letter
			
			i=i+1
		
		'''
		write teh decoder key to the decoder file
		written in order of a_sub b_sub ... z_sub, where a_sub si the letter that was substituted for a during the encoding
		'''
		sorted_keys=sorted(self.decoder_dict)
		decoder=open(decoder_path,"w+")
		[decoder.write(self.decoder_dict[ind]) for ind in sorted_keys]
		decoder.close()
	

	def print_cyphers(self):

		print(self.encoder_dict)
		print(self.decoder_dict)
		

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
	
class CaptureClass:
	'''
	Capture class takes in a large text and cuts it up into a designated set of texts of specified length
	requires a target text file
	the number of blocks that need to be cuts
	the size of each block
	
	'''
	def __init__(self,target,blocks,size):
		self.target=target #this is the file that we'll be extracting data from
		self.blocks=blocks	#this is the number of blocks we'll be creating
		self.size=size		#this is the size of each block/number of words it will contain
		
	'''
	for each block
	captures the specified number of words from teh text file
	saves each file under folder /[source]/blocks/"[target]_blk_x.txt" where x is the block index
	'''
	def create_blocks(self):
		
		read_path=os.path.join("./source_data/"+self.target)	#path to file we're reading from
		write_path_dir=os.path.join("./source_data/"+self.target.split(".")[0]+"/blks/")	#path to file directory we're writing to
		source_file=open(read_path,"r") #file we're reading from
		
		'''
		for each block we will create a new file
		reset the word count and write the requested number of words to the file
		'''
		for i in range(0,self.blocks):
			dest_file=open(os.path.join(write_path_dir,self.target.split(".")[0]+"_blk_%d.txt"%i),'w+')	#where we will write our words
			word_count=0	#number of words written to dest_file
			
			'''
			read each line in the file, note we will have some instances where we cut a line off early due to word count, but it doesn't matter for this
			use space separation to extract each word from the line
			also strip the endliens
			'''
			while word_count<self.size:
				line=source_file.readline().rstrip("\n")	#read each line
				words=line.split(" ")	#the words in the line
				
				'''
				write each word to the file and increment
				'''
				for word in words:
					dest_file.write(word+" ")
					word_count+=1
			dest_file.close()
			
		
		
		

if __name__=="__main__":
	'''
	if we're just runnign we'll do our basic test loop
	this will create 5000 files, each of 100 words of 'war_of_the_worlds'
	it will then create a key and encoded version of each file
	it will then do frequency analysis on each encoded versin
	it will then write the frequency analysis and key to a csv where each row contains:
	[block_name, A%, B%, ..., Z%, [array of key in the form of a_sub, b_sub, ...z_sub] where a_sub is the value that you substitute to decode "a" from the encoded text
	'''
	source_name="war_of_worlds" #name of our source_file
	num_blocks=50	#number of blocks
	block_len=100 #number words in the block
	csv_path=os.path.join("./source_data/",source_name+"_eval.csv")	#our csv file
	letters=string.ascii_lowercase	#userd below
	
	#capture the data
	cap=CaptureClass(source_name+".txt",num_blocks,block_len)	#create our source
	cap.create_blocks()
	
	csv=open(csv_path,"w+")	#file we're going to write our data to
	csv.write("block,a_pct,b_pct,c_pct,d_pct,e_pct,f_pct,g_pct,h_pct,i_pct,j_pct,k_pct,l_pct,m_pct,n_pct,o_pct,p_pct,q_pct,r_pct,s_pct,t_pct,u_pct,v_pct,w_pct,x_pct,y_pct,z_pct,key\n")
	'''
	for eah block, create a cypher key and encoded file in the file tree as described above
	additioanlly, perform the evaluationand write the data and the key to a "source_file_eval.csv" as described above
	'''
	
	
	for i in range(0,num_blocks):
		block_id=source_name+"_blk_%d"%i	#easy reference for the name of the block text file
		cyph=CypherClass(source_name,block_id+".txt")	
		cyph.create_cypher_pair()
		cyph.encode()
		
		#evaluation
		eval=EvalClass(os.path.join(cyph.encode_path_dir,block_id+"_enc.txt"))
		eval.freq_analysis()
		#do the writing
		csv.write(block_id+",")
		
		[csv.write("%.3f,"%eval.letter_frequency[letter]) for letter in letters]
		[csv.write(cyph.decoder_dict[letter]) for letter in letters]
		csv.write("\n")
	csv.close()
	
	
	