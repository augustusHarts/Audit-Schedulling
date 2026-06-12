from src.utils.decorators.logger import log_stage
from src.utils.decorators.save_output import save_output
from src.optimization.optimizer import AssignmentOptimizer
from src.utils.config import OUTPUT_DIR

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
        
        assignment_summary = (
            assignments
            .groupby("auditor_id")
            .agg(
                branch_count=(
                    "branch_code",
                    "count"
                )
            )
            .sort_values(
                "branch_count",
                ascending=False
            )
            .reset_index()
        )

        workload_summary = (
            assignments
            .merge(
                audit_job_master[
                    [
                        "branch_code",
                        "audit_days",
                    ]
                ],
                on="branch_code",
                how="left",
            )
            .groupby("auditor_id")
            .agg(
                total_audit_days=(
                    "audit_days",
                    "sum"
                )
            )
            .sort_values(
                "total_audit_days",
                ascending=False
            )
            .reset_index()
        )
        audit_type_split = (
            assignments
            .merge(
                audit_job_master[
                    [
                        "branch_code",
                        "audit_type",
                    ]
                ],
                on="branch_code",
                how="left",
            )
            .pivot_table(
                index="auditor_id",
                columns="audit_type",
                values="branch_code",
                aggfunc="count",
                fill_value=0,
            )
            .reset_index()
        )
        
        print("Assignment Summary \n",assignment_summary)
        print("Workload Summary \n",workload_summary)
        print("Audit type split \n",audit_type_split)

        return assignments