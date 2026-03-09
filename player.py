import webbrowser

opened_streams=set()

def open_stream(streamer, muted):
    if streamer in opened_streams:return
    opened_streams.add(streamer)
    m="true" if muted else "false"
    url=f"https://player.twitch.tv/?channel={streamer}&parent=localhost&muted={m}"
    print("Opening player for",streamer,"muted:",muted)
    webbrowser.open(url)