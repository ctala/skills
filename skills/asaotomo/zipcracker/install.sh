#!/bin/bash
# OpenClaw 技能挂载脚本 - ZipCracker

echo "=== 正在将 ZipCracker 接入 OpenClaw 工作区 ==="

# 1. 检查并安装核心依赖
if ! python3 -c "import pyzipper" &> /dev/null; then
    echo "📦 安装依赖: pyzipper..."
    pip3 install pyzipper --quiet
fi

# 2. 赋予执行权限
chmod +x zipcracker.py

# 3. 执行 ClawHub 本地注册
echo "🔗 正在向 OpenClaw 注册技能..."
if command -v npx &> /dev/null; then
    # 退回到上一级 skills 目录执行安装以确保锁文件更新
    cd .. && npx clawhub install ./zipcracker
    echo "✅ 技能注册完成！"
else
    echo "⚠️ 未找到 npx 环境，请手动在 skills 目录下运行: npx clawhub install ./zipcracker"
fi

echo "你可以运行 'openclaw skills list' 来验证挂载状态。"