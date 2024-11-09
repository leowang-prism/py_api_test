#!/bin/bash

echo "开始执行测试..."

# 清理并创建报告目录
rm -rf ./reports/*
mkdir -p reports

# 运行测试
pytest testcases/test_posts.py -v

# 运行方法:
# 1. 给脚本添加执行权限: chmod +x quick_test.sh
# 2. 执行脚本: ./quick_test.sh
# 或者直接使用 bash 运行: bash quick_test.sh
allure serve reports 