"""参数化测试数据管理"""
import csv
import json
from pathlib import Path

class TestDataProvider:
    @staticmethod
    def load_test_cases(file_path):
        """从CSV/JSON加载测试用例"""
        file_type = Path(file_path).suffix.lower()
        
        if file_type == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                return list(csv.DictReader(f))
        elif file_type == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f) 