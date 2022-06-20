import cProfile
import Search
import FeatureSimilarity
import pickle
from fuzzywuzzy import process
import pstats
from pstats import SortKey
from matplotlib import pyplot as plt
import numpy as np

def fuzzyGetSongTitle(songTitle, data, threshold=60):
    """
    Searches for a song title in the database.
    Returns the analysis of the song matching the most above a certian threshold.
    Threshold is from 0 to 100.
    """

    ratio = process.extract(songTitle.lower(), list(data), limit=1)
    if ratio[0][1] > threshold:
        print("Similarity: " + str(ratio[0][1]))
        return ratio[0][0]
    else:
        return None

def preformanceTest():
    # Read from the pickle file
    with open('database.pickle', 'rb') as handle:
        database = pickle.load(handle)

    # Ask for the song title    
    songTitle = "firework" #input("Enter the song title: ")
    # Find the song in the database
    songKey = fuzzyGetSongTitle(songTitle, database.keys(), threshold=10)
    if songKey is None:
        print("Song not found within the threshold")
    else:
        print("Found Song: " + songKey.split('\0')
                [0]+" by " + songKey.split('\0')[1])
    cProfile.run('Search.main(database, songKey)', sort='tottime', filename='profile.txt')
    p = pstats.Stats('profile.txt')
    p.sort_stats(SortKey.TIME, SortKey.CUMULATIVE).print_stats(100)

def printValues(values):
    '''
    Prints the values of the song from the database.
    '''
    print('Song: ' + values[0])
    print('Band: ' + values[1])
    print('Duration: ' + str(values[2]))
    print('Key: ' + str(values[3]))
    print('Mode: ' + str(values[4]))
    print('Speed: ' + str(values[5]))
    print('Loudness: ' + str(values[6]))
    print('Time signature: ' + str(values[7]))
    print('Year: ' + str(values[8]))
    print()

def compareValues(values1, values2):
    '''
    Prints the results of FeatureSimilarity.
    '''
    print("Same artist: " + str(FeatureSimilarity.methodDictionary[1](values1[1], values2[1])))
    print("Duration similarity: " + str(FeatureSimilarity.methodDictionary[2](values1[2], values2[2])))
    print("Key similarity: " + str(FeatureSimilarity.methodDictionary[3](values1[3], values2[3], values1[4], values2[4])))
    print("Speed similarity: " + str(FeatureSimilarity.methodDictionary[5](values1[5], values2[5], values1[7], values2[7])))
    print("Loudness similarity: " + str(FeatureSimilarity.methodDictionary[6](values1[6], values2[6])))
    print("Year similarity: " + str(FeatureSimilarity.methodDictionary[8](values1[8], values2[8])))
    print("Sections start similarity: " + str(FeatureSimilarity.methodDictionary[9](values1[9], values2[9])))
    print("Segments pitches similarity: " + str(FeatureSimilarity.methodDictionary[10](values1[10], values2[10])))
    print("Segments timbre similarity: " + str(FeatureSimilarity.methodDictionary[11](values1[11], values2[11])))
    print("Bars start similarity: " + str(FeatureSimilarity.methodDictionary[12](values1[12], values2[12])))
    print("Beats start similarity: " + str(FeatureSimilarity.methodDictionary[13](values1[13], values2[13])))
    print("Tatums start similarity: " + str(FeatureSimilarity.methodDictionary[14](values1[14], values2[14])))
    print()
    print("Overall similarity: " + str(Search.cosineSimilarity(values1, values2)))
    print()



def compareSongs(values1, values2):
    '''
    Compares the values of two songs in the database.
    '''

    plt.figure()

    #subplot(r,c) provide the no. of rows and columns
    f, axarr = plt.subplots(1, 4) 

    # normalize 2d array to 0-1
    a = (np.array(values1[10])-np.ones((len(values1[10]), len(values1[10][0])))*np.min(values1[10])) / (np.max(values1[10])-np.min(values1[10]))
    axarr[0].imshow(np.array([[(j, 0, 0) for j in i] for i in a]), interpolation='nearest')
    
    a = (np.array(values1[11])-np.ones((len(values1[11]), len(values1[11][0])))*np.min(values1[11])) / (np.max(values1[11])-np.min(values1[11]))
    axarr[1].imshow(np.array([[(j, 0, 0) for j in i] for i in a]), interpolation='nearest')

    a = (np.array(values2[10])-np.ones((len(values2[10]), len(values2[10][0])))*np.min(values2[10])) / (np.max(values2[10])-np.min(values2[10]))
    axarr[2].imshow(np.array([[(j, 0, 0) for j in i] for i in a]), interpolation='nearest')

    a = (np.array(values2[11])-np.ones((len(values2[11]), len(values2[11][0])))*np.min(values2[11])) / (np.max(values2[11])-np.min(values2[11]))
    axarr[3].imshow(np.array([[(j, 0, 0) for j in i] for i in a]), interpolation='nearest')

    axarr[0].title.set_text('Pitches 1')
    axarr[1].title.set_text('Timbre 1')
    axarr[2].title.set_text('Pitches 2')
    axarr[3].title.set_text('Timbre 2')

    printValues(values1)
    printValues(values2)

    compareValues(values1, values2)
    
    plt.show()