import logging

LG = logging.getLogger(__name__)

def main(config:dict):
    print(f"Extension -> {__name__}")
    LG.info(f"Extension -> {__name__}")
    pass