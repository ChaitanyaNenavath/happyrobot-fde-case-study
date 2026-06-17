from pydantic import BaseModel
from typing import Optional


class CallResult(BaseModel):
    mc_number: str
    carrier_name: Optional[str] = None
    load_id: str
    origin: Optional[str] = None
    destination: Optional[str] = None
    carrier_offer: Optional[float] = 0
    final_rate: Optional[float] = 0
    outcome: str
    sentiment: str