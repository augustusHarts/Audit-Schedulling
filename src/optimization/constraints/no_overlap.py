from __future__ import annotations

from ortools.sat.python import cp_model
import pandas as pd


def add_no_overlap_constraint(
    model: cp_model.CpModel,
    jobs: pd.DataFrame,
    interval_vars: dict,
) -> None:

    for auditor_id in jobs["auditor_id"].unique():

        auditor_jobs = jobs.loc[
            jobs["auditor_id"] == auditor_id,
            "job_id",
        ]

        intervals = [
            interval_vars[job]
            for job in auditor_jobs
        ]

        model.AddNoOverlap(
            intervals
        )