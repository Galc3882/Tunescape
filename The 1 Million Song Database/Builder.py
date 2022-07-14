import numpy as np
import os
import hdf5_getters
import multiprocessing as mp
import time
import pickle
import cv2
import gc
import datetime
import os


def getFeatures(hdf5_file):
    """
    Get features from an HDF5 file.
    """

    """ 
    ['get_analysis_sample_rate', 'get_artist_7digitalid',
       'get_artist_familiarity', 'get_artist_hotttnesss', 'get_artist_id',
       'get_artist_latitude', 'get_artist_location',
       'get_artist_longitude', 'get_artist_mbid', 'get_artist_mbtags',
       'get_artist_mbtags_count', 'get_artist_name',
       'get_artist_playmeid', 'get_artist_terms', 'get_artist_terms_freq',
       'get_artist_terms_weight', 'get_audio_md5', 'get_bars_confidence',
       'get_bars_start', 'get_beats_confidence', 'get_beats_start',
       'get_danceability', 'get_duration', 'get_end_of_fade_in',
       'get_energy', 'get_key', 'get_key_confidence', 'get_loudness',
       'get_mode', 'get_mode_confidence', 'get_release',
       'get_release_7digitalid', 'get_sections_confidence',
       'get_sections_start', 'get_segments_confidence',
       'get_segments_loudness_max', 'get_segments_loudness_max_time',
       'get_segments_loudness_start', 'get_segments_pitches',
       'get_segments_start', 'get_segments_timbre', 'get_similar_artists',
       'get_song_hotttnesss', 'get_song_id', 'get_start_of_fade_out',
       'get_tatums_confidence', 'get_tatums_start', 'get_tempo',
       'get_time_signature', 'get_time_signature_confidence', 'get_title',
       'get_track_7digitalid', 'get_track_id', 'get_year']
    """

    cropped_getters = ('get_title', 'get_artist_name', 'get_duration', 'get_key',
                       'get_mode', 'get_tempo', 'get_loudness', 'get_time_signature',
                       'get_year', 'get_sections_start', 'get_segments_pitches',
                       'get_segments_timbre', 'get_bars_start', 'get_beats_start',
                       'get_tatums_start')

    h5 = hdf5_getters.open_h5_file_read(hdf5_file)

    # Create a dataframe with the features
    cropped_values = []
    batchSize = 64

    for getter in cropped_getters:
        res = hdf5_getters.__getattribute__(getter)(h5, 0)

        if getter == 'get_segments_pitches' or getter == 'get_segments_timbre':
            if len(res) > batchSize:
                res = cv2.resize(res, dsize=(12, batchSize),
                                 interpolation=cv2.INTER_CUBIC)
        elif getter == 'get_sections_start' or getter == 'get_bars_start' or getter == 'get_beats_start' or getter == 'get_tatums_start':
            if len(res) > batchSize:
                res = np.array([i.item() for i in cv2.resize(
                    res, dsize=(1, batchSize), interpolation=cv2.INTER_NEAREST)])

        # if type is bytes, convert to string
        if type(res) == np.bytes_:
            cropped_values.append(res.decode('utf-8'))
        else:
            cropped_values.append(res)
    h5.close()

    return tuple(cropped_values)


if __name__ == '__main__':
    # Path to the Million Song Dataset
    root = r"D:\MSD\MillionSongDataset\data"

    database = {}

    # Path to all HDF5 files
    pathList = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if not name.endswith('.DS_Store'):
                if len(pathList)%1000 == 0:
                    print("Found "+str(len(pathList))+ " files and searching... ")
                pathList.append(os.path.join(path, name))

    # split the list into chunks of 5000
    chunkSize = 5000
    chunks = [pathList[i:i+chunkSize]
              for i in range(0, len(pathList), chunkSize)]

    for i, chunk in enumerate(chunks):
        print("Processing chunk {} of {}".format(i+1, len(chunks)))

        # multiprocessing to speed up the process of getting features from all the files
        starttime = time.time()
        pool = mp.Pool()
        result = pool.imap_unordered(getFeatures, chunk)

        lastIndex = 0
        while result._length == None:
            j = result._index
            if j >= lastIndex + 500:
                lastIndex = j
                print("Songs processed: " + str(j) + "\t|\t " + str(int(j*100/len(chunk))
                                                                    ) + "%\t|\t Time: " + str(datetime.timedelta(seconds=time.time() - starttime)))

        for features in result:
            # add each song to the database with key as the title + artist delimited by "\0"
            database[features[0]+"\0"+features[1]] = features
        pool.close()
        print('That took ' + str(datetime.timedelta(seconds=time.time() - starttime)))

        # remove songs with no features
        lr = ['Black Market Hell\0Aiden',
              'Genuine\0Five Fingers of Funk', 'bereit\0Panzer AG']
        for key in lr:
            if key in database:
                database.pop(key)
                lr.remove(key)

        # save the database to a pickle file
        starttime = time.time()
        with open(r'C:\Users\dkdkm\Documents\GitHub\database\database'+str(i) + '.pickle', 'wb') as handle:
            pickle.dump(database, handle)
            handle.close()
        print('Dump took ' + str(datetime.timedelta(seconds=time.time() - starttime)))
        print()

        # remove database from memory
        del database
        gc.collect()
        database = {}
