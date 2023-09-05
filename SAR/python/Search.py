import gc
from fuzzywuzzy import process
import numpy as np
import FeatureSimilarity
import pickle
import multiprocessing as mp
import queue
import Search
from sklearn.cluster import KMeans
import cv2



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


def findSimilarSongs(song, paths, numOfSongs=1, excludeSongs=[], q=None):
    """
    Finds the most similar songs to the song at the index.
    Returns the most similar songs using cosine similarity.
    """
    # for every 5 paths instead of 1
    batch = 5
    if len(paths) > batch:
        # Split the pathList into list of batch sized lists
        paths = np.array_split(paths, int(len(paths)/batch))
    else:
        paths = [paths]
    
    for path in paths:
        data = {}
        for p in path:
            with open(p, 'rb') as handle:
                data.update(pickle.load(handle))
                handle.close()

        for key in excludeSongs:
            if key in data:
                data.pop(key)
                # excludeSongs.remove(key)

        # Cap the number of songs to be returned
        if numOfSongs > len(data):
            numOfSongs = len(data)-1

        # Calculate the cosine similarity between the song and all the songs in the database
        similarSongs = []
        for row in data.items():
            # Add the song to the list of songs if cosine similarity is above numOfSongs lowest similarity and delete the lowest similarity
            cosSim = cosineSimilarity(song, row[1])
            # print(cosSim)
            # if cosSim < 0.4:
            #     continue
            if len(similarSongs) < numOfSongs:
                similarSongs.append((row[0], cosSim))
            else:
                smin = min(similarSongs, key=takeSecond)
                if smin[1] > 0.8 and len(similarSongs) < numOfSongs:
                    break
                iMin = similarSongs.index(smin)
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
    weights = np.array([0.05, 1, 1, 0.65, 0.5,
                       0.85, 0.4, 0.65, 0.15, 0.15, 0.15])

    # Calculate the dot product of the two songs
    similarities = np.array([0.0]*weights.size)
    j = 0
    for i in (2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 14):
        if i == 3:
            similarity = FeatureSimilarity.methodDictionary[i](
                song1[i], song2[i], song1[i+1], song2[i+1])
            if similarity < 0.68:
                return 0
        elif i == 5:
            similarity = FeatureSimilarity.methodDictionary[i](
                song1[i], song2[i], song1[i+2], song2[i+2])
            if similarity < 0.5:
                return 0
        else:
            similarity = FeatureSimilarity.methodDictionary[i](
                song1[i], song2[i])
        if similarity is not None:
            if similarity < 0.05:
                return 0
            if i == 9 and np.sum(similarities) < 3:
                return 0
            similarities[j] = similarity
        else:
            weights[j] = 0
        j += 1
    
    # if 0 not in similarities:
    #     print(similarities)

    # Return dot product of weights and similarities
    return np.dot(weights, similarities)/np.sum(weights)

def multiProcessing(func, batch, song, excludeSongs, pathList, n): 
    """
    Multi-processing function.
    """
    # randomise the order of the paths
    np.random.shuffle(pathList)

    pathList = pathList[:6]

    if len(pathList) > batch:
        # Split the pathList into list of batch sized lists
        pathList = np.array_split(pathList, batch)
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
            p = mp.Process(target=func, args=(song, pathList[i], n, excludeSongs, resultQueue))
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

def reduceSongs(songList, pathList, numOfSongs):
    """
    Uses k means clustering to reduce the number of songs.
    Returns the reduced list of songs with their values.
    """
    excludeSongs = []
    for song in songList:
        excludeSongs.append(song[0]+'\0'+song[1])

    kmeansList = []
    for i in range(len(songList)):
        kmeansList.append(np.array(songList[i][2:9]))
    kmeansList = kmeansList
    
    weights = [1/1000, 0.5, 1, 1/500, 1/10,
                          0.5, 1/5000]

    for i in range(len(kmeansList)):
        kmeansList[i] = np.array([a * b for a, b in zip(kmeansList[i], weights)])


    # Use k means clustering to reduce the number of songs
    kmeans = KMeans(n_clusters=min(int(len(songList)/5)+1, 4), max_iter=10000, n_init = 20).fit(kmeansList)
    centroids = kmeans.cluster_centers_

    for i in range(len(centroids)):
        centroids[i] = np.array([a / b for a, b in zip(centroids[i], weights)])
    
    reducedSongList = []
    for i in range(int(len(songList)/7)+1):
        k=[]
        reducedSongList.append(['','']+list(centroids[i]))
        for l in range(len(reducedSongList[i])):
            if l in (3,4,7,8):
                reducedSongList[i][l]=int(reducedSongList[i][l]+0.5)
        for j in range(len(kmeans.labels_)):
            if kmeans.labels_[j] == i:
                k.append(songList[j][9:])
        
        reducedSongList[i]+= avarageArray(k)

    similarSongs = []
    for song in reducedSongList:
        similarSongs += (multiProcessing(Search.findSimilarSongs, 8, song, excludeSongs, pathList, numOfSongs))

    # remove duplicates
    similarSongs = list(dict.fromkeys(similarSongs))

    # Sort the list by the similarity score
    sortedSimilarSongs = sorted(
        similarSongs, key=Search.takeSecond, reverse=True)

    return sortedSimilarSongs

def avarageArray(arrays):
    """
    calculates the average of array as the combinaton of multipul arrays with different lengths
    """
    arr = [0]*len(arrays)
    a = []
    for i in range(len(arrays[0])):
        minSize = 65
        for j in range(len(arrays)):
            if minSize > arrays[j][i].shape[0]:
                minSize = arrays[j][i].shape[0]
        for j in range(len(arrays)):
            if len(arrays[j][i].shape)==2:
                arr[j] = cv2.resize(arrays[j][i], dsize=(12, minSize), interpolation=cv2.INTER_NEAREST)
            else:
                arr[j]=np.array([l.item() for l in cv2.resize(arrays[j][i], dsize=(1, minSize), interpolation=cv2.INTER_NEAREST)])

        a.append(np.average(arr, axis=0))

    return a

def takeSecond(elem):
    '''
    Take second element for sort
    '''
    return elem[1]

