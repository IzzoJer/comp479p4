import math 
import json

#this computes the RSV so i just input the parameters
def RSV(term, N, df, tf, ld, lave, k1, b):
	if df == 0:
		return 0
	else:
		return (math.log(N/df))*( ( (k1+1) * tf) / ( k1 * ( (1-b) + b * (ld/lave) ) + tf )) 

#this function handles single word queries
def single(query):
	scores = []#here is where i will have docID and scores appended
	with open('invertedIndex.json', 'r') as f1:#access my index
		index = json.load(f1)
		with open('docLengths.json', 'r') as f2:#access my index for doc lengths
			docLengths = json.load(f2)
			if query not in index:
				return 0 #if query term not in dict then return 0
			else:
				docIDs = index[query] #list of doc IDs for the specific term
				k1 = 8 
				b = .5 
				lave = docLengths['Lave']#get the lave from my doclenth dict
				N = docLengths['N']#get N from doclength dict
				df = len(index[query])#df is just the lenth of the postings list
				for ids in docIDs:#for each posting then i compute RSV
					tf = ids[1]#term freq if taken dirrectly form my index (percomputed in the dict)
					ld = docLengths[str(ids[0])]#i get the legnth of hte document from doc length
					scores.append((ids[0],RSV(query, N, df, tf, ld, lave, k1, b)))#compute RSA for a term and append it in scores
				scores.sort(key= lambda x : x[1], reverse = True)#i sort my score in my list of (id,score)
				return scores

#here is where i compute the multi word query AND, takes in a string and returns a sorted list of id and scores
def multiAND(query):
	query = query.split()
	scores = []#here is where i will have docID and scores appended
	with open('invertedIndex.json', 'r') as f1:#access my index
		index = json.load(f1)
		with open('docLengths.json', 'r') as f2:#access my index for doc lengths
			docLengths = json.load(f2)
			for term in query: #if a query term is not in dict then return 0
				if term not in index:
					return 0

			docIDs = index[query[0]] # I use this as inital list to compare both
			newList = [] # I use this to put all the matches when comparing 

			for terms in query[1:]: #loop through each term to compare both postings list
				temp = index[terms]
				#this part checkes what docIDs are in each word in query and appends the docid list in docIDs
				for ele1 in range(len(docIDs)): #checking if doc id in both lists that are being compared if they are then append to newlist
					for ele2 in range(len(temp)):
						try:
							if docIDs[ele1][0] == temp[ele2][0]:#if the docID found in new terms list then i append to new list
								l = docIDs[ele1] + [temp[ele2][1]]#i append the term freq of the next term in this list
								newList.append(l)
						except:
							break
				docIDs = newList#newlist is the list of matches from the pervious searches so we know what to check for next terms
				newList = []#reset newList for next term
			#same as single term 
			k1 = 10
			b = .2
			lave = docLengths['Lave']
			N = docLengths['N']
			tot = 0 #tot is to sum the scores from RSA 
			for ids in docIDs:#for each ID in the id list
				for termID in range(len(query)):#
					df = len(index[query[termID]])#length of the postings list at that specific term
					tf = ids[termID+1]#i get the term freq for each term in order is appended above 
					ld = docLengths[str(ids[0])]#same is single term
					tot += RSV(query, N, df, tf, ld, lave, k1, b)#sum the RSA score for each term in the query
				scores.append((ids[0],tot))
				tot = 0
			scores.sort(key= lambda x : x[1], reverse = True)#sort the scores
			return scores
#here i compute the multiword OR taking in a string and outputing the docID list with score and word count
def multiOR(query):
	query = query.split()
	scores = {}#i tried to insert the scores in a dict to facilitate incluting the # of words that were found for that specif docID
	with open('invertedIndex.json', 'r') as f1:#same as above
		index = json.load(f1)
		with open('docLengths.json', 'r') as f2:#same as above
			docLengths = json.load(f2)
			#same as above
			k1 = 80
			b = .2
			lave = docLengths['Lave']
			N = docLengths['N']
			#for each term in the query i compute the RSA
			for term in query:
				if term in index:#here is just to check if the term is in the index
					docIDs = index[term]
					df = len(index[term])
					for ids in docIDs:#for every doc for that term i compute the RSA value and input in dict
						tf = ids[1]
						ld = docLengths[str(ids[0])]
						if ids[0] not in scores.keys():#is the doc id is not in my dict i compute RSA and append 1 withc rep the word count
							scores[ids[0]] = (RSV(query, N, df, tf, ld, lave, k1, b),1)
						else:#if the docID is already in my dict i sum the previous RSA with new and add 1 to the word count
							scores[ids[0]] = (scores[ids[0]][0]+RSV(query, N, df, tf, ld, lave, k1, b),scores[ids[0]][1]+1)
			scores = sorted(scores.items(), key = lambda x : (x[1][1],x[1][0]), reverse = True)#sort by score
			return scores


def multiORTFIDF(query):
	query = query.split()
	scores = {}#i tried to insert the scores in a dict to facilitate incluting the # of words that were found for that specif docID
	with open('invertedIndex.json', 'r') as f1:#same as above
		index = json.load(f1)
		with open('docLengths.json', 'r') as f2:#same as above
			docLengths = json.load(f2)
			#same as above
			k1 = 80
			b = .2
			lave = docLengths['Lave']
			N = docLengths['N']
			#for each term in the query i compute the tf/df
			for term in query:
				if term in index:#here is just to check if the term is in the index
					docIDs = index[term]
					df = len(index[term])
					for ids in docIDs:#for every doc for that term i compute the tf/df value and input in dict
						tf = ids[1]
						ld = docLengths[str(ids[0])]
						if ids[0] not in scores.keys():#is the doc id is not in my dict i compute tf/df and append 1 withc rep the word count
							scores[ids[0]] = ((tf/df),1)
						else:#if the docID is already in my dict i sum the previous tf/df with new and add 1 to the word count
							scores[ids[0]] = (scores[ids[0]][0]+(tf/df),scores[ids[0]][1]+1)
			scores = sorted(scores.items(), key = lambda x : (x[1][1],x[1][0]), reverse = True)#sort by score
			return scores



#i run this function once to create a file containing a dict of doc length and get N, Lave
#so i dont need to recompute it every time, its faster if i just get the data directly from the file 
def getLd():
	with open('tokens.json', 'r') as f:
		index = json.load(f)
		out = {}
		avg = 0
		#here the key of the dict is docID and the value is the words for that document
		for pair in index:
			if pair[1] in out:
				out[pair[1]] = out[pair[1]] + 1
			else:
				out[pair[1]] = 1
			avg += 1
		#here i get the avg of words per document by deviding the total words by the # of documents
		avg = avg / len(out)
		#here is just compute N which is # of docs and add it in my dict
		out['N'] = len(out.keys())
		#add the avg
		out['Lave'] = int(avg)
		with open('docLengths.json', 'w') as file:
			json.dump(out, file)

#i run this function once to create a file containing a dict term : doc freq
def getDF():
	with open('invertedIndex.json', 'r') as f: #uses inverted index to compute len
		invertedIndex = json.load(f)
		indexDict = {}
		for x in invertedIndex.keys():
			indexDict[x] = len(invertedIndex[x])

		with open('indexDict.json', 'w') as f1: #outputs the dict in file
			json.dump(indexDict, f1)

