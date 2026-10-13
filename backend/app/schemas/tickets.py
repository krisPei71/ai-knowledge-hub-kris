from datetime import datetime
from typing import List
from pydantic import BaseModel,ConfigDict,Field

class TicketCreate(BaseModel):
    title:str = Field(...,min_length=1,max_length=255)
    description:str = Field(...,min_length=1)

class TicketOut(BaseModel):
    id:int
    title:str
    description:str
    status:str
    priority:str
    category:str
    aiSummary:str = Field(alias="ai_summary")
    aiConfidence:float | None=Field(alias="ai_confidence")
    aiCategoryRaw:str|None=Field(alias="ai_category_raw")
    creatorId:int=Field(alias="creator_id")
    creatorUserNamee:str=Field(alias="creator_username")
    assigneeId:int | None=Field(alias="assignee_id")
    assigneeUserName:str | None =Field(alias="assignee_username")
    createdAt:datetime=Field(alias="created_at")
    updatedAt:datetime=Field(alias="updated_at")

    model_config=ConfigDict(from_attributes=True,alias_generator=True)

class TicketList(BaseModel):
    total:int
    items:List[TicketOut]
