from pydantic import BaseModel
from typing import Optional, Dict

class RouteOptions(BaseModel):
    preference: Optional[str] = "time"
    filters: Optional[Dict[str, bool]] = None