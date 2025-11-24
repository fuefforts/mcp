#!/usr/bin/env python3
"""
MCP工具：系统运维服务周月报生成器
功能：解析模板文件，填充数据，生成HTML格式的周月报
使用FastMCP现代API实现
"""

import asyncio
import json
import os
import random
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent


class ReportGenerator:
    """周月报生成器"""
    
    def __init__(self, template_path: str):
        self.template_path = template_path
        self.template_content = ""
        self.load_template()
    
    def load_template(self):
        """加载模板文件"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                self.template_content = f.read()
        except FileNotFoundError:
            raise Exception(f"模板文件不存在: {self.template_path}")
        except Exception as e:
            raise Exception(f"加载模板文件失败: {e}")
    
    def get_time_period(self, report_type: str) -> Dict[str, str]:
        """根据报告类型获取时间周期"""
        now = datetime.now()
        
        if report_type == "week":
            # 本周（周一到周日）
            start_of_week = now - timedelta(days=now.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            period_str = f"{start_of_week.strftime('%Y年%m月%d日')}-{end_of_week.strftime('%Y年%m月%d日')}"
            return {
                "period": period_str,
                "type": "周",
                "start_date": start_of_week,
                "end_date": end_of_week
            }
        else:  # month
            # 本月
            start_of_month = now.replace(day=1)
            next_month = start_of_month.replace(month=start_of_month.month % 12 + 1, year=start_of_month.year + (start_of_month.month // 12))
            end_of_month = next_month - timedelta(days=1)
            period_str = f"{start_of_month.strftime('%Y年%m月%d日')}-{end_of_month.strftime('%Y年%m月%d日')}"
            return {
                "period": period_str,
                "type": "月",
                "start_date": start_of_month,
                "end_date": end_of_month
            }
    
    def get_previous_period(self, current_period: Dict[str, Any]) -> Dict[str, str]:
        """获取上一个周期的时间"""
        if current_period["type"] == "周":
            prev_start = current_period["start_date"] - timedelta(days=7)
            prev_end = current_period["end_date"] - timedelta(days=7)
            period_str = f"{prev_start.strftime('%Y年%m月%d日')}-{prev_end.strftime('%Y年%m月%d日')}"
        else:  # month
            prev_start = (current_period["start_date"].replace(day=1) - timedelta(days=1)).replace(day=1)
            prev_end = current_period["start_date"] - timedelta(days=1)
            period_str = f"{prev_start.strftime('%Y年%m月%d日')}-{prev_end.strftime('%Y年%m月%d日')}"
        
        return {
            "period": period_str,
            "type": current_period["type"]
        }
    
    def fetch_data_from_api(self, period: Dict[str, Any]) -> Dict[str, Any]:
        """从API获取数据（预留接口）"""
        # 这里可以预留接口，实际使用时可以调用真实的API
        # 目前返回随机数据
        total_service = random.randint(50, 150)
        service_request = random.randint(20, 80)
        incident = random.randint(0, 5)
        approval = random.randint(20, 70)
        self_service = random.randint(10, 40)
        manual_service = random.randint(15, 50)
        previous_total = random.randint(40, 140)
        change_rate = round(random.uniform(-10.0, 10.0), 1)
        resolution_rate = random.randint(95, 100)
        completion_rate = random.randint(95, 100)
        timeliness_rate = random.randint(95, 100)
        satisfaction_rate = random.randint(95, 100)
        unresolved_current = random.randint(0, 10)
        unresolved_history = random.randint(0, 15)
        knowledge_base = random.randint(0, 5)
        
        # 生成随机的服务类别数据
        service_categories = [
            {"name": "装备调度管理系统/问题答疑/系统功能类", "count": random.randint(10, 40), "percentage": 0},
            {"name": "装备调度管理系统/问题答疑/流程类", "count": random.randint(3, 15), "percentage": 0},
            {"name": "装备调度管理系统/问题答疑/业务类", "count": random.randint(5, 20), "percentage": 0},
            {"name": "装备调度管理系统/系统BUG", "count": random.randint(5, 25), "percentage": 0},
            {"name": "装备调度管理系统/数据修改/装备信息数据修改", "count": random.randint(0, 5), "percentage": 0},
            {"name": "装备调度管理系统/权限开通/账号开通", "count": random.randint(1, 8), "percentage": 0},
            {"name": "装备调度管理系统/权限开通/功能调整", "count": random.randint(0, 5), "percentage": 0},
            {"name": "装备调度管理系统/问题答疑/财务云资产卡片推送", "count": random.randint(0, 3), "percentage": 0},
            {"name": "装备调度管理系统/权限开通/管理员申请", "count": random.randint(0, 3), "percentage": 0}
        ]
        
        # 计算百分比
        total_count = sum(category["count"] for category in service_categories)
        for category in service_categories:
            if total_count > 0:
                category["percentage"] = round((category["count"] / total_count) * 100, 2)
        
        return {
            "total_service": total_service,
            "service_request": service_request,
            "incident": incident,
            "approval": approval,
            "self_service": self_service,
            "manual_service": manual_service,
            "previous_total": previous_total,
            "change_rate": change_rate,
            "resolution_rate": resolution_rate,
            "completion_rate": completion_rate,
            "timeliness_rate": timeliness_rate,
            "satisfaction_rate": satisfaction_rate,
            "unresolved_current": unresolved_current,
            "unresolved_history": unresolved_history,
            "knowledge_base": knowledge_base,
            "service_categories": service_categories
        }
    
    def replace_template_variables(self, content: str, data: Dict[str, Any], period: Dict[str, Any]) -> str:
        """替换模板中的变量"""
        # 替换时间相关变量
        content = content.replace("【周|月】", f"【{period['type']}】")
        content = content.replace("【（2025年10月01日-2025年10月31日）】", f"【（{period['period']}）】")
        content = content.replace("【2025年10月01日-2025年10月31日】", f"【{period['period']}】")
        
        # 替换数据变量
        content = content.replace("【90】", f"【{data['total_service']}】")
        content = content.replace("【44】", f"【{data['service_request']}】")
        content = content.replace("【0】", f"【{data['incident']}】")
        content = content.replace("【46】", f"【{data['approval']}】")
        content = content.replace("【18】", f"【{data['self_service']}】")
        content = content.replace("【26】", f"【{data['manual_service']}】")
        content = content.replace("【91】", f"【{data['previous_total']}】")
        content = content.replace("【2.2】", f"【{abs(data['change_rate'])}】")
        content = content.replace("【下降|上升】", "【下降】" if data['change_rate'] < 0 else "【上升】")
        
        # 替换服务指标
        content = content.replace("【100】", f"【{data['resolution_rate']}】")
        content = content.replace("【100%】", f"【{data['completion_rate']}%】")
        
        # 替换未解决工单
        content = content.replace("【3】", f"【{data['unresolved_current']}】")
        content = content.replace("【5】", f"【{data['unresolved_history']}】")
        
        # 替换知识库
        content = content.replace("【空】", f"【{data['knowledge_base']}】")
        
        # 更新生成时间
        current_time = datetime.now().strftime("%Y年%m月%d日")
        content = content.replace("生成时间：2025年11月24日", f"生成时间：{current_time}")
        
        return content
    
    def generate_report(self, report_type: str = "month") -> str:
        """生成报告"""
        # 获取时间周期
        period = self.get_time_period(report_type)
        
        # 获取数据
        data = self.fetch_data_from_api(period)
        
        # 替换模板变量
        report_content = self.replace_template_variables(self.template_content, data, period)
        
        return report_content
    
    def save_report(self, content: str, output_path: str = None):
        """保存报告到文件"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"运维服务报告_{timestamp}.html"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_path


