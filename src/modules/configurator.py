CONFIGURATOR_MENU = """
    Select an option

        [0]: Get value from config
        [1]: Set value in config
"""


def setter(config: dict, key: str, val: str) -> dict:
    if key == "extensions":
        print("Cannot override extensions")
        return config
    old_key = config.get(key, None)
    if not old_key or old_key != val:
        return {**config, key: val}
    return config


def getter(config: dict, key: str) -> str:
    val = config.get(key, "")
    return val


def main(config: dict):
    running = True
    print(CONFIGURATOR_MENU)
    while running:
        option = input("Select option: ")
        if option == "0":
            key = input("Input the key: ")
            val = getter(config, key)
            if val == "":
                print("Empty value or missing key")
            print(val)
        if option == "1":
            key_val = input("Input key and value split by comma: ")
            key_val = key_val.split(",")
            if len(key_val) <= 1:
                print("Input the values as specified previously -> key,val")
            old_val = getter(config, key_val)
            print(f"Old key value: {old_val}")
            setter(config, key_val[0], key_val[1])
            print(f"New key value: {getter(config,key_val)}")
        else:
            print(f"Invalid option {option}")
