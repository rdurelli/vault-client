import logging
import os

import hvac
from dotenv import load_dotenv
from fastapi import FastAPI

from services.vaultservice import VaultService

from models.payload import Payload

load_dotenv()

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

app = FastAPI()
client = hvac.Client(
    url=os.environ.get('VAULT_URL'),
    token=os.environ.get('VAULT_TOKEN')
)
print(client.is_authenticated())

vault_service = VaultService(logger, client)


@app.get("/health")
async def health():
    logger.info("calling health endpoint")
    return {"ping": "pong"}


@app.post("/v1/api/vault/create_or_update/")
async def create_or_update(payload: Payload = None):
    logger.info("Calling create_or_update endpoint")
    secrets_engines_list = await vault_service.list_secrets_engines()
    flag = False
    for secrets_engine in secrets_engines_list:
        if secrets_engine != payload.secret_path + "/":
            flag = False
        else:
            logger.info("Path already existed")
            flag = True
            break
    if flag:
        logger.info("Path already existed. Then just update policy and members")
        await vault_service.create_update_path_existed(payload)
    else:
        logger.info("Path no existed. Then create path and update policy and members")
        await vault_service.create_secret_path(payload)
        await vault_service.create_update_path_existed(payload)
    return payload
