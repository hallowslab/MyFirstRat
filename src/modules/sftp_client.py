import os
from paramiko import SSHClient, WarningPolicy
from modules.utils import has_auth

HEADER = "{}@{} $"
SFTP_MENU = """
    Select an option

        [0] Upload a file
        [1] Download a file

        [h] Show menu
        [q] quit
"""


def create_client() -> SSHClient:
    target = SSHClient()
    target.load_system_host_keys()
    target.set_missing_host_key_policy(WarningPolicy())
    return target


def upload_file(config: dict, f_path: str, dest_path: str):
    l_path = os.path.abspath(f_path)
    if os.path.isfile(l_path):
        tgt = config["target"]
        user = config["user"]
        pwd = config["password"]
        try:
            session = create_client()
            session.connect(tgt, user, pwd)
            sftp = session.open_sftp()
            sftp.put(l_path, dest_path)
        except Exception as e:
            print(f"Failed to upload file: {l_path}: {e}")
            pass


def download_file(config: dict, dest_path: str, f_path: str):
    l_path = os.path.abspath(dest_path)
    if os.path.isfile(dest_path):
        tgt = config["target"]
        user = config["user"]
        pwd = config["password"]
        try:
            session = create_client()
            session.connect(tgt, user, pwd)
            sftp = session.open_sftp()
            sftp.get(f_path, l_path)
        except Exception as e:
            print(f"Failed to download file: {f_path}: {e}")


def main(config: dict):
    running = True if has_auth(config) else False
    if not running:
        print("Cannot connect, missing credentials")
        return
    tgt = config["target"]
    user = config["user"]
    print(SFTP_MENU)
    while running:
        option = input(f"{HEADER.format(tgt,user)} ")
        if option == "0":
            l_path = input("File to upload: ")
            dest = input("Upload path: ")
            upload_file(config, l_path, dest)
        elif option == "1":
            r_path = input("Remote file path: ")
            _, r_file = os.path.split(os.path.abspath(r_path))
            l_path = os.path.abspath(f"./output/{r_file}")
            download_file(config, l_path, r_path)
        elif option == "h":
            print(SFTP_MENU)
        elif option == "q":
            running = False
            break
