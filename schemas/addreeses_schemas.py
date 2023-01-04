from typing import Optional
from pydantic import BaseModel

class AddressesSchemaBase(BaseModel):
    id:Optional[int] = None
    site_id:int 