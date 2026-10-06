from app.ai import build_evidence_payload, build_prompt


def test_ai_evidence_separates_deterministic_calculation_from_narration():
    evidence = build_evidence_payload(
        season={"name": "2026/27"},
        analytics={"leader": "Atlas", "goals_total": 12},
        standings=[{"team": "Atlas", "points": 9}],
        forecasts=[{"home_team": "Atlas", "home_win_probability": 0.62}],
    )

    assert evidence["policy"]["calculations_are_deterministic"] is True
    assert "never recalculate standings" in evidence["policy"]["llm_role"]
    prompt = build_prompt(evidence)
    assert "Use only the JSON evidence" in prompt
    assert "Do not invent" in prompt
