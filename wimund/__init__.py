import argparse, sys, configparser, os, signal
from pathlib import Path
from wimund.cli import CLI
from pygments import highlight, lexers, formatters

CONF_PATH = os.path.join(str(Path.home()), ".config", "wimund.ini")
CONFIG = configparser.ConfigParser()
CONFIG.read(CONF_PATH)

CLI_ARGS = (CONFIG['SERVER']['URL'], CONFIG['SERVER']['USER'], CONFIG['SERVER']['PASSWORD'])

def signal_handler(sig, frame):
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def status_func(arg):
    c = CLI(*CLI_ARGS)
    c.status()

def search_func(arg):
    c = CLI(*CLI_ARGS)
    if arg.full:
        c.search(arg.query, dispatch=False, full=True)
    else:
        if arg.no_album:
            c.search(arg.query, dispatch=True, album=False)
        else:
            c.search(arg.query, dispatch=True, album=True)

def list_logs_func(arg):
    c = CLI(*CLI_ARGS)
    c.list_logs(True)

def tracks_func(arg):
    c = CLI(*CLI_ARGS)
    if arg.op == 'list':
        c.list_tracks()
    elif arg.op == 'delete':
        c.list_tracks(delete=True)
    elif arg.op == 'download':
        c.list_tracks(download=True)
    elif arg.op == 'play':
        c.list_tracks(play=True)

def spotify_func(arg):
    c = CLI(*CLI_ARGS)
    c.spotifyctl(arg.operation)

def test_func(arg):
    c = CLI(*CLI_ARGS)
    c.test()

def export_func(arg):
    c = CLI(*CLI_ARGS)
    c.export_all()

def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    search = subparsers.add_parser("search")
    search.add_argument("query", type=str)
    search.add_argument("--full", action="store_true")
    search.add_argument("--no-album", action="store_true")
    search.set_defaults(func=search_func)

    tracks = subparsers.add_parser("tracks")
    tracks.set_defaults(func=tracks_func)
    tracks.add_argument("--op", "--operation", choices=["list", "download", "delete", "play"], default="list")

    status = subparsers.add_parser("status")
    status.set_defaults(func=status_func)

    logs = subparsers.add_parser("logs")
    logs.set_defaults(func=list_logs_func)

    spotify = subparsers.add_parser("spotify")
    spotify.add_argument("operation", type=str)
    spotify.set_defaults(func=spotify_func)

    export = subparsers.add_parser("export")
    export.set_defaults(func=export_func)

    test = subparsers.add_parser("test")
    test.set_defaults(func=test_func)

    return parser

def main():
    parser = get_parser()

    if (len(sys.argv) == 1):
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)
