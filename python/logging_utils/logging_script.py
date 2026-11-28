from pathlib import Path
import logging

logging_utils_directory = \
  Path( __file__ ).parent
  
server_log = logging_utils_directory / "server.log"

logger = logging.getLogger('server_log')
handler = logging.FileHandler(server_log)

handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)