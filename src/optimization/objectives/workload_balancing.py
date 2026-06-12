from __future__ import annotations

import pandas as pd
from ortools.sat.python import cp_model


def add_workload_balancing_objective(
    model: cp_model.CpModel,
    variables: dict,
    eligibility_df: pd.DataFrame,
    audit_job_master: pd.DataFrame,
) -> None:

    workload_lookup = (
        audit_job_master
        .set_index("branch_code")["audit_days"]
        .to_dict()
    )

    auditors = (
        eligibility_df["auditor_id"]
        .unique()
        .tolist()
    )

    total_days = int(
        audit_job_master["audit_days"].sum()
    )

    workloads = {}

    for auditor in auditors:

        workload = model.NewIntVar(
            0,
            total_days,
            f"workload_{auditor}",
        )

        model.Add(
            workload
            ==
            sum(
                workload_lookup[branch]
                * variables[(auditor, branch)]
                for (a, branch) in variables
                if a == auditor
            )
        )

        workloads[auditor] = workload

    max_workload = model.NewIntVar(
        0,
        total_days,
        "max_workload",
    )

    min_workload = model.NewIntVar(
        0,
        total_days,
        "min_workload",
    )

    model.AddMaxEquality(
        max_workload,
        list(workloads.values()),
    )

    model.AddMinEquality(
        min_workload,
        list(workloads.values()),
    )

    model.Minimize(
        max_workload - min_workload
    )