"""增强的测试报告功能"""
import allure # type: ignore
import json
from datetime import datetime

class ReportEnhancer:
    @staticmethod
    def attach_api_info(request, response):
        """添加API请求和响应信息到报告"""
        allure.attach(
            json.dumps(request, indent=2),
            'Request',
            allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(response, indent=2),
            'Response',
            allure.attachment_type.JSON
        )
    
    @staticmethod
    def attach_test_data(data):
        """添加测试数据到报告"""
        allure.attach(
            json.dumps(data, indent=2),
            'Test Data',
            allure.attachment_type.JSON
        ) 