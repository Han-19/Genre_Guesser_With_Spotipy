import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials


# authenticate and connect to the API
client_credentials_manager = SpotifyClientCredentials(client_id='{here}',   #insert your client ID
                                                      client_secret='{here}') #insert your secret key
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# get track ids from playlist

def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

while True:
    playlist = input("Playlist ID si gir\n")
    
    tracks = get_playlist_tracks('Spotify', '{}'.format(playlist)) # insert here author name and playlist id

    ids = []
    for item in tracks:
        track = item['track']
        ids.append(track['id'])


    # get song info and audio analysis from song ids
    def getTrackFeatures(id):
          meta = sp.track(id)
          features = sp.audio_features(id)

    #Features can be removed/added according to the needs.
          # Meta
          name = meta['name']
          album = meta['album']['name']
          artist = meta['album']['artists'][0]['name']
          release_date = meta['album']['release_date']
          duration_ms = meta['duration_ms']
          popularity = meta['popularity']
          explicit = meta['explicit']
          available_markets = meta["available_markets"]
          #image_url = meta['album']['images'][1]['url'] #get the 300x300 format album image

          # Features
          acousticness = features[0]['acousticness']
          danceability = features[0]['danceability']
          energy = features[0]['energy']
          instrumentalness = features[0]['instrumentalness']
          liveness = features[0]['liveness']
          loudness = features[0]['loudness']
          speechiness = features[0]['speechiness']
          tempo = features[0]['tempo']
          valence = features[0]['valence']
          time_signature = features[0]['time_signature']

          track = [name, album, artist, release_date, duration_ms, popularity,explicit,available_markets, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
          return track

    # loop over track ids to create dataset
    tracks = []
    for i in range(0, len(ids)):
            track = getTrackFeatures(ids[i])
            tracks.append(track)
    
    df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'duration_ms', 'popularity','explicit','available_markets', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])

    nere= input("\nNereye ne olarak kaydedeyim\n")
    df.to_csv("{Path}/Spotipy/{}.csv".format(nere), sep = ',')
