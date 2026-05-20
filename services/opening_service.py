import requests
import os

TOKEN = os.getenv("LICHESS_TOKEN")

def is_book_move(move_list, played_move):
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

        print("STATUS:", response.status_code)

        if response.status_code != 200:
            return False, None

        data = response.json()

        for move_data in data.get("moves", []):

            if move_data["san"] == played_move:

                opening_data = data.get("opening")

                opening = None

                if opening_data:
                    opening = opening_data.get("name")

                return True, opening

        return False, None

    except Exception as e:

        print("Error occurred:", e)

        return False, None
    

def get_opening_name(move_list):

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

        opening_data = data.get("opening")

        if opening_data:
            return opening_data.get("name")

        return None

    except Exception as e:

        print("Opening lookup error:", e)

        return None
