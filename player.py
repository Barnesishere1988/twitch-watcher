import webbrowser

def open_stream(streamer):
    url=f"https://player.twitch.tv/?channel={streamer}&parent=localhost&muted=true"
    print("Opening player for",streamer)
    webbrowser.open(url)