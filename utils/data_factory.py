"""数据工厂：管理测试数据的生成和清理"""
from faker import Faker # type: ignore
import os
from datetime import datetime

class DataFactory:
    def __init__(self):
        self.faker = Faker(['zh_CN', 'en_US'])
        self.data_cache = {}
    
    def generate_test_data(self, data_type, **kwargs):
        """生成测试数据"""
        if data_type == 'user':
            data = {
                'username': self.faker.user_name(),
                'email': self.faker.email(),
                'phone': self.faker.phone_number(),
                'created_at': datetime.now().isoformat()
            }
        elif data_type == 'post':
            data = {
                'title': self.faker.sentence(),
                'body': self.faker.text(),
                'tags': self.faker.words(3)
            }
        
        # 缓存生成的数据
        self.data_cache[data_type] = data
        return data
    
    def cleanup_test_data(self):
        """清理测试数据"""
        self.data_cache.clear() 