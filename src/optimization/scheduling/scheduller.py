from ortools.sat.python import cp_model
from src.optimization.variables import create_schedule_variables
from src.optimization.constraints.no_overlap import add_no_overlap_constraint
from src.optimization.constraints.commencement import add_commencement_constraint
from src.optimization.constraints.horizon import add_horizon_constraint
import pandas as pd

class Scheduler:

    HORIZON = 90

    def __init__(
        self,
        jobs,
        quarter_start,
    ):
        self.jobs = jobs
        self.quarter_start = quarter_start
        self.model = cp_model.CpModel()

    def build_model(self):

        (
            self.start_vars,
            self.end_vars,
            self.interval_vars,
        ) = create_schedule_variables(
            self.model,
            self.jobs,
            self.HORIZON,
        )

        add_no_overlap_constraint(
            self.model,
            self.jobs,
            self.interval_vars,
        )

        # add_commencement_constraint(
        #     self.model,
        #     self.jobs,
        #     self.start_vars,
        #     self.quarter_start,
        # )

        # add_horizon_constraint(
        #     self.model,
        #     self.end_vars,
        #     self.HORIZON,
        # )

    def solve(self):

        self.build_model()

        solver = cp_model.CpSolver()

        status = solver.Solve(
            self.model
        )

        if status not in (
            cp_model.OPTIMAL,
            cp_model.FEASIBLE,
        ):
            raise ValueError(
                "No feasible schedule found."
            )

        schedule = []

        for row in self.jobs.itertuples(index=False):

            schedule.append(
                {
                    "job_id": row.job_id,
                    "auditor_id": row.auditor_id,
                    "branch_code": row.branch_code,
                    "audit_type": row.audit_type,
                    "start_day": solver.Value(
                        self.start_vars[row.job_id]
                    ),
                    "end_day": solver.Value(
                        self.end_vars[row.job_id]
                    ),
                }
            )

        return pd.DataFrame(schedule)