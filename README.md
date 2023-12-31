# spotify-playlist-app
Python code to create spotify playlist based on current track, your best artists, songs and your preferences

**1. Description**

This project is designed to create playlists on your Spotify account. It pulls in information about the tracks you are currently listening to, your favourite artists and your favourite songs to create personalised playlist recommendations. These suggestions can be edited and tailored to suit individual preferences. Users can also create recommended playlists based on their music tastes

**2. Instalation**
  
  2.1 To run this code you need to install Spotipy.
  run pip install spotipy
  More information about Spotipy: https://spotipy.readthedocs.io
  I used spotipy == 2.23.0
  
  2.2 To run this code you need to register on https://developer.spotify.com/ and create your own app
  
  ![2023-11-29](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/9abc9d5f-d6fb-478c-a7ad-ebdfada053e5)

2.3 To run this code you need to provide your username, client ID and client secret in line 8 of online_app.py

User name:

![user_id2](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/e07f8b16-f004-4279-89b1-dde2fc399d38)

Client ID and Client Secret:
![clientID](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/8e142c4b-5544-4208-8ce6-00c6769f0688)


**3. Running application and granting access:**

3.1 Once you installed and provided information you may run the application.

3.2 You will be redirected to usual login site. Login as always
![2023-11-30 (1)](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/b83c5e2b-c999-44ee-a6ab-3c9970d65f55)

3.3 Then you have to grant access to your account
![2023-11-30 (2)](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/2a569cf7-8c26-488f-81e4-2e6185ce9e49)

3.4 You will be redirected to www.wp.pl Copy adress of the site and paste it into python
![2023-11-30 (3)](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/9b5b71fa-a9aa-4067-910e-3a40240d422a)
![2023-11-30 (4)](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/5bbf2f4a-51d2-4b3c-833b-178803148786)

3.5 This will store cache file in your system and login will no longer be needed. You may delete the cache after using the app.
![2023-11-30 (5)](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/31a9660f-690a-4027-845b-22cae30daa79)

**4. Using app**
1. Run the online_app.py
2. If you are listening to a song, first playlist will be proposed

![01](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/d9ef9673-ec06-4373-ab11-4476b882be1e)

3. You can save it to your account or not
4. Then you will be asked what to base the next suggestions on

![02](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/fee2bd92-f697-48a8-8623-0b467cdc5764)

5. Playlist based on artist and on songs can be edited. You will be proposed which songs/asrtist you'd like to have in your playlist

![04](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/213adb58-8b55-4fae-a4c7-2fc80c7c2a31)


6. Finally, you may write your own preferences for next playlist

![06](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/38174f72-aeba-4e86-8466-bb335699fbb1)

7. Everytime when you hit to save - the playlist will be added to your account

![05](https://github.com/michalpiaszczyk/spotify-playlist-app/assets/112171020/8226c5aa-3a34-4288-889a-e3b29eb69255)









   



