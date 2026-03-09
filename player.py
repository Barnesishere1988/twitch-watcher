import webbrowser

opened_streams=set()

def open_stream(streamer, muted):
    global current_stream
    current_stream=streamer
    m="true" if muted else "false"
    url=f"https://player.twitch.tv/?channel={streamer}&parent=localhost&muted={m}"
    print("Opening player for",streamer,"muted:",muted)
    webbrowser.open(url)

def switch_stream(streamer,muted):
    print("Switching to",streamer)
    open_stream(streamer,muted)