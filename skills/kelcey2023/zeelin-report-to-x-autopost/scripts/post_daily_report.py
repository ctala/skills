#!/usr/bin/env python3
import json, os, requests, subprocess
from pathlib import Path

REPORTS_URL = os.environ.get('ZEELIN_REPORTS_URL', 'https://thu-nmrc.github.io/THU-ZeeLin-Reports/reports_config.json')
SITE_URL = os.environ.get('ZEELIN_SITE_URL', 'https://thu-nmrc.github.io/THU-ZeeLin-Reports/')
STATE_PATH = Path(os.environ.get('ZEELIN_STATE_PATH', '/Users/youke/.openclaw/workspace/memory/report-post-state.json'))
TWEET_SCRIPT = os.environ.get('ZEELIN_TWEET_SCRIPT', '/Users/youke/.openclaw/workspace/skills/zeelin-twitter-web-autopost/scripts/tweet.sh')
BASE_URL = os.environ.get('ZEELIN_X_BASE_URL', 'https://x.com')
LANG = os.environ.get('ZEELIN_TWEET_LANG', 'en')


def load_state():
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            pass
    return {"posted": []}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def build_tweet(report):
    title = report['title']
    abstract = (report.get('abstract') or '').strip().replace('\n', ' ')
    if LANG == 'zh':
        prefix = f"今日报告：{title}"
    else:
        prefix = f"Today's report: {title}"
    summary = abstract
    tweet = f"{prefix}\n\n{summary}\n\n{SITE_URL}"
    if len(tweet) > 280:
        keep = max(40, 280 - len(prefix) - len(SITE_URL) - 6)
        summary = summary[:keep].rstrip() + '...'
        tweet = f"{prefix}\n\n{summary}\n\n{SITE_URL}"
    return tweet


def main():
    reports = requests.get(REPORTS_URL, timeout=20).json()
    state = load_state()
    posted = set(state.get('posted', []))
    chosen = None
    for report in reports:
        if report['id'] not in posted:
            chosen = report
            break
    if not chosen:
        print('No unposted report found.')
        return 0
    tweet = build_tweet(chosen)
    print(tweet)
    subprocess.run(['bash', TWEET_SCRIPT, tweet, BASE_URL], check=True)
    state.setdefault('posted', []).append(chosen['id'])
    save_state(state)
    print(f"Posted: {chosen['id']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
