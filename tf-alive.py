import requests
import webbrowser
import sys
import time
import datetime
import json

args = sys.argv

if '-h' in args:
    print("""
    Launch arguments:
    
    -k          -> Steam Web API key
    
    [OPTIONAL]    
    -h          -> Show help (This list)
    -t [time]   -> Set refresh time (Default: 30s)
    -b          -> Should script open a browser on succses
    -l [link]   -> Parameter sets a new link to open. (Default: tf2mart.net)              
    """)
    sys.exit()

key = args[args.index('-k') + 1]
# You can use your own if you have the game, which you will track
steam_id64 = 76561198357516397  # Script creator's steam account ID.
open_browser_on_success = '-b' in args
browser_link = "https://tf2mart.net/order"
steam_api_last_known_online = datetime.datetime.now()
refresh_time = 30

if '-t' in args and args.index('-t') != len(args):
    refresh_time = int(args[args.index('-t') + 1])

if '-l' in args and args.index('-o') != len(args) - 1:
        browser_link = args[args.index('-o') + 1]

if refresh_time < 30:
    print("Strongly recommended to increase refresh time!")

decoder = json.JSONDecoder()
is_api_working = False


# Returns true if object is empty
def is_empty(q):
    return len(q) == 0


while True:
    # Change Steam game ID to get status of other in-game inventories           vvv
    req = decoder.decode(requests.get(f"https://api.steampowered.com/IEconItems_440/GetPlayerItems/v0001/?key={key}"
                                      f"&steamid={steam_id64}").text)
    is_api_working = not is_empty(req)
    print('-' * 60)

    if is_api_working:
        steam_api_last_known_online = datetime.datetime.now()
        print(" /// * INVENTORY API IS ALIVE * ///")
        if open_browser_on_success:
            webbrowser.open(browser_link)

    print("IS Steam Inventory API online >> " + str(is_api_working))
    print("Last online >> " + str(steam_api_last_known_online))
    print("Time past from the last online >> " + str(datetime.datetime.now() - steam_api_last_known_online))
    print(f"Waiting next {refresh_time}s...")

    time.sleep(refresh_time)
