import socket

SERVER="irc.chat.twitch.tv"
PORT=6667

class TwitchChat:
    def __init__(self,config):
        self.username=config["username"]
        self.token=config["access_token"]
        self.sock=socket.socket()
    def connect(self):
        self.sock.connect((SERVER,PORT))
        self.send(f"PASS oauth:{self.token}")
        self.send(f"NICK {self.username}")
        print("Connected to Twitch IRC")
    def join(self,channel):
        self(f"JOIN #{channel}")
        print("Joined chat",channel)
    def send(self,msg):
        self.sock.send((msg+"\r\n").encode("utf-8"))
    def receive(self):
        resp=self.sock.recv(2048).decode("utf-8")
        if resp.startswith("PING"):
            self.send("PONG :tmi.twitch.tv")
        return resp