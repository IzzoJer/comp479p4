# Jeremie Izzo - 40016103

from spimi import blockCreator, blockMerger, tokenizer
from searchEngine import single, multiAND, multiOR, getLd, getDF, multiORTFIDF
import json
import os


# uncomment to create file of tuples using my scraped output file

# with open('concordia/scraper.json', 'r') as f:
#     data = json.load(f)
#     tokenizer(data)

#uncomment to recreates blocks (SPIMI)

# blockCreator('tokens.json', 500)

#uncomment to merges blocks (create inverted index)

# blockMerger()
# getLd() #creates doc length dict (used for my ranking)(docLengths.json)
# getDF() #created a file containing a dict of term and document frequency (assignemtn requirement) (indexDict.json)


# this function takes in a list of results and prints the top results depending the format of the input
def displayTopResults(results):
    out = []
    if results == 0 or results == []:  # if the list is empty then print no results
        print('No Results Found')
    else:
        mapping = {}
        with open('mapping.json', 'r') as f:
            mapping = json.load(f)
        counter = 0
        for x in results:
            counter += 1
            if counter > 15:
                break
            out.append(f'URL: {mapping[str(x[0])]} Score: {x[1][0]}')
        return out

#these are my queries for my information gain

infoNeed1 = 'which researchers at Concordia worked on COVID 19-related research'
q1 = 'covid-19 pandemic research'
q2 = 'researchers help in covid-19'
infoNeed2 = 'which departments at Concordia have research in environmental issues, sustainability, energy and water conservation?'
q3 = 'department studies environmental issues'
q4 = 'awarded research department sustainability'

#running my ranking algo's and ouputing all results in file

# with open('results.txt', 'a') as f:
#     f.write(f'{infoNeed1}\n\n')
#
#     f.write(f'Query1 BM25: {q1}\n')
#     for x in displayTopResults(multiOR(q1)):
#         f.write(f'{x}\n')
#
#     f.write(f'\nQuery1 tf/idf: {q1}\n')
#     for x in displayTopResults(multiORTFIDF(q1)):
#         f.write(f'{x}\n')
#
#     f.write(f'{infoNeed1}\n\n')
#
#     f.write(f'Query2 BM25: {q2}\n')
#     for x in displayTopResults(multiOR(q1)):
#         f.write(f'{x}\n')
#
#     f.write(f'\nQuery2 tf/idf: {q2}\n')
#     for x in displayTopResults(multiORTFIDF(q1)):
#         f.write(f'{x}\n')
#
#     f.write(f'\n\n{infoNeed2}\n\n')
#
#     f.write(f'Query1 BM25: {q3}\n')
#     for x in displayTopResults(multiOR(q3)):
#         f.write(f'{x}\n')
#
#     f.write(f'\nQuery1 tf/idf: {q3}\n')
#     for x in displayTopResults(multiORTFIDF(q3)):
#         f.write(f'{x}\n')
#
#     f.write(f'{infoNeed1}\n\n')
#
#     f.write(f'Query2 BM25: {q4}\n')
#     for x in displayTopResults(multiOR(q4)):
#         f.write(f'{x}\n')
#
#     f.write(f'\nQuery2 tf/idf: {q4}\n')
#     for x in displayTopResults(multiORTFIDF(q4)):
#         f.write(f'{x}\n')
#




