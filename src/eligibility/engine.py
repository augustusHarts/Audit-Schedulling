import pandas as pd
from src.eligibility.lookup_builder import EligibilityLookup
from src.eligibility.rules.regional import check_regional_fail
from src.eligibility.rules.no_repeat import check_repeat_fail
from src.eligibility.rules.last_five import check_last5_fail
from src.utils.decorators.save_output import save_output
from src.utils.config import OUTPUT_DIR

class EligibilityEngine:

    def __init__(
        self,
        lookup: EligibilityLookup,
    ):
        self.lookup = lookup

    @save_output(
        "eligibility_dataset",
        OUTPUT_DIR,
    )
    def build(
        self,
        auditors: pd.DataFrame,
        branches: pd.DataFrame,
    ) -> pd.DataFrame:

        rows = []

        auditor_records = auditors.to_dict(
            "records"
        )

        branch_records = branches.to_dict(
            "records"
        )

        for auditor in auditor_records:

            auditor_id = auditor[
                "auditor_id"
            ]

            auditor_history = (
                self.lookup
                .repeat_map
                .get(
                    auditor_id,
                    set(),
                )
            )

            recent_branches = (
                self.lookup
                .last5_map
                .get(
                    auditor_id,
                    set(),
                )
            )

            for branch in branch_records:

                failures = []

                if check_regional_fail(
                    branch["circle"],
                    auditor["parent_circle"],
                ):
                    failures.append(
                        "REGIONAL"
                    )

                if check_repeat_fail(
                    branch["branch_code"],
                    auditor_history,
                ):
                    failures.append(
                        "REPEAT_AUDIT"
                    )

                if check_last5_fail(
                    branch["branch_code"],
                    recent_branches,
                ):
                    failures.append(
                        "LAST_5"
                    )

                rows.append(
                    {
                        "auditor_id":
                            auditor_id,

                        "branch_code":
                            branch[
                                "branch_code"
                            ],

                        "eligible":
                            len(
                                failures
                            ) == 0,

                        "failure_reason":
                            ",".join(
                                failures
                            ),
                    }
                )

        return pd.DataFrame(
            rows
        )