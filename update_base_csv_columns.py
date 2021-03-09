import csv


def add_header(header, headers, players_from_csv):
    headers.append(header)
    for player in players_from_csv:
        player.append("-1")


def remove_header(header, headers, players_from_csv):
    idx = headers.index(header)
    del headers[idx]
    for player in players_from_csv:
        del player[idx]


def main(add=[], remove=[], filepath="master.csv"):
    with open(filepath, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
        headers = rows[0]
        players_from_csv = rows[1:]

    for header in add:
        add_header(header, headers, players_from_csv)

    for header in remove:
        remove_header(header, headers, players_from_csv)
    
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(players_from_csv)


if __name__ == "__main__":
    main(
        add = [],
        remove = ["WhoScored ID"]
    )
