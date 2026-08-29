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


# ============================================================
# GITHUB LOGIN
# ============================================================

@router.get("/login")
def github_login():

    return {
        "authorization_url": get_github_login_url()
    }


# ============================================================
# GITHUB CALLBACK
# ============================================================

@router.get("/callback")
async def github_callback(code: str):

    try:

        # ----------------------------------------------------
        # Exchange GitHub authorization code for access token
        # ----------------------------------------------------

        token_data = await exchange_code_for_token(code)

        access_token = token_data.get("access_token")

        if not access_token:

            raise HTTPException(
                status_code=400,
                detail="GitHub authorization failed."
            )

        # ----------------------------------------------------
        # Get GitHub user
        # ----------------------------------------------------

        github_user = await get_github_user(
            access_token
        )

        # ----------------------------------------------------
        # Get GitHub repositories
        # ----------------------------------------------------

        repositories = await get_user_repositories(
            access_token
        )

        # ----------------------------------------------------
        # Server-side logging
        # ----------------------------------------------------

        print(
            f"GitHub connected: "
            f"{github_user.get('login')}"
        )

        print(
            f"Repositories found: "
            f"{len(repositories)}"
        )

        # ----------------------------------------------------
        # Redirect back to RepairX frontend
        # ----------------------------------------------------

        return RedirectResponse(
            url="http://localhost:5175/?github=connected"
        )

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
