import json

def load_config():
    with open("config.json","r") as f:return json.load(f)

def main():
    config=load_config()
    print("Configured streamers:",config["streamers"])

if __name__=="__main__":
    main()