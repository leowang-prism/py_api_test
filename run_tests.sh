#!/bin/bash

# 获取环境参数，默认为dev
ENV=${1:-dev}

# 验证环境参数
valid_envs=("dev" "test" "prod")
if [[ ! " ${valid_envs[@]} " =~ " ${ENV} " ]]; then
    echo "错误: 无效的环境名称。有效环境: ${valid_envs[*]}"
    exit 1
fi

# 打印醒目的环境信息
echo "
====================================================
                测试环境: ${ENV}
===================================================="

# 设置环境变量
export ENV=$ENV

# 显示当前环境信息
python -c "from utils.env_util import env_manager; print(f'当前环境配置:\n基础URL: {env_manager.get_config()[\"api\"][\"base_url\"]}')"

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

# 直接使用 allure serve 打开报告
echo "打开报告..."
allure serve reports