import json
from monitor import monitor_streamers
from events import EventManager
from player import open_stream
from streamer import Streamer
from chat import TwitchChat

CONFIG_FILE="config.json"

def load_config():
    with open(CONFIG_FILE,"r") as f:config=json.load(f)
    config["streamers"]=[Streamer(s) for s in config["streamers"]]
    return config

def save_config(config):
    data=dict(config)
    data["streamers"]=[s.to_dict() for s in config["streamers"]]
    with open(CONFIG_FILE,"w") as f:json.dump(data,f,indent=2)

def on_live(streamer):
    print(streamer.name,"went LIVE")
    if streamer.auto_open:
        open_stream(streamer.name,streamer.muted)
    else:
        print("Auto open disabled for",streamer.name)

def on_offline(streamer):
    print(streamer.name,"went OFFLINE")

def main():
    config=load_config()

    chat=TwitchChat(config)
    chat.connect()
    
    events=EventManager()
    events.on("stream_live",on_live)
    events.on("stream_offline",on_offline)
    try:
        monitor_streamers(config,events)
    except KeyboardInterrupt:
        print("\nProgram stopped")

if __name__=="__main__":
    main()