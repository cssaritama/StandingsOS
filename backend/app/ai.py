from datetime import datetime, timezone

import httpx

from app.config import AI_MODEL, AI_PROVIDER, AI_TIMEOUT_SECONDS, OLLAMA_BASE_URL


class AIUnavailable(RuntimeError):
    pass


def build_evidence_payload(*, season: dict, analytics: dict, standings: list[dict], forecasts: list[dict], readiness: dict | None = None) -> dict:
    return {
        "season": season,
        "data_readiness": readiness,
        "analytics": analytics,
        "standings": standings[:6],
        "forecasts": forecasts[:5],
        "policy": {
            "calculations_are_deterministic": True,
            "llm_role": "narrate and prioritize evidence, never recalculate standings",
        },
    }


def build_prompt(evidence: dict) -> str:
    return (
        "You are an analyst writing a concise competition briefing. Use only the JSON evidence "
        "below. Do not invent injuries, transfers, tactics, external news, or statistics. Do not "
        "recalculate standings. Write: (1) current state, (2) two evidence-backed observations, "
        "(3) one next-match watch item. Mention uncertainty when forecast probabilities are close.\n\n"
        f"EVIDENCE:\n{evidence}"
    )


async def generate_brief(evidence: dict) -> dict:
    if AI_PROVIDER == "disabled":
        raise AIUnavailable(
            "AI briefing is disabled. Set AI_PROVIDER=ollama and provide a reachable Ollama endpoint."
        )
    if AI_PROVIDER != "ollama":
        raise AIUnavailable(f"Unsupported AI provider: {AI_PROVIDER}")

    payload = {
        "model": AI_MODEL,
        "prompt": build_prompt(evidence),
        "stream": False,
    }
    async with httpx.AsyncClient(timeout=AI_TIMEOUT_SECONDS) as client:
        response = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload)
        response.raise_for_status()
        body = response.json()

    return {
        "provider": "ollama",
        "model": AI_MODEL,
        "generated_at": datetime.now(timezone.utc),
        "summary": body.get("response", "").strip(),
        "evidence": evidence,
    }
