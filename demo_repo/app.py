from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}")
def get_user(user_id: int):
    users = {
        1: "Monisha",
        2: "RepairX"
    }

    username = users.get(user_id)

    if username is None:
        return {"error": "User not found"}

    return {
        "user": username.upper()
    }
