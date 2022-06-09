To get a JSON file containing instruqt tracks:

```sh
curl -X POST https://play.instruqt.com/graphql \
  -H "Authorization: Bearer $INSTRUQT_TOKEN" \
  -d @tracks_query.json |jq > tracks.json
```

Where `$INSTRUQT_TOKEN` is the Instruqt API key found [here](https://play.instruqt.com/datadog/api-keys).

To generate a list of tracks in the learning-center repo:

```sh
find path/to/learning-center -type f -name track.yml |xargs grep "id:" > repo_tracks.txt
```

Once you have these files, you can run trackstar to get the full list of instruqt tracks and their corresponding learning-center repo file paths:

```sh
python3 trackstar.py|jq > result.json
```

If you need to convert this file to a csv, you can use [this online tool](https://www.convertcsv.com/json-to-csv.htm).
