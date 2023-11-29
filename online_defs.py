import os
from random import shuffle
from spotipy import util
def login(username, scope, client_id,client_secret,redirect_uri):
    try:
        token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
    except:
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
    return token

def greet(user):
    display_name = user["display_name"]
    print(f"Witaj {display_name}!")

def get_current_track(spotifyObject):
    
    current_track = spotifyObject.current_user_playing_track()
    current_track_name = current_track["item"]["name"]
    current_track_id = current_track["item"]["id"]
    current_track_artist = current_track["item"]["artists"][0]["name"]
    current_track_artist_id = current_track["item"]["artists"][0]["id"]
    current_track_album = current_track["item"]["album"]["name"]
    current_track_album_id = current_track["item"]["album"]["id"]
    return current_track_name, current_track_id, current_track_artist,current_track_artist_id, current_track_album, current_track_album_id
        

def introduce_current_track(current_track_name, current_track_artist, current_track_album):
    try:
        print(f"Now playing: {current_track_name} by {current_track_artist} from the album {current_track_album}\n")
    except:
        print("Nothing to show about current track")

def get_artist_top_tracks(spotifyObject, artist_id, user_country):
    artist_top_tracks = spotifyObject.artist_top_tracks(artist_id, country=user_country)
    artist_top_tracks = artist_top_tracks["tracks"]
    artist_top_tracks = [{
        "album": {
            "name": item["album"]["name"]
        },
        "artists": [
            {
                "name": item["album"]["artists"][0]["name"],
                "id": item["album"]["artists"][0]["id"]
            }
        ],
        "name": item["name"],
        "popularity": item["popularity"],
        "uri": item["uri"],
        "id": item["id"]
    } for item in artist_top_tracks]
    return artist_top_tracks


def get_for_main_artist (returned_playlist, top_tracks_playlist):
    shuffle(top_tracks_playlist)
    for i in range(3):
        try:
            a = top_tracks_playlist.pop()
            returned_playlist.append(a)
        except:
            pass

    top_tracks_playlist = sorted(top_tracks_playlist, key=lambda k: k['popularity'], reverse=False)
    for i in range(3):
        try:
            a = top_tracks_playlist.pop()
            returned_playlist.append(a)
        except:
            pass
    return returned_playlist

def get_for_other_artists(returned_playlist, top_tracks_playlist):
    shuffle(top_tracks_playlist)
    for i in range(2):
        try:
            a = top_tracks_playlist.pop()
            returned_playlist.append(a)
        except:
            pass

    top_tracks_playlist = sorted(top_tracks_playlist, key=lambda k: k['popularity'], reverse=False)
    for i in range(2):
        try:
            a = top_tracks_playlist.pop()
            returned_playlist.append(a)
        except:
            pass
    return returned_playlist

def get_for_recommended(returned_playlist, top_tracks_playlist):
    shuffle(top_tracks_playlist)
    for i in range(2):
        a = top_tracks_playlist.pop()
        returned_playlist.append(a)

    top_tracks_playlist = sorted(top_tracks_playlist, key=lambda k: k['popularity'], reverse=False)
    for i in range(2):
        a = top_tracks_playlist.pop()
        returned_playlist.append(a)
    return returned_playlist


def choose_similar_artists(spotifyObject, artist_id):
    chosen_similar_artists =[]
    curent_track_artist_similar_artist = spotifyObject.artist_related_artists(artist_id)
    curent_track_artist_similar_artist = curent_track_artist_similar_artist["artists"]
    history = spotifyObject.current_user_recently_played(limit=50, after=None, before=None)["items"]

    for x in curent_track_artist_similar_artist:
        for y in history:
            if x["id"]==y["track"]["artists"][0]["id"]:
                chosen_similar_artists.append(x)
            else: 
                continue
    
    saved = spotifyObject.current_user_saved_tracks(limit=50, offset=0, market=None)["items"]
    saved_artists_ids = [x["track"]["artists"][0]["id"] for x in saved]
    saved_tracks_ids = [x["track"]["id"] for x in saved]
    for x in curent_track_artist_similar_artist:
        for y in saved_artists_ids:
            if x["id"]==y:
                chosen_similar_artists.append(x)
            else:
                continue
    
    if len(chosen_similar_artists) < 2:
        shuffle(curent_track_artist_similar_artist)
        for i in range(1):
            try:
                chosen_artist = curent_track_artist_similar_artist.pop()
                chosen_similar_artists.append(chosen_artist)
            except:
                pass
        curent_track_artist_similar_artist= sorted(curent_track_artist_similar_artist, key=lambda k: k['popularity'], reverse=False)
        for i in range(1):
            try:
                chosen_artist = curent_track_artist_similar_artist.pop()
                chosen_similar_artists.append(chosen_artist)
            except:
                pass
        chosen_similar_artists = [x["id"] for x in chosen_similar_artists]
    return chosen_similar_artists, history, saved_artists_ids, saved_tracks_ids


