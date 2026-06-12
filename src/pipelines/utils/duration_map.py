from __future__ import annotations

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


DURATION_MAP = {
    ("TFCPC", "OFFSITE"): 6,
    ("TFCPC", "ONSITE"): 9,
    ("NORMAL", "OFFSITE"): 2,
    ("NORMAL", "ONSITE"): 3,
}


class DurationMapper:

    def __init__(self, branches_df: pd.DataFrame) -> None:
        self.branches_df = branches_df.copy()

    # ---------------------------------------------------------
    @staticmethod
    def _normalize_category(category: str) -> str:

        if pd.isna(category):
            return ""

        return (
            str(category)
            .strip()
            .upper()
        )

    # ---------------------------------------------------------l
    def create_tasks(self) -> pd.DataFrame:

        logger.info(
            "Creating audit tasks from %s branches",
            len(self.branches_df),
        )

        tasks = []

        for _, row in self.branches_df.iterrows():

            category = self._normalize_category(
                row["category"]
            )

            for audit_type in (
                "OFFSITE",
                "ONSITE",
            ):

                key = (
                    category,
                    audit_type,
                )

                if key not in DURATION_MAP:

                    logger.error(
                        "Unknown category=%s audit_type=%s "
                        "for branch=%s",
                        category,
                        audit_type,
                        row["br_code"],
                    )

                    raise ValueError(
                        f"Unknown mapping {key}"
                    )

                tasks.append(
                    {
                        "task_id":
                            f"{row['br_code']}_{audit_type}",

                        "br_code":
                            row["br_code"],

                        "br_name":
                            row["br_name"],

                        "circle_vertical":
                            row["circle_vertical"],

                        "category":
                            category,

                        "audit_type":
                            audit_type,

                        "duration_days":
                            DURATION_MAP[key],

                        "eligible_from_date":
                            row[
                                "eligible_from_date_dt"
                            ],

                        "quarter":
                            row["quarter"],
                    }
                )

        task_df = pd.DataFrame(tasks)

        logger.info(
            "Created %s audit tasks",
            len(task_df),
        )

        return task_df