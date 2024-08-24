
from typing import List

from pydantic import BaseModel

class Subset(BaseModel):
    status: int
    message: str 
    feature_id: int
    layers: List[str]
    output_file: str

class DownstreamLinks(BaseModel):
    status: int
    message: str
    feature_id: int
    downstream_feature_id: int
    layers: List[str]
    output_file: str
