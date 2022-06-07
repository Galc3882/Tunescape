from ctypes import sizeof
from scipy import spatial
import skimage.measure
import numpy as np
import math


keyArr = (((1, 0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
           (0, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
           (0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
           (0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
           (0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
           (0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),    
           (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
           (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5),
           (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5),
           (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5),
           (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5),
           (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5),
           (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1)),

            ((1, 0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
              (0, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
              (0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
              (0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
              (0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
              (0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),    
              (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5),
              (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5),
              (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5),
              (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.5),
              (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5),
              (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1, 0.5),
              (0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1)))

def equalizeDim(l1, l2):
    '''
    This function takes two lists and adds zeros where the value of the bigger list is smaller
    than the value of the smaller list. It returns the two lists with the same length.
    '''
    if l1 == []:
        return [0]*len(l2), l2
    elif l2 == []:
        return l1, [0]*len(l1)
    if len(l1) > len(l2):
        i = 0
        while len(l1) != len(l2):
            if l1[i] < l2[i]:
                l2.insert(i, 0)
                i += 1
            else:
                i += 1
                
            if i == len(l2):
                l2 = l2 + [0]*(len(l1)-len(l2))
                break
    elif len(l2) > len(l1):
        i = 0
        while len(l2) != len(l1):
            if l2[i] < l1[i]:
                l1.insert(i, 0)
                i += 1
            else:
                i += 1
            
            if i == len(l1):
                l1 = l1 + [0]*(len(l2)-len(l1))
                break
    return l1, l2

        
def key(key1, key2, mode1, mode2):
    '''
    This function takes two keys and returns the similarity between them.
    '''
    return keyArr[mode1 & mode2][key1][key2]


def tempo(tempo1, tempo2):
    '''
    This function takes two tempos and returns the similarity between them.
    '''
    # sigmoid
    return 1 / (1 + math.exp(-max(1-0.01*abs(float(tempo1) - float(tempo2)), 0)))


def loudness(loudness1, loudness2):
    '''
    This function takes two loudnesses and returns the similarity between them.
    '''
    return max(1-0.1*abs(float(loudness1) - float(loudness2)), 0)


def time_signature(time_signature1, time_signature2):
    '''
    This function takes two time signatures and returns the similarity between them.
    '''
    if time_signature1 == time_signature2:
        return 1
    else:
        return 0


def year(year1, year2):
    '''
    This function takes two years and returns the similarity between them.
    '''
    if year1 == 0 or year2 == 0:
        return None
    return max(1-0.05*abs(int(year1) - int(year2)), 0)


def duration(duration1, duration2):
    '''
    This function takes two durations and returns the similarity between them.
    '''
    return max(1-0.02*abs(float(duration1) - float(duration2)), 0)


def mode(mode1, mode2):
    '''
    This function takes two modes and returns the similarity between them.
    '''
    if mode1 == mode2:
        return 1
    else:
        return 0


def sections_start(sections_start1, sections_start2):
    '''
    This function takes two sections starts and returns the similarity between them.
    '''
    sections_start1, sections_start2 = equalizeDim(list(sections_start1), list(sections_start2))
    return max(1 - spatial.distance.cosine(sections_start1, sections_start2), 0)


def segments_pitches(segments_pitches1, segments_pitches2):
    '''
    This function takes two segments pitches and returns the similarity between them.
    '''
    # reshape matricies to smallest one
    r = min(len(segments_pitches1), len(segments_pitches2))
    c = min(len(segments_pitches1[0]), len(segments_pitches2[0]))
    segments_pitches1 = np.resize(segments_pitches1, (r, c))
    segments_pitches2 = np.resize(segments_pitches2, (r, c))

    # return euclidean distance between the two matrices to sigmoid
    return 1 / (1 + math.exp(-max(1-0.005*abs(np.linalg.norm(segments_pitches1-segments_pitches2)), 0)))


def segments_timbre(segments_timbre1, segments_timbre2):
    '''
    This function takes two segments timbre and returns the similarity between them.
    '''
    # reshape matricies to smallest one 
    r = min(len(segments_timbre1), len(segments_timbre2))
    c = min(len(segments_timbre1[0]), len(segments_timbre2[0]))
    segments_timbre1 = np.resize(segments_timbre1, (r, c))
    segments_timbre2 = np.resize(segments_timbre2, (r, c))

    # return euclidean distance between the two matrices to sigmoid
    return 1 / (1 + math.exp(-max(1-0.005*abs(np.linalg.norm(segments_timbre1-segments_timbre2)), 0)))


def bars_start(bars_start1, bars_start2):
    '''
    This function takes two bars starts and returns the similarity between them.
    '''
    bars_start1, bars_start2 = equalizeDim(list(bars_start1), list(bars_start2))
    return max(1 - spatial.distance.cosine(bars_start1, bars_start2), 0)


def tatums_start(tatums_start1, tatums_start2):
    '''
    This function takes two tatums starts and returns the similarity between them.
    '''
    tatums_start1, tatums_start2 = equalizeDim(list(tatums_start1), list(tatums_start2))
    return max(1 - spatial.distance.cosine(tatums_start1, tatums_start2), 0)

def beats_start(beats_start1, beats_start2):
    '''
    This function takes two beats starts and returns the similarity between them.
    '''
    beats_start1, beats_start2 = equalizeDim(list(beats_start1), list(beats_start2))
    return max(1 - spatial.distance.cosine(beats_start1, beats_start2), 0)

def artist_name(artist_name1, artist_name2):
    '''
    This function takes two artist names and returns the similarity between them.
    '''
    if artist_name1 == artist_name2:
        return 1
    else:
        return 0


# A dictionary of the similarity functions
methodDictionary = {1: artist_name, 2: duration, 3: key, 5: tempo, 6: loudness, 7: time_signature, 8: year,
                    9: sections_start, 10: segments_pitches, 11: segments_timbre, 12: bars_start,
                    13: beats_start, 14: tatums_start}

# ('get_title', 'get_artist_name', 'get_duration', 'get_key',
#   0               1                 2                 3
#  'get_mode', 'get_tempo', 'get_loudness', 'get_time_signature',
#   4               5                 6                 7 
#  'get_year', 'get_sections_start', 'get_segments_pitches', 
#   8               9                 10                
#  'get_segments_timbre', 'get_bars_start', 'get_beats_start',
#   11                      12                 13
#  'get_tatums_start')
#   14
