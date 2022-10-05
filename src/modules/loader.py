import logging
import os
import importlib

LG = logging.getLogger(__name__)


def load_extension(ext_name: str, config: dict):
    LG.info("Extension -> %s", __name__)
    print(f"Extension -> {__name__}")
    f_path = os.path.abspath(os.path.join("./modules/extensions", ext_name)) + ".py"
    print(f"Loading -> {f_path}")
    if os.path.isfile(f_path):
        try:
            pkg = importlib.import_module(f"modules.extensions.{ext_name}")
            pkg.main(config)
        except Exception as e:
            print(e.__class__.__name__)
            print(f"Failed to load extension {ext_name}, {e}")
            LG.critical("Failed to load extension %s: Exception: %s", ext_name, e)
    else:
        print(f"Failed to load extension: {f_path}")
        LG.error("Failed to load extension: %s", f_path)


def detect_extensions() -> list:
    extensions = []
    for _, _, files in os.walk(os.path.abspath("./modules/extensions")):
        for file in files:
            try:
                if file.endswith(".py"):
                    pkg = file.replace(".py", "")
                    pkg = importlib.import_module(f"modules.extensions.{pkg}")
                    print("Loading extension: ", pkg.__name__)
                    extensions.append(pkg.__name__)
            except ModuleNotFoundError:
                print(f"Module not found {file}")
                LG.error("Module not found %s", file)
                pass
            except Exception as e:
                print(f"Failed to load module {file}, {e}")
                LG.error("Failed to load module %s, Exception: %s", file, e)
    return extensions
