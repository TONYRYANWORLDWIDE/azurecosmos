import os
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import itertools
from itertools import combinations


client_id = SPOTIPY_CLIENT_ID ='bb7c475418484e7784d9cd25b5f9f52c'
client_secret = SPOTIPY_CLIENT_SECRET='b0da0baeeab1499884912aea11f4ca58'
redirect_uri =SPOTIPY_REDIRECT_URI='https://localhost:8080/callback/'


os.environ["SPOTIPY_CLIENT_ID"] = "bb7c475418484e7784d9cd25b5f9f52c"
os.environ["SPOTIPY_CLIENT_SECRET"] = "b0da0baeeab1499884912aea11f4ca58"
os.environ["SPOTIPY_REDIRECT_URI"] = "https://localhost:8080/callback/"

scope = "playlist-modify-public playlist-modify-private user-modify-playback-state user-top-read"
scope +=            " user-modify-playback-state user-read-playback-state user-library-read user-library-modify"
# username = '1238315340'
username ='tonyryanworldwide'

        
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)        
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,username=username))

from azure.cosmos import exceptions, CosmosClient, PartitionKey
import family

# Initialize the Cosmos client
endpoint = "https://8f3e613c-0ee0-4-231-b9ee.documents.azure.com:443/"
key = 'PZzg9ARn80V5WErDo0BCVtodRfSgTlmgUYzxKVhmZceKfEAIKjZtbs8Ag1CGlGSgoW4cQEUY1khdXl7wlFI8hg=='

# <create_cosmos_client>
client = CosmosClient(endpoint, key)
# </create_cosmos_client>

# Create a database
# <create_database_if_not_exists>
database_name = 'Spotify'
database = client.create_database_if_not_exists(id=database_name)
# </create_database_if_not_exists>

# Create a container
# Using a good partition key improves the performance of database operations.
# <create_container_if_not_exists>
container_name = 'playlists'
container = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/name"),
    offer_throughput=400
)
playlists = sp.current_user_playlists()['items']
# </create_container_if_not_exists>
def populateplaylistdb():
    
    for playlist in playlists:
        container.create_item(body=playlist)

def readplaylists():
    for playlist in playlists:
        item_response = container.read_item(item=playlist['id'], partition_key=playlist['name'])
        request_charge = container.client_connection.last_response_headers['x-ms-request-charge']
        print('Read item with id {0}. Operation consumed {1} request units'.format(item_response['id'], (request_charge)))

readplaylists()