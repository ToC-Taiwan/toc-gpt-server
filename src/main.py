from prometheus_client import start_http_server

from logger import logger

PROMETHEUS_PORT = 7777
start_http_server(PROMETHEUS_PORT)
logger.info("gpt server prometheus server started at port %d", PROMETHEUS_PORT)
