@echo off
setlocal

:: 获取环境参数，默认为dev
set ENV=%1
if "%ENV%"=="" set ENV=dev

:: 验证环境参数
set "valid=0"
for %%i in (dev test prod) do if /i "%ENV%"=="%%i" set "valid=1"
if "%valid%"=="0" (
    echo 错误: 无效的环境名称。有效环境: dev, test, prod
    exit /b 1
)

:: 打印醒目的环境信息
echo.
echo ====================================================
echo                 测试环境: %ENV%
echo ====================================================
echo.

:: 显示当前环境信息
python -c "from utils.env_util import env_manager; print(f'当前环境配置:\n基础URL: {env_manager.get_config()[\"api\"][\"base_url\"]}')"

:: 清理旧的报告
echo 清理旧报告...
rmdir /s /q reports 2>nul
rmdir /s /q allure-report 2>nul
mkdir reports

:: 运行测试
echo 运行测试用例...
pytest testcases/test_posts.py -v

:: 生成并打开报告
echo 打开报告...
allure serve reports

echo 完成！ 