from dataclasses import dataclass

from app.standings import MatchResult, Standing


@dataclass(frozen=True)
class SeasonAnalytics:
    fixtures_total: int
    fixtures_completed: int
    completion_rate: float
    goals_total: int
    average_goals_per_match: float
    home_win_rate: float
    draw_rate: float
    away_win_rate: float
    leader: str | None
    strongest_attack: str | None
    strongest_defense: str | None


def _pct(part: int, whole: int) -> float:
    return round((part / whole) * 100, 1) if whole else 0.0


def compute_analytics(
    standings: list[Standing], matches: list[MatchResult], fixtures_total: int
) -> SeasonAnalytics:
    completed = len(matches)
    goals = sum(match.home_goals + match.away_goals for match in matches)
    home_wins = sum(match.home_goals > match.away_goals for match in matches)
    draws = sum(match.home_goals == match.away_goals for match in matches)
    away_wins = sum(match.home_goals < match.away_goals for match in matches)

    played_rows = [row for row in standings if row.played > 0]
    leader = standings[0].team if standings and standings[0].played > 0 else None
    strongest_attack = (
        max(played_rows, key=lambda row: (row.goals_for, row.goal_difference, row.team)).team
        if played_rows
        else None
    )
    strongest_defense = (
        min(played_rows, key=lambda row: (row.goals_against, -row.goal_difference, row.team)).team
        if played_rows
        else None
    )

    return SeasonAnalytics(
        fixtures_total=fixtures_total,
        fixtures_completed=completed,
        completion_rate=_pct(completed, fixtures_total),
        goals_total=goals,
        average_goals_per_match=round(goals / completed, 2) if completed else 0.0,
        home_win_rate=_pct(home_wins, completed),
        draw_rate=_pct(draws, completed),
        away_win_rate=_pct(away_wins, completed),
        leader=leader,
        strongest_attack=strongest_attack,
        strongest_defense=strongest_defense,
    )
