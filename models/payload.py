from typing import List, Union

from pydantic import BaseModel


class Payload(BaseModel):
    policy_name: str
    policy_hcl: Union[str, None] = None
    group_name: str
    secret_path: str
    member_entity_ids: List[str]