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

def on_raid(from_streamer,to_streamer):

    print("Raid dtected:",from_streamer,"→",to_streamer)

    print("\nOptions:")
    print("1 Continue watching")
    print("2 Close stream")
    print("3 Add to watchlist")

    choice=input("Select option: ")

    if choice=="1":
        switch_stream(to_streamer,True)

    elif choice=="2":
        print("Raid ignored")

    elif choice=="3":
        print("Adding",to_streamer,"to watchlist")

def main():
    config=load_config()
    
    events=EventManager()
    events.on("stream_live",on_live)
    events.on("stream_offline",on_offline)
    events.on("raid",on_raid)

    chat=TwitchChat(config,events)
    chat.connect()

    for s in config["streamers"]:
        if s.enabled:
            chat.join(s.name)

    chat.start()

    try:
        monitor_streamers(config,events)
    except KeyboardInterrupt:
        print("\nProgram stopped")

if __name__=="__main__":
    main()