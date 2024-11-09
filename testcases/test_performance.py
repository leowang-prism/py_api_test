import time

class TestPerformance:
    def test_database_response_time(self, mysql_db):
        """测试数据库响应时间"""
        start_time = time.time()
        
        sql = "SELECT * FROM posts LIMIT 1000"
        results = mysql_db.execute_query(sql)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        assert execution_time < 1.0, f"数据库查询超时: {execution_time}秒" 