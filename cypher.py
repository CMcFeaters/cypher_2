#cypher_class
import os
import sys
import string
import random

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
		self.key=""	#stores teh key relative to the cypher
		
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
	
	def create_cypher_pair_substitution(self):
		'''
		creates a new cypher pair for substituion encdoing/deconding
		stores in a file,
		'''
		decoder_path=os.path.join(self.key_path_dir,self.name+"_key.txt")	#path to the decoder key file

		
		#two copies of the decoder 
		letters=[x for x in string.ascii_lowercase]	#used for popping off letters
		letters_copy=[x for x in string.ascii_lowercase]	#used as a whole list for indexing
		
		
		'''
		while there are letters in our original letters string
		pick a random letter
		pop it off the letters list
		our decoder will {random letter:letters_copy[i]}
		our encoder will contain {letters_copy[i]:random letter}
		'''
		i=0	#index variable
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
		'''
			i haven't figured out assigning valuves in a list comprehension so i'm going to leave the above as is
			and just run a lazy for loop to create the key
		'''
		for ind in sorted_keys:
			self.key+=self.decoder_dict[ind]
		decoder.close()
	
	def create_cypher_pair_caesar(self):
		'''
		creates a new cypher pair for caesar (rotation) encdoing/deconding
		stores in a file,
		'''
		decoder_path=os.path.join(self.key_path_dir,self.name+"_key.txt")	#path to the decoder key file
		
		
		#two copies of the decoder 
		#letters=[x for x in string.ascii_lowercase]	#used for popping off letters
		letters=string.ascii_lowercase	#letters used for popping
		rot=random.randrange(1,25)	#pick a random number to rotate our alphabet by (note, not 0 and not 26, which is 0)
		
		'''
			for each letter
			the encoding key =our rotated value +i mod 26
			the decode dict is the inverse, index by key and set to current letter 
		'''
		for i in range(0,26):
			self.encoder_dict[letters[i]]=letters[(rot+i)%26]
			self.decoder_dict[letters[(rot+i)%26]]=letters[i]
		
		'''
		write teh decoder key to the decoder file
		written in order of a_sub b_sub ... z_sub, where a_sub si the letter that was substituted for a during the encoding
		'''
		sorted_keys=sorted(self.decoder_dict)
		decoder=open(decoder_path,"w+")
		[decoder.write(self.decoder_dict[ind]) for ind in sorted_keys]
		decoder.write(",%s"%letters[rot])
		self.key=letters[rot]
		decoder.close()

	def print_cyphers(self):

		print(self.encoder_dict)
		print(self.decoder_dict)
