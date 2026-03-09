import json
from monitor import monitor_streamers
from events import EventManager
from player import open_stream

CONFIG_FILE="config.json"

def load_config():
    with open(CONFIG_FILE,"r") as f:return json.load(f)

def save_config(config):
    with open(CONFIG_FILE,"w") as f:json.dump(config,f,indent=2)

def on_live(streamer):
    print(streamer["name"],"went LIVE")
    open_stream(streamer["name"],streamer["muted"])

def on_offline(streamer):
    print(streamer["name"],"went OFFLINE")

def main():
    config=load_config()
    events=EventManager()
    events.on("stream_live",on_live)
    events.on("stream_offline",on_offline)
    try:
        monitor_streamers(config,events)
    except KeyboardInterrupt:
        print("\nProgram stopped")

if __name__=="__main__":
    main()