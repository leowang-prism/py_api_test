"""
重试机制模块
提供装饰器形式的重试功能

主要功能：
1. 异常重试
2. 延迟重试
3. 指数退避
4. 自定义异常处理

使用方法：
    @retry_on_failure(max_retries=3, delay=1)
    def your_function():
        # 可能失败的代码

作者: [您的名字]
创建日期: [创建日期]
"""

import time
from functools import wraps
from utils.log_util import logger

def retry_on_failure(max_retries=3, delay=1, backoff=2, exceptions=(Exception,)):
    """
    重试装饰器
    
    参数:
        max_retries (int): 最大重试次数
        delay (float): 初始延迟时间（秒）
        backoff (float): 延迟时间的增长因子
        exceptions (tuple): 需要重试的异常类型
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries == max_retries:
                        logger.error(f"重试次数已达上限 ({max_retries}次): {str(e)}")
                        raise
                    
                    logger.warning(f"第 {retries} 次重试: {str(e)}")
                    logger.info(f"等待 {current_delay} 秒后重试")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
        return wrapper
    return decorator