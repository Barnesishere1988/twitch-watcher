import json

CONFIG_FILE="config.json"
from monitor import monitor_streamers

def load_config():
    with open(CONFIG_FILE,"r") as f:return json.load(f)

def save_config(config):
    with open(CONFIG_FILE,"w") as f:json.dump(config,f,indent=2)

def main():
    config=load_config()
    monitor_streamers(config)

if __name__=="__main__":
    main()