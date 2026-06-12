from src.utils.models import SystemData
from concurrent.futures import  ThreadPoolExecutor
import pandas as pd

from src.utils.decorators.logger import log_stage
from src.preprocessing.preprocess_auditors import preprocess_auditors
from src.preprocessing.preprocess_branches import preprocess_branches
from src.preprocessing.preprocess_holidays import preprocess_holidays
from src.preprocessing.preprocess_history import preprocess_history
from src.preprocessing.preprocess_lat_long import preprocess_lat_long
from src.utils.models import SystemData

PREPROCESSORS = {
    "auditors": preprocess_auditors,
    "holidays": preprocess_holidays,
    "branches": preprocess_branches,
    "history": preprocess_history,
}

@log_stage('Preprocessing')
def preprocess_data(data: SystemData) -> SystemData:
    
    with ThreadPoolExecutor(max_workers=5) as executor:

        futures = {
            name: executor.submit(
                processor,
                getattr(data,name)
            )
            for name, processor
            in PREPROCESSORS.items()
        }

        processed = {
            name: future.result()
            for name, future
            in futures.items()
        }

    processed['lat_long'] = preprocess_lat_long(
        data.lat_long,
        processed['branches']
    )

    return SystemData(
        auditors=processed['auditors'],
        holidays=processed["holidays"],
        branches=processed["branches"],
        history=processed["history"],
        lat_long=processed["lat_long"]
    )