from src.utils.logger import get_logger
from src.utils.config import RAW_DIR
from src.utils.decorators.logger import log_stage
from src.utils.decorators.error_handling import error_handling
from src.utils.exceptions import InvalidFileFormat
from src.ingestion.utils.dataframe import clean_dataframe
import pandas as pd

logger = get_logger(__name__)

@error_handling
def load(file_name: str) -> pd.DataFrame:

    path = RAW_DIR / file_name

    if path.suffix.lower() not in {'.xlsx', '.csv'}:
        raise InvalidFileFormat(f'Expected .xlsx or .csv file, got {file_name}')

    if not path.exists():
        raise FileNotFoundError(
            f'Missing data file: {path}'
        )

    if path.suffix.lower() == '.xlsx':
        raw_df = pd.read_excel(
            path
        )

    else:
        raw_df = pd.read_csv(
            path
        )
        
    df = clean_dataframe(raw_df)

    logger.info(
        'Dataset loaded: %s (%s) rows', 
        path.name, 
        len(df)
    )

    return df