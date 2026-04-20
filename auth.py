"""Google OAuth2 helpers for Streamlit."""
import os
from urllib.parse import urlencode
import requests

def _secret(key: str, default: str = "") -> str:
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

def _client_id():     return _secret("GOOGLE_CLIENT_ID")
def _client_secret(): return _secret("GOOGLE_CLIENT_SECRET")
def _redirect_uri():  return _secret("GOOGLE_REDIRECT_URI", "https://numerologytarot.streamlit.app")

_AUTH_URL     = "https://accounts.google.com/o/oauth2/v2/auth"
_TOKEN_URL    = "https://oauth2.googleapis.com/token"
_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# Base scopes for standard login
_BASE_SCOPES  = "openid email profile"
# Extended scopes for Gmail pattern analysis
_GMAIL_SCOPES = "openid email profile https://www.googleapis.com/auth/gmail.readonly"


def is_configured() -> bool:
    return bool(_client_id() and _client_secret())


def get_auth_url(gmail_scope: bool = False) -> str:
    scope = _GMAIL_SCOPES if gmail_scope else _BASE_SCOPES
    params = {
        "client_id":     _client_id(),
        "redirect_uri":  _redirect_uri(),
        "response_type": "code",
        "scope":         scope,
        "access_type":   "offline",
        "prompt":        "consent",
    }
    return f"{_AUTH_URL}?{urlencode(params)}"


def exchange_code(code: str) -> dict:
    resp = requests.post(_TOKEN_URL, data={
        "client_id":     _client_id(),
        "client_secret": _client_secret(),
        "code":          code,
        "grant_type":    "authorization_code",
        "redirect_uri":  _redirect_uri(),
    }, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_user_info(access_token: str) -> dict:
    resp = requests.get(
        _USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()
