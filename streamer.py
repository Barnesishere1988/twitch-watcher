class Streamer:
    def __init__(self,data):
        self.name=data.get("name")
        self.muted=data.get("muted",True)
        self.auto_open=data.get("auto_open",True)
        self.enabled=data.get("enabled",True)
    def to_dict(self):
        return{
            "name":self.name,
            "muted":self.muted,
            "auto_open":self.auto_open,
            "enabled":self.enabled
        }