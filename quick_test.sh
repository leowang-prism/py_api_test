#!/bin/bash

echo "开始执行测试..."

# 清理并创建报告目录
rm -rf ./reports/*
mkdir -p reports

# 运行测试
pytest testcases/test_posts.py -v

# 直接启动 allure 服务并打开浏览器
allure serve reports 