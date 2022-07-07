import spotipy
import time
from datetime import timedelta
from spotipy.oauth2 import SpotifyClientCredentials


def authentiated_spotipy():
    '''Returns an authentiated Spotipy Instance'''
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    CLIENT_ID = 'd513b538756244beaabe189f5ba75be1'
    CLIENT_SECRET = '943e6dab04c34d78a05752b515e3fb2a'
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


def search(track_name, sp):
    '''Returns an array with up to 50 tracks (arrays)
    Each array contains: 0: song name, 1: artists names, 2: duration, 3: album art, 4: release date, 5: popularity, 6: explicit (T/F), 7: spotify url, 8: id (uri)'''
    result = sp.search(track_name, limit=50, type='track')
    print("DEBUG:", result['tracks']['total'], "tracks found")
    num_tracks_capped = len(result['tracks']['items'])

    results_trimmed = []

    for i in range(0, num_tracks_capped):
        name = result['tracks']['items'][i]['name']
        artists = "By"
        for j in range(0, len(result['tracks']['items'][i]['artists'])):
            artists += " " + result['tracks']['items'][i]['artists'][j]['name']
        duration = str(timedelta(
            seconds=result['tracks']['items'][i]['duration_ms']/1000))
        if duration[0] == '0':
            if duration[2] == '0':
                duration = duration[3:7]
            else:
                duration = duration[2:7]
        else:
            duration = duration[:7]
        album_art = result['tracks']['items'][i]['album']['images'][2]['url']
        release_date = result['tracks']['items'][i]['album']['release_date']
        popularity = result['tracks']['items'][i]['popularity']
        explicit = result['tracks']['items'][i]['explicit']
        url = result['tracks']['items'][i]['external_urls']['spotify']
        id = result['tracks']['items'][i]['id']

        track_info = [name, artists, duration, album_art,
                      release_date, popularity, explicit, url, id]

        results_trimmed.append(track_info)
    return results_trimmed


sp = authentiated_spotipy()

#start_time = time.time()
#name = ["Smooth Criminal"]
result = search("Smooth Criminal", sp)
# print(time.time()-start_time)
# for i in range(len(result)):
#print("Song", i + 1)
# print(result[i])

'''
# API_URL = 'https://api.spotify.com/v1/search?type=album&include_external=audio'
API_URL = 'https://api.spotify.com/v1/search?'

search_query = 'Firework'
search_query2 = 'test'
'''
