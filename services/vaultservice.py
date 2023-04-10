class VaultService:
    def __init__(self, logger, client):
        self.logger = logger
        self.client = client

    async def create_secret_path(self, payload):
        self.logger.info("Starting create secret path")
        self.client.sys.enable_secrets_engine(
            backend_type='kv',
            path=payload.secret_path,
        )
        self.logger.info("Secret path created")

    async def list_secrets_engines(self):
        self.logger.info("Listing secrets engines")
        return self.client.sys.list_mounted_secrets_engines()['data']

    async def create_update_path_existed(self, payload):
        self.logger.info("Starting create update policy")
        policy = '''
            path "%s/*" {
                capabilities = ["create", "read", "update", "delete", "list"]
            }
        ''' % payload.secret_path
        self.client.sys.create_or_update_policy(
            name=payload.policy_name,
            policy=policy,
        )
        self.logger.info("Policy created or updated")
        self.logger.info("Create or update group")
        self.client.secrets.identity.create_or_update_group(
            name=payload.group_name,
            policies=payload.policy_name,
            member_entity_ids=list(payload.member_entity_ids)
        )
        self.logger.info(
            f'Group {payload.group_name} updated with the following members: {payload.member_entity_ids} and '
            f'policy: {payload.policy_name}')
