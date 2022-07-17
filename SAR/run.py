import gc
import pickle
import Search
import debug
import os
import datetime
import time
import Spotify_Search_v4


def main1():
    starttime = time.time()
    # sp = Spotify_Search_v4.authentiated_spotipy()

    # # Ask for the song title
    # songTitle = input("Enter the song title: ")

    # # Find the song in spotify
    # songKey = Spotify_Search_v4.search(songTitle, sp)

    # if len(songKey) > 1:
    #     print("Multiple songs found:")
    #     for j in range(len(songKey)):
    #         print(str(j+1)+". "+songKey[j][0]+" by " + songKey[j][1])
    #     k = input("Please enter the number of the song you want to use: ")
    songKey = ['Darts'+'\0'+'System Of A Down'+'\0'+'7vg47qMIEdLfNdTE3WLf0T'] #songKey[int(k)-1][0]+"\0"+songKey[int(k)-1][1]
    # else:
    #     print(str(j+1)+". "+songKey[0][0]+" by " + songKey[0][1])
    # get everything after last \0

    root = r"C:\Users\dkdkm\Documents\GitHub\database"
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            pathList.append(os.path.join(path, name))
    
    sp = Spotify_Search_v4.authentiated_spotipy()
    songValues = [[key.split("\0")[0]]+[key.split("\0")[1]]+Spotify_Search_v4.get_features(key.split("\0")[2], sp) for key in songKey]
    

    if songValues == []:
        print("No songs found in the database")
        return
    
    print('That took ' + str(datetime.timedelta(seconds=time.time() - starttime)))

    numOfSongs = 5
    similarSongs = Search.reduceSongs(songValues, pathList, numOfSongs)
    similarSongs = similarSongs[:20]
    
    print("Similar Songs: ")
    for i in range(len(similarSongs)):
        print("Found Song: " + similarSongs[i][0].split('\0')
              [0]+" by " + similarSongs[i][0].split('\0')[1])
        print("Cosine Similarity: " + str(similarSongs[i][1]))
    print('That took ' + str(datetime.timedelta(seconds=time.time() - starttime)))


def main2():
    # Read from the pickle file

    songKey1 = "Love On A Mountain Top\x00Sinitta"
    songKey2 = "Reso Rafter\x00Jark Prongo"

    root = r"C:\Users\dkdkm\Documents\GitHub\database"
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
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
                del data
                gc.collect()
                break
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
