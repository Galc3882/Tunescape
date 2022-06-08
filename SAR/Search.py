import pickle
from fuzzywuzzy import process
import numpy as np
import FeatureSimilarity
import time


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


def findSimilarSongs(song, data, numOfSongs=1):
    """
    Finds the most similar songs to the song at the index.
    Returns the most similar songs using cosinw similarity.
    """
    # Cap the number of songs to be returned
    if numOfSongs > len(data):
        numOfSongs = len(data)-1

    # measure the time it takes to find the most similar songs
    starttime = time.time()
    i=0


    data.pop(song[0] + '\0' + song[1])
    
    # Calculate the cosine similarity between the song and all the songs in the database
    similarSongs = []
    for row in data.items():

        # every 500 songs, print the time it took to find the most similar songs
        if i % 500 == 0:
            pass
            #print("Songs processed: " + str(i) + "\t|\t " + str(int(i*100/len(data))) + "%\t|\t Time: {:.2f}".format(time.time() - starttime))
        i += 1

        # Add the song to the list of songs if cosine similarity is above numOfSongs lowest similarity and delete the lowest similarity
        cosSim = cosineSimilarity(song, row[1])
        if cosSim < 0.4:
            continue
        if len(similarSongs) < numOfSongs:
            similarSongs.append((row[0], cosSim))
        else:
            iMin = similarSongs.index(min(similarSongs, key=takeSecond))
            if cosSim > similarSongs[iMin][1]:
                similarSongs.append((row[0], cosSim))
                if len(similarSongs) > numOfSongs:
                    similarSongs.pop(iMin)

    print('That took {:.2f} seconds'.format(time.time() - starttime))

    return similarSongs


def cosineSimilarity(song1, song2):
    """
    Calculates the cosine similarity between two songs.
    Returns the similarity value.
    """
    
    if song1[4] != song2[4]:
        return 0

    # Vector of weights for each feature
    weights = np.array([0.02, 0.05, 1, 1, 0.65, 0.8, 0.5, 1, 0.4, 0.6, 0.3, 0.3, 0.3])

    # Calculate the dot product of the two songs
    similarities = np.array([0.0]*weights.size)
    j = 0
    for i in (1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
        if i == 3:
            similarity = FeatureSimilarity.methodDictionary[i](song1[i], song2[i], song1[i+1], song2[i+1])
        else:
            similarity = FeatureSimilarity.methodDictionary[i](song1[i], song2[i])
        if similarity is not None:
            if i == 9 and np.sum(similarities) < 3:
                return 0
            similarities[j] = similarity
        else:
            weights[i] = 0
        j+=1

    # Return dot product of weights and similarities
    return np.dot(weights, similarities)/np.sum(weights)

# take second element for sort
def takeSecond(elem):
    return elem[1]

def main(database, songKey):
    # Find most similar song using cosine similarity
    similarSongs = findSimilarSongs(database[songKey], database, 5)
    sortedSimilarSongs = sorted(similarSongs, key=takeSecond, reverse=True)
    print("Similar Songs: ")
    for i in range(len(sortedSimilarSongs)):
        print("Found Song: " + sortedSimilarSongs[i][0].split('\0')
            [0]+" by " + sortedSimilarSongs[i][0].split('\0')[1])
        print("Cosine Similarity: " + str(sortedSimilarSongs[i][1]))


if __name__ == '__main__':
    # Read from the pickle file
    with open('database.pickle', 'rb') as handle:
        database = pickle.load(handle)

    # Ask for the song title    
    songTitle = input("Enter the song title: ")
    # Find the song in the database
    songKey = fuzzyGetSongTitle(songTitle, database.keys(), threshold=10)
    if songKey is None:
        print("Song not found within the threshold")
    else:
        print("Found Song: " + songKey.split('\0')
              [0]+" by " + songKey.split('\0')[1])
    main(database, songKey)
