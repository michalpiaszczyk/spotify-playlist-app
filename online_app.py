import spotipy
from random import shuffle, choice

from online_defs import *



token = login('enter your user name', "user-read-private user-read-playback-state user-read-currently-playing user-read-recently-played playlist-modify-private playlist-modify-public user-read-recently-played user-library-read user-top-read user-follow-read", 'enter your CLIENT ID', 'enter your CLIENT secret', 'https://www.wp.pl/')

spotifyObject = spotipy.Spotify(auth=token)

#user details
user = spotifyObject.current_user()
user_country = str(user['country'])
greet(user)


######################################################################################
#playlist_based_on_current_track

try:
    playlist_based_on_current_track = []
    current_track_name, current_track_id, current_track_artist, current_track_artist_id, current_track_album, current_track_album_id = get_current_track(spotifyObject)
    introduce_current_track(current_track_name, current_track_artist, current_track_album)
    #artist top tracks
    current_track_artist_top_tracks = get_artist_top_tracks(spotifyObject, current_track_artist_id, user_country)
    get_for_main_artist(playlist_based_on_current_track, current_track_artist_top_tracks)
    #album top tracks
    try:
        add_current_album_tracks(spotifyObject, current_track_album_id, playlist_based_on_current_track)
    except:
        pass
    # similar artists choose

    chosen_similar_artists, history, saved_artists_ids, saved_tracks_ids = choose_similar_artists(spotifyObject, current_track_artist_id)
    try:
        for artist in chosen_similar_artists:
            similar_artist_top_tracks = get_artist_top_tracks(spotifyObject, artist, user_country)
            get_for_other_artists(playlist_based_on_current_track, similar_artist_top_tracks)
    except:
        pass
        
        
        #recomendation
    spotify_recomends = get_recommendations(spotifyObject, current_track_artist_id, current_track_id, user_country)
    
    spotify_recomends, chosen_recomended_artists, recomended_tracks_artists_ids = choose_recommended_artists(history, saved_artists_ids, spotify_recomends)

    is_following_recomended = spotifyObject.current_user_following_artists(ids=recomended_tracks_artists_ids)
    followed_recomended_artists = [id for id, artist in zip(recomended_tracks_artists_ids, is_following_recomended) if artist]
    chosen_recomended_artists.extend(followed_recomended_artists)
    chosen_recomended_artists = list(set(chosen_recomended_artists))
    
    for artist in chosen_recomended_artists:
        recomended_artist_top_tracks = get_artist_top_tracks(spotifyObject, artist, user_country)
        get_for_other_artists(playlist_based_on_current_track, recomended_artist_top_tracks)

    add_recomended_tracks(playlist_based_on_current_track, spotify_recomends, history, saved_tracks_ids)
    get_for_recommended(playlist_based_on_current_track, spotify_recomends)

    playlist_based_on_current_track_filtered = unique(playlist_based_on_current_track)
    playlist_based_on_current_track_filtered = playlist_based_on_current_track_filtered[:50]

    shuffle(playlist_based_on_current_track_filtered)
    print("My first playlist for you is: ")
    for i in playlist_based_on_current_track_filtered:
        print(f"{i['name']} by {i['artists'][0]['name']}")
    
    playlist_ids = [x["id"] for x in playlist_based_on_current_track_filtered]
    answer = input("Do you want to create a playlist? (y/n)\n")
    if answer.lower() == "y":
        spotifyObject.user_playlist_add_tracks(user['id'], spotifyObject.user_playlist_create(user['id'], 'current track', public=False, collaborative=False, description='')["id"],playlist_ids, position=None)
except:
    print("Nothing to show about current track")
    history = spotifyObject.current_user_recently_played(limit=50, after=None, before=None)["items"]
    saved = spotifyObject.current_user_saved_tracks(limit=50, offset=0, market=None)["items"]
    saved_artists_ids = [x["track"]["artists"][0]["id"] for x in saved]
    saved_tracks_ids = [x["track"]["id"] for x in saved]

