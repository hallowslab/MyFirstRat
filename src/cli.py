from json import JSONDecodeError
import logging
import os
import sys
from __version__ import VERSION
from modules import remote_shell, loader
from modules.utils import set_logging, get_args, read_config, INTIAL_MENU, HEADER

LG = logging.getLogger(__name__)

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
            "7": loader.load_extension,
            "8": print,
            "9": sys.exit
        }
        selection = input(f"{HEADER}")
        if selection in options.keys():
            if selection == "1":
                rcmd=input(f"{HEADER} Specify command to execute: ")
                options[selection](rcmd, config)
            elif selection == "7":
                mname=input(f"{HEADER} Specify module name: ")
                options[selection](mname, config)
            elif selection == "8":
                options[selection](INTIAL_MENU)
            elif selection == "9":
                options[selection](0)
            else:
                options[selection](config)
        else:
            print(f"Invalid option {selection}")
            LG.error(f"Invalid option {selection}")



if __name__ == "__main__":
    args = get_args()
    log_level = getattr(args, "log_level")
    set_logging(log_level)
    if getattr(args, "version"):
        print(VERSION)
        sys.exit(0)
    config = {
        "target": getattr(args, "target", None),
        "user": getattr(args, "user", None),
        "password": getattr(args, "password", None),
        "extensions": [loader.detect_extensions()]
    }
    if getattr(args, "config_file") and os.path.isfile(args.config_file):
        try:
            config = read_config(args.config_file)
            config["extensions"] = loader.detect_extensions()
        except JSONDecodeError as e:
            print("Failed to load config")
            LG.error(f"Failed to load config from file: {e}")
    if config["target"] is None:
        print("No target")
        LG.critical("No target")
        sys.exit(1)
    LG.info("Starting Command Line Interface")
    main(config)