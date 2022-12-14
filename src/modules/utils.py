import json
import logging
import argparse
import os
from random import choice
import re
from string import ascii_letters
from types import MethodType


def random_text():
    return "".join(choice(ascii_letters) for _ in range(choice(range(5, 15))))


def set_logging(log_level):
    numeric_level = getattr(logging, log_level.upper(), "INFO")
    logging.basicConfig(
        format="[%(asctime)s]-> %(levelname)s: %(message)s",
        filename="cli.log",
        level=numeric_level,
        datefmt="%d/%m %I:%M:%S",
    )
    logging.info("log level: %s", logging.getLevelName(logging.getLogger().level))


def get_args() -> MethodType:
    parser = argparse.ArgumentParser(prog="RCLI", description="Rat CLI")
    parser.add_argument("-t", "--target", help="Target")
    parser.add_argument("-u", "--user", help="For remote access")
    parser.add_argument("-p", "--password", help="Password for remote access")
    parser.add_argument("-cf", "--config-file", help="Config file")
    parser.add_argument("-v", "--version", action="store_true", help="version")
    parser.add_argument("-l", "--log-level", default="INFO", help="log level")
    parser.add_argument(
        "-sp", "--sftp-port", default=22, help="Port for SFTP connections"
    )
    return parser.parse_args()


def has_auth(config: dict):
    print(config)
    user = config.get("user", None)
    passwd = config.get("password", None)
    print("AUTH user", user)
    print("AUTH user", passwd)
    return bool(user and passwd)


def get_os() -> str:
    name = "windows" if os.name == "nt" else "other"
    return name


def read_config(cfg_file: str) -> dict:
    with open(cfg_file, "r") as fh:
        return json.load(fh)


def clean_output(otxt: str) -> list:
    clean = []
    for line in otxt:
        line = re.sub(r"\s+", " ", line)
        line = re.sub(r"\t+", " ", line)
        line = re.sub(r"\n+", "\n", line)
        line = re.sub(r"\r+", "", line)
        line = re.sub(r"-+", "-", line)
        if line and len(line) > 1:
            clean.append(line)
    return clean


def print_arr(arr: list):
    for line in arr:
        print(line)
