from __future__ import annotations

import pandas as pd

from src.preprocessing.utils.normalize import normalize_date, normalize_circle
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

logger = get_logger(__name__)

REQUIRED_COLUMNS = {
    "branch_code",
    "auditor_id",
    "circle",
    "aud_start_dt",
    "aud_end_dt",
}

FORMAT = [
    "%m/%d/%Y",
    '%m-%d-%Y'
]

def _fail(msg: str) -> None:
    logger.error(msg)
    raise ValueError(msg)

@log_stage('Preprocess History')
@error_handling
@save_output('history', CLEAN_DIR)
def preprocess_history(
    df: pd.DataFrame
) -> pd.DataFrame:

    # --------------------------------------------------
    # Empty Dataset
    # --------------------------------------------------

    if df.empty:
        raise EmptyDatasetError('History dataset is empty')

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
    # Rename Columns
    # --------------------------------------------------
    df = df.rename(
        columns={
            "brn_code": "branch_code",
            "brn_nme": "branch_name",
            "auditorid": "auditor_id",
            "circlename": "circle",
        }
    )

    # --------------------------------------------------
    # Required Columns
    # --------------------------------------------------

    missing = REQUIRED_COLUMNS.difference(df.columns)

    if missing:
        raise MissingColumnError(
            f'Missing required columns: {sorted(missing)}'
        )

    # --------------------------------------------------
    # Normalize Dates
    # --------------------------------------------------

    df = normalize_date(
        df,
        [
            'aud_start_dt',
            'aud_end_dt'
        ]
    )

    df['circle'] = normalize_circle(df['circle'])
    
    # --------------------------------------------------
    # Standardize Values
    # --------------------------------------------------

    df['branch_code'] = (
        df['branch_code']
        .astype('string')
        .str.strip()
    )

    df['auditor_id'] = (
        df['auditor_id']
        .astype('string')
        .str.strip()
        .str.upper()
    )

    # --------------------------------------------------
    # Branch Validation
    # --------------------------------------------------

    invalid_branch = (
        df['branch_code'].isna()
        |
        df['branch_code'].eq('')
    )

    if invalid_branch.any():
        raise DataValidationError(
            f'Invalid Branch Code detected in {invalid_branch.sum()} rows'
        )

    # --------------------------------------------------
    # Auditor Validation
    # --------------------------------------------------

    invalid_auditor = (
        df['auditor_id'].isna()
        |
        df['auditor_id'].eq('')
    )

    if invalid_auditor.any():
        raise DataValidationError(
            f'Invalid Auditor ID detected in {invalid_auditor.sum()} rows'
        )

    # --------------------------------------------------
    # Date Validation
    # --------------------------------------------------

    invalid_start = (
        df['aud_start_dt_dt']
        .isna()
    )

    if invalid_start.any():
        raise DataValidationError(
            f'Invalid Audit Start Date detected in {invalid_start.sum()} rows'
        )

    invalid_end = (
        df['aud_end_dt_dt']
        .isna()
    )

    if invalid_end.any():
        raise DataValidationError(
            f'Invalid Audit End Date detected in {invalid_end.sum()} rows'
        )

    # --------------------------------------------------
    # Date Range Validation
    # --------------------------------------------------

    invalid_range = (
        df['aud_start_dt_dt']
        >
        df['aud_end_dt_dt']
    )

    if invalid_range.any():
        raise DataValidationError(
            f'Invalid audit date range detected in {invalid_range.sum()} rows'
        )

    # --------------------------------------------------
    # Optional Duplicate Check
    # --------------------------------------------------

    duplicates = df.duplicated(
        subset=[
            'branch_code',
            'auditor_id',
            'aud_start_dt_dt',
            'aud_end_dt_dt'
        ],
        keep=False
    )

    if duplicates.any():

        logger.warning(
            'Found %s duplicate history records',
            duplicates.sum()
        )

    # --------------------------------------------------
    # Memory Optimization
    # --------------------------------------------------

    df['branch_code'] = df['branch_code'].astype('category')
    df['auditor_id'] = df['auditor_id'].astype('category')
    df['circle'] = df['circle'].astype('category')

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    return df