import csv
import requests


# a map from FPL team names to Understat team names
team_name_map = {
    "Arsenal": "Arsenal",
    "Aston Villa": "Aston Villa",
    "Brighton": "Brighton",
    "Burnley": "Burnley",
    "Chelsea": "Chelsea",
    "Crystal Palace": "Crystal Palace",
    "Everton": "Everton",
    "Fulham": "Fulham",
    "Leicester": "Leicester",
    "Leeds": "Leeds",
    "Liverpool": "Liverpool",
    "Man City": "Manchester City",
    "Man Utd": "Manchester United",
    "Newcastle": "Newcastle United",
    "Sheffield Utd": "Sheffield United",
    "Southampton": "Southampton",
    "Spurs": "Tottenham",
    "West Brom": "West Bromwich Albion",
    "West Ham": "West Ham",
    "Wolves": "Wolverhampton Wanderers"
}


def search(s, search_term):
    search_term = search_term.replace("'", "")  # fixes errors for players with apostrophes in their name
    resp = s.get(f"https://understat.com/main/getPlayersName/{search_term}")
    return resp.json()["response"]["players"]


def find_player_id(s, player, search_term):
    matches = search(s, search_term)
    n = len(matches)
    
    if n == 1:
        return matches[0]["id"]
    elif n > 1:
        # returns the first player matched that is at the correct club
        for match in matches:
            if match["team"] == team_name_map[player[1]]:
                return match["id"]
        return "-1"
    return "-1"


def main():
    with open("master.csv", "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
        headers = rows[0]
        players = rows[1:]

    with requests.Session() as s:
        for player in players:
            if player[6] == "-1":
                search_term = f"{player[2]} {player[3]}"  # `{first_name} {last_name}`
                player_id = find_player_id(s, player, search_term)
                if player_id == "-1":  # if there was no match
                    search_term = player[4]  # `web_name`
                    player_id = find_player_id(s, player, search_term)
                player[6] = player_id

    with open("master.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(players)


if __name__ == "__main__":
    main()
