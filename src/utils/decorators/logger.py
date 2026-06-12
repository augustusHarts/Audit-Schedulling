from src.utils.logger import get_logger
from functools import wraps
import time

logger = get_logger(__name__)

def log_stage(name=None):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            display_name = name or func.__name__

            logger.info(
                "Started %s",
                display_name
            )

            start = time.perf_counter()

            try:

                result = func(*args, **kwargs)

                duration = (
                    time.perf_counter()
                    - start
                )

                logger.info(
                    "Completed %s in %.2f sec",
                    display_name,
                    duration
                )

                return result

            except Exception:

                duration = (
                    time.perf_counter()
                    - start
                )

                logger.exception(
                    "Failed %s after %.2f sec",
                    display_name,
                    duration
                )

                raise

        return wrapper

    return decorator