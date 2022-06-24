import gc
import pickle
import Search
import debug
import os
import datetime
import time


def main1():
    starttime = time.time()

    # Ask for the song title
    songTitle = input("Enter the song title: ")

    # Find the song in the database
    songKey = Search.fuzzyGetSongTitle(songTitle, os.path.abspath(os.getcwd()) + r'\tmp\namelist.pickle', 40)

    if len(songKey) > 1:
        print("Multiple songs found:")
        for j in range(len(songKey)):
            print(str(j+1)+". "+songKey[j][0].split('\0')
                  [0]+" by " + songKey[j][0].split('\0')[1])
        k = input("Please enter the number of the song you want to use: ")
        songKey = songKey[int(k)-1][0]
    else:
        songKey = songKey[0][0]
    print("Found Song: " + songKey.split('\0')
          [0]+" by " + songKey.split('\0')[1])

    root = os.path.abspath(os.getcwd()) + r'\tmp'
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if not name.startswith("namelist"):
                pathList.append(os.path.join(path, name))

    songValue = None
    # Find song value in the database
    for path in pathList:
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
            handle.close()
            if songKey in data.keys():
                songValue = data[songKey]
                break
        del data
        gc.collect()
    if len(pathList) > 0:
        del data
        gc.collect()
    if songValue == None:
        pass  # ! Error: Song not found
    
    print('That took ' + str(datetime.timedelta(seconds=time.time() - starttime)))


    # Find most similar song using cosine similarity
    numOfSongs = 5
    similarSongs = Search.multiProcessing(
        Search.findSimilarSongs, 32, songValue, pathList, numOfSongs)

    # Sort the list by the similarity score
    sortedSimilarSongs = sorted(
        similarSongs, key=Search.takeSecond, reverse=True)
    if len(sortedSimilarSongs) > numOfSongs:
        sortedSimilarSongs = sortedSimilarSongs[:numOfSongs]

    print("Similar Songs: ")
    for i in range(len(sortedSimilarSongs)):
        print("Found Song: " + sortedSimilarSongs[i][0].split('\0')
              [0]+" by " + sortedSimilarSongs[i][0].split('\0')[1])
        print("Cosine Similarity: " + str(sortedSimilarSongs[i][1]))
    print('That took ' + str(datetime.timedelta(seconds=time.time() - starttime)))


def main2():
    # Read from the pickle file

    songKey1 = "Sympathy\0Thomas Battenstein"
    songKey2 = "Levallois Monte Carlo\0Georges Parys"

    root = os.path.abspath(os.getcwd()) + r'\tmp'
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if not name.startswith("namelist"):
                pathList.append(os.path.join(path, name))

    songValue1 = None
    songValue2 = None
    i = 0
    # Find song value in the database
    for path in pathList:
        with open(path, 'rb') as handle:
            data = pickle.load(handle)
            handle.close()
            if songKey1 in data.keys():
                songValue1 = data[songKey1]
                i+=1
            if songKey2 in data.keys():
                songValue2 = data[songKey2]
                i+=1
            if i == 2:
                break
        del data
        gc.collect()
    if len(pathList) > 0:
        del data
        gc.collect()

    debug.compareSongs(songValue1, songValue2)


if __name__ == '__main__':
    main1()

    # # Read from the pickle file
    # with open('database.pickle', 'rb') as handle:
    #     database = pickle.load(handle)
    #     handle.close()

    # m = ("", 0)
    # ml = ("", 0)
    # j = 0
    # for i in database.keys():
    #     if j % 100 == 0 and j != 0:
    #         print(j)
    #         print("Global: " + str(m))
    #         print("Local: " + str(ml))
    #         ml = ("", 0)
    #     try:
    #         a = Search.findSimilarSongs(database[i], database, 1)[0]
    #     except:
    #         print("Error: " + i)
    #         continue
    #     if a[1] > m[1]:
    #         m = a
    #     if a[1] > ml[1]:
    #         ml = a
    #     j += 1
