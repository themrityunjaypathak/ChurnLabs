import time
import logging

from churnlabs.core.logger import setup_logging
from churnlabs.data.loaders import load_raw_data
from churnlabs.data.preprocessor import basic_cleaning
from churnlabs.data.export import export_processed_data


logger = logging.getLogger(__name__)


def main():
    start_time = time.perf_counter()
    logger.info("Preprocessing started")

    logger.info("Loading raw dataset")
    data = load_raw_data()

    logger.info("Raw dataset shape: %s", data.shape)

    logger.info("Applying basic cleaning")
    clean_data = basic_cleaning(data)

    logger.info("Processed dataset shape: %s", clean_data.shape)

    logger.info("Exporting processed dataset")
    path = export_processed_data(clean_data)
    logger.info("Processed data saved to: %s", path)

    elapsed = time.perf_counter() - start_time
    logger.info("Preprocessing completed in %.2f seconds", elapsed)


if __name__ == "__main__":
    setup_logging()
    main()
