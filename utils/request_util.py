import yaml
import os
import requests
import threading
from utils.log_util import logger
import urllib3
import time
from utils.env_util import env_manager

# 禁用不安全的HTTPS请求警告（仅用于测试环境）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RequestUtil:
    _instance_lock = threading.Lock()
    _instances = {}

    def __new__(cls):
        thread_id = threading.get_ident()
        if thread_id not in cls._instances:
            with cls._instance_lock:
                if thread_id not in cls._instances:
                    cls._instances[thread_id] = super(RequestUtil, cls).__new__(cls)
        return cls._instances[thread_id]

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.session = requests.Session()
            self.config = env_manager.get_config()
            self.token = None
            self.initialized = True
            
            # 配置SSL验证
            self.verify_ssl = self.config['api']['verify_ssl']
            if not self.verify_ssl:
                logger.warning(f"[{env_manager.get_env()}] SSL验证已禁用！")
            
            # 设置自定义证书
            self.cert_path = self.config['api']['cert_path']
            if self.cert_path and os.path.exists(self.cert_path):
                self.verify_ssl = self.cert_path
                logger.info(f"使用自定义SSL证书: {self.cert_path}")
            
            logger.info(f"RequestUtil 初始化完成 [环境: {env_manager.get_env()}]")

    def set_token(self, token):
        """设置认证token"""
        self.token = token
        if token:
            self.session.headers.update({'Authorization': f'Bearer {token}'})
            logger.debug("Token已更新")

    def clear_token(self):
        """清除认证token"""
        self.token = None
        self.session.headers.pop('Authorization', None)
        logger.debug("Token已清除")

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
            # 添加SSL验证配置
            kwargs['verify'] = self.verify_ssl
            
            # 设置超时
            timeout = self.config.get('api', {}).get('timeout', 30)
            kwargs.setdefault('timeout', timeout)
            
            # 添加重试机制
            max_retries = 3
            retry_delay = 1
            
            for attempt in range(max_retries):
                try:
                    response = self.session.request(method, url, **kwargs)
                    logger.info(f"响应状态码: {response.status_code}")
                    logger.debug(f"响应内容: {response.text}")
                    return response
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:  # 最后一次重试
                        raise
                    logger.warning(f"请求失败，正在重试 ({attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
            
        except requests.exceptions.SSLError as e:
            logger.error(f"SSL证书验证失败: {str(e)}")
            if not self.verify_ssl:
                logger.error("即使禁用了SSL验证，仍然发生错误，可能是网络问题")
            raise Exception(f"请求失败: {str(e)}")
        except requests.exceptions.RequestException as e:
            logger.error(f"请求发生错误: {str(e)}")
            raise Exception(f"请求失败: {str(e)}")