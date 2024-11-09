"""
Pytest配置文件
定义了测试框架使用的fixture和其他配置

主要功能：
1. 数据库连接管理
2. 测试环境设置
3. 测试数据管理
"""

import pytest
from utils.env_util import env_manager
from utils.log_util import logger

# 尝试导入MySQL处理器
try:
    from database.mysql_handler import MySQLHandler
    HAS_MYSQL = True
except ImportError:
    HAS_MYSQL = False
    logger.warning("MySQL功能未启用（pymysql未安装）")

@pytest.fixture(scope="session")
def mysql_db():
    """
    数据库连接fixture
    
    作用域: session（整个测试会话）
    
    返回:
        MySQLHandler: 数据库处理器实例
        None: 如果数据库功能未启用
    
    注意:
        - 在模拟环境下会返回None
        - 在没有安装pymysql时会返回None
        - 会自动管理数据库连接的生命周期
    """
    # 检查是否为模拟环境
    if env_manager.get_config()['api'].get('mock'):
        logger.info("模拟API环境，跳过数据库初始化")
        yield None
        return
    
    # 检查MySQL支持是否启用    
    if not HAS_MYSQL:
        logger.warning("跳过数据库初始化（MySQL功能未启用）")
        yield None
        return
    
    # 初始化数据库连接    
    db = None
    try:
        db = MySQLHandler()
        logger.info("数据库连接初始化成功")
        yield db
    except Exception as e:
        logger.error(f"数据库fixture初始化失败: {str(e)}")
        yield None
    finally:
        # 清理资源
        if db and hasattr(db, 'pool'):
            logger.info("关闭数据库连接")
            db.cleanup()

@pytest.fixture(autouse=True)
def env_setup(request):
    """
    环境设置fixture
    
    作用域: function（每个测试函数）
    自动使用: 是
    
    功能:
        - 记录测试开始和结束
        - 提供测试环境信息
    """
    logger.info(f"开始执行测试: {request.node.name}")
    yield
    logger.info(f"测试执行完成: {request.node.name}")

@pytest.fixture
def test_data(request):
    """
    测试数据fixture
    
    作用域: function（每个测试函数）
    
    返回:
        dict: 测试数据字典
        
    用法:
        在测试模块中定义 TEST_DATA 变量，
        该fixture会返回该变量的值
    """
    return request.module.TEST_DATA if hasattr(request.module, 'TEST_DATA') else {}

@pytest.fixture(scope="function")
def test_data_setup(mysql_db):
    """
    准备测试数据的fixture
    
    作用域: function（每个测试函数）
    
    功能:
        - 创建测试表
        - 插入测试数据
        - 测试后清理数据
        
    依赖:
        - mysql_db fixture
    """
    if not mysql_db:
        logger.warning("数据库未连接，跳过测试数据准备")
        yield
        return
        
    try:
        # 创建测试表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS posts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            body TEXT,
            user_id INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        mysql_db.execute_query(create_table_sql)
        
        # 插入测试数据
        insert_sql = """
        INSERT INTO posts (title, body, user_id) 
        VALUES (%s, %s, %s)
        """
        mysql_db.execute_query(insert_sql, ("测试标题", "测试内容", 1))
        
        yield
        
        # 清理测试数据
        mysql_db.execute_query("TRUNCATE TABLE posts")
    except Exception as e:
        logger.error(f"测试数据准备失败: {str(e)}")
        yield