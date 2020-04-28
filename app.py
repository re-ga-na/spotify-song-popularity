import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from flask import request, Flask, render_template
import pickle
app = Flask(__name__)


# A. Load Models & Set Up API 
#-----------------------------------------------
# Load the model 1 (check file link)
pkl_filename = "C:/Users/Suhaib Kiani/Desktop/pickle_45.pkl"
#pkl_filename = "Resources/pickle/pickle_45.pkl" 
with open(pkl_filename, 'rb') as pkl:  
    Pickled_LR_Model = pickle.load(pkl)

# Load the model 2
pkl_filename2 = "C:/Users/Suhaib Kiani/Desktop/pickle_45_Model2.pkl"  
#pkl_filename2 = "Resources/pickle/pickle_45_Model2.pkl"  
with open(pkl_filename2, 'rb') as file2:  
    Pickled_Model2 = pickle.load(file2)

#set up API authonatication
client_id = "5028c957611248149d8c04007258f254"
client_secret = "aa56a507cb944f488f8835062a94115c"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# B. Run API Call and retrieve song information 
#-----------------------------------------------

#create link to input button for Artist and Track (or manually enter below)
Artist="Lionel Richie"
Track="Tonight Will Be Alright"


def api_call(Artist,Track):
    #set up blank features df 
    features = ['0', 'Artist', 'Track', 'Unnamed: 0', 'acousticness', 'danceability',
        'duration_ms', 'energy', 'followers', 'instrumentalness', 'key',
        'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo',
        'time_signature', 'valence']       
    features = pd.DataFrame(columns = features)

    try: 
        artistname= Artist
        search_str =  Track
        print(artistname+ ","+ search_str )
        result= sp.search(search_str+":"+artistname,type="track,artist")
        print(result["tracks"]["items"][0]["id"])
        
        track_id = result["tracks"]["items"][0]["id"]
        artist_id = result['tracks']['items'][0]["album"]['artists'][0]['id']
        
        features_i = sp.audio_features(track_id)
        features_i = pd.DataFrame(features_i)
        
        features_i["followers"] = sp.artist(artist_id)['followers']['total']
        features_i["tempo"] = sp.audio_analysis(track_id)['track']['tempo']
        features_i["popularity"] = sp.track(track_id)["popularity"]
        features_i["Artist"] = artistname
        features_i["Track"] = search_str
        features = features.append(features_i)        
        print (features)

    except: 
        print ('data not found')  


    return { 
                "Followers": features['followers'].values[0],
                "Instrumentalness": features['instrumentalness'],
                "Acousticness": features[['acousticness']],
                "Danceability": features[['danceability']],
                "Popularity": features[['popularity']],
                "features_x": features[['followers','instrumentalness','acousticness', 'danceability', 'duration_ms', 'energy', 'key', 'liveness', 'loudness', 'mode','speechiness', 'tempo', 'time_signature', 'valence']],
                "features_y": features['popularity'],
                #"song_name": search_str,
                #"artist_name" : artistname,
                #"popularity": features_i["popularity"],
                }

    


# C. Run the pickles  
#-----------------------------------------------

# helper function1
def lr_model(user_input_artist, user_input_song):
    result_dictionary= api_call(user_input_artist, user_input_song)
   # Predict the Labels using the reloaded Model
    Y_predict = Pickled_LR_Model.predict(result_dictionary["features_x"])  
    spotify_dict={
        "Actual Spotify song poularity:":result_dictionary["features_y"],
        "Model predicted popularity":Y_predict}
    return spotify_dict



from sklearn.metrics import make_scorer, accuracy_score, roc_auc_score 

# helper function2
def dt_model(user_input_artist, user_input_song):
   # Predict the Labels using the reloaded Model
    result_dictionary= api_call(user_input_artist, user_input_song)
    Y_predict2 = Pickled_Model2.predict(result_dictionary["features_x"])     
    spotify_dict2={
        "Actual Spotify song poularity:":result_dictionary["features_y"],
        "Model prediction popular_01":Y_predict2}
    return spotify_dict2



# D. Flask Handlers  
#-----------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")

  
@app.route("/handledata", methods=["POST"])

def handledata(): 
    # # use helper function to get result
    # song_name = lr_model(request.form["input_artist"], request.form["input_song"])
    # return render_template("index.html", **song_name)
 
    
    singer=request.form["input_artist"]
    print(singer)
    song=request.form["input_song"]
    print(song)
    
   #  use helper function to get result
    song_name=api_call(singer,song)
    #popularity=song_name[0]
    #popularity="test"
    # # use helper function2 to get 2nd result
    song_name2 = lr_model(singer,song)
    # return render_template("index.html", **song_name2)
    song_name3 = dt_model(singer,song)



    print("this is the result to pass")
    print(song_name)


    return render_template("index.html", song_name=song_name, song_name2=song_name2, song_name3=song_name3)
            


if __name__ == "__main__":
    app.run(debug=True)