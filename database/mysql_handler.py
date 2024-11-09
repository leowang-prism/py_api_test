try:
    import pymysql
    from dbutils.pooled_db import PooledDB
    HAS_DB_SUPPORT = True
except ImportError:
    HAS_DB_SUPPORT = False
    PooledDB = None
    pymysql = None

from utils.log_util import logger
from utils.env_util import env_manager
import time

class MySQLHandler:
    def __init__(self):
        if not HAS_DB_SUPPORT:
            logger.warning("数据库支持未启用 (pymysql 或 DBUtils 未安装)")
            return
            
        try:
            self.config = env_manager.get_config()['database']['mysql']
        except KeyError:
            logger.warning("数据库配置未找到，数据库功能将不可用")
            return
            
        try:
            self.pool = PooledDB(
                creator=pymysql,
                maxconnections=6,
                mincached=2,
                maxcached=4,
                host=self.config.get('host', 'localhost'),
                port=self.config.get('port', 3306),
                user=self.config.get('user', 'root'),
                password=self.config.get('password', ''),
                database=self.config.get('database', 'test'),
                charset='utf8mb4',
                autocommit=True
            )
            logger.info("数据库连接池初始化成功")
            
            # 初始化数据库结构
            self._init_database()
        except Exception as e:
            logger.error(f"数据库连接池初始化失败: {str(e)}")
            self.pool = None

    def _init_database(self):
        """初始化数据库结构"""
        try:
            # 先删除表（如果存在）
            drop_table_sql = "DROP TABLE IF EXISTS posts"
            self.execute_query(drop_table_sql)
            
            # 创建表
            create_table_sql = """
            CREATE TABLE posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                body TEXT NOT NULL,
                user_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
            self.execute_query(create_table_sql)
            logger.info("数据库表结构初始化完成")
        except Exception as e:
            logger.error(f"数据库初始化失败: {str(e)}")
            raise

    def execute_query(self, sql, params=None):
        """执行查询"""
        if not HAS_DB_SUPPORT or not self.pool:
            logger.warning("数据库功能未启用，跳过查询")
            return []
            
        connection = None
        try:
            connection = self.pool.connection()
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                logger.debug(f"执行SQL: {sql}")
                logger.debug(f"参数: {params}")
                
                cursor.execute(sql, params)
                
                if sql.strip().upper().startswith('SELECT'):
                    result = cursor.fetchall()
                    logger.debug(f"查询结果: {result}")
                else:
                    connection.commit()
                    result = cursor.rowcount
                    logger.debug(f"影响行数: {result}")
                    
                return result
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"SQL执行错误: {str(e)}")
            logger.error(f"SQL语句: {sql}")
            logger.error(f"参数: {params}")
            raise
        finally:
            if connection:
                connection.close()

    def cleanup(self):
        """清理资源"""
        if self.pool:
            self.pool.close()
            logger.info("数据库连接池已关闭")