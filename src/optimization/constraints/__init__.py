"""Constraint functions for the optimization model."""

from src.optimization.constraints.eligible_auditors import (
    add_eligibility_constraint,
)
from src.optimization.constraints.one_auditor_per_branch import (
    add_one_auditor_per_branch_constraint,
)

__all__ = [
    "add_eligibility_constraint",
    "add_one_auditor_per_branch_constraint",
]
