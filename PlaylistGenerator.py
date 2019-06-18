import sys
import spotipy
import spotipy.util as util

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: PlaylistGenerator.py [username]")

playlist_name = "Spotipy"
token = util.prompt_for_user_token(username, scope="user-top-read")
tracks = []

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    playlist = sp.user_playlist_create(username, playlist_name, False)
    playlist_id = playlist['uri']
    ranges = ['short_term', 'medium_term', 'long_term']

    print("Gathering top tracks...")
    for range in ranges:
        results = sp.current_user_top_tracks(time_range=range, limit=50)
        for i, item in enumerate(results['items']):
            if item['id'] not in tracks:
                tracks.append(item['id'])

    print("Adding tracks to playlist...")
    while tracks:
        try:
            results = sp.user_playlist_add_tracks(username, playlist_id, tracks[:1], position=None)
        except:
            print("Error adding track!")
        tracks = tracks[1:]

    print("Playlist complete!")
else:
    print("Can't get token for", username)


