import numpy as np
import os
import hdf5_getters
import multiprocessing as mp
import time
import pickle


def getFeatures(hdf5_file):
    """
    Get features from an HDF5 file.
    """

    h5 = hdf5_getters.open_h5_file_read(hdf5_file)

    # Get the list of all the features
    getters = list(
        filter(lambda x: x[:4] == 'get_', hdf5_getters.__dict__.keys()))
    getters.remove("get_num_songs")  # special case
    getters = np.sort(getters)

    values = []
    # Iterate over all the features
    for getter in getters:
        try:
            res = hdf5_getters.__getattribute__(getter)(h5, 0)
            values.append(res)
        except AttributeError:
            print('forgot -summary flag? specified wrong getter?')

    h5.close()

    cropped_getters = ['title', 'artist_name', 'duration', 'key', 'key_confidence', 'mode',
                       'mode_confidence', 'tempo', 'time_signature', 'time_signature_confidence', 'year']

    # Create a dataframe with the features
    cropped_values = []
    for getter in cropped_getters:
        # index[0] gives all locations (in an array)
        index = np.where(getters == "get_" + getter)

        # if type is bytes, convert to string
        if type(values[index[0][0]]) == np.bytes_:
            cropped_values.append(values[index[0][0]].decode('utf-8'))
        else:
            cropped_values.append(values[index[0][0]])

    return tuple(cropped_values)


if __name__ == '__main__':
    # Path to the Million Song Dataset
    root = r"C:\Users\dkdkm\Documents\GitHub\MillionSongSubset"

    database = {}

    # Path to all HDF5 files
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            pathList.append(os.path.join(path, name))

    # multiprocessing to speed up the process of getting features from all the files
    starttime = time.time()
    pool = mp.Pool()
    result = pool.imap_unordered(getFeatures, pathList)

    lastIndex = 0
    while result._length == None:
        i = result._index
        if i >= lastIndex + 500:
            lastIndex = i
            print("num index: " + str(i))

    for features in result:
        # add each song to the database with key as the title + artist delimited by "\0"
        database[features[0]+"\0"+features[1]] = features
    pool.close()
    print('That took {} seconds'.format(time.time() - starttime))


    starttime = time.time()
    # save the database to a pickle file
    with open('database.pickle', 'wb') as handle:
        pickle.dump(database, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('That took {} seconds'.format(time.time() - starttime))




    # starttime = time.time()

    # batch = 4
    # i = 0
    # result_queue = mp.Queue()

    # while i < len(pathList):
    #     print(i)
    #     processes = []

    #     j = i+batch
    #     while i < j:
    #         p = mp.Process(target=getFeatures, args=(
    #             pathList[i], result_queue))
    #         processes.append(p)
    #         p.start()
    #         i += 1

    #     for process in processes:
    #         process.join()
    #     results = [result_queue.get() for i in range(batch)]
    # print('That took {} seconds'.format(time.time() - starttime))