import logging
import os

import hvac
from dotenv import load_dotenv
from fastapi import FastAPI


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


@app.get("/health")
async def health():
    logger.info("calling health endpoint")
    return {"ping": "pong"}


@app.post("/v1/api/vault/create_or_update/")
async def create_or_update(payload: Payload = None):
    logger.info("Calling create_or_update endpoint")
    secrets_engines_list = client.sys.list_mounted_secrets_engines()['data']
    flag = False
    for secrets_engine in secrets_engines_list:
        if secrets_engine != payload.secret_path+"/":
            flag = False
        else:
            logger.info("Path already existed")
            flag = True
            break
    if flag:
        logger.info("Path already existed. Then just update policy and members")
        await create_update_path_existed(payload)
    else:
        logger.info("Path no existed. Then create path and update policy and members")
        await create_secret_path(payload)
        await create_update_path_existed(payload)
    return payload


async def create_update_path_existed(payload):
    logger.info("Starting create update policy")
    policy = '''
        path "%s/*" {
            capabilities = ["create", "read", "update", "delete", "list"]
        }
    ''' % payload.secret_path
    client.sys.create_or_update_policy(
        name=payload.policy_name,
        policy=policy,
    )
    logger.info("Policy created or updated")
    logger.info("Create or update group")
    client.secrets.identity.create_or_update_group(
        name=payload.group_name,
        policies=payload.policy_name,
        member_entity_ids=list(payload.member_entity_ids)
    )
    logger.info(f'Group {payload.group_name} updated with the following members: {payload.member_entity_ids} and '
                f'policy: {payload.policy_name}')


async def create_secret_path(payload):
    logger.info("Starting create secret path")
    client.sys.enable_secrets_engine(
        backend_type='kv',
        path=payload.secret_path,
    )
    logger.info("Secret path created")
