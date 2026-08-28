from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from backend.integrations.github import (
    get_github_login_url,
    exchange_code_for_token,
    get_github_user,
    get_user_repositories,
)


router = APIRouter(
    prefix="/api/v1/github",
    tags=["GitHub"],
)


@router.get("/login")
def github_login():
    return {
        "authorization_url": get_github_login_url()
    }


@router.get("/callback")
async def github_callback(code: str):

    try:
        token_data = await exchange_code_for_token(code)

        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(
                status_code=400,
                detail="GitHub authorization failed."
            )

        github_user = await get_github_user(access_token)

        repositories = await get_user_repositories(
            access_token
        )

        return {
            "message": "GitHub connected successfully",

            "github_user": {
                "login": github_user.get("login"),
                "name": github_user.get("name"),
            },

            "repositories": [
                {
                    "name": repo.get("name"),
                    "full_name": repo.get("full_name"),
                    "html_url": repo.get("html_url"),
                    "private": repo.get("private"),
                }
                for repo in repositories
            ],
        }

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )