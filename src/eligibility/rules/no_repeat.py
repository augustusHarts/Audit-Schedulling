def check_repeat_fail(
    branch_code: str,
    auditor_history: set[str],
) -> bool:
    return branch_code in auditor_history