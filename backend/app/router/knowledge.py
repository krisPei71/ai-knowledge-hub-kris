from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import getdb
from app.deps import get_current_user
from app.models.user import User
from app.models.knowledge import Knowledge
from app.schemas.ai import KnowledgeCreate,KnowledgeOut,KnowledgeSearchRequest,KnowledgeSearchResult
from app.services.ai.knowledge_service import create_knowledge,semantic_search

router=APIRouter(prefix="/api/knowledge",tags=["knowledge"])

@router.post("",response_model=KnowledgeOut)
async def create(data:KnowledgeCreate,db:Session=Depends(getdb),user:User=Depends(get_current_user)):
    knowledge=await create_knowledge(db,data,user)
    return knowledge

@router.get("",response_model=list[KnowledgeOut])
def list_knowledge(db:Session=Depends(getdb),user:User=Depends(get_current_user)):
    result = db.query(Knowledge).filter(Knowledge.status=="published").order_by(Knowledge.created_at.desc()).all()
    return result

@router.get("/{id}",response_model=KnowledgeOut)
def get_knowledge_detail(id:int,db:Session=Depends(getdb),user:User=Depends(get_current_user)):
    result = db.get(Knowledge,id)
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="知识库不存在")
    return result

@router.post("/search",response_model=list[KnowledgeSearchResult])
async def search_knoeledge(data:KnowledgeSearchRequest,db:Session=Depends(getdb),user:User=Depends(get_current_user)):
    result = await semantic_search(db,data.query,data.top_k)
    return result
