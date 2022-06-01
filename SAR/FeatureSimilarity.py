# All returns are between 0 and 1.

def key(key1, key2):
    '''
    This function takes two keys and returns the similarity between them.
    '''
    return max(1-0.5*abs(int(key1) - int(key2)), 0)

def tempo(tempo1, tempo2):
    '''
    This function takes two tempos and returns the similarity between them.
    '''
    return max(1-0.01*abs(float(tempo1) - float(tempo2)), 0)

# A dictionary of the similarity functions
methodDictionary = {1: key, 2:tempo}