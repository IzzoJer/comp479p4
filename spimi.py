import json
import os
import re
import nltk

fileFolder = 'Blocks/'
folder = os.listdir(fileFolder)

#takes in the coutput file from the web scraper and create a file of mappings from URL to docID
#and creates a file containting docID term pairs
def tokenizer(data):
	final = []#docId term pairs list
	mapping = {}#where the mapping from docID to url will append
	stopwords = []
	with open('stopwords/english', 'r') as f: #stopwords used for normalizing
			stopwords = f.read()

	for x in range(len(data)):
		mapping[x] = list(data[x].keys())[0] #create new dict entry for URL and docID
		tokens = nltk.word_tokenize(data[x][list(data[x].keys())[0]]) #tokenizing the text
		for token in tokens: #looping though tokens for hte specific text
			if re.match(r'\w+', token) is not None:
				token = token.lower() #compress
				if token not in stopwords and not token.isdigit(): #compress
					#normalizing covid-19
					if 'covid' in token or 'COVID' in token or 'Covid' in token or 'COVID-19' in token:
						token = 'covid-19'
					final.append((token,x))

	with open('tokens.json', 'w') as f:
		json.dump(final, f)
	with open('mapping.json', 'w') as f:
		json.dump(mapping,f)


#this function takes in a json file containing pairs of term and docID with a block size and creates blocks of dictionaries of SIZE
def blockCreator(pairs, size):

	block = {}#data for dict per block
	blockNum = 0
	counter = 0

	#simple function that inserts the tuples in the dictionary
	#I also included a parameter that will save the term freq per doc so i can keep track of TFd for quick retreival ****
	def addToDict(pair):
		if not block or pair[0] not in block.keys():#if dict doesnt have the value then add the key with a tuple for docID and a freq of 1
			block[pair[0]] = [(pair[1],int(1))]
		else:
			#here i check if the docID is already in the id list if not i append new doc with freq of 1
			if pair[1] not in map(lambda x : x[0], block[pair[0]]):
				block[pair[0]].append((pair[1],1))
			else:
				#if the docID is found then i increase the TF by one for that specific docID
				freq = block[pair[0]][0][1] + 1
				for x in range(len(block[pair[0]])):
					if block[pair[0]][x][0] == pair[1]:
						block[pair[0]][x] = (pair[1], freq)

	with open(pairs, 'r') as f:
		pairs = json.load(f)
		for p in pairs:
			addToDict(p)#using function above to add tuples
			if counter < size:
				counter += 1#this counts for the size of the blocks
			else:
				with open(f'{fileFolder}Block{blockNum}', 'w') as f:#if block size reaches limit then i create the block
					json.dump({key:block[key] for key in sorted(block.keys())},f)
				block = {}#reset parameters
				blockNum += 1
				counter = 0
		if block:#this is just to dump the remaining final elements once the pairs file end
			with open(f'{fileFolder}Block{blockNum}', 'w') as f:
				json.dump({key:block[key] for key in sorted(block.keys())},f)


#this function takes takes the blocks that were created and merges them together
def blockMerger():
	finalIndex = {}
	folder.sort(key=(lambda x: int(x[5:])))#i need to sort the file names because if not they dont parse in order

	for block in folder:
		with open(fileFolder+block, 'r') as f:
			block = json.load(f)

			#same function is above, to insert in dict but this also had to merge elements if the docID is in the other block also for a specific term
			for x in block:
				if x not in finalIndex:
					finalIndex[x] = block[x]#if the key in not in dict then we add it
				else:
					#this checks if the first docID is already in the final dict, if it is then i add both TF and append the rest
					if finalIndex[x][-1][0] == block[x][0][0]:
						summ = finalIndex[x][-1][1] + block[x][0][1]
						finalIndex[x][-1] = [finalIndex[x][-1][0], summ]
						finalIndex[x] = finalIndex[x] + block[x][1:]
					else:#if not then just append
						finalIndex[x] = finalIndex[x] + block[x]

	for x in finalIndex.keys():
		finalIndex[x].sort(key= lambda y: y[1], reverse=True)

	with open('invertedIndex.json', 'w') as f:
		json.dump(finalIndex, f)
	#i return the length of the dict to then display the amount of keys for comparison with naiveindexer
	return len(finalIndex.keys())

