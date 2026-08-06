@echo off
chcp 65001 >nul
echo ========================================
echo  LearnTide - 提交代码到 GitHub
echo ========================================
echo.

:: 确保在项目根目录
cd /d "%~dp0\.."

:: 查看当前变更状态
echo [1/2] 待提交内容预览：
git status --short
echo.

:: 暂存所有（.gitignore 会自动排除临时文件）
echo [2/2] 暂存...
git add -A
if %errorlevel% neq 0 (
    echo ⚠️ 暂存失败
    pause
    exit /b %errorlevel%
)

echo ✓ 暂存完成。请手动执行以下命令：
echo.
echo   git commit -m "feat: 批量更新描述"
echo   git push
echo.
pause
