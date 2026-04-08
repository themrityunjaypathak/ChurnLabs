import logging

from churnlabs.core.logger import setup_logging
from churnlabs.data.ingestion import run_ingestion


def main() -> None:
    logger = logging.getLogger(__name__)
    run_ingestion()
    logger.info("Data ingestion completed successfully.")


if __name__ == "__main__":
    setup_logging()
    main()
