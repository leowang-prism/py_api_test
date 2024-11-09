# 标准库
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
PROJECT_ROOT = str(Path(__file__).parent.parent)
sys.path.insert(0, PROJECT_ROOT)

# 第三方库
import allure
import pytest
import yaml

# 本地模块
from api.posts_api import PostsApi

@allure.epic("Posts API Testing")
class TestPosts:
    def setup_class(self):
        self.posts_api = PostsApi()
        # 加载测试数据
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'test_data.yaml')
        with open(data_path, 'r', encoding='utf-8') as f:
            self.test_data = yaml.safe_load(f)

    @allure.story("获取帖子")
    @allure.title("测试获取单个帖子")
    @allure.feature("Posts API")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
        测试获取帖子的功能：
        1. 验证正常获取帖子
        2. 验证获取不存在的帖子
    """)
    @pytest.mark.parametrize("post_id", [1, 2, 99999])
    def test_get_post(self, post_id):
        """测试获取帖子接口"""
        with allure.step(f"发送获取帖子请求 - ID: {post_id}"):
            try:
                response = self.posts_api.get_post(post_id)
                
                with allure.step("验证响应状态码"):
                    if post_id > 100:
                        assert response.status_code == 404, "不存在的帖子应返回404"
                    else:
                        assert response.status_code == 200, "有效帖子应返回200"
                
                if response.status_code == 200:
                    with allure.step("验证响应内容"):
                        response_data = response.json()
                        assert response_data['id'] == post_id
                        assert 'title' in response_data
                        assert 'body' in response_data
            except Exception as e:
                allure.attach(str(e), '异常信息', allure.attachment_type.TEXT)
                raise

    @allure.story("创建帖子")
    @allure.title("测试创建新帖子")
    def test_create_post(self):
        """测试创建帖子接口"""
        test_data = self.test_data['test_post']
        
        with allure.step("发送创建帖子请求"):
            try:
                response = self.posts_api.create_post(
                    title=test_data['title'],
                    body=test_data['body'],
                    user_id=test_data['user_id']
                )
                
                with allure.step("验证响应状态码"):
                    assert response.status_code == 201, "创建帖子应返回201状态码"
                
                with allure.step("验证响应内容"):
                    response_data = response.json()
                    assert response_data['title'] == test_data['title'], "标题不匹配"
                    assert response_data['body'] == test_data['body'], "内容不匹配"
                    assert response_data['userId'] == test_data['user_id'], "用户ID不匹配"
            except Exception as e:
                allure.attach(str(e), '异常信息', allure.attachment_type.TEXT)
                raise