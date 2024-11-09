"""环境检查工具"""
import socket
import requests # type: ignore
import os
from utils.env_util import get_current_env

class EnvironmentChecker:
    @staticmethod
    def check_api_availability(url, timeout=5):
        """检查API可用性"""
        try:
            response = requests.get(url, timeout=timeout)
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def check_database_connection(host, port):
        """检查数据库连接"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0 

def validate_environment():
    """验证当前环境配置是否正确"""
    current_env = get_current_env()
    valid_envs = ['dev', 'test', 'prod']
    
    if current_env not in valid_envs:
        raise ValueError(f"Invalid environment: {current_env}. Must be one of {valid_envs}")
    
    return current_env