def add_current_album_tracks(spotifyObject,album_id, returned_playlist):
    current_album_tracks = spotifyObject.album_tracks(album_id, limit=50, offset=0, market=None)
    current_album_tracks = current_album_tracks['items']
    for i in range(2):
        chosen_album_track = current_album_tracks.pop()
        returned_playlist.append(chosen_album_track)
    return returned_playlist

def get_recommendations(spotifyObject, artist_id, track_id, user_country):
    try:
        current_artist_genre1 = spotifyObject.artist(artist_id)['genres'][0]
        current_artist_genre2 = spotifyObject.artist(artist_id)['genres'][1]
        track_id2 = spotifyObject.artist_top_tracks(artist_id, country=user_country)["tracks"][0]["id"]
        recomended_tracks = spotifyObject.recommendations(seed_artists=[artist_id], seed_genres=[current_artist_genre1, current_artist_genre2], seed_tracks=[track_id, track_id2], limit=30, country=user_country)["tracks"]
    except:
        try:
            current_artist_genre1 = spotifyObject.artist(artist_id)['genres'][0]
            
            track_id2 = spotifyObject.artist_top_tracks(artist_id, country=user_country)["tracks"][0]["id"]
            recomended_tracks = spotifyObject.recommendations(seed_artists=[artist_id], seed_genres=[current_artist_genre1], seed_tracks=[track_id, track_id2], limit=30, country=user_country)["tracks"]
        except:
            track_id2 = spotifyObject.artist_top_tracks(artist_id, country=user_country)["tracks"][0]["id"]
            recomended_tracks = spotifyObject.recommendations(seed_artists=[artist_id], seed_tracks=[track_id, track_id2], limit=30, country=user_country)["tracks"]
    
    
    recomended_tracks = [
        {
            "artists": [{"name": track["artists"][0]["name"], "id":track["artists"][0]["id"]}],
            "name": track["name"],
            "popularity": track["popularity"],
            "id": track["id"],
        }
        for track in recomended_tracks
    ]
    return recomended_tracks


def add_recomended_tracks(returned_playlist, recomendation_playlist, history, saved_tracks_ids):
    recomended_tracks_ids = [x["id"] for x in recomendation_playlist]
    for x in recomended_tracks_ids:
        for y in history:
            if x == y["track"]["id"] and x not in returned_playlist:
                returned_playlist.append(x)
            else:
                continue
    for x in recomended_tracks_ids:
        for y in saved_tracks_ids:
            if x == y and x not in returned_playlist:
                returned_playlist.append(x)
            else:
                continue

def choose_recommended_artists(history, saved_artists_ids, spotify_recomends):
    chosen_recomended_artists = []
    recomended_tracks_artists_ids = [x["artists"][0]["id"] for x in spotify_recomends]
    for x in recomended_tracks_artists_ids:
        for y in history:
            if x == y["track"]["artists"][0]["id"] and x not in chosen_recomended_artists:
                chosen_recomended_artists.append(x)
            else:
                continue
    for x in recomended_tracks_artists_ids:
        for y in saved_artists_ids:
            if x == y and x not in chosen_recomended_artists:
                chosen_recomended_artists.append(x)
            else:
                continue
    if len(chosen_recomended_artists) < 2:
        shuffle(spotify_recomends)
        x=spotify_recomends.pop()
        a=x["artists"][0]["id"]
        chosen_recomended_artists.append(a)
        spotify_recomends = sorted(spotify_recomends, key=lambda k: k['popularity'], reverse=True)
        x=spotify_recomends.pop()
        a=x["artists"][0]["id"]
        chosen_recomended_artists.append(a)
    return spotify_recomends,chosen_recomended_artists,recomended_tracks_artists_ids
######################################################################################################################################
# unique
def unique(playlist):
    unique_items = {}
    for item in playlist:
        track_id = item["id"]
        if track_id not in unique_items:
            unique_items[track_id] = item
    playlist = list(unique_items.values())
    return playlist
######################################################################################################################################
#based on artists

