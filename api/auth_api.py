from utils.request_util import RequestUtil
from utils.log_util import logger

class AuthApi:
    def __init__(self):
        self.request_util = RequestUtil()
        self.base_url = self.request_util.get_base_url()
        logger.info("AuthApi 初始化完成")

    def login(self, username, password):
        """
        模拟登录（因为 JSONPlaceholder 没有真实的登录接口）
        """
        url = f"{self.base_url}/users/1"  # 使用用户信息接口模拟登录
        logger.info(f"模拟用户登录: {username}")
        response = self.request_util.send_request("GET", url)
        
        if response.status_code == 200:
            # 模拟生成token
            mock_token = "mock_token_12345"
            self.request_util.set_token(mock_token)
            logger.info("模拟登录成功，token已保存")
        return response

    def logout(self):
        """
        模拟登出
        """
        logger.info("模拟用户登出")
        self.request_util.clear_token()
        return type('Response', (), {'status_code': 200})()  # 返回模拟的响应对象