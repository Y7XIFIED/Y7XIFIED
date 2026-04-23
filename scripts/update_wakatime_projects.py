import os
import re
from typing import List, Dict

import requests


README_PATH = "README.md"
START_MARKER = "<!--START_SECTION:waka-projects-->"
END_MARKER = "<!--END_SECTION:waka-projects-->"
API_URL = "https://wakatime.com/api/v1/users/current/stats/last_7_days"


def format_duration(seconds: float) -> str:
    total_minutes = int(round(seconds / 60))
    hours = total_minutes // 60
    minutes = total_minutes % 60
    if hours > 0:
        return f"{hours} hrs {minutes} mins"
    return f"{minutes} mins"


def bar(percent: float, width: int = 24) -> str:
    filled = max(0, min(width, int(round((percent / 100) * width))))
    return "█" * filled + "░" * (width - filled)


def build_lines(projects: List[Dict]) -> str:
    top = sorted(projects, key=lambda p: p.get("total_seconds", 0), reverse=True)[:3]
    if not top:
        return "No project data found yet."

    total = sum(p.get("total_seconds", 0) for p in top)
    if total <= 0:
        return "No project data found yet."

    lines = []
    for p in top:
        name = p.get("name", "Unknown")
        secs = float(p.get("total_seconds", 0))
        pct = (secs / total) * 100
        lines.append(
            f"{name:<22} {format_duration(secs):>12}  {bar(pct)}  {pct:6.2f}%"
        )
    return "\n".join(lines)


def main() -> None:
    api_key = os.getenv("WAKATIME_API_KEY")
    if not api_key:
        raise RuntimeError("Missing WAKATIME_API_KEY")

    response = requests.get(API_URL, auth=(api_key, ""), timeout=20)
    response.raise_for_status()
    projects = response.json().get("data", {}).get("projects", [])

    content = open(README_PATH, "r", encoding="utf-8").read()
    replacement = build_lines(projects)
    pattern = rf"({re.escape(START_MARKER)})([\s\S]*?)({re.escape(END_MARKER)})"
    updated = re.sub(pattern, rf"\1\n{replacement}\n\3", content, count=1)

    if updated != content:
        with open(README_PATH, "w", encoding="utf-8", newline="\n") as f:
            f.write(updated)


if __name__ == "__main__":
    main()

