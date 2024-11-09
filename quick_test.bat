@echo off
echo 开始执行测试...

:: 清理并创建报告目录
rmdir /s /q reports 2>nul
mkdir reports

:: 运行测试
pytest testcases/test_posts.py -v

:: 直接启动 allure 服务并打开浏览器
allure serve reports 