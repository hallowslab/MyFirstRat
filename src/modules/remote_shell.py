import logging
from paramiko import SSHClient, WarningPolicy
from paramiko.util import log_to_file
from modules.utils import clean_output, print_arr, has_auth

LG = logging.getLogger(__name__)

HEADER = "{}@{} $"

def create_client()->SSHClient:
    target = SSHClient()
    target.load_system_host_keys()
    target.set_missing_host_key_policy(WarningPolicy())
    return target

def establish_session(config: dict):
    if has_auth(config):
        log_to_file(f"{config['target']}:{config['user']}.log")
        print(f"Extension -> {__name__}:{establish_session.__name__}")
        LG.info(f"Extension -> {__name__}:{establish_session.__name__}")
        LG.info(f"Connecting to -> {config['target']}")
        print(f"Connecting to -> {config['target']}")
        tgt = config["target"]
        user = config["user"]
        pwd = config["password"]
        target = create_client()
        try:
            target.connect(tgt, username=user, password=pwd, look_for_keys=False)
            connected = True
            while connected:
                rcmd = input(f"{HEADER.format(user, tgt)} (/@close to exit) -> $ ")
                if rcmd == "/@close":
                    connected = False
                    break
                _, stdout, stderr = target.exec_command("powershell " + rcmd)
                print("stdout:", print_arr(clean_output(stdout.readlines())))
                LG.info(f"{rcmd} stdout: {clean_output(stdout.readlines())}")
                LG.error(f"{rcmd} stderr: {clean_output(stderr.readlines())}")
        except Exception as e:
            print(f"Failed to connect: {e}")
            LG.error(f"Failed to connect: {e}")
        target.close()
    else:
        print("Cant connect no authentication")

def run_command(rcmd:str,config:dict)->dict:
    print(f"Extension -> {__name__}:{establish_session.__name__}")
    LG.info(f"Extension -> {__name__}:{run_command.__name__}")
    print(f"Running command: {rcmd} on target -> {config['target']}")
    if has_auth(config):
        tgt = config["target"]
        user = config["user"]
        pwd = config["password"]
        log_to_file(f"{tgt}:{user}.log")
        target=create_client()
        try:
            target.connect(tgt, username=user, password=pwd, look_for_keys=False)
            rcmd = input(f"{HEADER} Input command: ")
            _, stdout, stderr = target.exec_command(rcmd)
            LG.info(f"{rcmd} stdout: {clean_output(stdout.readlines())}")
            LG.error(f"{rcmd} stderr: {clean_output(stderr.readlines())}")
            return {
                "Output": clean_output(stdout.readlines()),
                "Errors": clean_output(stderr.readlines())
            }
        except Exception as e:
            print(f"Failed to connect: {e}")
            LG.error(f"Failed to connect: {e}")
            return {}
    else:
        print("Cant connect no authentication")
