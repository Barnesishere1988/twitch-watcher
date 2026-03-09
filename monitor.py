import time
from twitch_api import is_stream_live

def monitor_streamers(config,events):
    streamers=config["streamers"]
    status={s["name"]:False for s in streamers}
    print("Monitoring started")
    while True:
        for s in streamers:
            name=s["name"]
            live=is_stream_live(config,name)
            if live and not status[name]:
                events.emit("stream_live",s)
            if not live and status[name]:
                events.emit("Stream_offline",s)
            status[name]=live
        time.sleep(60)