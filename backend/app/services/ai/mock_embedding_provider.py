# app/services/ai/mock_embedding.py
import math
from app.services.ai.embedding import EmbeddingProvider

class MockEmbeddingProvider(EmbeddingProvider):
    """
    Mock Embedding：用中文双字哈希法把文字变成 128 维向量。
    完全模拟真实 Embedding 的行为，但不需要连网，也不花钱。
    """
    def __init__(self, dimension: int = 128):
        self.dimension = dimension

    def _text_to_vector(self, text: str) -> list[float]:
        # 1. 初始化全 0 向量
        vec = [0.0] * self.dimension
        
        # 2. 清理文本（去除空格、转小写）
        text = text.lower().replace(" ", "")
        
        # 3. 遍历每两个相邻的字（中文用双字切分，英文用单字）
        # 例如 "VPN连不上" -> "vp", "pn", "n连", "连不", "不上"
        for i in range(len(text) - 1):
            bigram = text[i:i+2]
            
            # 4. 用哈希值决定这个词放在哪个维度
            idx = hash(bigram) % self.dimension
            
            # 5. 计数累加
            vec[idx] += 1.0
            
        # 6. 长度归一化（让向量的长度等于 1）
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
            
        return vec

    async def embed_text(self, text: str) -> list[float]:
        return self._text_to_vector(text)

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        return [self._text_to_vector(t) for t in texts]