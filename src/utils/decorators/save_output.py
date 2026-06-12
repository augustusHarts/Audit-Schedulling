from functools import wraps
import pandas as pd

from src.utils.config import CLEAN_DIR

def save_output(name, path):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            df = func(*args, **kwargs)

            if not isinstance(df, pd.DataFrame):
                raise TypeError(
                    f"{func.__name__} "
                    "must return DataFrame"
                )

            df.to_csv(f'{path}/{name}.csv')

            return df

        return wrapper

    return decorator