def top_artists_chose(spotifyObject):
    top_artists_short = spotifyObject.current_user_top_artists(limit=20, offset=0, time_range='short_term')['items']
    top_artists_short_copy = top_artists_short

    top_artists_medium = spotifyObject.current_user_top_artists(limit=20, offset=0, time_range='medium_term')['items']
    top_artists_medium_copy = top_artists_medium

    top_artists_long = spotifyObject.current_user_top_artists(limit=20, offset=0, time_range='long_term')['items']
    top_artists_long_copy = top_artists_long


    chosen_top_artists = top_artists_short[:2]+top_artists_medium[:2]+top_artists_long[:2]
    del top_artists_short[:2]
    del top_artists_medium[:2]
    del top_artists_long[:2]



    shuffle(top_artists_short)
    shuffle(top_artists_medium)
    shuffle(top_artists_long)

    for i in range(2):
        try:
            chosen_artist = top_artists_short.pop()
            chosen_top_artists.append(chosen_artist)
        except:
            pass

    for i in range(2):
        try:
            chosen_artist = top_artists_medium.pop()
            chosen_top_artists.append(chosen_artist)
        except:
            pass

    for i in range(2):
        try:
            chosen_artist = top_artists_long.pop()
            chosen_top_artists.append(chosen_artist)
        except:
            pass

    top_artists_short= sorted(top_artists_short, key=lambda k: k['popularity'], reverse=False)
    top_artists_medium= sorted(top_artists_medium, key=lambda k: k['popularity'], reverse=False)
    top_artists_long= sorted(top_artists_long, key=lambda k: k['popularity'], reverse=False)

    for i in range(2):
        try:
            chosen_artist = top_artists_short.pop()
            chosen_top_artists.append(chosen_artist)
        except:
            pass

    for i in range(2):
        try:
            chosen_artist = top_artists_medium.pop()
            chosen_top_artists.append(chosen_artist)
        except:
            pass

    for i in range(2):
        try:
            chosen_artist = top_artists_long.pop()
            chosen_top_artists.append(chosen_artist)
        except:
            pass

    unique_items = {}
    for item in chosen_top_artists:
        artist_id = item["id"]
        if artist_id not in unique_items:
            unique_items[artist_id] = item
    chosen_top_artists = list(unique_items.values())    
    return chosen_top_artists, top_artists_short_copy, top_artists_medium_copy, top_artists_long_copy

def choose_artists(a_choice):
    chosen_top_artists = []
    shuffle(a_choice)
    for i in range(5):
        chosen_artist = a_choice.pop()
        chosen_top_artists.append(chosen_artist)

    a_choice = sorted(a_choice, key=lambda k: k['popularity'], reverse=False)
    for i in range(5):
        chosen_artist = a_choice.pop()
        chosen_top_artists.append(chosen_artist)
    return chosen_top_artists

def get_for_recommended_more(returned_playlist, top_tracks_playlist):
    shuffle(top_tracks_playlist)
    for i in range(5):
        a = top_tracks_playlist.pop()
        returned_playlist.append(a)

    top_tracks_playlist = sorted(top_tracks_playlist, key=lambda k: k['popularity'], reverse=False)
    for i in range(5):
        a = top_tracks_playlist.pop()
        returned_playlist.append(a)
    return returned_playlist

###################################################################################################################
###based on tracks###

def based_on_songs(spotifyObject):
    short_top_tracks = spotifyObject.current_user_top_tracks(limit=20, offset=0, time_range='short_term')['items']
    medium_top_tracks = spotifyObject.current_user_top_tracks(limit=20, offset=0, time_range='medium_term')['items']
    long_top_tracks = spotifyObject.current_user_top_tracks(limit=20, offset=0, time_range='long_term')['items']

    chosen_top_tracks = short_top_tracks[:6] + medium_top_tracks[:6] + long_top_tracks[:6]
    del short_top_tracks[:6]
    del medium_top_tracks[:6]
    del long_top_tracks[:6]

    shuffle(short_top_tracks)
    shuffle(medium_top_tracks)
    shuffle(long_top_tracks)

    for i in range(6):
            try:
                chosen_track = short_top_tracks.pop()
                chosen_top_tracks.append(chosen_track)
            except:
                pass

    for i in range(6):
        try:
            chosen_track = medium_top_tracks.pop()
            chosen_top_tracks.append(chosen_track)
        except:
            pass

    for i in range(6):
        try:
            chosen_track = long_top_tracks.pop()
            chosen_top_tracks.append(chosen_track)
        except:
            pass

    short_top_tracks= sorted(short_top_tracks, key=lambda k: k['popularity'], reverse=False)
    medium_top_tracks= sorted(medium_top_tracks, key=lambda k: k['popularity'], reverse=False)
    long_top_tracks= sorted(long_top_tracks, key=lambda k: k['popularity'], reverse=False)

    for i in range(6):
        try:
            chosen_track = short_top_tracks.pop()
            chosen_top_tracks.append(chosen_track)
        except:
            pass

    for i in range(6):
        try:
            chosen_track = medium_top_tracks.pop()
            chosen_top_tracks.append(chosen_track)
        except:
            pass

    for i in range(6):
        try:
            chosen_track = long_top_tracks.pop()
            chosen_top_tracks.append(chosen_track)
        except:
            pass
    return chosen_top_tracks