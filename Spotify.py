import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import itertools
from itertools import combinations
import json
import random
import string

letters = string.ascii_lowercase
credentials_file = 'credentials.json'
with open(credentials_file) as json_file:
        data = json.load(json_file)
        client_id = data['creds']['client_id']
        client_secret = data['creds']['client_secret']
        redirect_uri = data['creds']['redirect_uri']
        endpoint = data['creds']['endpoint']
        key = data['creds']['key']




os.environ["SPOTIPY_CLIENT_ID"] = client_id
os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
os.environ["SPOTIPY_REDIRECT_URI"] = redirect_uri

scope = "playlist-modify-public playlist-modify-private user-modify-playback-state user-top-read"
scope +=            " user-modify-playback-state user-read-playback-state user-library-read user-library-modify"
# username = '1238315340'
username ='tonyryanworldwide'

        
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)        
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username=username))

from azure.cosmos import exceptions, CosmosClient, PartitionKey
import family

# Initialize the Cosmos client
print("endpoint {0}: key {1}".format(endpoint,key))
client = CosmosClient(endpoint, key)

database_name = 'Spotify'
database = client.create_database_if_not_exists(id=database_name)

container_name = 'playlists'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/name"),
    offer_throughput=400
)

container_tracks = 'playlisttracks'
containertracks = database.create_container_if_not_exists(
id=container_tracks ,
# + '_' + ''.join(random.choice(letters) for i in range(10)) , 
partition_key=PartitionKey(path="/playlistid"),
offer_throughput=400
)

playlists = sp.current_user_playlists()['items']
# </create_container_if_not_exists>
def populateplaylistdb():    
    for playlist in playlists:        
        container.create_item(body=playlist)

def readplaylists():
    for playlist in playlists:
        print("startingreadplaylists", playlist['id'],playlist['name'])
        item_response = container.read_item(item=playlist['id'], partition_key=playlist['name'])
        request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
        print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))
        gettracksinplaylists(item_response['id'])

def gettracksinplaylists(playlistid):
    print("startinggettracksinplaylists")
    tracks = sp.playlist_tracks(playlistid)['items']    
    for track in tracks:
        tr = track['track']
        tr['id'] = tr['id'] + '_' + playlistid
        try:
            current = containertracks.read_item(tr['id'],playlistid)
            print('continue')
            continue
        except:
            print('insertit')
            tr['playlistid'] = playlistid
            # print(tr)
            containertracks.create_item(body=tr)


if __name__ == "__main__":
    # populateplaylistdb()
    readplaylists()

