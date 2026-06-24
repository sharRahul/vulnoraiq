"""Launches VulnoraIQ via Docker Compose — no local Python venv required."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPOSE_FILE = ROOT / "docker-compose.yml"


def _run_compose(args: list[str]) -> None:
    cmd = ["docker", "compose", *args]
    print("+ " + " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> None:
    try:
        subprocess.run(
            ["docker", "info"],
            capture_output=True,
            check=True,
            cwd=ROOT,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(
            "Docker engine is not running.\n\n"
            "VulnoraIQ requires Docker Desktop or a compatible Docker engine.\n"
            "Install / start Docker, then re-launch.\n"
        )
        sys.exit(1)

    if not COMPOSE_FILE.exists():
        print(f"docker-compose.yml not found at {COMPOSE_FILE}")
        sys.exit(1)

    _run_compose(["build"])
    _run_compose(["up", "-d"])
    _run_compose(["ps"])

    print("\nVulnoraIQ WebUI is running at http://127.0.0.1:8787")
    print("Run `docker compose down` to stop.")


if __name__ == "__main__":
    main()
