import math
from dataclasses import dataclass

from app.standings import MatchResult


@dataclass(frozen=True)
class Forecast:
    home_win_probability: float
    draw_probability: float
    away_win_probability: float
    model: str = "elo-v1"


def build_elo_ratings(teams: list[str], matches: list[MatchResult]) -> dict[str, float]:
    ratings = {team: 1500.0 for team in teams}
    k_factor = 24.0
    home_advantage = 55.0

    for match in matches:
        if match.home_team not in ratings or match.away_team not in ratings:
            continue
        home_rating = ratings[match.home_team] + home_advantage
        away_rating = ratings[match.away_team]
        expected_home = 1.0 / (1.0 + 10 ** ((away_rating - home_rating) / 400.0))

        if match.home_goals > match.away_goals:
            actual_home = 1.0
        elif match.home_goals < match.away_goals:
            actual_home = 0.0
        else:
            actual_home = 0.5

        margin = abs(match.home_goals - match.away_goals)
        margin_multiplier = 1.0 + math.log1p(margin) * 0.15
        delta = k_factor * margin_multiplier * (actual_home - expected_home)
        ratings[match.home_team] += delta
        ratings[match.away_team] -= delta

    return ratings


def forecast_match(
    home_team: str,
    away_team: str,
    teams: list[str],
    matches: list[MatchResult],
) -> Forecast:
    ratings = build_elo_ratings(teams, matches)
    home_rating = ratings.get(home_team, 1500.0) + 55.0
    away_rating = ratings.get(away_team, 1500.0)
    home_expectancy = 1.0 / (1.0 + 10 ** ((away_rating - home_rating) / 400.0))

    observed_draw_rate = (
        sum(match.home_goals == match.away_goals for match in matches) / len(matches)
        if matches
        else 0.25
    )
    draw_probability = min(0.35, max(0.18, observed_draw_rate))
    decisive = 1.0 - draw_probability
    home_probability = decisive * home_expectancy
    away_probability = decisive * (1.0 - home_expectancy)

    return Forecast(
        home_win_probability=round(home_probability, 3),
        draw_probability=round(draw_probability, 3),
        away_win_probability=round(away_probability, 3),
    )
