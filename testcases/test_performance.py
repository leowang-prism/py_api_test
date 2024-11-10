import pytest
import allure
from utils.markers import performance_test
from utils.log_util import logger
from api.posts_api import PostsApi
import time

@allure.epic("Performance Testing")
class TestPerformance:
    
    def setup_class(self):
        self.posts_api = PostsApi()
    
    @allure.story("API响应时间测试")
    @performance_test
    def test_api_response_time(self):
        """测试API响应时间"""
        start_time = time.time()
        response = self.posts_api.get_post(1)
        end_time = time.time()
        
        response_time = end_time - start_time
        logger.info(f"API响应时间: {response_time:.2f}秒")
        
        assert response_time < 2, f"API响应时间过长: {response_time:.2f}秒"
    
    @allure.story("并发请求测试")
    @performance_test
    def test_concurrent_requests(self):
        """测试并发请求处理"""
        import concurrent.futures
        
        def make_request(post_id):
            return self.posts_api.get_post(post_id)
        
        post_ids = range(1, 11)  # 测试前10个帖子
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request, pid) for pid in post_ids]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        logger.info(f"并发请求总时间: {total_time:.2f}秒")
        assert all(r.status_code == 200 for r in responses), "部分请求失败"
        assert total_time < 5, f"并发请求处理时间过长: {total_time:.2f}秒"