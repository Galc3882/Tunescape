import gc
from fuzzywuzzy import process
import numpy as np
import FeatureSimilarity
import pickle
import multiprocessing as mp
import queue


def fuzzyGetSongTitle(songTitle, path, threshold=60):
    """
    Searches for a song title in the database.
    Returns the analysis of the song matching the most above a certian threshold.
    Threshold is from 0 to 100.
    """

    with open(path, 'rb') as handle:
            data = pickle.load(handle)
            handle.close()
    ratio = process.extract(songTitle.lower(), data, limit=10)

    # Clean Ram from the data
    del data
    gc.collect()

    i = 0
    while i < len(ratio):
        if ratio[i][1] < threshold:
            ratio.pop(i)
        else:
            i += 1
    if len(ratio) == 0:
        return None
    else:
        return ratio


def findSimilarSongs(song, paths, numOfSongs=1, q=None):
    """
    Finds the most similar songs to the song at the index.
    Returns the most similar songs using cosine similarity.
    """

    for path in paths:
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
            handle.close()

        # Cap the number of songs to be returned
        if numOfSongs > len(data):
            numOfSongs = len(data)-1

        # Calculate the cosine similarity between the song and all the songs in the database
        similarSongs = []
        for row in data.items():
            if row[0] != song[0] + '\0' + song[1]:
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
        
        del data
        gc.collect()

        q.put(similarSongs)


def cosineSimilarity(song1, song2):
    """
    Calculates the cosine similarity between two songs.
    Returns the similarity value.
    """

    # return 0 if time signature is different
    if song1[7] != song2[7]:
        return 0

    # Vector of weights for each feature
    weights = np.array([0.02, 0.05, 1, 1, 0.65, 0.5,
                       0.8, 0.2, 0.65, 0.15, 0.15, 0.15])

    # Calculate the dot product of the two songs
    similarities = np.array([0.0]*weights.size)
    j = 0
    for i in (1, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 14):
        if i == 3:
            similarity = FeatureSimilarity.methodDictionary[i](
                song1[i], song2[i], song1[i+1], song2[i+1])
            if similarity < 0.5:
                return 0
        elif i == 5:
            similarity = FeatureSimilarity.methodDictionary[i](
                song1[i], song2[i], song1[i+2], song2[i+2])
            if similarity < 0.5:
                return 0
        # elif i == 9 or i == 10 or i == 11:
        #     similarity = FeatureSimilarity.methodDictionary[i](
        #         song1[i], song2[i])
        #     if similarity < 0.3:
        #         return 0
        else:
            similarity = FeatureSimilarity.methodDictionary[i](
                song1[i], song2[i])
        if similarity is not None:
            if i == 9 and np.sum(similarities) < 3:
                return 0
            similarities[j] = similarity
        else:
            weights[j] = 0
        j += 1

    # Return dot product of weights and similarities
    return np.dot(weights, similarities)/np.sum(weights)

def multiProcessing(func, batch, song, pathList, n): 
    """
    Multi-processing function.
    """

    if len(pathList) > batch:
        # Split the pathList into list of batch sized lists
        pathList = np.array_split(pathList, 4)
    else:
        pathList = [pathList]
        


    songList = []
    i = 0
    resultQueue = mp.Queue()

    while i < len(pathList):
        j = 0
        while j < batch:
            if i == len(pathList):
                break

            processes = []
            p = mp.Process(target=func, args=(song, pathList[i], n, resultQueue))
            processes.append(p)
            p.start()
            i += 1
            j += 1

        while True:
            try:
                result = resultQueue.get(False, 0.01)
                songList += result
            except queue.Empty:
                pass
            allExited = True
            for t in processes:
                if t.exitcode is None:
                    allExited = False
                    break
            if allExited & resultQueue.empty():
                break
    
    return songList



def takeSecond(elem):
    '''
    Take second element for sort
    '''
    return elem[1]

