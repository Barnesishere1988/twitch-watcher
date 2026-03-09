import requests

API_URL="https://api.twitch.tv/helix/streams"

def is_stream_live(config,streamer):
    headers={
        "Client-ID":config["client_id"],
        "Authorization":"Bearer "+config["access_token"]
    }
    params={"user_login":streamer}
    r=requests.get(API_URL,headers=headers,params=params)
    if r.status_code!=200:
        print("API error:",r.status_code,r.text)
        return False
    data=r.json()
    return len(data["data"])>0