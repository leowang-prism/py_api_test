import os
import yaml # type: ignore
from pathlib import Path
from utils.log_util import logger

class EnvManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.config_dir = Path(__file__).parent.parent / 'config'
        self.config = self._load_main_config()  # 先加载主配置
        self.env = self._get_env()  # 获取环境设置
        self.config = self._load_env_config()  # 加载环境特定配置
        self._print_env_info()
    
    def _get_env(self):
        """获取当前环境，优先级：环境变量 > 配置文件 > 默认值"""
        env = os.getenv('ENV')  # 从环境变量获取
        if not env:
            env = self.config.get('env', 'test')  # 从配置文件获取，默认为test
            if isinstance(env, str) and '${ENV:' in env:
                env = env.replace('${ENV:', '').replace('}', '')
        return env.lower()
    
    def _load_main_config(self):
        """加载主配置文件"""
        return self._load_yaml(self.config_dir / 'config.yaml')
    
    def _load_env_config(self):
        """加载并合并环境特定配置"""
        main_config = self.config.copy()
        env_config = self._load_yaml(self.config_dir / 'env' / f'{self.env}.yaml')
        return {**main_config, **env_config}
    
    def _print_env_info(self):
        """打印环境信息"""
        env_info = f"""
{'='*50}
当前测试环境: {self.env.upper()}
API地址: {self.config['api']['base_url']}
超时设置: {self.config['api']['timeout']}秒
SSL验证: {'启用' if self.config['api']['verify_ssl'] else '禁用'}
{'='*50}
"""
        logger.info(env_info)
    
    def _load_yaml(self, file_path):
        """加载YAML文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"加载配置文件失败 {file_path}: {str(e)}")
            raise
    
    def get_config(self):
        """获取当前环境的配置"""
        return self.config
    
    def get_env(self):
        """获取当前环境名称"""
        return self.env

def get_secret(key):
    """获取环境密钥"""
    return os.environ.get(key)

# 创建全局实例
env_manager = EnvManager() 