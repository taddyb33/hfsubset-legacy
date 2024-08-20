
from typing import List

from pydantic import BaseModel

class Subset(BaseModel):
    message: str 
    comid: int
    layers: List["str"]
    output_file: str
