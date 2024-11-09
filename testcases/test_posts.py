"""
Posts API 测试模块
该模块包含所有与帖子相关的API测试用例

主要功能：
1. 获取帖子测试
2. 创建帖子测试
3. 更新帖子测试
4. 删除帖子测试
5. 数据库验证测试

作者: [您的名字]
创建日期: [创建日期]
最后修改: [最后修改日期]
"""

# 标准库导入
import os
import sys
from pathlib import Path
import time

# 添加项目根目录到 Python 路径
PROJECT_ROOT = str(Path(__file__).parent.parent)
sys.path.insert(0, PROJECT_ROOT)

# 第三方库导入
import allure
import pytest
import yaml

# 本地模块导入
from api.posts_api import PostsApi
from utils.log_util import logger
from testcases.base_test import BaseTest
from utils.assert_util import Assertions
from utils.env_util import env_manager

# 验证 yaml 版本（可选）
logger.info(f"YAML 版本: {yaml.__version__}")

@allure.epic("Posts API Testing")
class TestPosts(BaseTest):
    """
    帖子API测试类
    继承自BaseTest，包含所有帖子相关的测试用例
    """
    
    def setup_class(self):
        """
        测试类级别的设置
        在所有测试方法执行前运行一次
        初始化API客户端和测试数据
        """
        self.posts_api = PostsApi()
        logger.info("测试类初始化完成")
        
        # 加载测试数据
        data_path = os.path.join(PROJECT_ROOT, 'data', 'test_data.yaml')
        with open(data_path, 'r', encoding='utf-8') as f:
            self.test_data = yaml.safe_load(f)
        logger.info("测试数据加载完成")

    @allure.story("获取帖子")
    @allure.title("测试获取单个帖子")
    @pytest.mark.parametrize("post_id", [1, 2, 99999])
    def test_get_post(self, post_id):
        """测试获取帖子接口"""
        with allure.step(f"获取帖子 ID: {post_id}"):
            response = self.posts_api.get_post(post_id)
            
            if post_id <= 100:
                assert response.status_code == 200, "有效帖子应返回200"
                data = response.json()
                assert data['id'] == post_id, "返回的帖子ID不匹配"
            else:
                assert response.status_code == 404, "无效帖子应返回404"

    @allure.story("创建帖子")
    @allure.title("测试创建新帖子")
    def test_create_post(self):
        """测试创建帖子接口"""
        test_data = self.test_data['test_post']
        
        with allure.step("创建新帖子"):
            response = self.posts_api.create_post(
                title=test_data['title'],
                body=test_data['body'],
                user_id=test_data['user_id']
            )
            
            assert response.status_code == 201, "创建帖子应返回201"
            data = response.json()
            assert data['title'] == test_data['title'], "帖子标题不匹配"
            assert data['body'] == test_data['body'], "帖子内容不匹配"

    @allure.story("更新帖子")
    @allure.title("测试更新帖子")
    def test_update_post(self):
        """测试更新帖子接口"""
        update_data = self.test_data['update_post']
        post_id = 1  # 使用已存在的帖子ID
        
        with allure.step(f"更新帖子 ID: {post_id}"):
            response = self.posts_api.update_post(
                post_id=post_id,
                title=update_data['title'],
                body=update_data['body'],
                user_id=update_data['user_id']
            )
            
            assert response.status_code == 200, "更新帖子应返回200"
            data = response.json()
            assert data['title'] == update_data['title'], "更新后的标题不匹配"
            assert data['body'] == update_data['body'], "更新后的内容不匹配"

    @allure.story("删除帖子")
    @allure.title("测试删除帖子")
    def test_delete_post(self):
        """测试删除帖子接口"""
        # 先创建一个帖子
        test_data = self.test_data['test_post']
        create_response = self.posts_api.create_post(
            title=test_data['title'],
            body=test_data['body'],
            user_id=test_data['user_id']
        )
        post_id = create_response.json()['id']
        
        # 删除帖子
        with allure.step(f"删除帖子 ID: {post_id}"):
            response = self.posts_api.delete_post(post_id)
            assert response.status_code == 200, "删除帖子应返回200"
            
        # 验证帖子已被删除
        with allure.step("验证帖子已被删除"):
            get_response = self.posts_api.get_post(post_id)
            assert get_response.status_code == 404, "已删除的帖子应返回404"

    @allure.story("创建帖子并验证数据库记录")
    @allure.title("测试创建帖子并验证数据库记录")
    def test_create_post_with_db_validation(self, mysql_db):
        """
        创建帖子并验证数据库记录（在非dev环境下执行）
        
        参数:
            mysql_db: 数据库连接对象
            
        验证点:
            1. API创建帖子成功
            2. 数据库记录正确
            3. 数据清理成功
        """
        try:
            # 1. 准备测试数据
            title = "测试标题"
            body = "测试内容"
            user_id = 1
            
            # 2. 通过 API 创建帖子
            response = self.posts_api.create_post(
                title=title,
                body=body,
                user_id=user_id
            )
            assert response.status_code == 201, "创建帖子失败"
            post_data = response.json()
            
            # 3. 数据库验证（仅在非dev环境下执行）
            if env_manager.get_env() != 'dev' and mysql_db:
                # 插入数据到数据库
                insert_sql = """
                INSERT INTO posts (title, body, user_id) 
                VALUES (%s, %s, %s)
                """
                with allure.step("插入测试数据到数据库"):
                    result = mysql_db.execute_query(insert_sql, (title, body, user_id))
                    logger.info(f"插入数据结果: {result}")
                
                # 验证数据库记录
                select_sql = """
                SELECT * FROM posts 
                WHERE title = %s AND body = %s 
                ORDER BY id DESC 
                LIMIT 1
                """
                with allure.step("验证数据库记录"):
                    db_record = mysql_db.execute_query(select_sql, (title, body))
                    logger.info(f"查询结果: {db_record}")
                
                assert db_record, "数据库中未找到创建的帖子"
                assert db_record[0]['title'] == title, "帖子标题不匹配"
                assert db_record[0]['body'] == body, "帖子内容不匹配"
            
        except Exception as e:
            logger.error(f"测试失败: {str(e)}")
            allure.attach(
                f"错误信息: {str(e)}\n"
                f"标题: {title}\n"
                f"内容: {body}\n"
                f"用户ID: {user_id}",
                "测试失败详情",
                allure.attachment_type.TEXT
            )
            raise
        finally:
            # 清理测试数据
            if env_manager.get_env() != 'dev' and mysql_db:
                with allure.step("清理测试数据"):
                    cleanup_sql = "DELETE FROM posts WHERE title = %s"
                    mysql_db.execute_query(cleanup_sql, (title,))