import importlib.metadata
import logging
import sys

__version__ = importlib.metadata.version("metadata_pepxxx")

logger = logging.getLogger("metadata_pepxxx")
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)
