from cmath import sqrt
import csv
import os
from xml.etree.ElementInclude import include
from fuzzywuzzy import fuzz
import numpy as np
import FeatureSimilarity



def fuzzySearchSongTitle(songTitle, data, threshold=60):
    """
    Searches for a song title in the database.
    Returns the analysis of the song matching the most above a certian threshold.
    Threshold is from 0 to 100.
    """
    maxRatio = [0, 0]

    for row in range(len(data)):
        ratio = fuzz.ratio(songTitle, data[row][0])  # 50 is the song title
        if ratio > threshold and ratio > maxRatio[0]:
            maxRatio[0] = ratio
            maxRatio[1] = row
    if maxRatio[0] == 0:
        return None
    print("Ratio of Fuzzy Search: " + str(maxRatio[0])) # print the ratio of the song
    return data[maxRatio[1]]

def findSimilarSongs(song, numOfSongs, data):
    """
    Finds the most similar songs to the song at the index.
    Returns the most similar songs using cosinw similarity.
    """
    # Cap the number of songs to be returned
    if numOfSongs > len(data):
        numOfSongs = len(data)-1
    # Calculate the cosine similarity between the song and all the songs in the database
    Songs = [[], []]
    for row in range(len(data)):
        if data[row][0] != song[0]:
            Songs[0].append(data[row])
            Songs[1].append(cosineSimilarity(song, data[row]))
    
    # pick numOfSongs most similar songs
    similarSongs = []
    for i in range(numOfSongs):
        maxIndex = Songs[1].index(max(Songs[1]))
        similarSongs.append([Songs[0][maxIndex], Songs[1][maxIndex]])
        Songs[1][maxIndex] = 0
    return similarSongs

def cosineSimilarity(song1, song2):
    """
    Calculates the cosine similarity between two songs.
    Returns the similarity value.
    """
    # Vector of weights for each feature
    weights = [1.3, 1] # [1 for i in range(len(song1)-1)]

    # Calculate the dot product of the two songs
    similarities = []
    for i in range(1, len(song1)):
        similarities.append(FeatureSimilarity.methodDictionary[i](song1[i], song2[i]))
    # Return dot product of weights and similarities
    return np.dot(weights, similarities)/sum(weights)

if __name__ == '__main__':
    # Read in the csv file
    with open(os.getcwd()+'\\'+'database.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    # remove the header
    data.pop(0)
    # remove empty rows
    data = [row for row in data if row != [] and row != ['']]

    # Ask for the song title
    songTitle = input("Enter the song title: ")
    songAnalysis = fuzzySearchSongTitle(songTitle, data, threshold=10)
    if (songAnalysis == None):
        print("Song not found within the threshold")
    else:
        print("Found Song: " + songAnalysis[0]) # b'Amor De Cabaret'

    # Find most similar song using cosine similarity
    similarSongs = findSimilarSongs(songAnalysis, 5, data)
    print("Similar Songs: ")
    for i in range(len(similarSongs)):
        print(similarSongs[i][0][0])
        print("Cosine Similarity: " + str(similarSongs[i][1]))
