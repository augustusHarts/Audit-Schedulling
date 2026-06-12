from __future__ import annotations

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


class HistoryLookupBuilder:

    def __init__(
        self,
        history_df: pd.DataFrame,
    ) -> None:

        self.history_df = history_df.copy()

    # --------------------------------------------------
    def build_auditor_to_branches(
        self,
    ) -> dict[str, set[str]]:

        logger.info(
            "Building auditor -> branches lookup"
        )

        lookup = (
            self.history_df
            .groupby("auditor_id")["brn_code"]
            .agg(set)
            .to_dict()
        )

        logger.info(
            "Created lookup for %s auditors",
            len(lookup),
        )

        return lookup

    # --------------------------------------------------
    def build_last_5_branches(
        self,
    ) -> dict[str, set[str]]:

        logger.info(
            "Building last 5 branch lookup"
        )

        history = self.history_df.sort_values(
            by="aud_end_dt_dt",
            ascending=False,
        )

        lookup: dict[str, set[str]] = {}

        for auditor_id, group in history.groupby(
            "auditor_id"
        ):

            last_5 = (
                group["brn_code"]
                .drop_duplicates()
                .head(5)
                .tolist()
            )

            lookup[auditor_id] = set(last_5)

        logger.info(
            "Last-5 lookup built for %s auditors",
            len(lookup),
        )

        return lookup

    # --------------------------------------------------
    def build_branch_to_auditors(
        self,
    ) -> dict[str, set[str]]:

        logger.info(
            "Building branch -> auditors lookup"
        )

        lookup = (
            self.history_df
            .groupby("brn_code")["auditor_id"]
            .agg(set)
            .to_dict()
        )

        return lookup