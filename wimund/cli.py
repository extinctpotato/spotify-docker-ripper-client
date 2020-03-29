import json
from prettytable import PrettyTable
from wimund.client import WimundClient
from pygments import highlight, lexers, formatters

def pretty_list_of_dicts(json, numbered=False):
    ptable = PrettyTable()
    if numbered:
        ptable.field_names = ['id'] + list(json[0].keys())
        id = 0
    else:
        ptable.field_names = json[0].keys()


    for i in json:
        if numbered:
            values = [id] + list(i.values())
            id += 1 
        else:
            values = list(i.values())
        ptable.add_row(values)

    print(ptable)

class CLI:
    def __init__(self, url="http://localhost:9000", user=None, password=None):
        self.client = WimundClient(url, user, password)

    def test(self):
        j = self.client.dispatch_track("test")
        jj = json.dumps(j, ensure_ascii=False, sort_keys=True, indent=4)
        colorful_json = highlight(jj, lexers.JsonLexer(), formatters.TerminalFormatter())
        print(colorful_json)

    def status(self):
        j = self.client.status()
        jj = json.dumps(j, ensure_ascii=False, sort_keys=True, indent=4)
        colorful_json = highlight(jj, lexers.JsonLexer(), formatters.TerminalFormatter())
        print(colorful_json)

    def search(self, query, dispatch=False, full=False):
        if full:
            j = self.client.search(query, full=True)
            jj = json.dumps(j, ensure_ascii=False, sort_keys=True, indent=4)
            colorful_json = highlight(jj, lexers.JsonLexer(), formatters.TerminalFormatter())
            print(colorful_json)
            return None
        else:
            j = self.client.search(query, full=False)['results']

        ptable = PrettyTable()

        ptable.field_names = ['id', 'artist', 'title']

        id = 0

        for res in j:
            artists = ", ".join(res['artists'])
            values = [id, artists, res['title']]

            ptable.add_row(values)

            id += 1

        print(ptable)

        if not dispatch:
            return None

        picked = False

        while not picked:
            pick = input("Pick a track to dispatch. [0-{}] ".format(id-1))
            try:
                pick_int = int(pick)
            except ValueError:
                print("I don't want a string!")
                pick_int = None
            if pick_int in range(0, id):
                picked = True

        print("Dispatching track_id: {}...".format(j[pick_int]['track_id']))
        response = self.client.dispatch_track(j[pick_int]['track_id'])
        print("Job ID: {}".format(response.get('job')))
        print("Message: {}".format(response.get('msg')))

    def spotifyctl(self, operation):
        if operation == 'start':
            print("Starting Spotify...")
            resp = self.client.spotify_start()
            print("Response: {}".format(resp.get('msg')))
        elif operation == 'stop':
            print("Stopping Spotify...")
            resp = self.client.spotify_stop()
            print("Response: {}".format(resp.get('msg')))
        else:
            print("Unknown operation.")

    def list_logs(self, download=False):
        json = self.client.list_logs()
        count = json['count']-1
        
        if not download:
            pretty_list_of_dicts(json['logs'])
            return None
        else:
            pretty_list_of_dicts(json['logs'], True)

            picked = False

            while not picked:
                if count > 0:
                    pick_msg = "Pick a log file to show. [0-{}] ".format(count)
                else:
                    pick_msg = "Pick a log file to show. Not much of a choice! [0] "

                pick = input(pick_msg)
                try:
                    pick_int = int(pick)
                except ValueError:
                    print("I don't want a string!")
                    pick_int = None
                if pick_int in range(0, len(json)):
                    picked = True

            print("Showing {}".format(json['logs'][pick_int]['file']))
            log_content = self.client.get_log(json['logs'][pick_int]['file'])
            print(log_content)



    def list_tracks(self, album=False, download=False):
        json = self.client.list_tracks()
        json_tracks = json['tracks']
        json_tracks_strip = json_tracks
        ptable = PrettyTable()

        for i in range(len(json_tracks_strip)):
            del json_tracks_strip[i]['file']
            del json_tracks_strip[i]['track_id']

        print("Total tracks in storage: {}".format(json['count']))

        field_names = ['id', 'artist', 'title']
        if album:
            field_names.append('album')
        field_names.append('size')

        ptable.field_names = field_names

        id = 0

        for i in json_tracks_strip:
            values = [id, i['artist'], i['title']]
            if album:
                values.append(i['album'])
            values.append(i['size_mb'])

            ptable.add_row(values)

            id += 1

        print(ptable)
