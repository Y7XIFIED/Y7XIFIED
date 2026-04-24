import os
from datetime import datetime, timedelta, timezone

import gifos
import requests


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


def fetch_rest_stats(username: str, token: str) -> dict:
    user_resp = requests.get(
        f"https://api.github.com/users/{username}",
        headers=_headers(token),
        timeout=20,
    )
    user_resp.raise_for_status()
    user = user_resp.json()

    stars = 0
    page = 1
    while True:
        repos_resp = requests.get(
            f"https://api.github.com/users/{username}/repos?per_page=100&page={page}",
            headers=_headers(token),
            timeout=20,
        )
        repos_resp.raise_for_status()
        repos = repos_resp.json()
        if not isinstance(repos, list) or not repos:
            break
        stars += sum(r.get("stargazers_count", 0) for r in repos)
        page += 1

    return {
        "followers": user.get("followers", 0),
        "repos": user.get("public_repos", 0),
        "stars": stars,
    }


def fetch_graphql_stats(username: str, token: str) -> dict:
    now = datetime.now(timezone.utc)
    one_year_ago = now - timedelta(days=365)
    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
        }
      }
    }
    """
    resp = requests.post(
        "https://api.github.com/graphql",
        headers=_headers(token),
        json={
            "query": query,
            "variables": {
                "login": username,
                "from": one_year_ago.isoformat(),
                "to": now.isoformat(),
            },
        },
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    user = data.get("data", {}).get("user")
    if not user:
        return {"commits": 0, "prs": 0, "issues": 0}
    cc = user["contributionsCollection"]
    return {
        "commits": cc.get("totalCommitContributions", 0),
        "prs": cc.get("totalPullRequestContributions", 0),
        "issues": cc.get("totalIssueContributions", 0),
    }


def main() -> None:
    username = os.environ.get("GITHUB_REPOSITORY_OWNER", "Y7XIFIED")
    token = os.environ.get("GITHUB_TOKEN", "")

    stats = {"followers": 0, "stars": 0, "commits": 0, "prs": 0, "issues": 0, "repos": 0}
    if token:
        try:
            stats.update(fetch_rest_stats(username, token))
            stats.update(fetch_graphql_stats(username, token))
        except Exception:
            pass

    # Compact height to reduce README vertical footprint.
    t = gifos.Terminal(width=700, height=280, xpad=10, ypad=8)
    t.set_prompt(f"\x1b[91m{username}\x1b[0m@\x1b[93mgithub\x1b[0m ~> ")

    # Auto-advancing terminal effect (gif progression).
    t.gen_text("init terminal...", row_num=1)
    t.clone_frame(2)
    t.gen_text("[OK] ready", row_num=2)
    t.clone_frame(2)

    t.gen_prompt(row_num=3)
    t.gen_typing_text(f"github-stats --user {username}", row_num=3, contin=True, speed=1)
    t.clone_frame(2)

    t.gen_text(f"Followers: {stats['followers']}  Stars: {stats['stars']}  Repos: {stats['repos']}", row_num=5)
    t.gen_text(
        f"Commits: {stats['commits']}  PRs: {stats['prs']}  Issues: {stats['issues']}",
        row_num=6,
    )
    t.clone_frame(3)

    t.gen_prompt(row_num=8)
    t.gen_typing_text("pwd", row_num=8, contin=True, speed=1)
    t.clone_frame(2)
    t.gen_text(f"/home/{username}", row_num=9)

    t.gen_prompt(row_num=10)
    t.gen_typing_text("ls -la", row_num=10, contin=True, speed=1)
    t.clone_frame(2)
    t.gen_text("README.md assets/ workflows/ scripts/", row_num=11)

    t.gen_prompt(row_num=12)
    t.gen_typing_text("Y7XIFIEE_SKILLS.TXT", row_num=12, contin=True, speed=1)
    t.clone_frame(2)
    t.gen_text("Skills: React | Next.js | Astro | Node | GitHub Actions", row_num=13)
    t.clone_frame(16)

    t.gen_gif()


if __name__ == "__main__":
    main()

