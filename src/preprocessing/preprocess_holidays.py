from __future__ import annotations

import pandas as pd

from src.utils.exceptions import (
    EmptyDatasetError, 
    MissingColumnError,
    DataValidationError
)
from src.utils.config import CLEAN_DIR
from src.utils.logger import get_logger
from src.utils.decorators.save_output import save_output
from src.utils.decorators.logger import log_stage
from src.utils.decorators.error_handling import error_handling
from src.preprocessing.utils.normalize import normalize_date

REQUIRED_COLUMNS = {
    'calendr_group',
    'holidaydate'
}

FORMAT = [
    '%Y-%m-%d'
]

logger = get_logger(__name__)

@log_stage('Preprocess Holiday')
@error_handling
@save_output('holidays', CLEAN_DIR)
def preprocess_holidays(
    df: pd.DataFrame
) -> pd.DataFrame:

    if df.empty:
        raise EmptyDatasetError('Holiday dataset is empty')

    df = df.copy()

    # --------------------------------------------------
    # Standardize Columns
    # --------------------------------------------------

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[ /\-]+", "_", regex=True) 
    )   

    

    # --------------------------------------------------
    # Required Columns
    # --------------------------------------------------

    missing = (
        REQUIRED_COLUMNS
        .difference(df.columns)
    )

    if missing:
        raise MissingColumnError(f'Missing required columns: {sorted(missing)}')

    # --------------------------------------------------
    # Dates
    # --------------------------------------------------

    df = normalize_date(
        df,
        ['holidaydate']
    )

    invalid_dates = (
        df['holidaydate_dt']
        .isna()
    )

    if invalid_dates.any():
        invalid_count = (
            invalid_dates.sum()
        )
        raise DataValidationError(f'{invalid_count} invalid holiday dates detected')

    # --------------------------------------------------
    # Calendar Group
    # --------------------------------------------------

    df['calendr_group'] = (
        df['calendr_group']
        .astype('string')
        .str.strip()
        .str.upper()
    )

    invalid_groups = (
        df['calendr_group'].isna()
        |
        df['calendr_group'].eq('')
    )

    if invalid_groups.any():
        raise DataValidationError('Invalid Calendar Group detected')

    # --------------------------------------------------
    # Remove duplicate holidays
    # --------------------------------------------------

    before = len(df)

    df = (
        df
        .drop_duplicates(
            subset=[
                'calendr_group',
                'holidaydate_dt'
            ]
        )
        .reset_index(drop=True)
    )

    removed = before - len(df)

    if removed:
        logger.warning(
            'Removed %s duplicate holiday records',
            removed
        )

    # --------------------------------------------------
    # Optimize Dtypes
    # --------------------------------------------------

    df['calendr_group'] = (
        df['calendr_group']
        .astype('category')
    )
    
    return df