"""接口依赖管理"""
class DependencyManager:
    def __init__(self):
        self.dependencies = {}
    
    def set_dependency(self, key, value):
        """设置依赖数据"""
        self.dependencies[key] = value
    
    def get_dependency(self, key):
        """获取依赖数据"""
        return self.dependencies.get(key)
    
    def clear_dependencies(self):
        """清理依赖数据"""
        self.dependencies.clear() 