from __future__ import annotations
from src.utils.logger import get_logger
from src.utils.config import QUARTER, FOREX_CATEGORY, CATEGORY
import pandas as pd

REQUIRED_COLUMNS = {
    'quarter',
    'forex_category',
    'category'
}

logger = get_logger(__name__)

def _fail(logger,msg: str) -> None:
    logger.error(msg)
    raise ValueError(msg)

def _normalize(
    series: pd.Series
) -> pd.Series:

    return (
        series
        .astype('string')
        .str.strip()
        .str.upper()
    )

def _apply_filter(
    df: pd.DataFrame,
    column: str,
    values: list[str],
    logger
) -> pd.DataFrame:

    values = [
        value.strip().upper()
        for value in values
    ]

    df = df[
        _normalize(df[column])
        .isin(values)
    ]

    return df

def filter_branches(
    df: pd.DataFrame,
    quarter: str | None = QUARTER,
    forex_category: list[str] | None = FOREX_CATEGORY,
    category: list[str] | None = CATEGORY
) -> pd.DataFrame:

    logger.info('Started Branch Filtering')

    if df.empty:
        _fail(
            logger,
            'Branch Dataset is empty'
        )

    df = df.copy()

    missing = (
        REQUIRED_COLUMNS
        .difference(df.columns)
    )

    if missing:
        _fail(
            logger,
            f'Missing Required Columns: '
            f'{sorted(missing)}'
        )

    #-----Quarter Filter-----
    if quarter:
        
        df = df[
            _normalize(
                df['quarter']
            )
            ==
            quarter.strip().upper()
        ]

        logger.info('Branch Count After Quarter Filter: %s', len(df))

    #-----Forex Category-----
    if forex_category:
        df = _apply_filter(
            df=df,
            column='forex_category',
            values=FOREX_CATEGORY,
            logger=logger
        )

    if category:

        df = _apply_filter(
            df=df,
            column='category',
            values=category,
            logger=logger
        )

    logger.info(
        'Final Branch Count: %s',
        len(df)
    )

    return df