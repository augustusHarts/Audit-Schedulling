# regional.py

def check_regional_fail(
    branch_circle: str,
    auditor_parent_circle: str,
) -> bool:

    return (
        branch_circle
        == auditor_parent_circle
    )