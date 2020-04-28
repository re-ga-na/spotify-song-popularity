from flask import request, Flask, render_template
import pickle

app = Flask(__name__)

# # Load the model
# with open('pickle415.pickle', 'rb') as pkl:    
#     model = pickle.load(pkl)

# genres={1: 'Movie',
#     2: 'R&B',
#     3: 'Dance',F
#     4: 'Hip-Hop',
#     5: 'Pop',
#     6: 'Soul',
#     7: 'Indie',
#     8: 'Alternative',
#     9: 'Rap',
#     10: 'Folk',
#     11: 'Rock',
#     12: 'A Capella',
#     13: 'Country',
#     14: 'Blues',
#     15: 'Jazz',
#     16: 'Reggae',
#     17: 'World',
#     18: 'Electronic',
#     19: 'Reggaeton',
#     20: 'Ska',
#     21: 'Anime',
#     22: 'Soundtrack',
#     23: 'Classical',
#     24: 'Opera'}
#for flask app
import numpy as np
import pandas as pd
import io
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import spotipy.util as util
import datetime
#import pdb; pdb.set_trace()

#print("I am here1")
#set up API authonatication
client_id = "5028c957611248149d8c04007258f254"
client_secret = "aa56a507cb944f488f8835062a94115c"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#print("I am here2")

#username = 'jq42@cornell.edu'
#scope = 'user-read-private user-read-email'
#uri = 'http://localhost'
#client_cred = SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET)
#auth_spotify = spotipy.client.Spotify(client_credentials_manager=client_cred)

categoricals = [
    'acousticness',
    'danceability',
    'duration_ms', 
    'energy',
    'instrumentalness',
    'key',
    'liveness',
    'loudness',
    'mode',
    'speechiness',
    'tempo',
    'time_signature',
    'valence'

]



Artist="Lionel Richie"
Track="Tonight Will Be Alright"

#Artist="Casual"
#Track="I Didn't Mean To"


def api_call(Artist,Track):
    try: 
        artistname=Artist
        search_str=Track
        
        print(artistname)
        print(search_str)
        
        
        print(artistname+ ","+ search_str )
        #console.log(artistname+ ","+ search_str )
        result= sp.search(search_str+":"+artistname,type="track,artist")
        print(result["tracks"]["items"][0]["id"])
        
        track_id = result["tracks"]["items"][0]["id"]
        artist_id = result['tracks']['items'][0]["album"]['artists'][0]['id']
        
        popularity= sp.track(track_id)["popularity"]
        followers= sp.artist(artist_id)['followers']['total']
        tempo = sp.audio_analysis(track_id)['track']['tempo']   
        Artist = artistname
        Track = search_str
        
        
        features_i = sp.audio_features(track_id)
        
        features_i2 = features_i [['instrumentalness','popularity','acousticness', 'danceability', 'duration_ms', 'energy', 'key', 'liveness', 'loudness', 'mode',
       'speechiness', 'tempo', 'time_signature', 'valence']]

        
        print(features_i)
        print(popularity)
        print("I am here4")
        #features_i = pd.DataFrame(features_i)
        
        #features["genres"] = sp.artist(artist_id)['genres']
        #features_i["followers"] = sp.artist(artist_id)['followers']['total']
        #features_i["tempo"] = sp.audio_analysis(track_id)['track']['tempo']
        #features_i["popularity"] = sp.track(track_id)["popularity"]
        #features_i["Artist"] = artistname
        #features_i["Track"] = search_str
        #features = features.append(features_i)
        #print("I am here5")
        
        #print("this is popularity")
        #print(features_i["popularity"])
        
    except: 
        print ('data not found')
        

    #print("This is the result")
    print(result["tracks"]["items"][0]["id"])
        
    return features_i, popularity, followers, tempo, Artist, Track       
    


features_i=api_call(Artist,Track)



@app.route("/")
def index():
    song_name=features_i
    return render_template("index_rc.html", song_name=song_name)
    
  


@app.route("/handledata", methods=["POST"])
def handledata():
    
    singer=request.form["input_artist"]
    print(singer)
    song=request.form["input_song"]
    print(song)
    
   #  use helper function to get result
    song_name=api_call(singer,song)
    #popularity=song_name[0]
    popularity="test"
    
    print("this is the result to pass")
    print(song_name)


    return render_template("index_rc.html", song_name=song_name)

#return the list
    #return render_template("index.html", **song_name)



if __name__ == "__main__":
    app.run(debug=True)