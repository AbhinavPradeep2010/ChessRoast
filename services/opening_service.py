import requests
import os

TOKEN = os.getenv("LICHESS_TOKEN")

opening_cache = {}

def fetch_opening_data(move_list):
    key = tuple(move_list)
    if key in opening_cache:
        return opening_cache[key]
    
    try:

        response = requests.get(
            "https://explorer.lichess.ovh/masters",
            params={
                "play": ",".join(move_list)
            },
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "User-Agent": "ChessRoast/1.0"
            },
            timeout=5
        )

        if response.status_code != 200:
            return None

        data = response.json()

        opening_cache[key] = data

        return data

    except Exception as e:

        print("Opening lookup error:", e)

        return None

def is_book_move(move_list, played_move):
    
    data = fetch_opening_data(move_list)

    if not data:
        return False, None

    for move_data in data.get("moves", []):

        if move_data["san"] == played_move:

            opening_data = data.get("opening")

            opening = None

            if opening_data:
                opening = opening_data.get("name")

            return True, opening

    return False, None
    

def get_opening_name(move_list):

    data = fetch_opening_data(move_list)

    if not data:
        return None

    opening_data = data.get("opening")

    if opening_data:
        return opening_data.get("name")

    return None