#!/usr/bin/env python3
"""
测试脚本：验证报告生成功能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from main import ReportGenerator

def test_report_generation():
    """测试报告生成功能"""
    print("开始测试报告生成功能...")
    
    try:
        # 创建报告生成器实例
        generator = ReportGenerator("统建系统运维服务周月报模板-20251110.html")
        print("✓ 模板文件加载成功")
        
        # 测试周报生成
        weekly_report = generator.generate_report("week")
        print("✓ 周报生成成功")
        
        # 测试月报生成
        monthly_report = generator.generate_report("month")
        print("✓ 月报生成成功")
        
        # 保存测试报告
        weekly_path = generator.save_report(weekly_report, "测试周报.html")
        monthly_path = generator.save_report(monthly_report, "测试月报.html")
        
        print(f"✓ 周报已保存至: {weekly_path}")
        print(f"✓ 月报已保存至: {monthly_path}")
        
        # 验证报告内容
        assert "【周】" in weekly_report, "周报时间类型替换失败"
        assert "【月】" in monthly_report, "月报时间类型替换失败"
        assert "生成时间：" in weekly_report, "生成时间替换失败"
        assert "生成时间：" in monthly_report, "生成时间替换失败"
        
        print("✓ 所有测试通过！")
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_report_generation()
    sys.exit(0 if success else 1)
