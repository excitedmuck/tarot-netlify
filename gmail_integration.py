"""Gmail integration — fetch recent email subjects/snippets for pattern analysis.

Uses Gmail REST API with the user's existing Google OAuth token.
Requires the gmail.readonly scope to be requested during OAuth.
"""
import requests
from typing import Optional

GMAIL_MESSAGES_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages"
GMAIL_MESSAGE_URL  = "https://gmail.googleapis.com/gmail/v1/users/me/messages/{id}"
GMAIL_PROFILE_URL  = "https://gmail.googleapis.com/gmail/v1/users/me/profile"

# Emotional/thematic keywords to search for patterns
EMOTIONAL_QUERIES = [
    "subject:(urgent OR worried OR anxious OR stressed)",
    "subject:(happy OR excited OR celebration OR congrats)",
    "subject:(decision OR choice OR thinking OR wondering)",
    "subject:(love OR relationship OR friend OR family)",
    "subject:(money OR payment OR invoice OR salary)",
    "subject:(job OR career OR opportunity OR interview)",
]


def has_gmail_scope(access_token: str) -> bool:
    """Check if the token has Gmail access."""
    try:
        resp = requests.get(
            GMAIL_PROFILE_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=8,
        )
        return resp.status_code == 200
    except Exception:
        return False


def fetch_recent_subjects(access_token: str, max_results: int = 25) -> list[dict]:
    """Fetch recent email subjects and snippets (no body content).

    Returns list of dicts with keys: subject, snippet, date_str.
    """
    try:
        # Get message IDs
        params = {
            "maxResults": max_results,
            "q": "in:inbox -category:promotions -category:social",
        }
        resp = requests.get(
            GMAIL_MESSAGES_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        messages = resp.json().get("messages", [])

        results = []
        for msg in messages[:max_results]:
            msg_id = msg["id"]
            detail_resp = requests.get(
                GMAIL_MESSAGE_URL.format(id=msg_id),
                headers={"Authorization": f"Bearer {access_token}"},
                params={"format": "metadata", "metadataHeaders": ["Subject", "Date"]},
                timeout=8,
            )
            if detail_resp.status_code != 200:
                continue
            data = detail_resp.json()
            headers = {h["name"]: h["value"] for h in data.get("payload", {}).get("headers", [])}
            subject = headers.get("Subject", "(no subject)")
            snippet = data.get("snippet", "")[:120]
            date_str = headers.get("Date", "")[:16]
            results.append({"subject": subject, "snippet": snippet, "date": date_str})

        return results
    except Exception:
        return []


def extract_email_themes(emails: list[dict]) -> str:
    """Create a compact summary of email themes for AI analysis."""
    if not emails:
        return "No recent emails available."

    lines = []
    for e in emails[:20]:
        subj = e.get("subject", "")[:60]
        snip = e.get("snippet", "")[:80]
        lines.append(f"• {subj}" + (f" — {snip}" if snip else ""))

    return "\n".join(lines)


def build_gmail_tarot_prompt(email_summary: str, question: str, cards_desc: str) -> str:
    """Build an AI prompt combining Gmail patterns with tarot reading."""
    return (
        "You are a mystical sage and intuitive counsellor with deep tarot wisdom. "
        "You have been given access to a seeker's recent email subjects (no private content — "
        "only subjects and brief snippets) to understand the emotional landscape of their life.\n\n"
        f"Recent life themes from their inbox:\n{email_summary}\n\n"
        f"Tarot spread drawn:\n{cards_desc}\n\n"
        f"Seeker's question: {question}\n\n"
        "Weave together the themes emerging from their daily life (as seen in their inbox) with "
        "the wisdom of the cards. Notice any patterns — what are they dealing with? "
        "What are the cards reflecting back? Be warm, specific, and insightful. "
        "Keep it poetic but grounded in the real themes you observe. End with a single, "
        "actionable piece of cosmic guidance. (200-300 words)"
    )
