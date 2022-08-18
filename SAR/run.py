import gc
import pickle
import Search
import debug
import os
import datetime
import time
import Spotify_Search_v4

def getKey(sp):
    # Ask for the song title
    songTitle = input("Enter the song title: ")

    # Find the song in spotify
    songKey = Spotify_Search_v4.search(songTitle, sp)

    if len(songKey) > 1:
        print("Multiple songs found:")
        for j in range(len(songKey)):
            print(str(j+1)+". "+songKey[j][0]+" by " + songKey[j][1])
        k = input("Please enter the number of the song you want to use: ")
        print("'" + songKey[int(k)-1][0] + "'+'" + r"\0" + "'+'" + songKey[int(k)-1][1] + "'+'" + r"\0" + "'+'" + songKey[int(k)-1][8] + "'")
    else:
        print(songKey[0][0]+"\0"+songKey[0][1]+"\0"+songKey[0][8])

def search(sp, songKey, databasePath):
    starttime = time.time()

    pathList = []
    for path, subdirs, files in os.walk(databasePath):
        for name in files:
            pathList.append(os.path.join(path, name))
    
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


def compareTwoSongs(sp, song1, song2, databasePath):
    # Read from the pickle file

    values = []
    for key, inSpotify in (song1, song2):
        if inSpotify:
            values.append([key.split("\0")[0]]+[key.split("\0")[1]]+Spotify_Search_v4.get_features(key.split("\0")[2], sp))
        else:
            pathList = []
            for path, subdirs, files in os.walk(databasePath):
                for name in files:
                    pathList.append(os.path.join(path, name))

            # Find song value in the database
            for path in pathList:
                with open(path, 'rb') as handle:
                    data = pickle.load(handle)
                    handle.close()
                    if key in data.keys():
                        values.append(data[key])
                        break
                    del data
                    gc.collect()
                        
                del data
                gc.collect()

    

    debug.compareSongs(values[0], values[1])


if __name__ == '__main__':
    sp = Spotify_Search_v4.authentiated_spotipy()

    # # get the song key
    # getKey(sp)

    # # search for the recommendations (song key list, database path)
    search(sp, ['Money Trees'+'\0'+'Kendrick Lamar Jay Rock'+'\0'+'2HbKqm4o0w5wEeEFXm2sD4',], r"C:\Users\dkdkm\Documents\GitHub\database")

    # # compare two songs. either one can be from MSD dataset or spotify (True for spotify, False for MSD)
    # song1 = ('Darts Of Pleasure\0Franz Ferdinand\07h0jDykw4RpWFqUhZQuElW', True)
    # song2 = ('Love On A Mountain Top\x00Sinitta', False)

    # compareTwoSongs(sp, song1, song2, r"C:\Users\dkdkm\Documents\GitHub\database")

    
