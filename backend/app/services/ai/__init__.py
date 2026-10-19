from app.services.ai.base import AIAnalysisResult,AIProvider

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
    
__all__=["AIProvider","AIAnalysisResult","get_ai_provider"]