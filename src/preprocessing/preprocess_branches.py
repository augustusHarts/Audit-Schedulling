from src.utils.exceptions import (
    EmptyDatasetError, 
    MissingColumnError,
    DuplicateValueError,
    DataValidationError
)
from src.utils.logger import get_logger
from src.utils.decorators.save_output import save_output
from src.utils.decorators.logger import log_stage
from src.utils.decorators.error_handling import error_handling
from src.preprocessing.utils.normalize import normalize_date, normalize_circle
from src.preprocessing.utils.filter import filter_branches
from src.utils.config import VALID_CIRCLES, CLEAN_DIR

import pandas as pd

logger = get_logger(__name__)

REQUIRED_COLUMNS = {
    'branch_code',
    'circle',
    'category',
    'forex_category',
    'eligible_from_date',
    'quarter'
}

FORMAT = [
        "%m/%d/%Y"
    ]

@log_stage('Preprocess Branches')
@error_handling
@save_output('branches', CLEAN_DIR)
def preprocess_branches(
    df: pd.DataFrame
) -> pd.DataFrame:

    if df.empty:
        raise EmptyDatasetError('Preprocessing Stage Failed: Branches Dataset is empty')
    
    df = df.copy()

    #-----Standardize Columns-----
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[ /\-]+", "_", regex=True) 
    )   

    #-----Rename Columns-----
    df = df.rename(
        columns={
            "br_code": "branch_code",
            "br_name": "branch_name",
            "to_be_commenced_before": "eligible_from_date",
            "circle_vertical": "circle",
        }
    )
    
    #-----Required Columns-----
    missing = REQUIRED_COLUMNS.difference(df.columns)   
    if missing:
        raise MissingColumnError(f'Missing required columns: {sorted(missing)}')

    #-----Normalize Date-----
    df = normalize_date(
        df,
        ['eligible_from_date']
    )

    #-----Branch Code-----
    df['branch_code'] = (
        df['branch_code']
        .astype('string')
        .str.strip()
    )

    invalid_branch_codes = (
        df['branch_code']
        .astype('string')
        .str.strip()
        .eq('')
    )
    
    if invalid_branch_codes.any():
        raise DataValidationError('Preprocessing Stage Failed: Empty Branches ID')

    #-----Circle------
    df['circle'] = normalize_circle(df['circle'])

    unknown = set(df["circle"]) - VALID_CIRCLES

    # if unknown:
    #     raise ValueError(
    #         f"Unknown circles found: {sorted(unknown)}"
    #     )

    #-----To Be Commenced Date-----
    if df['eligible_from_date_dt'].isna().any():
        invalid_count = (
            df['eligible_from_date_dt']
            .isna()
            .sum()
        )
        
        raise DataValidationError(f'Preprocessing Stage Failed: {invalid_count} Invalid Commencement date detected in Branches')

    #-----Duplicate Branches-----
    duplicates = df['branch_code'].duplicated(keep=False)
    
    if duplicates.any():
        duplicate_ids = (
            df.loc[duplicates, 'branch_code']
            .unique()
            .tolist()
        )
        raise DuplicateValueError(f'Duplicate Branch Codes detected: {duplicate_ids}')

    #-----Branch Filter-----
    df = filter_branches(
        df=df,
        quarter='Q1',
        forex_category=['B']
    )

    if df.empty:
        raise EmptyDatasetError('No eligible branches found after branch filtering')
        
    return df