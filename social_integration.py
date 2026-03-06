"""Social integration for pattern analysis.

Facebook Graph API integration (requires FB App credentials) and
manual social context input for users without FB app access.
"""
import os
import requests
from urllib.parse import urlencode

# Facebook OAuth config (optional — requires FB App)
FB_APP_ID     = os.getenv("FACEBOOK_APP_ID", "")
FB_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET", "")
FB_REDIRECT_URI = os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:8501")

FB_AUTH_URL  = "https://www.facebook.com/v19.0/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/v19.0/oauth/access_token"
FB_ME_URL    = "https://graph.facebook.com/v19.0/me"
FB_POSTS_URL = "https://graph.facebook.com/v19.0/me/posts"


def is_fb_configured() -> bool:
    return bool(FB_APP_ID and FB_APP_SECRET)


def get_fb_auth_url() -> str:
    params = {
        "client_id": FB_APP_ID,
        "redirect_uri": FB_REDIRECT_URI,
        "scope": "user_posts,user_status",
        "response_type": "code",
        "state": "tarot_fb_oauth",
    }
    return f"{FB_AUTH_URL}?{urlencode(params)}"


def exchange_fb_code(code: str) -> dict:
    resp = requests.get(FB_TOKEN_URL, params={
        "client_id": FB_APP_ID,
        "client_secret": FB_APP_SECRET,
        "redirect_uri": FB_REDIRECT_URI,
        "code": code,
    }, timeout=10)
    resp.raise_for_status()
    return resp.json()


def fetch_fb_posts(access_token: str, limit: int = 20) -> list[dict]:
    """Fetch recent Facebook posts for pattern analysis."""
    try:
        resp = requests.get(
            FB_POSTS_URL,
            params={
                "access_token": access_token,
                "fields": "message,story,created_time",
                "limit": limit,
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        posts = []
        for p in data.get("data", []):
            text = p.get("message") or p.get("story", "")
            if text:
                posts.append({
                    "text": text[:200],
                    "date": p.get("created_time", "")[:10],
                })
        return posts
    except Exception:
        return []


def build_social_tarot_prompt(
    social_text: str,
    question: str,
    cards_desc: str,
    source: str = "social media",
) -> str:
    """Build AI prompt combining social patterns with tarot reading."""
    return (
        "You are a mystical counsellor with deep tarot wisdom and sharp intuitive pattern recognition. "
        f"The seeker has shared their recent thoughts and experiences from {source}:\n\n"
        f"{social_text}\n\n"
        f"Tarot spread drawn:\n{cards_desc}\n\n"
        f"Seeker's question: {question}\n\n"
        "Looking at the emotional patterns, recurring themes, and life situations in what they've shared, "
        "combined with the cards drawn, give a deeply personalised cosmic reading. "
        "What patterns do you notice in their life? How do the cards mirror or speak to these themes? "
        "What hidden dynamics or opportunities are revealed? Be warm, poetic, and specific. "
        "End with one clear, actionable cosmic insight. (250-350 words)"
    )


def extract_social_themes(posts: list[dict]) -> str:
    """Summarize social posts for the AI prompt."""
    if not posts:
        return ""
    lines = [f"[{p['date']}] {p['text'][:150]}" for p in posts[:15]]
    return "\n".join(lines)
