import logging
import asyncio
from app.services.ai.base import AIAnalysisResult,AIProvider

logger=logging.getLogger(__name__)

CATEGORY_KEYWORDS={
    "网络": ["vpn", "网络", "断网", "wifi", "wi-fi", "连接", "远程", "网速", "网线", "路由"],
    "硬件": ["电脑", "蓝屏", "死机", "打印机", "显示器", "键盘", "鼠标", "开机", "黑屏", "卡顿"],
    "软件": ["软件", "安装", "崩溃", "报错", "闪退", "系统", "office", "word", "excel"],
    "账号权限": ["密码", "登录", "账号", "权限", "锁定", "忘记密码", "重置", "认证失败"],
    "邮箱": ["邮箱", "邮件", "outlook", "收不到", "发不出", "收件", "发件"],
}

PRIORITY_HIGH_KEYWORDS=["紧急", "影响", "会议", "客户", "断网", "全部", "无法工作", "马上", "立刻"]

PRIORITY_LOW_KEYWORDS=["不急", "有空", "建议", "优化", "希望", "慢慢"]

def _detect_category(text:str)->tuple[str,float]:
    text_lower=text.lower()

    for category,keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return category,0.75
            
    return '其他',0.3

def _detect_priority(text:str)->str:
    text_lower=text.lower()
    if any(kw in text_lower for kw in PRIORITY_HIGH_KEYWORDS):
        return 'high'
    
    if any(kw in text_lower for kw in PRIORITY_LOW_KEYWORDS):
        return 'low'
    
    return 'medium'

def _generate_summary(title:str,description:str):
    summary = title.strip()
    desc_clean=description.strip().replace("\n","")

    if len(desc_clean)>30:
        summary+=','+desc_clean[:30]+"..."
    else:
        summary+=','+desc_clean

    return summary[:100]

class MockAIProvider(AIProvider):
    async def analyze(self, title, description):
        combined_text=f"{title}{description}"

        category,confidence=_detect_category(combined_text)
        priority=_detect_priority(combined_text)
        summary=_generate_summary(title,description)

        logger.info(f"[MOCKAI] 分类={category} 优先级{priority} 置信度{summary}")

        return AIAnalysisResult(
            category=category,
            priority=priority,
            confidence=confidence,
            summary=summary
        )
    async def generate_stream(self,prompt:str):
        reply = f"根据知识库，建议您检查网络。您的问题是：{prompt[:10]}... 请按步骤排查。"

        for char in reply:
            yield char
            await asyncio.sleep(0.05)