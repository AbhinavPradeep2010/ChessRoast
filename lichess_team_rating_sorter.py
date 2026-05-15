import requests
import json

# -----------------------------------
# CONFIG
# -----------------------------------

TOKEN = ""

TEAM_ID = "priyarang-chess-academy"

RATING_TYPE = "rapid"   # bullet, blitz, rapid, classical
TOP_N = 15

# -----------------------------------
# HEADERS
# -----------------------------------

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

# -----------------------------------
# GET TEAM MEMBERS
# -----------------------------------

team_url = f"https://lichess.org/api/team/{TEAM_ID}/users"

response = requests.get(team_url, headers=headers)

print("Team API Status:", response.status_code)

if response.status_code != 200:
    print(response.text)
    exit()

lines = response.text.strip().split("\n")

usernames = []

for line in lines:

    user = json.loads(line)

    username = user.get("id")

    if username:
        usernames.append(username)

print(f"Found {len(usernames)} users")

# -----------------------------------
# BATCH FETCH USER DATA
# -----------------------------------

# Lichess accepts comma-separated usernames
payload = ",".join(usernames)

users_url = "https://lichess.org/api/users"

users_response = requests.post(
    users_url,
    headers=headers,
    data=payload
)

print("Users API Status:", users_response.status_code)

users_data = users_response.json()

players = []

# -----------------------------------
# EXTRACT RATINGS
# -----------------------------------

for user in users_data:

    username = user.get("username")

    perfs = user.get("perfs", {})

    if RATING_TYPE in perfs:

        rating = perfs[RATING_TYPE].get("rating")

        if rating:

            players.append({
                "username": username,
                "rating": rating
            })


# -----------------------------------
# SORT
# -----------------------------------

players.sort(
    key=lambda x: x["rating"],
    reverse=True
)

# -----------------------------------
# RESULTS
# -----------------------------------

print(f"\nTOP {TOP_N} {RATING_TYPE.upper()} PLAYERS:\n")

for i, player in enumerate(players[:TOP_N], start=1):

    print(
        f"{i}. {player['username']} - {player['rating']}"
    )