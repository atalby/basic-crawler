import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s"
)

def log_info(message: str) -> None:
    logging.info(message)

def log_warn(message: str) -> None:
    logging.warning(message)

def log_error(message: str) -> None:
    logging.error(message)

