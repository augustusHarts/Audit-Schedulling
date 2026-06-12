# src/geospatial/geocode_branch.py

from __future__ import annotations

import pandas as pd

from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

from src.utils.logger import get_logger

logger = get_logger(__name__)

def _build_queries(
    branch_name: str,
    circle_name: str
) -> list[str]:
    """
    Generate progressively broader search queries.
    """

    return [
        f"{branch_name}, {circle_name}, State Bank of India, India",
        f"State Bank of India {branch_name}, India",
    ]


def _create_geocoder() -> RateLimiter:
    """
    Create Nominatim geocoder with rate limiting.
    """

    geolocator = Nominatim(
        user_agent="audit_scheduler_v1",
        timeout=10
    )

    return RateLimiter(
        geolocator.geocode,
        min_delay_seconds=1.1,
        error_wait_seconds=5,
        max_retries=2
    )


def geocode_missing(
    df: pd.DataFrame
) -> pd.DataFrame:

    logger.info("Started Branch Geocoding")

    df = df.copy()

    # --------------------------------------------------
    # Missing Coordinates
    # --------------------------------------------------

    missing_mask = (
        df["latitude"].isna()
        |
        df["longitude"].isna()
    )

    missing_df = (
        df.loc[missing_mask]
        .drop_duplicates(subset=["brnch_nbr"])
        .copy()
    )

    logger.info(
        "Branches Missing Coordinates: %s",
        len(missing_df)
    )

    if missing_df.empty:

        logger.info(
            "No Missing Coordinates Found"
        )

        return df

    # --------------------------------------------------
    # Geocoder
    # --------------------------------------------------

    logger.info(
        "Initializing Geocoder Service"
    )

    geocode = _create_geocoder()

    filled_log: list[dict] = []

    # --------------------------------------------------
    # Geocode Missing Branches
    # --------------------------------------------------

    for row in missing_df.itertuples(index=False):

        branch_code = str(row.BRNCH_NBR).strip()

        branch_name = str(
            getattr(row, "brnch_nme", "")
        ).strip()

        circle_name = str(
            getattr(row, "crcl_nme", "")
        ).strip()

        logger.info(
            "Geocoding Branch %s | %s",
            branch_code,
            branch_name
        )

        latitude = None
        longitude = None

        for query in _build_queries(
            branch_name,
            circle_name
        ):

            try:

                location = geocode(query)

                if location:

                    latitude = round(
                        location.latitude,
                        6
                    )

                    longitude = round(
                        location.longitude,
                        6
                    )

                    logger.info(
                        "Coordinates Found | %s | (%s,%s)",
                        branch_code,
                        latitude,
                        longitude
                    )

                    break

            except Exception:

                logger.exception(
                    "Geocoding Failed For Query: %s",
                    query
                )

        # ----------------------------------------------
        # Update Coordinates
        # ----------------------------------------------

        if latitude is not None:

            df.loc[
                df["brnch_nbr"] == branch_code,
                ["latitude", "longitude"]
            ] = [
                latitude,
                longitude
            ]

            status = "FILLED"

        else:

            logger.warning(
                "Coordinates Not Found | %s | %s",
                branch_code,
                branch_name
            )

            status = "FAILED"

        filled_log.append(
            {
                "brnch_nbr": branch_code,
                "brnch_nme": branch_name,
                "latitude": latitude,
                "longitude": longitude,
                "status": status,
            }
        )
        
    logger.info(
        "Completed Branch Geocoding"
    )

    return df