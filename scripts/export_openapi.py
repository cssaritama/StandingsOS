from pathlib import Path
import sys

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.main import app  # noqa: E402

output = REPOSITORY_ROOT / "openapi.yaml"
output.write_text(yaml.safe_dump(app.openapi(), sort_keys=False), encoding="utf-8")
print(output)
