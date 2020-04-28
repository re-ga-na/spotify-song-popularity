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

#print("I am here3")

Artist="Lionel Richie"
Track="Tonight Will Be Alright"

#print(Artist)
#print(Track)



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
        
        features_i = sp.audio_features(track_id)
        print(features_i)
        print("I am here4")
        #features_i = pd.DataFrame(features_i)
        
        #features["genres"] = sp.artist(artist_id)['genres']
        features_i["followers"] = sp.artist(artist_id)['followers']['total']
        features_i["tempo"] = sp.audio_analysis(track_id)['track']['tempo']
        features_i["popularity"] = sp.track(track_id)["popularity"]
        features_i["Artist"] = artistname
        features_i["Track"] = search_str
        #features = features.append(features_i)
        print("I am here5")
    except: 
        print ('data not found')

    print(result["tracks"]["items"][0]["id"])
        
    return result       
    
print("I am here6")

api_call(Artist,Track)

print("I am here7")
print("End")


# def get_requested_song_df(title):
#         q = title
#         result = auth_spotify.search(q)
#         result_track_id = result['tracks']["items"][0]["id"]
#         result_track_features =  auth_spotify.audio_features(result_track_id)
#         result_track=pd.DataFrame()
#         for i in categoricals:
#                 result_track[i] = [0]
#         for i in categoricals:
#                 result_track[i] = result_track_features[0][i]
#         result_track['explicit'] = auth_spotify.track(result_track_id)["explicit"]
#         result_track['explicit'] = result_track['explicit'].map({
#             True: 1,  
#             False: 0,    
#         })
#         result_track['release_year']=auth_spotify.track(result_track_id)["album"]["release_date"][:4]
#         song_name = auth_spotify.track(result_track_id)["name"]
#         artist_name = auth_spotify.track(result_track_id)["album"]["name"]
#         artwork = auth_spotify.track(result_track_id)["album"]["images"][0]["url"]
#         artist_id = auth_spotify.track(result_track_id)["artists"][0]["id"]
#         actual_genre = ", ".join(auth_spotify.artist(artist_id)["genres"])
#         recommendation_track_name =auth_spotify.recommendations(seed_artists=[artist_id],seed_tracks=[result_track_id])\
#         ["tracks"][0]["name"]
#         recommendation_url =auth_spotify.recommendations(seed_artists=[artist_id],seed_tracks=[result_track_id])\
#         ["tracks"][0]["external_urls"]["spotify"]
#         recommendation_artist_name =auth_spotify.recommendations(seed_artists=[artist_id],seed_tracks=[result_track_id])\
#         ["tracks"][0]["artists"][0]["name"]
#         song_id = result_track_id
#         preview_url = auth_spotify.track(result_track_id)["preview_url"]
#         return {"model_df":result_track, 
#                 "song_name":song_name,
#                 "artist_name":artist_name,
#                 "artwork":artwork,
#                 "actual_genre":actual_genre,
#                 "song_id":song_id,
#                 "preview_url":preview_url,
#                 "recommendation_track_name": recommendation_track_name,
#                 "recommendation_artist_name": recommendation_artist_name,
#                 "recommendation_url":recommendation_url,
#                  "artist_id": artist_id}
  
  


# # helper function
# def use_model(user_input_song):
#     result_dictionary=get_requested_song_df(user_input_song)
#     prediction=model.predict(result_dictionary["model_df"])
#     confidence=f"{np.amax(model.predict_proba(result_dictionary['model_df'])):.2%}"
#     # turn prediction into text
#     spotify_dict={
#         "user_song_genre":genres[prediction[0]],
#         "song_name":result_dictionary["song_name"],
#         "artist_name":result_dictionary["artist_name"],
#         "artwork":result_dictionary["artwork"],
#         "actual_genre":result_dictionary["actual_genre"],
#         "song_id":result_dictionary["song_id"],
#         "confidence":confidence,
#         "recommendation_track_name":result_dictionary["recommendation_track_name"],
#         "recommendation_artist_name":result_dictionary["recommendation_artist_name"],
#         "recommendation_url":result_dictionary["recommendation_url"]
#     }
#     return spotify_dict
    
    
    
Artist="Lionel Richie"
Track="Tonight Will Be Alright"

@app.route("/")
def index():
    return render_template("new_index.html")

  

@app.route("/handledata", methods=["POST"])

def handledata():
    
   #  use helper function to get result
    song_name=api_call(request.form["artist_input","song_input"])
    
    
    #print(song_name)

    return render_template("new_index.html", **song_name)

    



if __name__ == "__main__":
    app.run(debug=True)