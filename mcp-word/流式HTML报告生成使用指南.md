# 流式HTML报告生成使用指南

## 概述

本系统实现了支持流式传输的HTML报告生成功能，能够在生成报告的同时通过流式传输将HTML内容实时回传给智能体。

## 核心功能

### 1. 流式报告生成工具

- `generate_weekly_report_streaming` - 流式生成周报
- `generate_monthly_report_streaming` - 流式生成月报  
- `generate_custom_report_streaming` - 流式生成自定义报告

### 2. 传统报告生成工具（向后兼容）

- `generate_weekly_report` - 传统周报生成
- `generate_monthly_report` - 传统月报生成
- `generate_custom_report` - 传统自定义报告生成

## 技术实现

### 流式传输机制

系统使用 `AsyncGenerator` 实现流式传输：

```python
async def generate_report_streaming(self, report_type: str = "month") -> AsyncGenerator[str, None]:
    """流式生成报告"""
    try:
        # 步骤1: 获取时间周期
        yield "正在获取时间周期...\n"
        period = self.get_time_period(report_type)
        yield f"时间周期: {period['period']}\n"
        
        # 步骤2: 获取数据
        yield "正在获取服务数据...\n"
        data = self.fetch_data_from_api(period)
        yield f"获取到 {data['total_service']} 条服务记录\n"
        
        # 步骤3: 替换模板变量
        yield "正在生成报告内容...\n"
        report_content = self.replace_template_variables(self.template_content, data, period)
        
        # 步骤4: 返回完整的HTML内容
        yield "报告生成完成！\n"
        yield "=== HTML报告内容开始 ===\n"
        yield report_content
        yield "=== HTML报告内容结束 ===\n"
        
    except Exception as e:
        yield f"生成报告时出错: {str(e)}\n"
```

### MCP工具实现

```python
@mcp.tool()
async def generate_weekly_report_streaming(system_name: Optional[str] = None) -> AsyncGenerator[TextContent, None]:
    """流式生成系统运维服务周报"""
    try:
        async for chunk in generator.generate_report_streaming("week"):
            yield TextContent(type="text", text=chunk)
            
        # 保存文件并返回文件路径
        report_content = generator.generate_report("week")
        output_path = generator.save_report(report_content)
        yield TextContent(type="text", text=f"\n📁 文件已保存至: {output_path}")
        
    except Exception as e:
        yield TextContent(type="text", text=f"生成周报失败: {str(e)}")
```

## 使用方式

### 1. 直接使用MCP服务器

```bash
# 启动流式报告生成器
cd mcp-word
python streaming_main.py
```

### 2. 通过智能体调用

智能体可以通过MCP协议调用流式工具：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_weekly_report_streaming",
    "arguments": {
      "system_name": "装备调度管理系统"
    }
  }
}
```

### 3. 使用测试脚本

```bash
# 运行测试
cd mcp-word
python test_streaming.py
```

## 流式响应格式

### 进度信息
```
正在获取时间周期...
时间周期: 2025年11月18日-2025年11月24日
正在获取服务数据...
获取到 120 条服务记录
正在生成报告内容...
报告生成完成！
```

### HTML内容
```
=== HTML报告内容开始 ===
<!DOCTYPE html>
<html>
<head>
    <title>系统运维服务周报</title>
    ...
</head>
<body>
    ...
</body>
</html>
=== HTML报告内容结束 ===
```

### 文件保存信息
```
📁 文件已保存至: 运维服务报告_20251124_102057.html
```

## 优势特点

### 1. 实时反馈
- 生成过程中实时返回进度信息
- 用户可以了解当前处理状态
- 避免长时间等待的焦虑

### 2. 完整内容传输
- 最终返回完整的HTML报告内容
- 智能体可以直接使用HTML内容
- 支持内容分析和进一步处理

### 3. 文件保存
- 自动保存HTML文件到本地
- 生成唯一的文件名（包含时间戳）
- 便于后续查看和管理

### 4. 错误处理
- 完善的异常处理机制
- 流式传输中的错误实时反馈
- 保证系统的稳定性

## 集成示例

### 智能体集成代码

```python
import asyncio
from mcp.client import create_session

async def generate_report_with_streaming():
    """使用流式传输生成报告"""
    async with create_session("streaming-report-generator") as session:
        # 调用流式工具
        async for chunk in session.call_tool_streaming(
            "generate_weekly_report_streaming",
            system_name="装备调度管理系统"
        ):
            # 实时处理每个数据块
            print(f"收到数据: {chunk}")
            
            # 如果是HTML内容，可以进行进一步处理
            if "=== HTML报告内容开始 ===" in chunk:
                print("开始接收HTML内容...")
            elif "=== HTML报告内容结束 ===" in chunk:
                print("HTML内容接收完成")
```

### 处理HTML内容

```python
def extract_html_from_stream(stream_data):
    """从流式数据中提取HTML内容"""
    html_content = ""
    is_html_section = False
    
    for line in stream_data.split('\n'):
        if "=== HTML报告内容开始 ===" in line:
            is_html_section = True
            continue
        elif "=== HTML报告内容结束 ===" in line:
            is_html_section = False
            break
            
        if is_html_section:
            html_content += line + '\n'
    
    return html_content
```

## 注意事项

1. **性能考虑**: 流式传输会增加一些网络开销，但提供了更好的用户体验
2. **错误处理**: 确保正确处理流式传输中的异常情况
3. **内容格式**: HTML内容使用明确的开始和结束标记，便于解析
4. **向后兼容**: 保留了传统的非流式工具，确保现有系统不受影响

## 扩展建议

1. **自定义模板**: 可以扩展支持多种报告模板
2. **数据源集成**: 可以集成真实的数据源API
3. **格式转换**: 可以添加PDF、Word等格式转换功能
4. **实时数据**: 可以支持实时数据更新和推送

通过这个流式HTML报告生成系统，智能体可以实时获取报告生成进度，并在生成完成后立即获得完整的HTML内容，大大提升了交互体验和处理效率。
