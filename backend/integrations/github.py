import os
from urllib.parse import urlencode

import httpx
from dotenv import load_dotenv

load_dotenv()


GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API_URL = "https://api.github.com"

GITHUB_CALLBACK_URL = (
    "https://repairx-78w9.onrender.com/api/v1/github/callback"
)


def get_github_login_url():
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_CALLBACK_URL,
        "scope": "repo",
    }

    return f"{GITHUB_AUTHORIZE_URL}?{urlencode(params)}"


async def exchange_code_for_token(code: str):

    data = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GITHUB_CALLBACK_URL,
    }

    headers = {
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:

        response = await client.post(
            GITHUB_TOKEN_URL,
            data=data,
            headers=headers,
        )

        response.raise_for_status()

        return response.json()


async def get_github_user(access_token: str):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{GITHUB_API_URL}/user",
            headers=headers,
        )

        response.raise_for_status()

        return response.json()


async def get_user_repositories(access_token: str):

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{GITHUB_API_URL}/user/repos",
            headers=headers,
            params={
                "per_page": 100,
                "sort": "updated",
            },
        )

        response.raise_for_status()

        return response.json()