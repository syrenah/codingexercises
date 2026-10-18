from datetime import datetime
from functools import wraps
import logging
import os
from pathlib import Path
from typing import Any, Callable

TIMING_LOG = Path(__file__).with_name("method_timing.log")
logger = logging.getLogger(__name__)


def retry(tries: int = 3) -> Callable:
    if tries < 1:
        raise ValueError("tries must be at least 1")

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            subject = next(
                (arg for arg in args if isinstance(arg, str)),
                func.__name__,
            )
            for attempt in range(1, tries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    if _is_aws_permission_error(exc):
                        # Permission denials are not transient: retrying will not
                        # change IAM or bucket policy and only adds denied requests
                        # and audit-log noise. AWS does not normally lock accounts
                        # for this, but repeated requests can still be wasteful.
                        logger.error(
                            "Permission error in %s for %s; not retrying: %s",
                            func.__name__,
                            subject,
                            exc,
                        )
                        raise
                    if attempt < tries:
                        logger.warning(
                            "Attempt %d/%d failed in %s for %s: %s. Retrying.",
                            attempt,
                            tries,
                            func.__name__,
                            subject,
                            exc,
                        )
                    else:
                        raise

        return wrapper

    return decorator


def _is_aws_permission_error(exc: Exception) -> bool:
    response = getattr(exc, "response", None)
    if not isinstance(response, dict):
        return False

    error = response.get("Error", {})
    metadata = response.get("ResponseMetadata", {})
    error_code = str(error.get("Code", ""))
    status_code = metadata.get("HTTPStatusCode")

    return (
        error_code in {
            "AccessDenied",
            "AccessDeniedException",
            "AllAccessDisabled",
            "UnauthorizedOperation",
            "Forbidden",
            "403",
        }
        or status_code == 403
    )


def log_times(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        subject = f" | {args[0]}" if args and isinstance(args[0], str) else ""

        def write_event(event: str) -> None:
            timestamp = datetime.now().astimezone().isoformat(timespec="milliseconds")
            with TIMING_LOG.open("a", encoding="utf-8") as log_file:
                log_file.write(
                    f"{timestamp} | PID {os.getpid()} | {event} | "
                    f"{func.__name__}{subject}\n"
                )

        write_event("START")
        try:
            return func(*args, **kwargs)
        finally:
            write_event("END")

    return wrapper
