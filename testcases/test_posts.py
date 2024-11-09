# 标准库
import os
import sys
from pathlib import Path
import time

# 添加项目根目录到 Python 路径
PROJECT_ROOT = str(Path(__file__).parent.parent)
sys.path.insert(0, PROJECT_ROOT)

# 第三方库
import allure
import pytest
import yaml

# 本地模块
from api.posts_api import PostsApi
from utils.log_util import logger

@allure.epic("Posts API Testing")
class TestPosts:
    def setup_class(self):
        self.posts_api = PostsApi()
        logger.info("测试类初始化完成")
        # 加载测试数据
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'test_data.yaml')
        with open(data_path, 'r', encoding='utf-8') as f:
            self.test_data = yaml.safe_load(f)
        logger.info("测试数据加载完成")

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

    @allure.story("创建并更新帖子流程")
    @allure.title("测试创建和更新帖子的完整流程")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_and_update_post_flow(self):
        """测试创建和更新帖子的完整流程"""
        logger.info("开始测试：创建和更新帖子流程")
        try:
            # 第一步：创建帖子
            with allure.step("创建新帖子"):
                create_data = self.test_data['test_post']
                create_response = self.posts_api.create_post(
                    title=create_data['title'],
                    body=create_data['body'],
                    user_id=create_data['user_id']
                )
                
                # 验证创建响应
                assert create_response.status_code == 201, "创建帖子应返回201状态码"
                created_post = create_response.json()
                assert created_post['title'] == create_data['title'], "创建的帖子标题不匹配"
                assert created_post['body'] == create_data['body'], "创建的帖子内容不匹配"
                
                # 记录响应信息
                allure.attach(
                    f"创建响应: {create_response.text}\n"
                    f"状态码: {create_response.status_code}",
                    '创建帖子响应详情',
                    allure.attachment_type.TEXT
                )

            # 第二步：更新帖子
            with allure.step("更新帖子"):
                update_data = self.test_data['update_post']
                update_response = self.posts_api.update_post(
                    post_id=created_post['id'],
                    title=update_data['title'],
                    body=update_data['body'],
                    user_id=update_data['user_id']
                )
                
                # 记录响应信息（无论成功与否）
                allure.attach(
                    f"更新请求数据: {update_data}\n"
                    f"更新响应: {update_response.text}\n"
                    f"状态码: {update_response.status_code}",
                    '更新帖子响应详情',
                    allure.attachment_type.TEXT
                )
                
                # 验证更新响应
                assert update_response.status_code in [200, 201], f"更新帖子应返回200或201状态码，实际返回{update_response.status_code}"
                updated_post = update_response.json()
                
                # 验证更新的字段
                if 'title' in updated_post:
                    assert updated_post['title'] == update_data['title'], "更新的帖子标题不匹配"
                if 'body' in updated_post:
                    assert updated_post['body'] == update_data['body'], "更新的帖子内容不匹配"
                
            logger.info("测试完成：创建和更新帖子流程")
        except Exception as e:
            logger.error(f"测试失败：{str(e)}")
            raise

    @allure.story("删除帖子")
    @allure.title("测试删除帖子")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_post(self):
        """测试删除帖子"""
        # 第一步：创建要删除的帖子
        with allure.step("创建待删除的帖子"):
            create_data = self.test_data['test_post']
            create_response = self.posts_api.create_post(
                title=create_data['title'],
                body=create_data['body'],
                user_id=create_data['user_id']
            )
            assert create_response.status_code == 201
            post_id = create_response.json()['id']

        # 第二步：删除帖子
        with allure.step(f"删除帖子 - ID: {post_id}"):
            delete_response = self.posts_api.delete_post(post_id)
            assert delete_response.status_code == 200

        # 第三步：验证帖子已被删除
        with allure.step("验证帖子已被删除"):
            get_response = self.posts_api.get_post(post_id)
            assert get_response.status_code == 404