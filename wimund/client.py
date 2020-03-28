import requests
from urllib.parse import urljoin
from prettytable import PrettyTable
from requests.auth import HTTPBasicAuth

class WimundClient:
    def __init__(self, url="http://localhost:9000", user=None, password=None):
        self.url = url
        self.auth = HTTPBasicAuth(user, password)

    def dispatch_track(self, track_id):
        url = urljoin(self.url, "track/{}".format(track_id))
        r = requests.post(url, auth=self.auth)
        return r.json()

    def list_tracks(self):
        url = urljoin(self.url, "list/tracks")
        r = requests.get(url, auth=self.auth)
        return r.json()

    def list_logs(self):
        url = urljoin(self.url, "list/logs")
        r = requests.get(url, auth=self.auth)
        return r.json()

    def spotify_start(self):
        url = urljoin(self.url, "spotify/start")
        r = requests.post(url, auth=self.auth)
        return r.json()

    def spotify_stop(self):
        url = urljoin(self.url, "spotify/stop")
        r = requests.post(url, auth=self.auth)
        return r.json()

    def status(self):
        url = urljoin(self.url, "status")
        r = requests.get(url, auth=self.auth)
        return r.json()

    def search(self, query, full=False):
        url = urljoin(self.url, "sapi/search")
        params = {"q":query}
        if full:
            params.update({"full":"true"})
        r = requests.get(url, auth=self.auth, params=params)
        return r.json()
