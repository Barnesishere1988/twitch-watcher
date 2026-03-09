import time
from twitch_api import is_stream_live

def monitor_streamers(config,events):
    streamers=[s for s in config["streamers"] if s.enabled]
    status={s.name:False for s in streamers}
    print("Monitoring started")
    while True:
        for s in streamers:
            live=is_stream_live(config,s.name)
            if live and not status[s.name]:
                events.emit("stream_live",s)
            if not live and status[s.name]:
                events.emit("Stream_offline",s)
            status[s.name]=live
        time.sleep(60)