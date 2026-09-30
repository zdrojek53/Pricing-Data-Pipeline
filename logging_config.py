import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(level=logging.INFO, log_dir='logs'):
    Path(log_dir).mkdir(exist_ok=True)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            RotatingFileHandler(
                Path(log_dir) / "pricing_pipeline.log",
                maxBytes=5_000_000,
                backupCount=5,
                encoding="utf-8",
            ),
        ],
    )

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

