from __future__ import annotations

from ortools.sat.python import cp_model
import pandas as pd


def add_commencement_constraint(
    model: cp_model.CpModel,
    jobs: pd.DataFrame,
    start_vars: dict,
    quarter_start: pd.Timestamp,
) -> None:

    for row in jobs.itertuples(index=False):

        offset = (
            pd.Timestamp(
                row.eligible_from_date
            )
            - quarter_start
        ).days

        model.Add(
            start_vars[row.job_id]
            >=
            max(offset, 0)
        )