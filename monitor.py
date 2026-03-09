import time
from twitch_api import is_stream_live

def monitor_streamers(config):
    streamers=config["streamers"]
    status={s:False for s in streamers}
    while True:
        for s in streamers:
            live=is_stream_live(config,s)
            if live and not status[s]:
                print(s,"went LIVE")
            if not live and status[s]:
                print(s,"went OFFLINE")
            status[s]=live
        time.sleep(60)