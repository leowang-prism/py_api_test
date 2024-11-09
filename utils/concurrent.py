"""并发测试支持模块"""
from concurrent.futures import ThreadPoolExecutor
import threading
from utils.log_util import logger

class ConcurrentTester:
    """并发测试执行器"""
    
    def __init__(self, max_workers=5):
        """
        初始化并发测试执行器
        
        参数:
            max_workers (int): 最大工作线程数
        """
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.results = []
        self._lock = threading.Lock()
        logger.info(f"初始化并发测试执行器，最大线程数: {max_workers}")
    
    def run_concurrent_tests(self, test_func, test_data_list):
        """
        并发执行测试
        
        参数:
            test_func (callable): 测试函数
            test_data_list (list): 测试数据列表
            
        返回:
            list: 测试结果列表
        """
        futures = []
        logger.info(f"开始并发执行测试，数据量: {len(test_data_list)}")
        
        # 提交所有测试任务
        for data in test_data_list:
            future = self.executor.submit(test_func, data)
            futures.append(future)
        
        # 收集测试结果
        for future in futures:
            try:
                result = future.result()
                with self._lock:
                    self.results.append(result)
                    logger.debug(f"测试结果: {result}")
            except Exception as e:
                logger.error(f"并发测试异常: {str(e)}")
                
        logger.info(f"并发测试完成，结果数量: {len(self.results)}")
        return self.results