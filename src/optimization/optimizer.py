from __future__ import annotations
import pandas as pd
from ortools.sat.python import cp_model
from src.optimization.variables import create_variables
from src.optimization.constraints import (
    add_eligibility_constraint,
    add_one_auditor_per_branch_constraint,
)
from src.optimization.solver import solve_model
from src.optimization.objectives.workload_balancing import (
    add_workload_balancing_objective,
)

class AssignmentOptimizer:

    def __init__(
        self,
        eligibility_df: pd.DataFrame,
        audit_job_master: pd.DataFrame
    ):
        self.df = eligibility_df.copy()
        self.audit_job = audit_job_master.copy()
        self.model = cp_model.CpModel()
        self.variables: dict = {}

    def add_constraints(self):

        add_eligibility_constraint(
            self.model,
            self.variables,
            self.df,
        )

        add_one_auditor_per_branch_constraint(
            self.model,
            self.variables,
            self.df,
        )

    def add_objectives(self):

        auditors = (
            self.df["auditor_id"]
            .unique()
            .tolist()
        )

        branches = (
            self.df["branch_code"]
            .unique()
            .tolist()
        )
        
        add_workload_balancing_objective(
            self.model,
            self.variables,
            self.df,
            self.audit_job,
        )

    def add_variables(
        self,
    ) -> None:

        self.variables = (
            create_variables(
                self.model,
                self.df,
            )
        )

    def build_model(self):

        self.variables = create_variables(
            self.model,
            self.df,
        )

        self.add_constraints()

        self.add_objectives()

    def solve(
        self,
    ) -> pd.DataFrame:

        self.build_model()

        solver, status = solve_model(
            self.model
        )

        if status not in (
            cp_model.OPTIMAL,
            cp_model.FEASIBLE,
        ):
            raise ValueError(
                "No feasible solution found."
            )

        assignments = []

        for (
            auditor_id,
            branch_code,
        ), var in self.variables.items():

            if solver.Value(var):

                assignments.append(
                    {
                        "auditor_id": auditor_id,
                        "branch_code": branch_code,
                    }
                )

        return pd.DataFrame(
            assignments
        )