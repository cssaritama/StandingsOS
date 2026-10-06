from app.analytics import compute_analytics
from app.forecasting import build_elo_ratings, forecast_match
from app.standings import MatchResult, compute_standings


def test_analytics_use_completed_results_only():
    matches = [
        MatchResult("Atlas", "Aurora", 2, 1),
        MatchResult("Harbor", "Atlas", 0, 0),
    ]
    table = compute_standings(["Atlas", "Aurora", "Harbor"], matches)
    analytics = compute_analytics(table, matches, fixtures_total=4)

    assert analytics.fixtures_completed == 2
    assert analytics.completion_rate == 50.0
    assert analytics.goals_total == 3
    assert analytics.average_goals_per_match == 1.5
    assert analytics.leader == "Atlas"


def test_forecast_is_normalized_and_transparent():
    matches = [
        MatchResult("Atlas", "Aurora", 3, 0),
        MatchResult("Atlas", "Harbor", 2, 0),
        MatchResult("Aurora", "Harbor", 1, 1),
    ]
    forecast = forecast_match(
        "Atlas", "Harbor", ["Atlas", "Aurora", "Harbor"], matches
    )
    total = (
        forecast.home_win_probability
        + forecast.draw_probability
        + forecast.away_win_probability
    )
    assert abs(total - 1.0) <= 0.002
    assert forecast.home_win_probability > forecast.away_win_probability
    assert forecast.model == "elo-v1"


def test_elo_ratings_reward_results():
    ratings = build_elo_ratings(
        ["Atlas", "Aurora"],
        [MatchResult("Atlas", "Aurora", 4, 0)],
    )
    assert ratings["Atlas"] > 1500
    assert ratings["Aurora"] < 1500
