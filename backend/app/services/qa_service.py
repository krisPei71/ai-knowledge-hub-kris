import json
from app.services.ai import get_ai_provider
from app.services.ai.knowledge_service import semantic_search
from sqlalchemy.orm import Session

async def stream_qa_answer(db:Session,query:str,history:list=None):
    # 1. 语义检索：找相关的知识
    search_results = await semantic_search(db,query,top_k=3)
    #2. 拼装上下文
    context=""
    sources=[]
    for res in search_results:
        context+=f"【标题】{res['title']}\n【内容】{res['content']}"
        sources.append({"id":res["id"],"title":res["title"]})

    history_str=""
    if history:
        for msg in history:
            role_name="用户" if msg.role=='user' else "AI助手"
            history_str+=f"{role_name}:{msg.content}"

    # 拼装prompt
    prompt=f"""
你是一个 IT 助手。请根据以下【知识库内容】和【历史对话】，回答用户的【当前问题】。
如果找不到答案，请说不知道，不要编造。
【知识库内容】:
{context if context else "(无相关参考)"}

【历史对话】:
{history_str if history_str else '无'}

【问题】:
{query}
    """

    # 4. 通过 SSE 格式输出
    # ⚠️ SSE 规定：推给前端的数据必须以 "data: " 开头，以 "\n\n" 结尾

    # 先推文献来源
    sources_data=json.dumps({"type":"sources","data":sources},ensure_ascii=False)
    yield f"data:{sources_data}\n\n"

    # 再推流式文本
    ai=get_ai_provider()
    if hasattr(ai,"generate_stream"):
        async for chunk in ai.generate_stream(prompt):
            chunk_data=json.dumps({"type":"text","data":chunk},ensure_ascii=False)
            # yield f"data:{chunk_data}\n\n"
            payload = f"data: {chunk_data}\n\n"
            print("【后端发送】", repr(payload)) 
            yield payload
    # 结束信号
    yield f"data:{json.dumps({'type':'done'})}\n\n"

