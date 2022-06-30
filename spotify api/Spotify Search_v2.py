import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials 

AUTH_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = 'd513b538756244beaabe189f5ba75be1'
CLIENT_SECRET = '943e6dab04c34d78a05752b515e3fb2a'

start_time = time.time()
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

name = ["Smooth Criminal"]
result = sp.search(name, type='track') 
print(result['tracks']['items'][1]['artists'])
#print(result['tracks']['items'][1]['artists'])
print(time.time()-start_time)


'''
# API_URL = 'https://api.spotify.com/v1/search?type=album&include_external=audio'
API_URL = 'https://api.spotify.com/v1/search?'

search_query = 'Firework'
search_query2 = 'test'
'''