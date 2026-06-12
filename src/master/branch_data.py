import pandas as pd

from src.utils.exceptions import (
    EmptyDatasetError,
    DuplicateValueError,
    DataValidationError
)

from src.utils.decorators.save_output import save_output
from src.utils.config import MASTER_DIR


class BranchMasterBuilder:

    def __init__(self):
        pass

    @save_output("branch_master", MASTER_DIR)
    def build(
        self,
        branches: pd.DataFrame,
        lat_long: pd.DataFrame,
    ) -> pd.DataFrame:

        if branches.empty:
            raise EmptyDatasetError(
                "Branches dataset is empty"
            )

        if lat_long.empty:
            raise EmptyDatasetError(
                "Lat Long dataset is empty"
            )

        branch_master = (
            branches.merge(
                lat_long[
                    [
                        "branch_code",
                        "latitude",
                        "longitude",
                    ]
                ],
                on="branch_code",
                how="left",
            )
        )

        required_columns = [
            "branch_code",
            "branch_name",
            "circle",
            "category",
            "eligible_from_date_dt",
            "latitude",
            "longitude",
        ]

        missing = (
            set(required_columns)
            - set(branch_master.columns)
        )

        if missing:
            print(branch_master.columns)
            # raise DataValidationError(
            #     f"Missing columns: {sorted(missing)}"
            # )

        duplicate_codes = (
            branch_master["branch_code"]
            .duplicated(keep=False)
        )

        if duplicate_codes.any():

            duplicates = (
                branch_master.loc[
                    duplicate_codes,
                    "branch_code"
                ]
                .unique()
                .tolist()
            )

            raise DuplicateValueError(
                f"Duplicate branch codes found: {duplicates}"
            )

        branch_master = (
            branch_master[
                [
                    "branch_code",
                    "branch_name",
                    "circle",
                    "category",
                    "eligible_from_date_dt",
                    "latitude",
                    "longitude",
                ]
            ]
            .rename(
                columns={
                    "eligible_from_date_dt": "eligible_from_date",
                }
            )
            .sort_values("branch_code")
            .reset_index(drop=True)
        )

        return branch_master