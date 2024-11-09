import yaml
import os
import requests
from utils.log_util import logger

class RequestUtil:
    def __init__(self):
        self.session = requests.Session()
        self.config = self._load_config()
        logger.info("RequestUtil 初始化完成")

    def _load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
        logger.debug(f"加载配置文件: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_base_url(self):
        """获取基础URL"""
        base_url = self.config['api']['base_url']
        logger.debug(f"获取基础URL: {base_url}")
        return base_url

    def send_request(self, method, url, **kwargs):
        """发送HTTP请求"""
        logger.info(f"发送 {method} 请求到 {url}")
        logger.debug(f"请求参数: {kwargs}")
        
        try:
            response = self.session.request(method, url, **kwargs)
            logger.info(f"响应状态码: {response.status_code}")
            logger.debug(f"响应内容: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"请求发生错误: {str(e)}")
            raise Exception(f"请求发生错误: {str(e)}")