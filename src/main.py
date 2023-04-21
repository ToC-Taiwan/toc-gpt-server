import os

import openai
from prometheus_client import start_http_server

from logger import logger

PROMETHEUS_PORT = 7777
start_http_server(PROMETHEUS_PORT)
logger.info("gpt server prometheus server started at port %d", PROMETHEUS_PORT)

openai.api_key = os.getenv("OPENAI_API_KEY")

models = openai.Model.list()
for model in models.data:
    logger.info("model: %s", model.id)

prompt_message = """Say this is a test"""

res = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt_message,
    max_tokens=1000,
    temperature=1.5,
)

logger.info("res: %s", res)
