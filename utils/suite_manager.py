import yaml # type: ignore
from pathlib import Path


class TestSuiteManager:
    def __init__(self):
        self.suites = {}
        self.priorities = {}
        self.load_suite_config()
    
    def load_suite_config(self):
        """加载测试套件配置"""
        config_path = Path(__file__).parent.parent / 'config' / 'test_suite.yaml'
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            self.suites = config.get('suites', {})
            self.priorities = config.get('priorities', {})
    
    def get_suite_tests(self, suite_name):
        """获取指定套件的测试用例"""
        return self.suites.get(suite_name, [])
    
    def get_priority_tests(self, priority):
        """获取指定优先级的测试用例"""
        return self.priorities.get(priority, [])
    
    def is_test_in_suite(self, test_name, suite_name):
        """检查测试是否在指定套件中"""
        suite_tests = self.get_suite_tests(suite_name)
        return any(test_name.startswith(test) for test in suite_tests)
    
    def get_test_priority(self, test_name):
        """获取测试用例的优先级"""
        for priority, tests in self.priorities.items():
            if any(test_name.startswith(test) for test in tests):
                return priority
        return 'low'  # 默认优先级

suite_manager = TestSuiteManager() 