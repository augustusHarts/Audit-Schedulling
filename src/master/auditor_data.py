import pandas as pd
from src.utils.decorators.save_output import save_output
from src.utils.config import MASTER_DIR
from src.utils.models import AuditorData
import re

class AuditorMasterBuilder:

    def __init__(self):
        pass

    def _normalize_circles_worked(self, value: str) -> str:

        if pd.isna(value):
            return ""

        value = str(value).upper().strip()

        value = value.replace(" AND ", ",")
        value = value.replace("&", ",")

        value = re.sub(r"\s*,\s*", ",", value)

        return value

    @save_output('auditor_master', MASTER_DIR)
    def build(
        self,
        auditors: pd.DataFrame
    ) -> pd.DataFrame:

        auditor_master = auditors[
            [
                "auditor_id",
                "parent_circle",
                "circles_worked_earlier"
            ]
        ].copy()

    
        auditor_master['circles_worked_earlier'] = (
            auditor_master['circles_worked_earlier']
            .apply(self._normalize_circles_worked)
        )

        auditor_master = (
            auditor_master
            .drop_duplicates(subset=["auditor_id"])
            .sort_values("auditor_id")
            .reset_index(drop=True)
        )

        return auditor_master