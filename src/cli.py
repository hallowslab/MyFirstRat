import getpass
from json import JSONDecodeError
import logging
import os
import sys
from __version__ import VERSION
from modules import remote_shell, loader, sftp_client, configurator
from modules.utils import set_logging, get_args, read_config

LG = logging.getLogger(__name__)
INTIAL_MENU = """
    Select an option to proceed

    [0]: Remote shell connection
    [1]: Run remote command
    [2]: SFTP Menu
    [9]: Run extension
    [e]: Show loaded extensions
    [c]: Change config
    [h]: Show this menu
    [q]: exit
"""
LUSER = getpass.getuser()
HEADER = f"{LUSER}@RCLI $ "


def main(config: dict):
    running = True
    print("Config:")
    print(config)
    LG.info(config)
    print(INTIAL_MENU)
    while running:
        options = {
            "0": remote_shell.establish_session,
            "1": remote_shell.run_command,
            "2": sftp_client.main,
            "9": loader.load_extension,
            "e": "",
            "c": configurator.main,
            "h": "",
            "q": "",
        }
        selection = input(f"{HEADER}")
        if selection in options.keys():
            if selection == "1":
                rcmd = input(f"{HEADER} Specify command to execute: ")
                options[selection](rcmd, config)
            elif selection == "9":
                mname = input(f"{HEADER} Specify module name: ")
                options[selection](mname, config)
            elif selection == "e":
                print(config["extensions"])
            elif selection == "h":
                print(INTIAL_MENU)
            elif selection == "q":
                sys.exit(0)
            else:
                options[selection](config)
        else:
            print(f"Invalid option {selection}")
            LG.error("Invalid option %s", selection)


if __name__ == "__main__":
    args = get_args()
    log_level = getattr(args, "log_level")
    set_logging(log_level)
    if not os.path.isdir("output"):
        os.mkdir("output")
    if getattr(args, "version"):
        print(VERSION)
        sys.exit(0)
    config = {
        "target": getattr(args, "target", None),
        "user": getattr(args, "user", None),
        "password": getattr(args, "password", None),
        "sftp_port": getattr(args, "sftp_port", None),
        "extensions": [*loader.detect_extensions()],
    }
    if getattr(args, "config_file") and os.path.isfile(args.config_file):
        try:
            config = read_config(args.config_file)
            config["extensions"] = loader.detect_extensions()
        except JSONDecodeError as e:
            print("Failed to load config")
            LG.error("Failed to load config from file: %s", e)
    if config["target"] is None:
        print("No target")
        LG.critical("No target")
        sys.exit(1)
    LG.info("Starting Command Line Interface")
    main(config)
