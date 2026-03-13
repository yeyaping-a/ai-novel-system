#!/bin/bash

# 自动推送到 GitHub 脚本
# 使用方法：bash push_to_github.sh

set -e

echo "========================================="
echo "   GitHub 自动推送脚本"
echo "========================================="
echo ""

# 检查是否在 Git 仓库中
if [ ! -d .git ]; then
    echo "❌ 错误：当前目录不是 Git 仓库"
    exit 1
fi

# 检查 gh 是否安装
if ! command -v gh &> /dev/null; then
    echo "📦 检测到 gh 未安装，正在安装..."
    echo ""
    brew install gh
fi

# 检查 gh 是否已登录
echo "🔍 检查 GitHub 登录状态..."
if ! gh auth status &> /dev/null; then
    echo ""
    echo "🔐 需要登录 GitHub"
    echo "请按照提示完成登录："
    echo ""
    gh auth login
fi

# 获取仓库名称
REPO_NAME="ai-novel-system"
echo ""
echo "📝 仓库名称: $REPO_NAME"
echo ""

# 检查远程仓库是否已存在
if git remote get-url origin &> /dev/null; then
    echo "✅ 远程仓库已配置"
    echo "🚀 正在推送..."
    git push -u origin main
else
    echo "🔧 创建 GitHub 仓库..."
    gh repo create $REPO_NAME --public --source=. --remote=origin --push
fi

echo ""
echo "✅ 推送成功！"
echo ""
echo "🔗 仓库地址："
gh repo view --web
