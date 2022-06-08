import cProfile
import Search
import pickle
from fuzzywuzzy import process
import pstats
from pstats import SortKey

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