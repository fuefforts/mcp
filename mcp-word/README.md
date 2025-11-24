# 系统运维服务周月报生成器 MCP 工具

这是一个基于 Model Context Protocol (MCP) 的系统运维服务周月报生成工具，能够自动解析模板文件、填充数据并生成HTML格式的运维服务报告。

## 功能特性

- ✅ **模板解析**: 自动解析HTML模板文件
- ✅ **时间适配**: 根据当前时间自动适配本周或本月时间范围
- ✅ **数据填充**: 预留API接口用于获取真实数据（目前使用模拟数据）
- ✅ **HTML生成**: 生成格式化的HTML报告
- ✅ **MCP集成**: 提供标准的MCP工具接口

## 安装和配置

### 前置要求

- Python 3.13+
- MCP 库

### 安装依赖

```bash
cd mcp-word
uv sync
```

## MCP 工具

该MCP服务器提供以下工具：

### 1. generate_weekly_report
生成系统运维服务周报

**参数:**
- `system_name` (可选): 系统名称

**示例:**
```json
{
  "system_name": "装备调度管理平台"
}
```

### 2. generate_monthly_report
生成系统运维服务月报

**参数:**
- `system_name` (可选): 系统名称

**示例:**
```json
{
  "system_name": "装备调度管理平台"
}
```

### 3. generate_custom_report
生成自定义时间范围的系统运维服务报告

**参数:**
- `start_date` (必需): 开始日期，格式：YYYY-MM-DD
- `end_date` (必需): 结束日期，格式：YYYY-MM-DD
- `system_name` (可选): 系统名称

**示例:**
```json
{
  "start_date": "2025-11-01",
  "end_date": "2025-11-30",
  "system_name": "装备调度管理平台"
}
```

## 使用方法

### 1. 运行MCP服务器

```bash
cd mcp-word
python main.py
```

### 2. 在支持MCP的客户端中使用

在支持MCP的AI助手（如Claude Desktop）中配置该服务器后，可以直接调用工具：

```
请生成装备调度管理平台的周报
```

或

```
请生成装备调度管理平台的月报
```

### 3. 独立测试

```bash
cd mcp-word
python test_report.py
```

## 报告内容

生成的报告包含以下部分：

- **服务总量概述**: 总工单量、服务请求、事件单、审批单统计
- **工单分类情况**: 详细的工单分类和占比分析
- **服务指标情况**: 解决率、完成率、及时率等关键指标
- **未解决工单情况**: 当前和历史未解决工单详情
- **知识库**: 知识库采编情况
- **热点事件解析**: 重要事件分析
- **存在问题与建议**: 运维过程中发现的问题和改进建议

## 模板定制

### 模板文件位置
`统建系统运维服务周月报模板-20251110.html`

### 模板变量
模板中使用以下格式的变量，系统会自动替换：

- `【周|月】`: 根据报告类型自动替换为【周】或【月】
- `【（2025年10月01日-2025年10月31日）】`: 自动替换为当前时间周期
- `【90】`, `【44】`, `【0】` 等: 数据占位符，自动填充实际数据

### 自定义模板
要使用自定义模板，只需：
1. 创建新的HTML模板文件
2. 使用相同的变量格式
3. 在代码中更新模板路径

## 数据源配置

当前版本使用模拟数据。要连接真实数据源，请修改 `fetch_data_from_api` 方法：

```python
def fetch_data_from_api(self, period: Dict[str, Any]) -> Dict[str, Any]:
    # 调用真实API获取数据
    # response = requests.get("your-api-endpoint", params=period)
    # return process_api_response(response.json())
    pass
```

## 输出文件

生成的报告默认保存在当前目录，文件名格式：
- `运维服务报告_YYYYMMDD_HHMMSS.html`
- `测试周报.html` (测试时)
- `测试月报.html` (测试时)

## 故障排除

### 常见问题

1. **模板文件不存在**
   - 确保 `统建系统运维服务周月报模板-20251110.html` 文件存在
   - 检查文件路径是否正确

2. **MCP连接失败**
   - 确保MCP客户端正确配置
   - 检查Python依赖是否正确安装

3. **报告生成失败**
   - 检查模板文件格式是否正确
   - 验证时间计算逻辑

### 日志和调试

启用调试模式查看详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 许可证

本项目基于 MIT 许可证开源。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具。
