import pandas as pd
from src.utils.models import EligibilityLookup

class LookupBuilder:

    def build(
        self,
        history: pd.DataFrame,
    ) -> EligibilityLookup:

        history = (
            history
            .sort_values(
                [
                    "auditor_id",
                    "audit_end_date",
                ]
            )
            .copy()
        )

        repeat_map = {}
        last5_map = {}

        for auditor_id, group in history.groupby(
            "auditor_id"
        ):

            repeat_map[auditor_id] = set(
                group["branch_code"]
            )

            last5_map[auditor_id] = set(
                group
                .tail(5)["branch_code"]
            )

        return EligibilityLookup(
            repeat_map=repeat_map,
            last5_map=last5_map,
        )