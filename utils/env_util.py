import os
import yaml

class EnvManager:
    def __init__(self):
        self._config = None
        self._env = None
        self.load_environment()
    
    def load_environment(self):
        """加载环境配置"""
        # 首先从配置文件加载默认环境设置
        with open('config/config.yaml', 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
        
        # 获取环境设置，优先级：
        # 1. 环境变量
        # 2. 配置文件中的设置
        self._env = os.getenv('APP_ENV') or self._config.get('env', 'test')
        
        # 加载对应环境的配置文件
        env_config_path = f'config/env/{self._env}.yaml'
        if os.path.exists(env_config_path):
            with open(env_config_path, 'r', encoding='utf-8') as f:
                env_config = yaml.safe_load(f)
                self._config.update(env_config)
    
    def get_config(self):
        """获取当前配置"""
        if self._config is None:
            self.load_environment()
        return self._config
    
    def get_current_env(self):
        """获取当前环境"""
        if self._env is None:
            self.load_environment()
        return self._env
    
    # 添加 get_env 方法作为 get_current_env 的别名
    def get_env(self):
        """获取当前环境（别名方法）"""
        return self.get_current_env()
    
    def reload(self):
        """重新加载配置"""
        self.load_environment()

# 创建全局环境管理器实例
env_manager = EnvManager()

# 为了保持向后兼容，保留原有的函数
def load_environment():
    return env_manager.get_config(), env_manager.get_current_env()

def get_current_env():
    return env_manager.get_current_env()