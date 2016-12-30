from flask import Flask
from flask import request, Response
from flask import abort
from flask import jsonify
from functools import wraps
import settings
import subprocess
import time
import soco

app = Flask(__name__)

@app.route('/sonos/play', methods=['POST'])
def sonos_play():
    
    if (not request.json or not 'playerName' in request.json or not 'playlistName' in request.json):
        return "Invalid data", 400 

    playlistName = request.json['playlistName']
    playerName = request.json['playerName']

    speakers = soco.discover()

    if speakers:
        for speaker in soco.discover():
            print speaker.player_name
            if speaker.player_name in playerName:
                break
        else:
            speaker = None
    else:
        return "None speaker found", 404
    
    if not speaker:
        return "Speaker not found", 404
    
    return play_playlist(speaker, playlistName)

def play_playlist(speaker, playlistName):
    playlists = speaker.get_sonos_playlists()

    if playlists:
        for playlist in playlists:
            if playlist.title == playlistName:
                break
        else:
            return "Playlist {0} not found".format(playlistName), 404
    else:
        return "None playlist found", 404

    print "Clear queue"
    speaker.clear_queue()

    for song in playlist.resources:
        speaker.add_uri_to_queue(song.uri)
        
    speaker.play_from_queue(0)
    return "", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=settings.PORT, debug=settings.DEBUG)