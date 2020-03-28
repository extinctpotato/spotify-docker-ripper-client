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
    c.search(arg.query, dispatch=True)

def list_tracks_func(arg):
    c = CLI(*CLI_ARGS)
    c.list_tracks()

def get_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    search = subparsers.add_parser("search")
    search.add_argument("query", type=str)
    search.set_defaults(func=search_func)

    tracks = subparsers.add_parser("tracks")
    tracks.set_defaults(func=list_tracks_func)

    status = subparsers.add_parser("status")
    status.set_defaults(func=status_func)

    return parser

def main():
    parser = get_parser()

    if (len(sys.argv) == 1):
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)
