from datetime import datetime
from pydantic import BaseModel, Field,ConfigDict
class AIClassifyRequert(BaseModel):
    title:str=Field(...,min_length=1,max_length=255)
    description:str | None

class KnowledgeCreate(BaseModel):
    title:str=Field(...,min_length=1,max_length=200)
    content:str=Field(...,min_length=1)
    source_ticket_id:int | None=None

class KnowledgeOut(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    source_ticket_id: int | None
    status: str
    created_at: datetime

class KnowledgeSearchRequest(BaseModel):
    query:str=Field(...,min_length=1)
    top_k:int=Field(5,ge=1,le=20)

class KnowledgeSearchResult(BaseModel):
    id:int
    title:str
    content:str
    score:float
    
class KnowledgeFromTicketRequest(BaseModel):
    solution:str | None = Field(None,max_length=2000)


class ChatMessage(BaseModel):
    role:str=Field(...,description="角色")
    content:str=Field(...,description="内容")
class QARequest(BaseModel):
    query:str=Field(...,min_length=1)
    history:list[ChatMessage]=Field(default_factory=list,description="历史对话")