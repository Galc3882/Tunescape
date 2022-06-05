from scipy import spatial
import numpy as np


# All returns are between 0 and 1.

def key(key1, key2):
    '''
    This function takes two keys and returns the similarity between them.
    '''
    if key1 == key2:
        return 1
    else:
        return 0


def tempo(tempo1, tempo2):
    '''
    This function takes two tempos and returns the similarity between them.
    '''
    return max(1-0.01*abs(float(tempo1) - float(tempo2)), 0)

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
    return max(1-0.1*abs(int(year1) - int(year2)), 0)

def duration(duration1, duration2):
    '''
    This function takes two durations and returns the similarity between them.
    '''
    return max(1-0.1*abs(float(duration1) - float(duration2)), 0)

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
    if len(sections_start1) > len(sections_start2) or len(sections_start2) > len(sections_start1):
        return None
    return max(1 - spatial.distance.cosine(sections_start1, sections_start2), 0)

def segments_pitches(segments_pitches1, segments_pitches2):
    '''
    This function takes two segments pitches and returns the similarity between them.
    '''
    if len(segments_pitches1) > len(segments_pitches2) or len(segments_pitches2) > len(segments_pitches1):
        return None
    l = []
    for i in range(len(segments_pitches1)):
        l.append(1 - spatial.distance.cosine(segments_pitches1[i], segments_pitches2[i]))
    return max(sum(l)/len(l), 0)

def segments_timbre(segments_timbre1, segments_timbre2):
    '''
    This function takes two segments timbre and returns the similarity between them.
    '''
    if len(segments_timbre1) > len(segments_timbre2) or len(segments_timbre2) > len(segments_timbre1):
        return None
    l = []
    for i in range(len(segments_timbre1)):
        l.append(1 - spatial.distance.cosine(segments_timbre1[i], segments_timbre2[i]))
    return max(sum(l)/len(l), 0)
    

def bars_start(bars_start1, bars_start2):
    '''
    This function takes two bars starts and returns the similarity between them.
    '''
    if len(bars_start1) > len(bars_start2) or len(bars_start2) > len(bars_start1):
        return None
    return max(1 - spatial.distance.cosine(bars_start1, bars_start2), 0)

def tatums_start(tatums_start1, tatums_start2):
    '''
    This function takes two tatums starts and returns the similarity between them.
    '''
    if len(tatums_start1) > len(tatums_start2) or len(tatums_start2) > len(tatums_start1):
        return None
    return max(1 - spatial.distance.cosine(tatums_start1, tatums_start2), 0)

# A dictionary of the similarity functions
methodDictionary = {2: duration, 3: key, 5: mode, 7: tempo, 8: loudness, 9: time_signature, 11: year,
                    12: sections_start, 13: segments_pitches, 14: segments_timbre, 15: bars_start, 18: tatums_start}

# ('title', 'artist_name', 'duration', 'key', 'key_confidence',
#  0           1                2           3           4
# 'mode', 'mode_confidence', 'tempo', 'loudness', 'time_signature',
#  5           6                7           8           9
# 'time_signature_confidence', 'year', 'sections_start', 'segments_pitches',
#  10                           11          12                  13
# 'segments_timbre', 'bars_start', 'bars_confidence', 'tatums_confidence', 'tatums_start')
#  14                           15          16                  17              18
