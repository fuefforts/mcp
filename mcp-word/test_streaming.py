#!/usr/bin/env python3
"""
测试流式HTML报告生成功能
"""

import asyncio
import subprocess
import json
import os
import time
from typing import Dict, Any


class StreamingReportTester:
    """流式报告测试器"""
    
    def __init__(self, mcp_server_path: str):
        self.mcp_server_path = mcp_server_path
        self.process: subprocess.Popen = None
        
    def start_server(self) -> bool:
        """启动MCP服务器"""
        try:
            self.process = subprocess.Popen(
                ['python', self.mcp_server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            print(f"✅ MCP服务器已启动: {self.mcp_server_path}")
            # 等待服务器启动
            time.sleep(2)
            return True
        except Exception as e:
            print(f"❌ 启动MCP服务器失败: {e}")
            return False
            
    def call_streaming_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        调用流式工具并收集所有输出
        
        Args:
            tool_name: 工具名称
            **kwargs: 工具参数
            
        Returns:
            包含处理结果的字典
        """
        if not self.process:
            if not self.start_server():
                return {"success": False, "error": "无法启动MCP服务器"}
        
        try:
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": kwargs
                }
            }
            
            # 发送请求
            request_str = json.dumps(request, ensure_ascii=False) + '\n'
            print(f"📤 发送请求: {request_str[:100]}...")
            self.process.stdin.write(request_str)
            self.process.stdin.flush()
            
            # 收集所有响应
            all_responses = []
            html_content = ""
            is_collecting_html = False
            
            print("📥 开始接收流式响应...")
            while True:
                response_line = self.process.stdout.readline()
                if not response_line:
                    break
                    
                print(f"📄 收到响应: {response_line.strip()}")
                all_responses.append(response_line)
                
                # 检查是否开始收集HTML内容
                if "=== HTML报告内容开始 ===" in response_line:
                    is_collecting_html = True
                    continue
                elif "=== HTML报告内容结束 ===" in response_line:
                    is_collecting_html = False
                    break
                    
                # 收集HTML内容
                if is_collecting_html:
                    html_content += response_line
            
            return {
                "success": True,
                "all_responses": all_responses,
                "html_content": html_content,
                "message": f"成功接收到 {len(all_responses)} 条响应"
            }
            
        except Exception as e:
            return {
                "success": False, 
                "error": f"调用工具失败: {str(e)}"
            }
            
    def stop_server(self):
        """停止MCP服务器"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("✅ MCP服务器已停止")


async def test_streaming_functionality():
    """测试流式功能"""
    print("=" * 60)
    print("流式HTML报告生成测试")
    print("=" * 60)
    
    # 获取当前目录的MCP服务器路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_server_path = os.path.join(current_dir, 'streaming_main.py')
    
    if not os.path.exists(mcp_server_path):
        print(f"❌ 找不到MCP服务器文件: {mcp_server_path}")
        return
        
    # 创建测试器
    tester = StreamingReportTester(mcp_server_path)
    
    try:
        # 测试用例
        test_cases = [
            {
                "name": "流式周报生成",
                "tool": "generate_weekly_report_streaming",
                "args": {}
            },
            {
                "name": "流式月报生成", 
                "tool": "generate_monthly_report_streaming",
                "args": {}
            }
        ]
        
        for test_case in test_cases:
            print(f"\n🧪 测试: {test_case['name']}")
            print("-" * 40)
            
            result = tester.call_streaming_tool(
                tool_name=test_case['tool'],
                **test_case['args']
            )
            
            if result["success"]:
                print(f"✅ {test_case['name']} 测试成功!")
                print(f"📊 响应数量: {len(result['all_responses'])}")
                print(f"📄 HTML内容长度: {len(result['html_content'])} 字符")
                
                # 显示部分HTML内容预览
                if result['html_content']:
                    preview = result['html_content'][:200] + "..." if len(result['html_content']) > 200 else result['html_content']
                    print(f"🔍 HTML预览: {preview}")
            else:
                print(f"❌ {test_case['name']} 测试失败: {result['error']}")
                
            print("-" * 40)
            time.sleep(1)  # 避免请求过于频繁
            
    finally:
        # 停止服务器
        tester.stop_server()


def quick_demo():
    """快速演示"""
    print("\n" + "=" * 60)
    print("快速演示")
    print("=" * 60)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_server_path = os.path.join(current_dir, 'streaming_main.py')
    
    tester = StreamingReportTester(mcp_server_path)
    
    try:
        print("🚀 开始流式生成周报...")
        result = tester.call_streaming_tool("generate_weekly_report_streaming")
        
        if result["success"]:
            print("🎉 流式传输成功!")
            print(f"📊 共收到 {len(result['all_responses'])} 条实时更新")
            print(f"📄 生成的HTML报告大小: {len(result['html_content'])} 字符")
            
            # 保存HTML内容到文件用于验证
            if result['html_content']:
                output_file = "test_streaming_output.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result['html_content'])
                print(f"💾 HTML内容已保存到: {output_file}")
        else:
            print(f"❌ 失败: {result['error']}")
            
    finally:
        tester.stop_server()


if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_streaming_functionality())
    
    # 运行快速演示
    quick_demo()
    
    print("\n📝 使用说明:")
    print("1. 流式工具会在生成过程中实时返回进度信息")
    print("2. 最终会返回完整的HTML报告内容")
    print("3. 同时会保存HTML文件到本地")
    print("4. 支持实时监控生成过程")
