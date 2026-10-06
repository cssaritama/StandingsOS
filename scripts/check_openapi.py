from __future__ import annotations

import json
from pathlib import Path
import sys

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.main import app  # noqa: E402


def canonical(value) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False)


committed_path = REPOSITORY_ROOT / "openapi.yaml"
committed = yaml.safe_load(committed_path.read_text(encoding="utf-8"))
generated = app.openapi()

if committed != generated:
    committed_paths = set((committed or {}).get("paths", {}))
    generated_paths = set(generated.get("paths", {}))

    print("OpenAPI contract is out of date.")
    print()
    print("Added paths:", sorted(generated_paths - committed_paths))
    print("Removed paths:", sorted(committed_paths - generated_paths))
    print()
    print("Regenerate the contract with:")
    print("  cd backend && uv run python ../scripts/export_openapi.py")
    print()
    # Keep the CI output bounded while still making diagnosis possible.
    if committed_paths == generated_paths:
        print("The route set is unchanged; schema or metadata changed.")
        print("Committed info:")
        print(canonical((committed or {}).get("info", {})))
        print("Generated info:")
        print(canonical(generated.get("info", {})))
    raise SystemExit(1)

print("OpenAPI contract is current.")
