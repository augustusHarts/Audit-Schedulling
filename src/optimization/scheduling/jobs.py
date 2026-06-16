from __future__ import annotations

import pandas as pd


def create_schedule_jobs(
    assignments: pd.DataFrame,
    audit_job_master: pd.DataFrame,
) -> pd.DataFrame:

    jobs = (
        assignments
        .merge(
            audit_job_master[
                [
                    "branch_code",
                    "audit_type",
                    "audit_days",
                    "eligible_from_date",
                ]
            ],
            on="branch_code",
            how="left",
        )
        .reset_index(drop=True)
    )

    jobs["job_id"] = [
        f"J{i+1}"
        for i in range(len(jobs))
    ]

    return jobs[
        [
            "job_id",
            "auditor_id",
            "branch_code",
            "audit_type",
            "audit_days",
            "eligible_from_date",
        ]
    ]