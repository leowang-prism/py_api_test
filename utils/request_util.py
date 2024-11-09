import yaml
import os
import requests

class RequestUtil:
    def __init__(self):
        self.session = requests.Session()
        self.config = self._load_config()

    def _load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get_base_url(self):
        """获取基础URL"""
        return self.config['api']['base_url']

    def send_request(self, method, url, **kwargs):
        """发送HTTP请求"""
        try:
            response = self.session.request(method, url, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求发生错误: {str(e)}") 