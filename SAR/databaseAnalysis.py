import pickle

if __name__=='__main__':
    with open('database.pickle', 'rb') as handle:
        database = pickle.load(handle)


    # l = list(database.keys())
    # for i in range(4000):
    #     database.pop(l[i])

    # with open('database_6000.pickle', 'wb') as handle:
    #     pickle.dump(database, handle, protocol=pickle.HIGHEST_PROTOCOL)


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
