#!/bin/bash

echo "开始执行测试..."

# 清理旧的报告
echo "清理旧报告..."
rm -rf ./reports/* ./allure-report/*
mkdir -p reports

# 运行测试
echo "运行测试用例..."
pytest testcases/test_posts.py -v

# 生成报告
echo "生成Allure报告..."
allure generate ./reports -o ./allure-report --clean

# 启动浏览器打开报告
echo "打开报告..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "http://localhost:63342/allure-report/index.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "http://localhost:63342/allure-report/index.html"
fi

# 启动 Python HTTP 服务器
echo "启动HTTP服务器..."
python3 -m http.server 63342 --directory allure-report