# 创建FastMCP实例
mcp = FastMCP("report-generator")

# 初始化报告生成器
generator = ReportGenerator("统建系统运维服务周月报模板-20251110.html")


@mcp.tool()
async def generate_weekly_report(system_name: Optional[str] = None) -> str:
    """生成系统运维服务周报
    
    Args:
        system_name: 系统名称（可选）
    """
    try:
        report_content = generator.generate_report("week")
        output_path = generator.save_report(report_content)
        return f"周报生成成功！文件已保存至: {output_path}"
    except Exception as e:
        return f"生成周报失败: {str(e)}"


@mcp.tool()
async def generate_monthly_report(system_name: Optional[str] = None) -> str:
    """生成系统运维服务月报
    
    Args:
        system_name: 系统名称（可选）
    """
    try:
        report_content = generator.generate_report("month")
        output_path = generator.save_report(report_content)
        return f"月报生成成功！文件已保存至: {output_path}"
    except Exception as e:
        return f"生成月报失败: {str(e)}"


@mcp.tool()
async def generate_custom_report(start_date: str, end_date: str, system_name: Optional[str] = None) -> str:
    """生成自定义时间范围的系统运维服务报告
    
    Args:
        start_date: 开始日期（格式：YYYY-MM-DD）
        end_date: 结束日期（格式：YYYY-MM-DD）
        system_name: 系统名称（可选）
    """
    try:
        # 这里可以实现自定义时间范围的报告生成
        # 目前暂时使用月报逻辑
        report_content = generator.generate_report("month")
        output_path = generator.save_report(report_content)
        return f"自定义报告生成成功！文件已保存至: {output_path}"
    except Exception as e:
        return f"生成自定义报告失败: {str(e)}"


@mcp.tool()
async def get_report_template_info() -> str:
    """获取报告模板信息"""
    try:
        template_path = "统建系统运维服务周月报模板-20251110.html"
        if os.path.exists(template_path):
            file_size = os.path.getsize(template_path)
            return f"模板文件存在，大小: {file_size} 字节"
        else:
            return "模板文件不存在"
    except Exception as e:
        return f"获取模板信息失败: {str(e)}"


if __name__ == "__main__":
    mcp.run("sse")
