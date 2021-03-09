import csv
import requests
from utils import team_converter, position_converter


def main():
    with open("master.csv", "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
        headers = rows[0]
        players_from_csv = rows[1:]

    with requests.Session() as s:
        boostrap_static = "https://fantasy.premierleague.com/api/bootstrap-static/"
        players_from_bootstrap = s.get(boostrap_static).json()["elements"]

        fpl_ids_from_csv = [int(x[5]) for x in players_from_csv]
        fpl_ids_from_bootstrap = [x["id"] for x in players_from_bootstrap]
        ids_to_add = list(set(fpl_ids_from_bootstrap) - set(fpl_ids_from_csv))

        for player in players_from_bootstrap:
            if player["id"] in ids_to_add:
                pos = position_converter(player["element_type"])
                team = team_converter(player["team"])
                first = player["first_name"]
                second = player["second_name"]
                web = player["web_name"]
                fpl_id = str(player["id"])
                players_from_csv.append([pos, team, first, second, web, fpl_id, -1, -1, -1, -1])

    players_from_csv = sorted(players_from_csv, key=lambda x: int(x[5]))

    with open("master.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(players_from_csv)


if __name__ == "__main__":
    main()
