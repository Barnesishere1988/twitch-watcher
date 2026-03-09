import json
from monitor import monitor_streamers
from events import EventManager
from player import open_stream,switch_stream
from streamer import Streamer
from chat import TwitchChat
from pubsub import TwitchPubSub

CONFIG_FILE="config.json"

def load_config():
    with open(CONFIG_FILE,"r") as f:config=json.load(f)
    config["streamers"]=[Streamer(s) for s in config["streamers"]]
    return config

def save_config(config):
    data=dict(config)
    data["streamers"]=[s.to_dict() for s in config["streamers"]]
    with open(CONFIG_FILE,"w") as f:json.dump(data,f,indent=2)

def add_streamer(config,name):

    for s in config["streamers"]:
        if s.name.lower()==name.lower():
            print(name,"already in watchlist")
            return
        
    print("Adding",name,"to watchlist")

    streamer=Streamer({
        "name":name,
        "muted":True,
        "auto_open":False,
        "enabled":True
    })

    config["streamers"].append(streamer)
    save_config(config)

def on_points(channel):
    print("Channel points event from",channel)

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
        add_streamer(config,to_streamer)

def main():
    global config
    config=load_config()
    
    events=EventManager()
    events.on("stream_live",on_live)
    events.on("stream_offline",on_offline)
    events.on("raid",on_raid)
    events.on("points_bonus",on_points)

    chat=TwitchChat(config,events)
    chat.connect()

    channels=[s.name for s in config["streamers"] if s.enabled]

    for s in config["streamers"]:
        if s.enabled:
            chat.join(s.name)

    chat.start()

    pubsub=TwitchPubSub(config,events)
    pubsub.start(channels)

    try:
        monitor_streamers(config,events)
    except KeyboardInterrupt:
        print("\nProgram stopped")

if __name__=="__main__":
    main()