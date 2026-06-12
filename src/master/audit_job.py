import pandas as pd
from src.utils.logger import get_logger
from src.utils.decorators.save_output import save_output
from src.utils.config import MASTER_DIR


class AuditJobBuilder:
    
    logger = get_logger(__name__)

    def __init__(self):
        pass

    @save_output(
        "audit_job_master",
        MASTER_DIR,
    )
    def build(
        self,
        branches: pd.DataFrame,
        duration_master: pd.DataFrame,
    ) -> pd.DataFrame:

        duration_lookup = {
            (
                row["category"],
                row["audit_type"]
            ): row["audit_days"]
            for _, row
            in duration_master.iterrows()
        }

        rows = []

        job_counter = 1

        for _, branch in branches.iterrows():

            for audit_type in (
                "ONSITE",
                "OFFSITE",
            ):

                # self.logger.info(
                #     "Duration Keys: %s",
                #     list(duration_lookup.keys())
                # )

                audit_days = duration_lookup[
                    (
                        branch["category"],
                        audit_type,
                    )
                ]

                rows.append(
                    {
                        "job_id":
                            f"J{job_counter:06d}",

                        "branch_code":
                            branch["branch_code"],

                        "audit_type":
                            audit_type,

                        "audit_days":
                            audit_days,

                        "eligible_from_date":
                            branch["eligible_from_date"],
                    }
                )

                job_counter += 1

        return pd.DataFrame(rows)