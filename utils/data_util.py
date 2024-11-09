import json
import csv
import random
import string
from datetime import datetime
from pathlib import Path
from utils.log_util import logger

class DataGenerator:
    @staticmethod
    def generate_random_string(length=10):
        """生成随机字符串"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_random_email():
        """生成随机邮箱"""
        return f"test_{DataGenerator.generate_random_string(8)}@example.com"

    @staticmethod
    def generate_random_phone():
        """生成随机手机号"""
        return f"1{''.join(random.choices(string.digits, k=10))}"

class DataLoader:
    @staticmethod
    def load_json(file_path):
        """加载JSON文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载JSON文件失败: {str(e)}")
            raise

    @staticmethod
    def load_csv(file_path):
        """加载CSV文件"""
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            logger.error(f"加载CSV文件失败: {str(e)}")
            raise 