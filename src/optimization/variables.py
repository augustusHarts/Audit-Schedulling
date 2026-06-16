from __future__ import annotations
from ortools.sat.python import cp_model
import pandas as pd

def create_schedule_variables(
    model: cp_model.CpModel,
    jobs: pd.DataFrame,
    horizon: int,
):

    start_vars = {}
    end_vars = {}
    interval_vars = {}

    for row in jobs.itertuples(index=False):

        start = model.NewIntVar(
            0,
            horizon,
            f"start_{row.job_id}",
        )

        end = model.NewIntVar(
            0,
            horizon,
            f"end_{row.job_id}",
        )

        interval = model.NewIntervalVar(
            start,
            int(row.audit_days),
            end,
            f"interval_{row.job_id}",
        )

        start_vars[row.job_id] = start
        end_vars[row.job_id] = end
        interval_vars[row.job_id] = interval

    return (
        start_vars,
        end_vars,
        interval_vars,
    )


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