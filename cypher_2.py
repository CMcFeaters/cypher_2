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


required file tree:
/source_data/	#where the source files are
//[whatever the file is]/ #container for all the subfolders created and teh output data
///blks/	#where all the blocks will be stored
///enc/		#where the encoded files are stored
///keys/	#where the keys are stored

This library is intended to create the data pool to be used by the machien learning script


'''


#python class that can perform basic cyphers

import string
import random
import os
import sys
from cypher import CypherClass
from capture import CaptureClass
from eval import EvalClass

def build_files(target):
	'''
	function builds the file tree to store everything
	/source_data/
	//target
	///blks/
	///keys/
	///0enc/
	'''
	base_path=os.path.join("./source_data/",target)	#our baseline path
	try:
		print(base_path)
		os.mkdir(base_path)	
	except FileExistsError:
		print("FUCK YOU")
	
	pth=["/blks","/keys","/enc"]
	for i in range (0,3):
		try:
			print("making dir: "+base_path+pth[i])
			os.mkdir(base_path+pth[i])
		except FileExistsError:
			print("File "+pth[i]+" exists")
	
	
	


if __name__=="__main__":
	'''
	if we're just runnign we'll do our basic test loop
	this will create 5000 files, each of 100 words of 'war_of_the_worlds'
	it will then create a key and encoded version of each file
	it will then do frequency analysis on each encoded versin
	it will then write the frequency analysis and key to a csv where each row contains:
	[block_name, A%, B%, ..., Z%, [array of key in the form of a_sub, b_sub, ...z_sub] where a_sub is the value that you substitute to decode "a" from the encoded text
	'''
	
	source_name="war_and_peace" #name of our source_file
	build_files(source_name)
	num_blocks=1000	#number of blocks
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
		cyph.create_cypher_pair_caesar()
		cyph.encode()
		
		#evaluation
		eval=EvalClass(os.path.join(cyph.encode_path_dir,block_id+"_enc.txt"))
		eval.freq_analysis()
		#do the writing
		csv.write(block_id+",")
		
		[csv.write("%.3f,"%eval.letter_frequency[letter]) for letter in letters]
		#[csv.write(cyph.decoder_dict[letter]) for letter in letters]
		csv.write(cyph.key)	#write teh key
		csv.write("\n")
	csv.close()
	
	
	