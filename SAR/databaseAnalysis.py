import ujson
import json
import os
import pickle
import numpy as np
import time
import datetime

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.int32):
            return int(obj)
        return json.JSONEncoder.default(self, obj)

if __name__=='__main__':
    starttime = time.time()
    with open(os.path.abspath(os.getcwd()) + r'\tmp\database0.json', 'r') as f:
        database = ujson.load(f)
        f.close()
    print('That took ' + str(datetime.timedelta(seconds=time.time() - starttime)))
    
    starttime = time.time()
    with open(os.path.abspath(os.getcwd()) + r'\tmp\database0.pickle', 'rb') as f:
        database = pickle.load(f)
        f.close()
    print('That took ' + str(datetime.timedelta(seconds=time.time() - starttime)))

    
    
    # with open(os.path.abspath(os.getcwd()) + r'\tmp\database0.pickle', 'rb') as f:
    #     database = pickle.load(f)
    #     f.close()

    # starttime = time.time()
    # with open(os.path.abspath(os.getcwd()) + r'\tmp\database' + str(0) +'.json', 'w', encoding='utf8') as f:
    #     for i in database.items():
    #         f.write(json.dumps(i, cls=MyEncoder))
    #         f.write('\n')
    #     f.close()
    # print('That took ' + str(datetime.timedelta(seconds=time.time() - starttime)))





    # with open('songs.txt', 'w') as f:
        


    #     i = 0
    #     j = 2000
    #     # print dictionary in nice format
    #     for x in database.items():
    #         f.write(x[1][0]+ ' by ' + x[1][1])
    #         f.write('\n')
                
    #         # if i<1:
    #         #     # print('Song: ' + x[1][0])
    #         #     # print('Band: ' + x[1][1])
    #         #     # print('Duration: ' + str(x[1][2]))
    #         #     # print('Key and confidence: ' + str(x[1][3]) + '\t' + str(x[1][4]))
    #         #     # print('Mode and confidence: ' + str(x[1][5]) + '\t' + str(x[1][6]))
    #         #     # print('Tempo: ' + str(x[1][7]))
    #         #     # print('Loudness: ' + str(x[1][8]))
    #         #     # print('Time signature and confidence: ' + str(x[1][9]) + '\t' + str(x[1][10]))
    #         #     # print('Year: ' + str(x[1][11]))
    #         #     # print('Sections start: ')
    #         #     # print(*x[1][12])

    #         #     # print('Segments pitches: ')
    #         #     # for y in x[1][13]:
    #         #     #     print(*y)

    #         #     # print('Segments timbre: ')
    #         #     # for y in x[1][14]:
    #         #     #     print(*y)

    #         #     # print('Bars start: ')
    #         #     # print(*x[1][15])

    #         #     # print('Bars confidence: ')
    #         #     # print(*x[1][16])

    #         #     # print('Tatums confidence: ')
    #         #     # print(*x[1][17])

    #         #     print('Tatums start: ')
    #         #     print(*x[1][18])
    #         #     # print('\n')
    #         # else:
    #         #     break
    #         # i+=1
