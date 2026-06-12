# src/optimization/variables.py

from __future__ import annotations

from ortools.sat.python import cp_model
import pandas as pd


def create_variables(
    model: cp_model.CpModel,
    eligibility_df: pd.DataFrame,
) -> dict[tuple[str, int], cp_model.IntVar]:

    variables: dict[
        tuple[str, int],
        cp_model.IntVar
    ] = {}

    eligible_df = (
        eligibility_df
        .loc[eligibility_df["eligible"]]
        .copy()
    )

    for row in eligible_df.itertuples(index=False):

        key = (
            row.auditor_id,
            row.branch_code,
        )

        variables[key] = model.NewBoolVar(
            f"x_{row.auditor_id}_{row.branch_code}"
        )

    return variables