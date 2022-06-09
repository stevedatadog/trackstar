import json
import re

# Requisite files
# curl -H "Authorization: Bearer $INSTRUQT_TOKEN" -X POST -d @tracks_query.json https://play.instruqt.com/graphql |jq > tracks.json
# find ~/Code/learning-center -type f -name track.yml |xargs grep "id:" > repo_tracks.txt

def get_instruqt_tracks():
    with open('tracks.json') as f:
        data = json.load(f)

    tracks = {}

    # turn into an object with track ids as keys, track info as values
    for item in data['data']['tracks']:
      tracks[item['id']] = item

    return tracks


def get_repo_tracks():
    with open('repo_tracks.txt') as f:
        data = f.readlines()
    
    tracks = {}
    pattern = re.compile("(^.+?):id: ([a-z0-9]+)")
    
    # turn into a dict with track ids as keys, track info as values
    for line in data:
        match = pattern.match(line)
        if match:
            tracks[match[2]] = { 'id': match[2], 'path': match[1] }

    return tracks


instruqt_tracks = get_instruqt_tracks()
repo_tracks = get_repo_tracks()

for track_id in instruqt_tracks:
   if track_id in repo_tracks:
       instruqt_tracks[track_id]['repo_path'] = repo_tracks[track_id]['path']
   else:
       instruqt_tracks[track_id]['repo_path'] = "none"

print(json.dumps(instruqt_tracks))
