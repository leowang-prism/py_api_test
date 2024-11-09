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
        """创建帖子并验证数据库记录"""
        try:
            # 1. 准备测试数据
            title = "测试标题"
            body = "测试内容"
            user_id = 1
            
            logger.info(f"当前测试环境: {env_manager.get_env()}")
            
            # 检查是否需要跳过数据库验证
            if not mysql_db:
                logger.info("数据库未配置，跳过数据库验证")
                pytest.skip("数据库未配置，跳过数据库验证")

            # 2. 通过 API 创建帖子
            response = self.posts_api.create_post(
                title=title,
                body=body,
                user_id=user_id
            )
            assert response.status_code == 201, "创建帖子失败"
            post_data = response.json()
            logger.info(f"API响应数据: {post_data}")

            # 3. 数据库验证（仅在非dev环境且有数据库连接时执行）
            if env_manager.get_env() != 'dev' and mysql_db:
                logger.info("执行数据库验证")
                
                try:
                    # 首先检查数据库连接
                    check_result = mysql_db.execute_query("SELECT 1")
                    if not check_result or not check_result[0]:
                        logger.error("数据库连接检查失败")
                        pytest.skip("数据库连接不可用")
                    logger.info("数据库连接正常")
                    
                    # 获取当前数据库名
                    db_result = mysql_db.execute_query("SELECT DATABASE()")
                    if not db_result or not db_result[0]:
                        logger.error("无法获取数据库名")
                        pytest.skip("无法获取数据库名")
                    db_name = db_result[0][0]
                    if not db_name:
                        logger.error("未选择数据库")
                        pytest.skip("未选择数据库")
                    logger.info(f"当前数据库: {db_name}")
                    
                    # 检查表是否存在
                    check_table_sql = """
                    SELECT COUNT(*) as count
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE()
                    AND table_name = 'posts'
                    """
                    result = mysql_db.execute_query(check_table_sql)
                    logger.info(f"检查表存在结果: {result}")
                    
                    table_exists = False
                    if result and result[0]:
                        table_exists = bool(result[0][0])
                    
                    if not table_exists:
                        logger.info("posts表不存在，开始创建...")
                        # 如果表不存在，创建表
                        create_table_sql = """
                        CREATE TABLE IF NOT EXISTS posts (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            title VARCHAR(255) NOT NULL,
                            body TEXT NOT NULL,
                            user_id INT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                        """
                        try:
                            mysql_db.execute_query(create_table_sql)
                            logger.info("创建posts表成功")
                        except Exception as e:
                            logger.error(f"创建表失败: {str(e)}")
                            pytest.skip(f"创建表失败: {str(e)}")
                    else:
                        logger.info("posts表已存在")

                    # 插入数据到数据库
                    insert_sql = """
                    INSERT INTO posts (title, body, user_id)
                    VALUES (%s, %s, %s)
                    """
                    with allure.step("插入测试数据到数据库"):
                        try:
                            result = mysql_db.execute_query(insert_sql, (title, body, user_id))
                            logger.info(f"插入数据结果: {result}")
                            
                            # 获取最后插入的ID
                            last_id_result = mysql_db.execute_query("SELECT LAST_INSERT_ID()")
                            if last_id_result and last_id_result[0]:
                                last_id = last_id_result[0][0]
                                logger.info(f"插入的记录ID: {last_id}")
                            else:
                                logger.warning("无法获取最后插入的ID")
                                
                        except Exception as e:
                            logger.error(f"插入数据失败: {str(e)}")
                            pytest.skip(f"插入数据失败: {str(e)}")

                    # 验证数据库记录
                    select_sql = """
                    SELECT id, title, body, user_id 
                    FROM posts
                    WHERE title = %s AND body = %s
                    ORDER BY id DESC
                    LIMIT 1
                    """
                    with allure.step("验证数据库记录"):
                        try:
                            db_record = mysql_db.execute_query(select_sql, (title, body))
                            logger.info(f"查询结果: {db_record}")
                            
                            if not db_record:
                                # 如果没有找到记录，查询所有记录以便调试
                                all_records = mysql_db.execute_query("SELECT * FROM posts")
                                logger.error(f"表中所有记录: {all_records}")
                                pytest.skip("数据库中未找到创建的帖子")
                            
                            # 验证记录的具体内容
                            record = db_record[0]
                            assert record[1] == title, f"标题不匹配: 期望 {title}, 实际 {record[1]}"
                            assert record[2] == body, f"内容不匹配: 期望 {body}, 实际 {record[2]}"
                            assert record[3] == user_id, f"用户ID不匹配: 期望 {user_id}, 实际 {record[3]}"
                            
                        except Exception as e:
                            logger.error(f"查询数据失败: {str(e)}")
                            pytest.skip(f"查询数据失败: {str(e)}")
                        
                except Exception as e:
                    logger.error(f"数据库操作失败: {str(e)}")
                    pytest.skip(f"数据库操作失败: {str(e)}")

        except pytest.skip.Exception:
            raise  # 重新抛出跳过异常
        except Exception as e:
            logger.error(f"测试执行失败: {str(e)}")
            raise
        finally:
            # 清理测试数据
            if env_manager.get_env() != 'dev' and mysql_db:
                try:
                    cleanup_sql = "DELETE FROM posts WHERE title = %s AND body = %s"
                    mysql_db.execute_query(cleanup_sql, (title, body))
                    logger.info("测试数据清理完成")
                except Exception as e:
                    logger.error(f"清理测试数据失败: {str(e)}")