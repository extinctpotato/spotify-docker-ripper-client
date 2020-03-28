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

    def status(self):
        url = urljoin(self.url, "status")
        r = requests.get(url, auth=self.auth)
        return r.json()

    def search(self, query):
        url = urljoin(self.url, "sapi/search")
        r = requests.get(url, auth=self.auth, params={"q":query})
        return r.json()
