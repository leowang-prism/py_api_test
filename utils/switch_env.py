import os
import argparse
from utils.env_util import env_manager
from utils.log_util import logger

def switch_environment(env_name):
    """切换测试环境"""
    valid_envs = ['dev', 'test', 'prod']
    
    if env_name.lower() not in valid_envs:
        raise ValueError(f"无效的环境名称。有效环境: {', '.join(valid_envs)}")
    
    # 设置环境变量
    os.environ['ENV'] = env_name
    
    # 重新加载配置
    env_manager._initialized = False
    env_manager.__init__()
    
    logger.info(f"已切换到环境: {env_name}")
    logger.info(f"当前API地址: {env_manager.get_config()['api']['base_url']}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='切换测试环境')
    parser.add_argument('environment', choices=['dev', 'test', 'prod'], help='目标环境')
    args = parser.parse_args()
    
    switch_environment(args.environment) 