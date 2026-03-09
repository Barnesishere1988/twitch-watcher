import json,threading,websocket,uuid

URL="wss://pubsub-edge.twitch.tv"

class TwitchPubSub:

    def __init__(self,config,events):
        self.token=config["access_token"]
        self.events=events

    def start(self,channels):

        t=threading.Thread(target=self.run,args=(channels,))
        t.daemon=True
        t.start()

    def run(self,channels):

        ws=websocket.WebSocket()
        ws.connect(URL)

        topics=[f"channel-points-channel-v1.{c}" for c in channels]

        payload={
            "type":"LISTEN",
            "nonce":str(uuid.uuid4()),
            "data":{
                "topics":topics,
                "auth_token":self.token
            }
        }

        ws.send(json.dumps(payload))

        print("PubSub connected")

        while True:

            msg=json.loads(ws.recv())

            if msg["type"]=="MESSAGE":

                data=json.loads(msg["data"]["message"])

                if data["type"]=="reward-redeemed":
                    continue

                if data["type"]=="points-earned":

                    if data["data"]["point_gain"]["reason"]=="WATCH":

                        channel=data["data"]["channel_id"]
                        print("Channel points earned:",channel)

                        self.events.emit("points_bonus",channel)