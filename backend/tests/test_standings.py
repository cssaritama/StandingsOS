from app.standings import MatchResult, compute_standings


def test_standings_are_derived_from_match_facts():
    table = compute_standings(
        ["Atlas", "Aurora", "Harbor"],
        [
            MatchResult("Atlas", "Aurora", 2, 1),
            MatchResult("Harbor", "Atlas", 0, 0),
            MatchResult("Aurora", "Harbor", 3, 1),
        ],
    )

    assert [row.team for row in table] == ["Atlas", "Aurora", "Harbor"]
    assert table[0].points == 4
    assert table[0].goal_difference == 1
    assert table[1].points == 3
    assert table[2].points == 1


def test_unknown_match_team_does_not_corrupt_table():
    table = compute_standings(
        ["Atlas"],
        [MatchResult("Atlas", "Unknown", 5, 0)],
    )
    assert table[0].played == 0
    assert table[0].points == 0
