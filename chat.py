import socket, threading, re

SERVER="irc.chat.twitch.tv"
PORT=6667

class TwitchChat:
    def __init__(self,config,events):
        self.username=config["username"]
        self.token=config["access_token"]
        self.events=events
        self.sock=socket.socket()
        self.running=False

    def connect(self):
        self.sock.connect((SERVER,PORT))
        self.send(f"PASS oauth:{self.token}")
        self.send(f"NICK {self.username}")
        print("Connected to Twitch IRC")

    def join(self,channel):
        self.send(f"JOIN #{channel}")
        print("Joined chat",channel)

    def send(self,msg):
        self.sock.send((msg+"\r\n").encode("utf-8"))

    def start(self):
        self.running=True
        t=threading.Thread(target=self.listen)
        t.daemon=True
        t.start()

    def listen(self):
        while self.running:
            resp=self.sock.recv(2048).decode("utf-8")

            if resp.startswith("PING"):
                self.send("PONG: :tmi.twitch.tv")
                continue

            self.parse(resp)

    def parse(self,msg):

        raid=re.search(r"(\w+) is raiding (\w+)",msg)
        if raid:
            from_streamer=raid.group(1)
            to_streamer=raid.group(2)
            print("Raid detected:",from_streamer,"→",to_streamer)
            self.events.emit("raid",from_streamer,to_streamer)

    def receive(self):
        resp=self.sock.recv(2048).decode("utf-8")
        if resp.startswith("PING"):
            self.send("PONG :tmi.twitch.tv")
        return resp