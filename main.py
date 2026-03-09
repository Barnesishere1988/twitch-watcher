import json

CONFIG_FILE="config.json"
from twitch_api import is_stream_live

def load_config():
    with open(CONFIG_FILE,"r") as f:return json.load(f)

def save_config(config):
    with open(CONFIG_FILE,"w") as f:json.dump(config,f,indent=2)

def main():
    config=load_config()
    for streamer in config["streamers"]:
        live=is_stream_live(config,streamer)
        print(streamer,"LIVE" if live else "offline")

if __name__=="__main__":
    main()