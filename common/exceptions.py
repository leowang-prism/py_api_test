class BaseError(Exception):
    """基础异常类"""
    def __init__(self, message, code=None):
        self.message = message
        self.code = code
        super().__init__(self.message)

class APIException(BaseError):
    """API异常"""
    pass

class ConfigError(BaseError):
    """配置错误"""
    pass

class DataError(BaseError):
    """数据错误"""
    pass

class AssertionError(BaseError):
    """断言错误"""
    pass 