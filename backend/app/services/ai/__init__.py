from app.services.ai.base import AIAnalysisResult,AIProvider
from app.services.ai.embedding import EmbeddingProvider

def get_ai_provider()->AIProvider:
    from app.config import settings

    name=settings.ai_provider.lower()

    if name=="mock":
        from app.services.ai.mock_provider import MockAIProvider
        return MockAIProvider()
    elif name=="openai":
        from app.services.ai.openai_provider import OpenAIProvider
        return OpenAIProvider()
    else:
        raise ValueError(f"未知的AI provider：{name}")
    
def get_embedding_provider()->EmbeddingProvider:
    from app.config import settings

    name=settings.embedding_provider.lower()

    if name=="mock":
        from app.services.ai.mock_embedding_provider import MockEmbeddingProvider
        return MockEmbeddingProvider()
    else:
        raise ValueError(f"未知的embedding provider：{name}")
    
__all__=["AIProvider","AIAnalysisResult","get_ai_provider","EmbeddingProvider","get_embedding_provider"]