class TestDataConsistency:
    def test_api_db_consistency(self, mysql_db):
        """测试API和数据库数据一致性"""
        # 通过API获取数据
        response = self.posts_api.get_post(1)
        api_data = response.json()
        
        # 从数据库获取数据
        sql = "SELECT * FROM posts WHERE id = %s"
        db_data = mysql_db.execute_query(sql, (1,))[0]
        
        # 验证一致性
        assert api_data['title'] == db_data['title']
        assert api_data['body'] == db_data['body'] 