import os
import sys

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
			
		
		
		
