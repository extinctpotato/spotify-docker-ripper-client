import requests, sys, subprocess
from tqdm import tqdm
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
        url = urljoin(self.url, "track")
        r = requests.get(url, auth=self.auth)
        return r.json()

    def delete_track(self, track_id):
        url = urljoin(self.url, "track/{}".format(track_id))
        r = requests.delete(url, auth=self.auth)
        return r.json()

    def download_track(self, track_id, filename=None, quiet=False, only_play=False, chunk_size=1024*1024):
        url = urljoin(self.url, "track/{}".format(track_id))

        with requests.get(url, stream=True, auth=self.auth, headers={'Accept-Encoding': None}) as r:
            if filename is None:
                filename = "{}.ogg".format(track_id.split(":")[2])

            r.raise_for_status()

            if not only_play:
                size = int(r.headers['Content-Length'])
                progress = tqdm(total=size, initial=0, unit='B', unit_scale=True, ascii=True, ncols=120, file=sys.stdout)
            else:
                player = subprocess.Popen(
                        "ffplay -autoexit -nodisp -hide_banner -loglevel 32 -i /dev/stdin", 
                        shell=True, 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.DEVNULL, 
                        )

            if only_play:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    player.stdin.write(chunk)
                player.stdin.close()
                player.wait()
            else:
                with open(filename, "wb") as f:
                    f.write(chunk)
                    if not quiet:
                        progress.update(sys.getsizeof(chunk))

    def list_logs(self):
        url = urljoin(self.url, "log")
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

    def export_all(self):
        url = urljoin(self.url, "export")
        r = requests.post(url, auth=self.auth)
        return r.json()

    def get_log(self, logname):
        url = urljoin(self.url, "log/{}".format(logname))
        r = requests.get(url, auth=self.auth)
        return r.content.decode()

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
