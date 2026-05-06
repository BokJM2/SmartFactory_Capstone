import json

config = json.load(open("config.json"))

def reload_conf():
    global config
    config = json.load(open("config.json"))

def conf() -> dict:
    return config
