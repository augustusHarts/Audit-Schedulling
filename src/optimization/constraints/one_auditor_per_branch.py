# src/optimization/constraints/one_auditor_per_branch.py

from __future__ import annotations

from ortools.sat.python import cp_model
import pandas as pd


def add_one_auditor_per_branch_constraint(
    model: cp_model.CpModel,
    variables: dict,
    eligibility_df: pd.DataFrame,
) -> None:

    branches = sorted(
        eligibility_df["branch_code"]
        .unique()
    )

    for branch in branches:

        branch_vars = [
            var
            for (auditor, branch_code), var
            in variables.items()
            if branch_code == branch
        ]

        model.Add(
            sum(branch_vars) == 1
        )