import pytest # type: ignore
from .suite_manager import suite_manager

def smoke_test(func):
    """标记为冒烟测试"""
    return pytest.mark.smoke(func)

def regression_test(func):
    """标记为回归测试"""
    return pytest.mark.regression(func)

def performance_test(func):
    """标记为性能测试"""
    return pytest.mark.performance(func)

def priority(level):
    """优先级装饰器"""
    def decorator(func):
        return pytest.mark.priority(level)(func)
    return decorator 