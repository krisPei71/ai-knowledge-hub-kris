import json
import logging
from openai import AsyncOpenAI
from app.config import settings
from app.services.ai import AIAnalysisResult,AIProvider

logger = logging.getLogger(__name__)

class OpenAIProvider(AIProvider):

    def __init__(self):
        self.client=AsyncOpenAI(
            api_key=settings.ai_api_key,
            base_url=settings.ai_base_url
        )
        self.model=settings.ai_model
    async def analyze(self, title, description)->AIAnalysisResult:
        prompt = f"""
        你是一个 IT 工单助手。请分析以下工单，并严格以 JSON 格式返回结果。
        不要输出任何其他解释文字，只输出 JSON。

        工单标题：{title}
        工单描述：{description}

        返回 JSON 格式要求：
        {{
            "category": "必须是以下之一：网络, 硬件, 软件, 账号权限, 邮箱, 其他",
            "priority": "必须是以下之一：low, medium, high",
            "confidence": 0.0到1.0之间的浮点数,
            "summary": "一句话摘要，不超过50字"
        }}
        """
        try:
            response=await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role":"user","content":prompt}],
                response_format={"type":"json_object"},
                temperature=0.1
            )
            content=response.choices[0].message.content
            data=json.loads(content)
            return AIAnalysisResult(
                category=data.get("category", "其他"),
                priority=data.get("priority", "medium"),
                confidence=float(data.get("confidence", 0.5)),
                summary=data.get("summary", "无法生成摘要")[:100],
            )
        except Exception as e:
            logger.error("大模型调用失败",e)
            raise e
        
    async def generate_stream(self,prompt:str):
        try:
            response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True,  # 开启流式
                    temperature=0.3,
                )
            async for chunk in response:
                content=chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            logger.error("deepseek流式调用失败",e)
            raise e