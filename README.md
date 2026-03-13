# AI 小说自动化系统

一个完整的 AI 驱动的小说创作与发布系统，支持番茄小说平台。

## 项目概述

本项目旨在通过 AI 技术实现小说的自动化创作、管理和发布，包含以下核心功能：

- 📝 **AI 小说创作引擎** - 自动生成章节内容
- 📚 **本地管理系统** - Web 界面管理和阅读
- 🤖 **自动化发布** - 定时发布到番茄小说平台
- 📊 **数据统计** - 创作进度和收益分析

## 技术栈

- **前端**: React + TypeScript + Tailwind CSS
- **后端**: Python Flask
- **数据库**: SQLite
- **AI 模型**: DeepSeek V3
- **自动化**: Playwright + APScheduler

## 项目结构

```
ai-novel-system/
├── frontend/          # React 前端应用
├── backend/           # Flask 后端服务
├── ai_engine/         # AI 创作引擎
├── automation/        # 自动化脚本
├── data/              # 数据存储
└── docs/              # 文档
```

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- DeepSeek API Key

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/yeyaping-a/ai-novel-system.git
cd ai-novel-system

# 安装后端依赖
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 安装前端依赖
cd frontend
npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

### 启动服务

```bash
# 启动后端
python app.py

# 启动前端（新终端）
cd frontend
npm run dev
```

访问 http://localhost:3000 开始使用。

## 功能特性

### 1. 小说创作系统

- 自动生成大纲
- AI 生成章节内容
- 智能润色和优化
- 一致性检查

### 2. 本地管理系统

- 章节管理
- 在线编辑
- 本地阅读器
- 数据统计

### 3. 自动化发布

- 定时生成新章节
- 自动发布到番茄小说
- 发布状态监控

## 当前小说

**《代码掘金者》**

- 类型：科幻小说
- 主题：一个普通人如何通过 AI 赚了第一桶金
- 计划章节：50 章
- 总字数：约 12-15 万字

## 文档

- [系统设计方案](./docs/design.md)
- [API 文档](./docs/api.md)
- [部署指南](./docs/deployment.md)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- GitHub: [@yeyaping-a](https://github.com/yeyaping-a)
