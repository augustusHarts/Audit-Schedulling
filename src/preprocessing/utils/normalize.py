from __future__ import annotations

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype
from src.utils.config import CIRCLE_MAPPING


def normalize_date(
    df: pd.DataFrame,
    date_cols: list[str],
    create_dt_column: bool = True,
) -> pd.DataFrame:

    df = df.copy()

    for col in date_cols:

        if col not in df.columns:
            continue

        if is_datetime64_any_dtype(df[col]):
            parsed = pd.to_datetime(
                df[col],
                errors="coerce"
            )

        else:
            parsed = pd.to_datetime(
                df[col]
                .astype("string")
                .str.strip(),
                format="%Y-%m-%d",
                errors="coerce"
            )

        if create_dt_column:
            df[f"{col}_dt"] = parsed

        df[col] = (
            parsed
            .dt.strftime("%Y-%m-%d")
            .astype("string")
        )

    return df

def normalize_circle(series: pd.Series) -> pd.Series:
    return (
        series
        .astype('string')
        .str.strip()
        .str.upper()
        .replace(CIRCLE_MAPPING)
    )