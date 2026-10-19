from datetime import datetime
from typing import List
from pydantic import BaseModel,ConfigDict,Field

class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    category: str | None = None
    priority: str | None = None
    ai_category_raw: str | None = None
    ai_confidence: float | None = None
    ai_summary: str | None = None

class TicketOut(BaseModel):
    id:int
    title:str
    description:str
    status:str
    priority:str
    category:str | None
    ai_summary:str | None 
    ai_confidence:float | None
    ai_category_raw:str | None
    creator_id:int
    creator_username:str
    assignee_id:int | None
    assignee_username:str | None 
    created_at:datetime
    updated_at:datetime

    model_config=ConfigDict(from_attributes=True)

class TicketList(BaseModel):
    total:int
    items:List[TicketOut]

class TicketStatusUpdate(BaseModel):
    to_status:str = Field(...,min_length=1,max_length=20)
    remark:str | None = Field(None,max_length=255)

class TicketLogOut(BaseModel):
    id:int
    ticket_id:int
    from_status:str
    to_status:str
    operator_id:int
    operator_username:str
    remark:str | None = None
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)
