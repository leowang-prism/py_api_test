# API 自动化测试项目


![Uploading image.png…]()




各目录详细说明

api/
作用：封装所有 API 接口调用
特点：模块化、可复用、易维护
主要文件：
base_api.py：提供基础请求方法
auth_api.py：处理认证相关接口
posts_api.py：处理帖子相关接口



common/
作用：存放通用功能和定义
特点：跨模块使用的通用代码
主要文件：
exceptions.py：自定义异常类定义


config/
作用：管理配置信息
特点：环境隔离、配置集中
主要文件：
config.yaml：主配置文件
env/*.yaml：环境特定配置


data/
作用：管理测试数据
特点：数据驱动、易维护
主要文件：
test_data.yaml：测试数据定义


testcases/
作用：存放测试用例
特点：结构化、易扩展
主要文件：
conftest.py：pytest 配置和 fixtures
test_*.py：各类测试用例


utils/
作用：工具类集合
特点：功能独立、可复用
主要文件：
env_checker.py：环境检查工具
env_util.py：环境管理工具
log_util.py：日志工具
report_enhancer.py：报告增强工具
request_util.py：HTTP 请求工具
retry.py：重试机制


.github/
作用：CI/CD 配置
特点：自动化流程
主要文件：
workflows/api-test.yml：GitHub Actions 配置


logs/
作用：日志存储
特点：问题追踪、调试支持


reports/
作用：测试报告存储
特点：结果展示、数据分析


项目优势
清晰的职责划分
良好的可维护性
高度的可扩展性
完整的功能支持
规范的代码组织
