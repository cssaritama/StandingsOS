from dataclasses import dataclass


@dataclass(frozen=True)
class MatchResult:
    home_team: str
    away_team: str
    home_goals: int
    away_goals: int


@dataclass
class Standing:
    team: str
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    points: int = 0

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against


def compute_standings(teams: list[str], matches: list[MatchResult]) -> list[Standing]:
    table = {team: Standing(team=team) for team in teams}

    for match in matches:
        if match.home_team not in table or match.away_team not in table:
            continue

        home = table[match.home_team]
        away = table[match.away_team]
        home.played += 1
        away.played += 1
        home.goals_for += match.home_goals
        home.goals_against += match.away_goals
        away.goals_for += match.away_goals
        away.goals_against += match.home_goals

        if match.home_goals > match.away_goals:
            home.won += 1
            away.lost += 1
            home.points += 3
        elif match.home_goals < match.away_goals:
            away.won += 1
            home.lost += 1
            away.points += 3
        else:
            home.drawn += 1
            away.drawn += 1
            home.points += 1
            away.points += 1

    return sorted(
        table.values(),
        key=lambda row: (
            -row.points,
            -row.goal_difference,
            -row.goals_for,
            row.team.casefold(),
        ),
    )
