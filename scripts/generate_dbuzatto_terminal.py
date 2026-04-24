import os
from datetime import datetime, timedelta, timezone

import gifos
import requests


def github_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


def fetch_rest_stats(username: str, token: str) -> dict:
    headers = github_headers(token)
    user_resp = requests.get(
        f"https://api.github.com/users/{username}", headers=headers, timeout=20
    )
    user_resp.raise_for_status()
    user_data = user_resp.json()

    followers = user_data.get("followers", 0)
    repos_count = user_data.get("public_repos", 0)

    stars = 0
    page = 1
    while True:
        repos_resp = requests.get(
            f"https://api.github.com/users/{username}/repos?per_page=100&page={page}",
            headers=headers,
            timeout=20,
        )
        repos_resp.raise_for_status()
        repos = repos_resp.json()
        if not isinstance(repos, list) or len(repos) == 0:
            break
        stars += sum(repo.get("stargazers_count", 0) for repo in repos)
        page += 1

    return {"followers": followers, "repos": repos_count, "stars": stars}


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
    payload = {
        "query": query,
        "variables": {
            "login": username,
            "from": one_year_ago.isoformat(),
            "to": now.isoformat(),
        },
    }
    resp = requests.post(
        "https://api.github.com/graphql",
        headers=github_headers(token),
        json=payload,
        timeout=20,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("data") or not data["data"].get("user"):
        raise RuntimeError("Invalid GraphQL response")
    if "errors" in data:
        raise RuntimeError(data["errors"][0]["message"])
    cc = data["data"]["user"]["contributionsCollection"]
    return {
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "issues": cc["totalIssueContributions"],
    }


def main() -> None:
    username = os.environ.get("GITHUB_REPOSITORY_OWNER", "Y7XIFIED")
    token = os.environ.get("GITHUB_TOKEN", "")

    stats = {
        "followers": 0,
        "stars": 0,
        "commits": 0,
        "prs": 0,
        "issues": 0,
        "repos": 0,
    }

    if token:
        try:
            rest_stats = fetch_rest_stats(username, token)
            gql_stats = fetch_graphql_stats(username, token)
            stats.update(rest_stats)
            stats.update(gql_stats)
        except Exception as e:
            print("ERROR:", e)

    t = gifos.Terminal(width=700, height=450, xpad=10, ypad=10)
    t.set_prompt(f"\x1b[91m{username}\x1b[0m@\x1b[93mgithub\x1b[0m ~> ")

    t.gen_text("Initializing terminal...", row_num=1)
    t.clone_frame(5)
    t.gen_text("\x1b[32m[OK]\x1b[0m System ready", row_num=2)
    t.clone_frame(6)

    t.gen_prompt(row_num=3)
    t.gen_typing_text(f"github-stats --user {username}", row_num=3, contin=True, speed=1)
    t.clone_frame(4)

    t.gen_text("", row_num=4)
    t.gen_text(f"\x1b[96m=== GitHub Stats for {username} ===\x1b[0m", row_num=5)

    lines = [
        f"\x1b[93mName:\x1b[0m        {username}",
        f"\x1b[93mCommits:\x1b[0m     {stats['commits']} (last year)",
        f"\x1b[93mRepos:\x1b[0m       {stats['repos']}",
    ]
    for i, line in enumerate(lines):
        t.gen_text(line, row_num=6 + i)
        t.clone_frame(2)

    base = 6 + len(lines)
    t.gen_text("\x1b[96m================================\x1b[0m", row_num=base)
    t.clone_frame(6)

    t.gen_prompt(row_num=base + 1)
    t.gen_typing_text("pwd", row_num=base + 1, contin=True, speed=1)
    t.clone_frame(3)
    t.gen_text(f"/home/{username}", row_num=base + 2)
    t.clone_frame(3)

    t.gen_prompt(row_num=base + 3)
    t.gen_typing_text("Y7XIFIEE_SKILLS.TXT", row_num=base + 3, contin=True, speed=1)
    t.clone_frame(4)

    t.gen_text("\x1b[96m=== Y7XIFIEE SKILLS ===\x1b[0m", row_num=base + 5)
    skill_lines = [
        ("\x1b[94mFrontend:\x1b[0m   ", "React, Next.js, Astro, TypeScript"),
        ("\x1b[94mStyling:\x1b[0m    ", "SCSS, CSS, Tailwind, Motion"),
        ("\x1b[94mBackend:\x1b[0m    ", "Node.js, Express, REST APIs"),
        ("\x1b[94mTooling:\x1b[0m    ", "npm, Git, GitHub Actions, Vercel"),
        ("\x1b[94mPlatform:\x1b[0m   ", "Windows 11 sometimes mac"),
        ("", "*Every bug is just an undocumented feature, waiting for its moment.*"),
    ]
    for i, (k, v) in enumerate(skill_lines):
        t.gen_text(f"{k}{v}", row_num=base + 6 + i)
        t.clone_frame(2)

    t.clone_frame(20)
    t.gen_gif()


if __name__ == "__main__":
    main()