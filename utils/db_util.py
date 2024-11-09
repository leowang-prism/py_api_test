class TestDatabaseManager:
    def __init__(self, mysql_db):
        self.db = mysql_db
    
    def prepare_test_environment(self):
        """准备测试环境"""
        # 创建必要的表
        self.db.execute_query("""
            CREATE TABLE IF NOT EXISTS test_posts (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(255),
                body TEXT,
                user_id INT
            )
        """)
        
    def cleanup_test_environment(self):
        """清理测试环境"""
        self.db.execute_query("TRUNCATE TABLE test_posts") 