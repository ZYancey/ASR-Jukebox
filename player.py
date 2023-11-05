import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

scope = "user-read-playback-state,user-modify-playback-state,playlist-modify-public,playlist-modify-private," \
        "playlist-read-private "
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def queue(artist, size):
    if artist:
        search_str = artist
    else:
        search_str = 'Lorde'

    result = sp.search(search_str, 1, 0, 'artist')

    try:
        # extract the id
        id = result['artists']['items'][0]['id']
    except IndexError:
        print(f"No artists found for '{search_str}'.")
        return

    results = sp.artist_top_tracks(id)
    print(results)
    for track in results['tracks'][:size]:
        sp.add_to_queue(track['uri'])
        print('track    : ' + track['name'])
        print('artist   : ' + track['artists'][0]['name'])


def like():
    results = sp.currently_playing()
    if results is not None:
        print(results)
        track = results['item']['id']
        print(track)
        sp.playlist_add_items('5yKXBGfHT2isg9EkQI11xP', [track])


def toggle_repeat():
    results = sp.currently_playing()
    if results is not None:
        print(results)
        type = results['currently_playing_type']
        if type == 'track':
            sp.repeat('context')
        else:
            sp.repeat('track')


def play():
    results = sp.currently_playing()
    if results is not None:
        isPlaying = results['is_playing']
        if isPlaying:
            sp.pause_playback()
        else:
            sp.start_playback()


def pause():
    results = sp.currently_playing()
    if results is not None:
        isPlaying = results['is_playing']
        if isPlaying:
            sp.pause_playback()
        else:
            sp.start_playback()


def previous():
    sp.previous_track()


def next():
    sp.next_track()


def np():
    track = ''
    artist = ''
    art = ''
    progress = 0.0
    isPlaying = True

    results = sp.currently_playing()
    if results is not None:
        track = results['item']['name']
        artist = results['item']['album']['artists'][0]['name']
        progress = int(results['progress_ms']) / int(results['item']['duration_ms'])
        art = results['item']['album']['images'][0]['url']
        isPlaying = results['is_playing']

    return track, art, artist, progress, isPlaying
