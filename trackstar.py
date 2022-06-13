import json
import re
import csv
import os
import requests
import sys

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
            tracks[match[2]] = {'id': match[2], 'path': match[1]}

    return tracks


def delete_tracks(tracks):
    # curl -H "Authorization: Bearer $INSTRUQT_TOKEN" -X POST -d @tracks_query.json https://play.instruqt.com/graphql |jq
    token = os.environ['INSTRUQT_TOKEN']
    url = 'https://play.instruqt.com/graphql'
    headers = {'Authorization': f'Bearer {token}'}
    deleted_tracks = []
    for track in tracks:
        query = '''mutation {{
            deleteTrack(trackID: "{id}") {{
            }}
        }}'''.format(id=track['id'])
        r = requests.post(url, headers=headers, json={"query": query})
        result = 'deleted'
        if r.status_code != requests.codes.ok:
            result = 'error'
        response = r.json()
        if 'errors' in response.keys():
            sys.exit(response)
        else:
            deleted_tracks.append({'id': track['id'], 'title': track['title'], 'result': result})
    return deleted_tracks

def get_tracks_to_delete():
    tracks = []
    with open('tracks_from_sheet.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['action'] == 'delete':
                tracks.append({'id': row['id'], 'title': row['title']})
    return tracks


# tracks_to_delete = get_tracks_to_delete()
# deleted_tracks = delete_tracks(tracks_to_delete)
# print(deleted_tracks)

instruqt_tracks = get_instruqt_tracks()
repo_tracks = get_repo_tracks()

for track_id in instruqt_tracks:
   if track_id in repo_tracks:
       instruqt_tracks[track_id]['repo_path'] = repo_tracks[track_id]['path']
   else:
       instruqt_tracks[track_id]['repo_path'] = "none"

print(json.dumps(instruqt_tracks))
