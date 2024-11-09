@echo off
echo 开始执行测试...

:: 清理旧的报告
echo 清理旧报告...
rmdir /s /q reports 2>nul
rmdir /s /q allure-report 2>nul
mkdir reports

:: 运行测试
echo 运行测试用例...
pytest testcases/test_posts.py -v

:: 生成报告
echo 生成Allure报告...
allure generate ./reports -o ./allure-report --clean

:: 启动默认浏览器打开报告
echo 打开报告...
start "" "http://localhost:63342/allure-report/index.html"

:: 使用 Python 启动一个简单的 HTTP 服务器
echo 启动HTTP服务器...
python -m http.server 63342 --directory allure-report

echo 完成！ 