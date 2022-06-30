import requests

AUTH_URL = 'https://accounts.spotify.com/api/token'
REQUEST_URL = 'https://api.spotify.com/v1/audio-analysis/'
CLIENT_ID = 'd513b538756244beaabe189f5ba75be1'
CLIENT_SECRET = '943e6dab04c34d78a05752b515e3fb2a'

# FEATURES_URL = 'https://api.spotify.com/v1/audio-features'

# r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
'''
r = requests.get('https://api.spotify.com/v1/audio-analysis/id', auth=('d513b538756244beaabe189f5ba75be1', '943e6dab04c34d78a05752b515e3fb2a'))
print(r.status_code)
print()
print(r.headers['content-type'])
print()
print(r.text)
print()
print(r.json())
'''



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
# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'
# Track ID from the URI
track_id = '6y0igZArWVi6Iz0rj35c1Y'
# actual GET request with proper header
r = requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)
r = r.json()
print(r)

#r = requests.get(REQUEST_URL + track_id, headers=headers)
#r = r.json()
#print(r)

import json
with open('spotify_data.json', 'w', encoding='utf-8') as f:
    json.dump(r, f, ensure_ascii=False, indent=4)
    print("DATA DUMP COMPLETE!")

'''
CLIENT_CREDENTIALS = f"{CLIENT_ID}:{CLIENT_SECRET}"
CLIENT_CRDENTIALS_B64 = base64.b64encode(CLIENT_CREDENTIALS.encode())
print(CLIENT_CRDENTIALS_B64)
'''

data = {
    'employees' : [
        {
            'name' : 'John Doe',
            'department' : 'Marketing',
            'place' : 'Remote'
        },
        {
            'name' : 'Jane Doe',
            'department' : 'Software Engineering',
            'place' : 'Remote'
        },
        {
            'name' : 'Don Joe',
            'department' : 'Software Engineering',
            'place' : 'Office'
        }
    ]
}


json_string = json.dumps(data)
print(json_string)
  
# Using a JSON string
with open('json_data.json', 'w') as outfile:
    outfile.write(json_string)