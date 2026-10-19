import asyncio
from app.services.ai.mock_provider import MockAIProvider


async def main():
    provider = MockAIProvider()
    
    test_cases = [
        ("VPN连不上", "今天早上来公司，VPN一直连不上，提示认证失败，急！下午要跟客户开会。"),
        ("打印机没墨", "行政部打印机没墨了，有空来换一下"),
        ("忘记密码", "我的账号密码忘记了，登录不了"),
        ("电脑蓝屏", "电脑突然蓝屏，重启后还是这样"),
        ("WiFi信号弱", "办公室WiFi信号很弱，网速很慢"),
        ("随便说点什么", "就是随便写写，没什么问题"),
    ]
    
    for title, desc in test_cases:
        result = await provider.analyze(title, desc)
        print(f"\n输入：{title} | {desc[:30]}...")
        print(f"输出：")
        print(f"  分类：{result.category}")
        print(f"  优先级：{result.priority}")
        print(f"  置信度：{result.confidence}")
        print(f"  摘要：{result.summary}")


if __name__ == "__main__":
    asyncio.run(main())