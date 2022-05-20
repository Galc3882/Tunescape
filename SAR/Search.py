import csv
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def fuzzySearchSongTitle(songTitle, data, threshold=80):
    """
    Searches for a song title in the database.
    Returns the analysis of the song matching th most above a certian threshold.
    Threshold is from 0 to 100.
    """
    maxRatio = [0, 0]

    for row in range(len(data)):
        ratio = fuzz.ratio(songTitle, data[row][50])  # 50 is the song title
        if ratio > threshold and ratio > maxRatio[0]:
            maxRatio[0] = ratio
            maxRatio[1] = row
    if maxRatio[0] == 0:
        return None
    print("Ratio of Fuzzy Search: " + str(maxRatio[0])) # print the ratio of the song
    return data[maxRatio[1]]


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
        print("Found Song" + songAnalysis[50]) # b'Amor De Cabaret'

