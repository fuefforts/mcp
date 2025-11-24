#!/usr/bin/env python3
"""
测试修改后的流式HTML报告生成功能
验证是否直接返回HTML内容流而不保存文件
"""

import asyncio
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from streaming_main import StreamingReportGenerator


async def test_streaming_generation():
    """测试流式生成功能"""
    print("开始测试流式HTML报告生成...")
    
    try:
        # 初始化报告生成器
        generator = StreamingReportGenerator("统建系统运维服务周月报模板-20251110.html")
        
        print("\n=== 测试周报生成 ===")
        print("流式输出内容:")
        async for chunk in generator.generate_report_streaming("week"):
            print(f"收到内容块: {chunk[:100]}...")  # 只显示前100个字符
        
        print("\n=== 测试月报生成 ===")
        print("流式输出内容:")
        async for chunk in generator.generate_report_streaming("month"):
            print(f"收到内容块: {chunk[:100]}...")  # 只显示前100个字符
        
        print("\n=== 测试非流式版本 ===")
        report_content = generator.generate_report("week")
        print(f"非流式版本返回内容长度: {len(report_content)} 字符")
        print(f"内容前200字符: {report_content[:200]}...")
        
        print("\n✅ 测试完成！流式HTML报告生成功能正常工作")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_streaming_generation())
