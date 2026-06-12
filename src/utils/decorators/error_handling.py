from functools import wraps
from src.utils.logger import get_logger

logger = get_logger(__name__)

def error_handling(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except Exception as e:
            logger.exception(
                "Error in %s: %s ",
                func.__name__,
                e
            )
            raise

    return wrapper    