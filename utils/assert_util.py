import allure
from utils.log_util import logger

class Assertions:
    @staticmethod
    def assert_status_code(response, expected_code):
        """断言响应状态码"""
        with allure.step(f"验证响应状态码是否为 {expected_code}"):
            actual_code = response.status_code
            try:
                assert actual_code == expected_code
                logger.info(f"状态码断言成功: {actual_code} == {expected_code}")
            except AssertionError:
                logger.error(f"状态码断言失败: {actual_code} != {expected_code}")
                raise

    @staticmethod
    def assert_response_contains(response, expected_content):
        """断言响应包含特定内容"""
        with allure.step(f"验证响应包含: {expected_content}"):
            try:
                assert expected_content in response.text
                logger.info(f"响应内容断言成功: 包含 {expected_content}")
            except AssertionError:
                logger.error(f"响应内容断言失败: 不包含 {expected_content}")
                raise

    @staticmethod
    def assert_json_value(response, json_path, expected_value):
        """断言JSON响应中的值"""
        with allure.step(f"验证JSON路径 {json_path} 的值是否为 {expected_value}"):
            try:
                actual_value = response.json()
                for key in json_path.split('.'):
                    actual_value = actual_value[key]
                assert actual_value == expected_value
                logger.info(f"JSON值断言成功: {json_path} = {expected_value}")
            except Exception as e:
                logger.error(f"JSON值断言失败: {str(e)}")
                raise 