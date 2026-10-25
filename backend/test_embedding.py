import asyncio
from app.services.ai.mock_embedding_provider import MockEmbeddingProvider
from app.services.ai.similarity import cosine_similarity

async def main():
    embedder = MockEmbeddingProvider()
    
    # 准备几段话
    query = "连不上VPN怎么办"
    doc1 = "VPN连接失败排查指南"
    doc2 = "VPN总是连不上，提示认证失败"
    doc3 = "打印机没墨了怎么换"

    # 1. 全部转成向量
    v_query = await embedder.embed_text(query)
    v_doc1 = await embedder.embed_text(doc1)
    v_doc2 = await embedder.embed_text(doc2)
    v_doc3 = await embedder.embed_text(doc3)

    # 2. 算相似度
    sim1 = cosine_similarity(v_query, v_doc1)
    sim2 = cosine_similarity(v_query, v_doc2)
    sim3 = cosine_similarity(v_query, v_doc3)

    print(f"用户问题：{query}\n")
    print(f"相似度 Doc1 (VPN连接失败排查指南) : {sim1:.4f}")
    print(f"相似度 Doc2 (VPN总是连不上...   ) : {sim2:.4f}")
    print(f"相似度 Doc3 (打印机没墨了...     ) : {sim3:.4f}")

if __name__ == "__main__":
    asyncio.run(main())