#!/bin/bash

# AI 小说自动化系统启动脚本

echo "==================================="
echo "  AI 小说自动化系统"
echo "==================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 请先安装 Python 3.9+"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 请先安装 Node.js 16+"
    exit 1
fi

# 初始化后端
echo "📦 初始化后端..."
cd backend
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

echo "激活虚拟环境..."
source venv/bin/activate

echo "安装 Python 依赖..."
pip install -r requirements.txt

echo "初始化数据库..."
python -c "from app import init_db; init_db()"

# 创建 .env 文件
if [ ! -f ".env" ]; then
    echo "创建环境配置文件..."
    cp ../.env.example .env
    echo "⚠️  请编辑 backend/.env 文件，填入你的 API Key"
fi

echo ""
echo "✅ 后端初始化完成！"
echo ""

# 初始化前端
echo "📦 初始化前端..."
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "安装 Node.js 依赖..."
    npm install
fi

echo ""
echo "✅ 前端初始化完成！"
echo ""

# 启动服务
echo "==================================="
echo "  启动服务"
echo "==================================="
echo ""
echo "启动后端服务 (端口 5000)..."
cd ../backend
source venv/bin/activate
python app.py &

BACKEND_PID=$!

echo "等待后端启动..."
sleep 3

echo "启动前端服务 (端口 5173)..."
cd ../frontend
npm run dev &

FRONTEND_PID=$!

echo ""
echo "==================================="
echo "  ✅ 启动成功！"
echo "==================================="
echo ""
echo "前端地址: http://localhost:5173"
echo "后端地址: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 等待用户中断
trap "echo ''; echo '停止服务...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" INT

wait
