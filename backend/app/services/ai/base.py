from abc import ABC,abstractmethod
from pydantic import BaseModel,Field

class AIAnalysisResult(BaseModel):
    category:str=Field(...,description="工单分类")
    priority:str=Field(...,description="工单优先级")
    confidence:float=Field(...,min=0,max=1,description="可信度")
    summary:str=Field(...,description="一句话摘要")




class AIProvider(ABC):
    @abstractmethod
    async def analyze(self,title,description)->AIAnalysisResult:
        ...