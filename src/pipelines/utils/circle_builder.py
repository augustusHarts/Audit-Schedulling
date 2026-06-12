from __future__ import annotations

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from src.utils.logger import get_logger

logger = get_logger(__name__)


class CircleMasterBuilder:

    def __init__(
        self,
        auditors_df: pd.DataFrame,
        branches_df: pd.DataFrame,
        history_df: pd.DataFrame,
    ) -> None:

        self.auditors_df = auditors_df
        self.branches_df = branches_df
        self.history_df = history_df

    # ----------------------------------------------------------
    def _extract_circles(self) -> list[str]:

        circles = set()

        circles.update(
            self.auditors_df["Parent_Circle"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.upper()
        )

        circles.update(
            self.branches_df["Circle_Vertical"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.upper()
        )

        circles.update(
            self.history_df["circlename"]
            .dropna()
            .astype(str)
            .str.strip()
            .str.upper()
        )

        return sorted(circles)

    # ----------------------------------------------------------
    def build(self) -> pd.DataFrame:

        circles = self._extract_circles()

        logger.info(
            "Found %s unique circles",
            len(circles)
        )

        geolocator = Nominatim(
            user_agent="audit_scheduler"
        )

        geocode = RateLimiter(
            geolocator.geocode,
            min_delay_seconds=1
        )

        records = []

        for circle in circles:

            state = None

            try:

                location = geocode(
                    f"{circle}, India",
                    addressdetails=True
                )

                if (
                    location
                    and "address"
                    in location.raw
                ):

                    address = (
                        location.raw["address"]
                    )

                    state = address.get(
                        "state"
                    )

            except Exception as exc:

                logger.warning(
                    "Failed geocoding %s: %s",
                    circle,
                    exc
                )

            records.append(
                {
                    "raw_circle": circle,
                    "canonical_circle": circle,
                    "state": state,
                    "review_required":
                        state is None,
                }
            )

        return pd.DataFrame(records)

    # ----------------------------------------------------------
    @staticmethod
    def save(
        circle_master_df: pd.DataFrame,
        path: str,
    ) -> None:

        circle_master_df.to_csv(
            path,
            index=False,
        )