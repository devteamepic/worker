import urllib.request
import os
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


PROTOCOL = "http://"
FILES_URL_ROOT = PROTOCOL + "localhost:3000"
ROOT_DIR = get_project_root()


def download(uri):
    create_dirs_from_uri(uri)
    urllib.request.urlretrieve(f"{FILES_URL_ROOT}{uri}", f"{ROOT_DIR}{uri}")


def create_dirs_from_uri(path_string):
    file_path = '/'.join(path_string.split("/")[1:-1])
    if not os.path.isdir(file_path):
        os.makedirs(file_path)

