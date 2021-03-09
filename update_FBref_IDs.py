import csv
import requests
from bs4 import BeautifulSoup, Comment

# a map from FPL team names to FBref team names
team_name_map = {
    "Arsenal": "Arsenal",
    "Aston Villa": "Aston Villa",
    "Brighton": "Brighton",
    "Burnley": "Burnley",
    "Chelsea": "Chelsea",
    "Crystal Palace": "Crystal Palace",
    "Everton": "Everton",
    "Fulham": "Fulham",
    "Leeds": "Leeds United",
    "Leicester": "Leicester City",
    "Liverpool": "Liverpool",
    "Man City": "Manchester City",
    "Man Utd": "Manchester Utd",
    "Newcastle": "Newcastle Utd",
    "Sheffield Utd": "Sheffield Utd",
    "Southampton": "Southampton",
    "Spurs": "Tottenham",
    "West Brom": "West Brom",
    "West Ham": "West Ham",
    "Wolves": "Wolves",
}


def get_FBref_data():
    """
    All the player data on this page is stored in a long comment inside the HTML, where some js is then used to 
    render it into an html table as you see in the browser
    """
    url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats"
    with requests.Session() as s:
        resp = s.get(url)
        soup = BeautifulSoup(resp.content , 'html.parser')

    soup = BeautifulSoup(resp.text, 'html.parser')
    comments = soup.find_all(text=lambda text:isinstance(text, Comment))
    for comment in comments:
        if len(comment) > 100000:
            break
    table_body = BeautifulSoup(comment , 'html.parser').find("tbody")
    rows = table_body.find_all("tr")
    wanted = [row for row in rows if ["thead"] not in row.attrs.values()]

    FBref_data = []
    for row in wanted:
        data = row.find_all("td")
        name = data[0].text
        team = data[3].text
        player_ID = data[0].find("a")["href"].split("/")[-2]
        FBref_data.append([name, team, player_ID])
    return FBref_data


def main():
    players_from_FBref = get_FBref_data()

    with open("master.csv", "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
        headers = rows[0]
        players_from_csv = rows[1:]

    for player in players_from_csv:
        if player[8] == "-1":
            full_fpl_name = f"{player[2]} {player[3]}"  # `{first_name} {last_name}`
            for p in players_from_FBref:
                if p[0] == full_fpl_name:
                    player[8] = p[2]
                    break
                else:
                    c = player[4] == " ".join(p[0].split(" ")[-len(player[4]):])  # fpl web_name occurs at the end of FBref name
                    d = team_name_map[player[1]] == p[1]  # both sites say they play for the same team
                    if  c:
                        print(player[4], p[1], p[0])
                    if c and d:
                        player[8] = p[2]  # set the id, but don't break in case an exact match is found

    with open("master.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(players_from_csv)

if __name__ == "__main__":
    main()