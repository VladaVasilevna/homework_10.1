import functools
import logging
import sys
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования вызовов функций."""
    logger = logging.getLogger("FunctionLogger")
    logger.setLevel(logging.DEBUG)

    # Объявляем handler один раз
    handler: logging.Handler

    # Определяем обработчик
    if filename:
        handler = logging.FileHandler(filename)
    else:
        handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """Декоратор для функции, который добавляет логирование."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                logger.info(f"Calling function: {func.__name__} with args: {args}, kwargs: {kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok, result: {result}")
                return result
            except Exception as e:
                logger.error(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise

        return wrapper

    return decorator
