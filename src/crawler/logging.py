import logging

logger = logging.getLogger("crawler")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def set_verbose(verbose: bool) -> None:
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)


def log_crawl_start(url: str, depth: int) -> None:
    logger.info(f"Starting crawl at {url} (depth={depth})")


def log_visit(url: str, depth: int) -> None:
    logger.debug(f"[depth={depth}] Visiting: {url}")


def log_skip(url: str, reason: str) -> None:
    logger.debug(f"Skipping {url} - {reason}")


def log_error(url: str, error: Exception) -> None:
    logger.warning(f"Error fetching {url}: {error}")


def log_summary(total: int, skipped: int, errors: int) -> None:
    logger.info(f"[DONE] Crawled {total} pages, skipped {skipped}, errors {errors}")

