import csv
import requests
from utils import team_converter, position_converter

def main():
    with requests.Session() as s:
        boostrap_static = "https://fantasy.premierleague.com/api/bootstrap-static/"
        data = s.get(boostrap_static).json()["elements"]

    headers = ["Position", "Team", "First Name", "Second Name", "Web Name", "FPL ID", "Understat ID", "WhoScored ID", "FBref ID"]

    player_info = []
    for player in data:
        pos = position_converter(player["element_type"])
        team = team_converter(player["team"])
        first = player["first_name"]
        second = player["second_name"]
        web = player["web_name"]
        fpl_id = str(player["id"])
        player_info.append([pos, team, first, second, web, fpl_id, -1, -1, -1])

    player_info = sorted(player_info, key=lambda x: int(x[5]))

    with open("master.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(player_info)


if __name__ == "__main__":
    main()