import requests

AUTH_URL = 'https://accounts.spotify.com/api/token'
# API_URL = 'https://api.spotify.com/v1/search?type=album&include_external=audio'
API_URL = 'https://api.spotify.com/v1/search?'
CLIENT_ID = 'd513b538756244beaabe189f5ba75be1'
CLIENT_SECRET = '943e6dab04c34d78a05752b515e3fb2a'

search_query = 'Firework'
search_query2 = 'test'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()
print(auth_response_data)

# save the access token
access_token = auth_response_data['access_token']


headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}



# actual GET request with proper header
r = requests.get(API_URL + 'q=track:' + search_query + '%20artist:' + search_query2 + 'type=track', headers=headers)
r = r.json()
print(r)
