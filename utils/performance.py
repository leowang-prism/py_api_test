"""性能监控工具模块"""
import time
import psutil
import statistics
from utils.log_util import logger

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        """初始化性能监控器"""
        self.metrics = []
        logger.info("性能监控器初始化完成")
    
    def record_metric(self, name, value, unit):
        """记录性能指标"""
        metric = {
            'name': name,
            'value': value,
            'unit': unit,
            'timestamp': time.time()
        }
        self.metrics.append(metric)
        logger.debug(f"记录性能指标: {metric}")
    
    def monitor_request(self, func):
        """请求性能监控装饰器"""
        def wrapper(*args, **kwargs):
            start_time = time.time()
            cpu_start = psutil.cpu_percent()
            mem_start = psutil.Process().memory_info().rss
            
            try:
                result = func(*args, **kwargs)
                
                duration = time.time() - start_time
                cpu_end = psutil.cpu_percent()
                mem_end = psutil.Process().memory_info().rss
                
                self.record_metric('response_time', duration, 'seconds')
                self.record_metric('cpu_usage', cpu_end - cpu_start, 'percent')
                self.record_metric('memory_usage', mem_end - mem_start, 'bytes')
                
                logger.info(f"请求执行时间: {duration:.2f}秒")
                logger.debug(f"CPU使用: {cpu_end - cpu_start}%, 内存使用: {(mem_end - mem_start)/1024/1024:.2f}MB")
                
                return result
            except Exception as e:
                logger.error(f"性能监控异常: {str(e)}")
                raise
            
        return wrapper