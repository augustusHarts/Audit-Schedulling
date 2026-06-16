from src.utils.decorators.logger import log_stage
from src.utils.decorators.save_output import save_output
from src.optimization.optimizer import AssignmentOptimizer
from src.utils.config import OUTPUT_DIR
from src.optimization.scheduling.jobs import create_schedule_jobs
from src.optimization.scheduling.scheduller import Scheduler
import pandas as pd

class OptimizationPipeline:

    @save_output('audit_assignment', OUTPUT_DIR)
    @log_stage("Optimization")
    def run(
        self,
        eligibility_df,
        audit_job_master
    ):

        optimizer = AssignmentOptimizer(
            eligibility_df,
            audit_job_master
        )

        assignments = (
            optimizer.solve()
        )
        
        kpi_report = (
            assignments
            .merge(
                audit_job_master[
                    [
                        "branch_code",
                        "audit_days",
                        "audit_type",
                    ]
                ],
                on="branch_code",
                how="left",
            )
        )

        summary = (
            kpi_report
            .groupby("auditor_id")
            .agg(
                branch_count=(
                    "branch_code",
                    "nunique",      # <-- important
                ),
                total_audit_days=(
                    "audit_days",
                    "sum",
                ),
                onsite_count=(
                    "audit_type",
                    lambda x: (x == "ONSITE").sum(),
                ),
                offsite_count=(
                    "audit_type",
                    lambda x: (x == "OFFSITE").sum(),
                ),
            )
            .reset_index()
        )

        jobs = create_schedule_jobs(
            assignments,
            audit_job_master,
        )

        scheduler = Scheduler(
            jobs=jobs,
            quarter_start=pd.Timestamp(
                "2025-04-01"
            ),
        )

        result = scheduler.solve()

        return result