# end of current track block
#############################################################################################################################


print("Chose playlist based on your favourite: \n Artist ('A') \n Songs ('S'). \n Your preferences ('P'). You can also close the app ('C') ")
user_choice="0"
while user_choice[0].lower() == "0":
    user_choice = input("Choose an option A - Artists, S - Songs, P - Your preferences, C - Close the app \n")

    ##################################
    ## artist block

    if user_choice[0].lower() == 'a':
        print("This is my playlist with your best artists. You can save it ('S'), edit it ('E') or dismiss it ('D').")
        
        #ARTIST MAKE#
        playlist_based_on_artist = []
        chosen_top_artists, top_artists_short, top_artists_medium, top_artists_long = top_artists_chose(spotifyObject)
        chosen_top_artists_ids = [i['id'] for i in chosen_top_artists]

        for id in chosen_top_artists_ids:
            artist_top_tracks = get_artist_top_tracks(spotifyObject, id, user_country)
            get_for_main_artist(playlist_based_on_artist, artist_top_tracks)

        artist_id1 = choice(chosen_top_artists_ids)
        artist_id2 = choice(chosen_top_artists_ids)
        while artist_id1 == artist_id2:
            artist_id2 = choice(chosen_top_artists_ids)
        artist_id3 = choice(chosen_top_artists_ids)
        while artist_id1 == artist_id3 or artist_id2 == artist_id3:
            artist_id3 = choice(chosen_top_artists_ids)
        try:
            genre = choice(chosen_top_artists)["genres"][0]
        except:
            genre=[]
        track_id = choice(playlist_based_on_artist)["id"]

        recomended_tracks_based_on_top_artists = spotifyObject.recommendations(seed_artists=[artist_id1, artist_id2, artist_id3], seed_genres=[genre], seed_tracks=[track_id], limit=50, country=user_country)["tracks"]
        
        spotify_recomends, chosen_recomended_artists, recomended_tracks_artists_ids = choose_recommended_artists(history, saved_artists_ids, recomended_tracks_based_on_top_artists)
        
        is_following_recomended = spotifyObject.current_user_following_artists(ids=recomended_tracks_artists_ids)
        followed_recomended_artists = [id for id, artist in zip(recomended_tracks_artists_ids, is_following_recomended) if artist]
        chosen_recomended_artists.extend(followed_recomended_artists)
        chosen_recomended_artists = list(set(chosen_recomended_artists))
            
        for artist in chosen_recomended_artists:
            recomended_artist_top_tracks = get_artist_top_tracks(spotifyObject, artist, user_country)
            get_for_other_artists(playlist_based_on_artist, recomended_artist_top_tracks)
        add_recomended_tracks(playlist_based_on_artist, recomended_tracks_based_on_top_artists, history, recomended_tracks_artists_ids)
        get_for_recommended_more(playlist_based_on_artist, recomended_tracks_based_on_top_artists)

        playlist_based_on_artist = unique(playlist_based_on_artist)
        shuffle(playlist_based_on_artist)
        playlist_based_on_artist = playlist_based_on_artist[:50]

        print("My top artist playlist for you is: \n")
        for i in playlist_based_on_artist:
            print(f"{i['name']} by {i['artists'][0]['name']}")

        artist_answer = input("Do you want to save, edit or dismiss this playlist? ('S', 'E' or 'D')\n")

        if artist_answer[0].lower() == 's':
            print("Saving...")
            playlist_ids = [x["id"] for x in playlist_based_on_artist]
            spotifyObject.user_playlist_add_tracks(user['id'], spotifyObject.user_playlist_create(user['id'], 'top artists', public=False, collaborative=False, description='')["id"],playlist_ids, position=None)
            print("Saved!")
            user_choice="0"
        #END OF ARTIST MAKE#

        elif artist_answer[0].lower() == 'e':
            #ARTIST EDIT#
            playlist_based_on_artist = []
            print("\nYour latest favourite artists are (1): \n")
            for artist in top_artists_short[:10]:
                print(artist["name"])
            print("\nYour favourite artists lately are (2): \n")
            for artist in top_artists_medium[:10]:
                print(artist["name"])
            print("\nYour all time favourite artists are (3): \n")
            for artist in top_artists_long[:10]:
                print(artist["name"])
            
            a_choice=0
            while a_choice==0:
                a_choice = input("\nWhich fit your mood right now? (1,2,3) \n")
                if a_choice == "1":
                    a_choice = top_artists_short
                elif a_choice == '2':
                    a_choice = top_artists_medium
                elif a_choice == '3':
                    a_choice = top_artists_long
                else:
                    a_choice = 0
                
            chosen_top_artists = choose_artists(a_choice)
            chosen_top_artists_ids = [i['id'] for i in chosen_top_artists]

            for id in chosen_top_artists_ids:
                artist_top_tracks = get_artist_top_tracks(spotifyObject, id, user_country)
                get_for_main_artist(playlist_based_on_artist, artist_top_tracks)

            artist_id1 = choice(chosen_top_artists_ids)
            artist_id2 = choice(chosen_top_artists_ids)
            while artist_id1 == artist_id2:
                artist_id2 = choice(chosen_top_artists_ids)
            artist_id3 = choice(chosen_top_artists_ids)
            while artist_id1 == artist_id3 or artist_id2 == artist_id3:
                artist_id3 = choice(chosen_top_artists_ids)

            genre = choice(chosen_top_artists)["genres"][0]
            track_id = choice(playlist_based_on_artist)["id"]

            recomended_tracks_based_on_top_artists = spotifyObject.recommendations(seed_artists=[artist_id1, artist_id2, artist_id3], seed_genres=[genre], seed_tracks=[track_id], limit=50, country=user_country)["tracks"]
            
            spotify_recomends, chosen_recomended_artists, recomended_tracks_artists_ids = choose_recommended_artists(history, saved_artists_ids, recomended_tracks_based_on_top_artists)
            
            is_following_recomended = spotifyObject.current_user_following_artists(ids=recomended_tracks_artists_ids)
            followed_recomended_artists = [id for id, artist in zip(recomended_tracks_artists_ids, is_following_recomended) if artist]
            chosen_recomended_artists.extend(followed_recomended_artists)
            chosen_recomended_artists = list(set(chosen_recomended_artists))
                
            for artist in chosen_recomended_artists:
                recomended_artist_top_tracks = get_artist_top_tracks(spotifyObject, artist, user_country)
                get_for_other_artists(playlist_based_on_artist, recomended_artist_top_tracks)

            #add recomended tracks - z historii i saved
            add_recomended_tracks(playlist_based_on_artist, recomended_tracks_based_on_top_artists, history, saved_tracks_ids)
            get_for_recommended_more(playlist_based_on_artist, recomended_tracks_based_on_top_artists)

            playlist_based_on_artist = unique(playlist_based_on_artist)
            shuffle(playlist_based_on_artist)
            playlist_based_on_artist = playlist_based_on_artist[:50]

            print("My top artist playlist for you is: \n")
            for i in playlist_based_on_artist:
                print(f"{i['name']} by {i['artists'][0]['name']}")

            artist_answer = input("Do you want to save or dismiss this playlist? ('S', 'E' or 'D')\n")
            if artist_answer[0].lower() == 's':
                print("Saving...")
                playlist_ids = [x["id"] for x in playlist_based_on_artist]
                spotifyObject.user_playlist_add_tracks(user['id'], spotifyObject.user_playlist_create(user['id'], 'top artists edited', public=False, collaborative=False, description='')["id"],playlist_ids, position=None)
                print("Saved!")
                user_choice="0"
            else:
                user_choice="0"
            #END OF ARTIST EDIT#
        else:
            user_choice="0"
            ##END OF ARTIST BLOCK########
    ##############################################################################################################
    ###SONG BLOCK#######   
        
    elif user_choice[0].lower() == 's':
        
        chosen_top_tracks = based_on_songs(spotifyObject)
        track_ids = []
        for i in range(5):
            track_id = choice(chosen_top_tracks)["id"]
            track_ids.append(track_id)

        recomended_tracks_based_on_top_tracks = spotifyObject.recommendations(seed_artists=[], seed_genres=[], seed_tracks=track_ids, limit=50, country=user_country)["tracks"]
        
        add_recomended_tracks(chosen_top_tracks, recomended_tracks_based_on_top_tracks, history, saved_tracks_ids)

        get_for_recommended_more(chosen_top_tracks, recomended_tracks_based_on_top_tracks)

        try:
            chosen_top_tracks = unique(chosen_top_tracks)
        except:
            pass

        shuffle(chosen_top_tracks)
        chosen_top_tracks = chosen_top_tracks[:50]
        print("My playlist for you:")
        for track in chosen_top_tracks:
            print(f'{track["name"]} by {track["artists"][0]["name"]}')
        
        songs_answer = input("Do you want to save or dismiss this playlist? ('S', 'E' or 'D')\n")
        if songs_answer[0].lower() == 's':
            print("Saving...")
            playlist_ids = [x["id"] for x in chosen_top_tracks]
            spotifyObject.user_playlist_add_tracks(user['id'], spotifyObject.user_playlist_create(user['id'], 'my best tracks', public=False, collaborative=False, description='')["id"],playlist_ids, position=None)
            print("Saved")
            user_choice = "0"
            
        elif songs_answer[0].lower() == 'e':
            
            ### songs edit###
            chosen_top_tracks = []
            short_top_tracks = spotifyObject.current_user_top_tracks(limit=50, offset=0, time_range='short_term')['items']
            medium_top_tracks = spotifyObject.current_user_top_tracks(limit=50, offset=0, time_range='medium_term')['items']
            long_top_tracks = spotifyObject.current_user_top_tracks(limit=50, offset=0, time_range='long_term')['items']
            print("\nYour latest favourite tracks are (1): \n")
            for track in short_top_tracks[:20]:
                print(f'{track["name"]} by {track["artists"][0]["name"]}')
            print("\nYour favourite tracks lately are (2): \n")
            for track in medium_top_tracks[:20]:
                print(f'{track["name"]} by {track["artists"][0]["name"]}')
            print("\nYour all time favourite tracks are (3): \n")
            for track in long_top_tracks[:20]:
                print(f'{track["name"]} by {track["artists"][0]["name"]}')

            t_choice=0
            while t_choice==0:
                t_choice = input("\nWhich fit your mood right now? (1,2,3) \n")
                if t_choice == "1":
                    chosen_top_tracks = short_top_tracks
                elif t_choice == '2':
                    chosen_top_tracks = medium_top_tracks
                elif t_choice == '3':
                    chosen_top_tracks = long_top_tracks
                else:
                    t_choice = 0
            track_ids = []
            for i in range(5):
                track_id = choice(chosen_top_tracks)["id"]
                track_ids.append(track_id)

            recomended_tracks_based_on_top_tracks = spotifyObject.recommendations(seed_artists=[], seed_genres=[], seed_tracks=track_ids, limit=50, country=user_country)["tracks"]
            #add recomended tracks - z historii i saved
            add_recomended_tracks(chosen_top_tracks, recomended_tracks_based_on_top_tracks, history, saved_tracks_ids)
            get_for_recommended_more(chosen_top_tracks, recomended_tracks_based_on_top_tracks)
            try:
                chosen_top_tracks = unique(chosen_top_tracks)
            except:
                pass
            shuffle(chosen_top_tracks)
            chosen_top_tracks = chosen_top_tracks[:50]

            print("My playlist for you:")
            for track in chosen_top_tracks:
                print(f'{track["name"]} by {track["artists"][0]["name"]}')
            songs_answer = input("Do you want to save or dismiss this playlist? ('S' or 'D')\n")
            if songs_answer[0].lower() == 's':
                print("Saving...")
                playlist_ids = [x["id"] for x in chosen_top_tracks]
                spotifyObject.user_playlist_add_tracks(user['id'], spotifyObject.user_playlist_create(user['id'], 'my best tracks - edited', public=False, collaborative=False, description='')["id"],playlist_ids, position=None)
                print("Saved")
                user_choice = "0"
            else:
                user_choice = "0"
            ## koniec songs edit###        
        else:
            user_choice = "0"
    elif user_choice[0].lower() == 'p':
        print("Preferences")
        print("Let's play with spotify recomendations. You can propose up to 5 artists/tracks and I'll do the magic for you")
        artists = input("Type up to 5 artists (separated with coma ',') leave blank to skip\n")
        if len(artists) > 0:
            artists = artists.split(",")
            artists = [item.strip() for item in artists]
            if len(artists) > 5:
                artists = artists[:5]
        if len(artists) < 5:
            tracks_available = 5 - len(artists)
            tracks = input(f"Type up to {tracks_available} tracks (separated with coma ',') leave blank to skip\n")
            if len(tracks) > 0:
                tracks = tracks.split(",")
                tracks = [item.strip() for item in tracks]
                if len(tracks) > tracks_available:
                    tracks = tracks[:tracks_available]
        else:
            tracks=[]
        if len(artists) == 0 and len(tracks) == 0:
            print("Thank you")
            user_choice = "0"
        else:
            artists = [spotifyObject.search(item, limit=1, offset=0,type="artist",market=None) for item in artists]
            tracks = [spotifyObject.search(item, limit=1, offset=0,type="track",market=None) for item in tracks]
            a_lenght = len(artists)+len(tracks)
            genres =[]
            if a_lenght < 5 and len(artists)>0:
                space_available = 5 - a_lenght
                artist_for_genres = choice(artists)
                genres = artist_for_genres['artists']['items'][0]['genres']
                if len(genres)>space_available:
                    genres = genres[:space_available]
            
            artists_ids = [artist['artists']['items'][0]['id'] for artist in artists]
            tracks_ids = [track['tracks']['items'][0]['id'] for track in tracks]
            user_choice_playlist = spotifyObject.recommendations(seed_artists=artists_ids, seed_genres=genres, seed_tracks=tracks_ids, limit=50, country=user_country)["tracks"]
            
            #wcześniej dodać wyświetlanie playlisty
            tracks = [track["tracks"]["items"][0] for track in tracks]
            user_choice_playlist.extend(tracks)

            for artist_id in artists_ids:
                artist_top_tracks = spotifyObject.artist_top_tracks(artist_id, country=user_country)["tracks"]
                user_choice_playlist.extend(artist_top_tracks)
            
            unique(user_choice_playlist)
            shuffle(user_choice_playlist)
            user_choice_playlist = user_choice_playlist[:50]
            print("\nMy playlist for you is: ")
            for i in user_choice_playlist:
                print(f"{i['name']} by {i['artists'][0]['name']}")

            save = input("Do you want to save (S) or dismiss playlist(D)?\n ")
            if save[0].lower() == "s":
                print("Saving...")
                
                user_choice_playlist = [track["id"] for track in user_choice_playlist]
                spotifyObject.user_playlist_add_tracks(user['id'], spotifyObject.user_playlist_create(user['id'], 'my choice playlist', public=False, collaborative=False, description='')["id"],user_choice_playlist, position=None)
                print("Saved")
                user_choice="0"
            else:
                print("Thank you")
                user_choice="0"
    else:
        print("Thank you. Closing...")
        pass

###############################################################################################################################

# os.remove(f'.cache-{username}')