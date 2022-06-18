import pickle
import Search
import debug

def main1():
    # Read from the pickle file
    with open('database.pickle', 'rb') as handle:
        database = pickle.load(handle)

    # Ask for the song title
    songTitle = input("Enter the song title: ")
    # Find the song in the database
    songKey = Search.fuzzyGetSongTitle(songTitle, database.keys(), threshold=40)
    if len(songKey) > 1:
        print("Multiple songs found:")
        for j in range(len(songKey)):
            print(str(j+1)+". "+songKey[j][0].split('\0')[0]+" by " + songKey[j][0].split('\0')[1])
        k = input("Please enter the number of the song you want to use: ")
        songKey = songKey[int(k)-1][0]
    else:
        songKey = songKey[0][0]
    print("Found Song: " + songKey.split('\0')
              [0]+" by " + songKey.split('\0')[1])

    # Find most similar song using cosine similarity
    similarSongs = Search.findSimilarSongs(database[songKey], database, 5)
    sortedSimilarSongs = sorted(similarSongs, key=Search.takeSecond, reverse=True)
    print("Similar Songs: ")
    for i in range(len(sortedSimilarSongs)):
        print("Found Song: " + sortedSimilarSongs[i][0].split('\0')
              [0]+" by " + sortedSimilarSongs[i][0].split('\0')[1])
        print("Cosine Similarity: " + str(sortedSimilarSongs[i][1]))

def main2():
    # Read from the pickle file
    with open('database.pickle', 'rb') as handle:
        database = pickle.load(handle)

    songKey1 = "Mystic River\0Blue Rodeo"
    songKey2 = "Stir The Gift\0Deitrick Haddon"

    debug.compareSongs(database[songKey1], database[songKey2])


if __name__ == '__main__':
    main1()

    # # Read from the pickle file
    # with open('database.pickle', 'rb') as handle:
    #     database = pickle.load(handle)

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
