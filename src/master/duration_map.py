import pandas as pd

from src.utils.decorators.save_output import save_output
from src.utils.config import MASTER_DIR


class DurationMasterBuilder:

    def __init__(self):
        pass

    @save_output(
        "duration_master",
        MASTER_DIR,
    )
    def build(self) -> pd.DataFrame:

        rows = [
            {
                "category": 'RETAIL',
                "audit_type": "ONSITE",
                "audit_days": 3,
            },
            {
                "category": 'RETAIL',
                "audit_type": "OFFSITE",
                "audit_days": 2,
            },
            {
                "category": 'TRADE',
                "audit_type": "ONSITE",
                "audit_days": 9,
            },
            {
                "category": 'TRADE',
                "audit_type": "OFFSITE",
                "audit_days": 6,
            },
        ]

        return pd.DataFrame(rows)