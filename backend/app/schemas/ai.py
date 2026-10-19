from pydantic import BaseModel, Field
class AIClassifyRequert(BaseModel):
    title:str=Field(...,min_length=1,max_length=255)
    description:str | None