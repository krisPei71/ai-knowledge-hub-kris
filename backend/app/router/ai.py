import logging
from fastapi import APIRouter,Depends
from fastapi.responses import StreamingResponse
from app.schemas.ai import AIClassifyRequert,QARequest
from app.services.ai import get_ai_provider,AIAnalysisResult
from app.models.user import User
from app.deps import get_current_user
from sqlalchemy.orm import Session
from app.database import getdb
from app.services.qa_service import stream_qa_answer

logger=logging.getLogger(__name__)
router=APIRouter(prefix="/api/ai",tags=["AI"])

@router.post("/classify",response_model=AIAnalysisResult)
async def classify_ticket(data:AIClassifyRequert):
    try:
        ai=get_ai_provider()
        result=await ai.analyze(data.title,data.description)
        return result
    except Exception as e:
        logger.error(f"AI 分析失败：{type(e).__name__}:{e}",exc_info=True)
        return AIAnalysisResult(
            category="其他",
            priority="medium",
            confidence=0.0,
            summary="AI分析失败"
        )

@router.post("/chat")
def chat(data:QARequest,db:Session=Depends(getdb)):
    return StreamingResponse(
        stream_qa_answer(db,data.query,data.history),
        media_type="text/event-stream"
    )

