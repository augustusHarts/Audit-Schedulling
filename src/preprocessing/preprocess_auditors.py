from __future__ import annotations

import pandas as pd

from src.utils.exceptions import (
    EmptyDatasetError, 
    MissingColumnError,
    DuplicateValueError,
    DataValidationError
)
from src.utils.config import CLEAN_DIR
from src.utils.logger import get_logger
from src.utils.decorators.save_output import save_output
from src.utils.decorators.logger import log_stage
from src.utils.decorators.error_handling import error_handling
from src.preprocessing.utils.normalize import normalize_date, normalize_circle

REQUIRED_COLUMNS = {
    'auditor_id',
    'circles_worked_earlier',
    'iad_since',
    'parent_circle'
}

FORMAT = [
    "%m/%d/%Y",
    "%Y-%d-%m %H:%M:%S",
    "%d.%m.%Y",
]

logger = get_logger(__name__)

@log_stage('Preprocess Auditor')
@error_handling
@save_output('auditors', CLEAN_DIR)
def preprocess_auditors(
    df: pd.DataFrame
) -> pd.DataFrame:

    if df.empty:
        raise EmptyDatasetError('Preprocessing Stage Failed: Auditors Dataset is empty')

    df = df.copy()

    #-----Standardize Columns-----
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[ /\-]+", "_", regex=True) 
    )   

    missing = REQUIRED_COLUMNS.difference(df.columns)   
    if missing:
        raise MissingColumnError(f'Missing required columns: {sorted(missing)}')

    #-----Normalize Date-----
    df = normalize_date(
        df, 
        ['iad_since']
    )

    #-----Auditor ID-----
    df['auditor_id'] = (
        df['auditor_id']
        .astype('string')
        .str.strip()
        .str.upper()
    )

    invalid_auditors = (
        df['auditor_id'].isna()
        |
        df['auditor_id'].eq('')
    )

    if invalid_auditors.any():
        raise ValueError(f'Found {invalid_auditors.sum()} invalid Auditor IDs')

    #-----Parent Circle-----
    df['parent_circle'] = normalize_circle(df['parent_circle'])

    df['circles_worked_earlier'] = normalize_circle(df['circles_worked_earlier'])

    missing_parent = (
        df['parent_circle'].isna()
        |
        df['parent_circle'].eq('')
    )

    if missing_parent.any():
        raise DataValidationError(f'Found {missing_parent.sum()} auditors with missing parent_circle')
        
    #-----IAD Since-----
    invalid_iad = (
        df['iad_since_dt']
        .isna()
    )

    if invalid_iad.any():

        logger.warning(
            'Found %s invalid iad_since dates',
            invalid_iad.sum()
        )

    #-----Duplicate Auditor ID-----
    duplicates = (
        df['auditor_id']
        .duplicated(keep=False)
    )

    if duplicates.any():

        duplicate_ids = (
            df.loc[
                duplicates,
                'auditor_id'
            ]
            .unique()
            .tolist()
        )

        raise DuplicateValueError(f'Duplicate Auditor IDs detected: {duplicate_ids[:10]}')

    #-----Memory Optimization-----
    categorical_cols = [
        'parent_circle'
    ]

    for col in categorical_cols:

        if col in df.columns:
            df[col] = (
                df[col]
                .astype('category')
            )

    return df