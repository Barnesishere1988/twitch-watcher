import time
from twitch_api import is_stream_live

def monitor_streamers(config,events):
    streamers=config["streamers"]
    status={s:False for s in streamers}
    print("Monitoring started")
    while True:
        for s in streamers:
            live=is_stream_live(config,s)
            if live and not status[s]:
                events.emit("stream_live",s)
            if not live and status[s]:
                events.emit("Stream_offline",s)
            status[s]=live
        time.sleep(60)