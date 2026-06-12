# last5.py

def check_last5_fail(
    branch_code: str,
    recent_branches: set[str],
) -> bool:

    return branch_code in recent_branches