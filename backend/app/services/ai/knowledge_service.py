import logging
import json
from sqlalchemy.orm import Session
from app.models.knowledge import Knowledge
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ai import KnowledgeCreate,KnowledgeOut,KnowledgeSearchRequest,KnowledgeSearchResult
from app.services.ai import get_embedding_provider
from app.services.ai.similarity import cosine_similarity

logger = logging.getLogger(__name__)

async def create_knowledge(db:Session,data:KnowledgeCreate,currrent_user:User):
    embed = get_embedding_provider()

    text_to_embed = f"{data.title}\n{data.content}"

    embed_text = await embed.embed_text(text_to_embed)
    embed_json=json.dumps(embed_text)

    knowledge=Knowledge(
        title=data.title,
        content=data.content,
        source_ticket_id=data.source_ticket_id,
        embedding=embed_json,
        creator_id=currrent_user.id
    )
    db.add(knowledge)
    db.commit()
    db.refresh(knowledge)
    return knowledge

async def semantic_search(db:Session,query:str,top_k:int):
    embed = get_embedding_provider()

    query_embed=await embed.embed_text(query)

    all_knowledge=db.query(Knowledge).filter(Knowledge.embedding.isnot(None)).all()

    result=[]
    for k in all_knowledge:
       try:
           k_vector=json.loads(k.embedding)
           score = cosine_similarity(query_embed,k_vector)
           if score >0.1:
               result.append({
                    "id": k.id,
                    "title": k.title,
                    "content": k.content,
                    "score": score,
               })
       except Exception as e:
            logger.error(f"计算知识 {k.id} 的相似度失败: {e}")
            continue
       
    result.sort(key=lambda x:x['score'],reverse=True)
    return result[:top_k]

async def create_knowledge_from_ticket(ticket_id:int,solution:str | None,db:Session,current_user:User):
    ticket = db.get(Ticket,ticket_id)
    if not ticket:
        raise ValueError("工单不存在")
    
    content_parts=[f"【问题现象】\n{ticket.description}"]

    if solution:
        content_parts.append(f"【解决方案】\n{solution}")
    else:
        from app.models.ticket_log import TicketLog
        log=db.query(TicketLog).filter(TicketLog.ticket_id==ticket_id,TicketLog.to_status=="resolved").order_by(TicketLog.created_at.desc()).first()
        if log and log.remark:
            content_parts.append(f"【解决方案】\n{log.remark}")

    full_content="\n\n".join(content_parts)

    from app.schemas.ai import KnowledgeCreate
    data = KnowledgeCreate(
        title=f"工单沉淀{ticket.title}",
        content=full_content,
        source_ticket_id=ticket_id
    )

    return await create_knowledge(db,data,current_user)
    

