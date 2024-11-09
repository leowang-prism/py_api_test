import pytest
import allure
from api.auth_api import AuthApi
from utils.log_util import logger
from utils.env_util import env_manager

class BaseTest:
    @pytest.fixture(autouse=True)
    def setup_test(self):
        """每个测试方法执行前的设置"""
        # 打印环境信息
        env_info = f"""
{'='*50}
测试开始执行
环境: {env_manager.get_env().upper()}
API地址: {env_manager.get_config()['api']['base_url']}
{'='*50}
"""
        logger.info(env_info)
        
        with allure.step("用户登录"):
            self.auth_api = AuthApi()
            try:
                response = self.auth_api.login(
                    username=self.test_data['auth']['username'],
                    password=self.test_data['auth']['password']
                )
                assert response.status_code == 200, "登录失败"
                logger.info("测试前置：登录成功")
            except Exception as e:
                logger.error(f"登录失败: {str(e)}")
                raise

        yield  # 执行测试用例

        with allure.step("清理登录状态"):
            self.auth_api.logout()
            logger.info("测试后置：已登出") 