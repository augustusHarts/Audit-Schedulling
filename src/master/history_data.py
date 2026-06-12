import pandas as pd

from src.utils.decorators.save_output import save_output
from src.utils.config import MASTER_DIR
from src.utils.exceptions import (
    EmptyDatasetError,
    MissingColumnError,
)

class AuditorHistoryMasterBuilder:

    REQUIRED_COLUMNS = {
        "auditor_id",
        "branch_code",
        "aud_start_dt",
        "aud_end_dt",
        "circle",
    }

    @save_output(
        "auditor_history_master",
        MASTER_DIR
    )
    def build(
        self,
        history: pd.DataFrame
    ) -> pd.DataFrame:

        history_master = (
            history[
                [
                    "auditor_id",
                    "branch_code",
                    "aud_start_dt",
                    "aud_end_dt",
                    "circle",
                ]
            ]
            .rename(
                columns={
                    "aud_start_dt": "audit_start_date",
                    "aud_end_dt": "audit_end_date",
                }
            )
            .sort_values(
                [
                    "auditor_id",
                    "audit_end_date",
                ]
            )
            .reset_index(drop=True)
        )

        return history_master