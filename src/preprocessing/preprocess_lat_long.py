from src.utils.logger import get_logger
from src.utils.config import CLEAN_DIR
from src.utils.decorators.save_output import save_output
from src.utils.decorators.logger import log_stage
from src.utils.decorators.error_handling import error_handling
from src.preprocessing.utils.normalize import normalize_circle
from src.preprocessing.utils.geopy import geocode_missing

import pandas as pd

logger = get_logger(__name__)

REQUIRED_COLUMNS = {
    'branch_code',
    'latitude',
    'longitude'
}


def _fail(msg: str) -> None:
    logger.error(msg)
    raise ValueError(msg)

@log_stage('Preprocess Lat Long')
@error_handling
@save_output('lat_long', CLEAN_DIR)
def preprocess_lat_long(
    lat_long_df: pd.DataFrame,
    branches_df: pd.DataFrame
) -> pd.DataFrame:

    # --------------------------------------------------
    # Empty Dataset Validation
    # --------------------------------------------------

    if lat_long_df.empty:
        _fail('Lat-Long dataset is empty')

    if branches_df.empty:
        _fail('Branches dataset is empty')

    df = lat_long_df.copy()

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
            "brnch_nbr": "branch_code",
            "brnch_nme": "branch_name",
            "crcl_nme": "circle",
        }
    )

    # --------------------------------------------------
    # Standardize Columns
    # --------------------------------------------------
    df['circle'] = normalize_circle(df['circle'])

    # --------------------------------------------------
    # Required Columns
    # --------------------------------------------------

    missing = REQUIRED_COLUMNS.difference(df.columns)

    if missing:
        _fail(
            f'Missing required columns: {sorted(missing)}'
        )

    # --------------------------------------------------
    # Branch Code Cleanup
    # --------------------------------------------------

    df['branch_code'] = (
        df['branch_code']
        .astype('string')
        .str.strip()
        .str.upper()
    )

    invalid_branch_codes = (
        df['branch_code'].isna()
        |
        df['branch_code'].eq('')
    )

    if invalid_branch_codes.any():
        _fail('Invalid Branch Code detected')

    duplicates = (
        df['branch_code']
        .duplicated(keep=False)
    )

    if duplicates.any():

        duplicate_codes = (
            df.loc[
                duplicates,
                'branch_code'
            ]
            .unique()
            .tolist()
        )

        _fail(
            f'Duplicate Branch Codes detected: '
            f'{duplicate_codes[:10]}'
        )

    # --------------------------------------------------
    # Keep Only Eligible Audit Branches
    # --------------------------------------------------

    branch_codes = (
        branches_df['branch_code']
        .astype('string')
        .str.strip()
        .str.upper()
        .unique()
    )

    df = df[
        df['branch_code']
        .isin(branch_codes)
    ].copy()

    logger.info(
        'Lat-Long records after filtering: %s',
        len(df)
    )

    if df.empty:
        _fail(
            'No matching branch coordinates found'
        )

    # --------------------------------------------------
    # Coordinate Cleanup
    # --------------------------------------------------

    for col in ['latitude', 'longitude']:

        df[col] = (
            df[col]
            .astype('string')
            .str.replace('#', '.', regex=False)
        )

        df[col] = pd.to_numeric(
            df[col],
            errors='coerce'
        )

    # Some SBI datasets store missing coords as 0,0

    zero_mask = (
        (df['latitude'] == 0)
        &
        (df['longitude'] == 0)
    )

    df.loc[
        zero_mask,
        ['latitude', 'longitude']
    ] = pd.NA

    # --------------------------------------------------
    # Geocode Missing Coordinates
    # --------------------------------------------------

    df = geocode_missing(df)

    # --------------------------------------------------
    # Coordinate Validation
    # --------------------------------------------------

    if (
        df['latitude']
        .isna()
        .any()
    ):

        logger.warning(
            'Some branch coordinates could not be geocoded'
        )

    invalid_lat = (
        df['latitude'].notna()
        &
        ~df['latitude'].between(-90, 90)
    )

    if invalid_lat.any():
        _fail('Invalid Latitude Range detected')

    invalid_lon = (
        df['longitude'].notna()
        &
        ~df['longitude'].between(-180, 180)
    )

    if invalid_lon.any():
        _fail('Invalid Longitude Range detected')

    return df