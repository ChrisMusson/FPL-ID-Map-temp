def team_converter(team_id):
    """Converts a team's FPL ID to their FPL name."""
    team_map = {
        1: "Arsenal",
        2: "Aston Villa",
        3: "Brighton",
        4: "Burnley",
        5: "Chelsea",
        6: "Crystal Palace",
        7: "Everton",
        8: "Fulham",
        9: "Leicester",
        10: "Leeds",
        11: "Liverpool",
        12: "Man City",
        13: "Man Utd",
        14: "Newcastle",
        15: "Sheffield Utd",
        16: "Southampton",
        17: "Spurs",
        18: "West Brom",
        19: "West Ham",
        20: "Wolves",
        None: None
    }
    return team_map[team_id]


def position_converter(position):
    """Converts an FPL player's `element_type` to their actual position."""
    position_map = {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Forward"
    }
    return position_map[position]
