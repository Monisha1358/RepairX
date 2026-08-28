from dataclasses import dataclass


@dataclass
class PatchProposal:
    file_path: str
    old_code: str
    new_code: str
    reason: str


class MinimalPatchGenerator:

    def generate_keyerror_patch(self, file_path: str) -> PatchProposal:
        old_code = """username = users[user_id]

    return {
        "user": username.upper()
    }"""

        new_code = """username = users.get(user_id)

    if username is None:
        return {"error": "User not found"}

    return {
        "user": username.upper()
    }"""

        reason = (
            "Replace direct dictionary indexing with a safe lookup and "
            "handle missing users before calling .upper()."
        )

        return PatchProposal(
            file_path=file_path,
            old_code=old_code,
            new_code=new_code,
            reason=reason
        )