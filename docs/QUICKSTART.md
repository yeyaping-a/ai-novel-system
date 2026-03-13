# AI 小说自动化系统 - 快速开始指南

## 系统要求

- Python 3.9+
- Node.js 16+
- DeepSeek API Key（或其他兼容 OpenAI API 的模型）

## 第一步：环境配置

### 1. 配置环境变量

```bash
cd backend
cp ../.env.example .env
```

编辑 `backend/.env` 文件，填入你的配置：

```env
# AI 配置（必填）
AI_API_KEY=your-deepseek-api-key-here

# 其他配置（可选）
AUTO_GENERATE_TIME=10:00
AUTO_PUBLISH_TIME=20:00
```

### 2. 获取 DeepSeek API Key

1. 访问 https://platform.deepseek.com/
2. 注册并登录
3. 在 API Keys 页面创建新的 API Key
4. 复制 API Key 到 `.env` 文件

## 第二步：安装依赖

### 后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows 用: venv\Scripts\activate
pip install -r requirements.txt
```

### 前端

```bash
cd frontend
npm install
```

## 第三步：初始化数据库

```bash
cd backend
source venv/bin/activate
python -c "from app import init_db; init_db()"
python init_novel.py  # 创建默认小说
```

## 第四步：启动服务

### 方式 1：使用启动脚本（推荐）

```bash
chmod +x start.sh
./start.sh
```

### 方式 2：手动启动

**终端 1 - 后端：**
```bash
cd backend
source venv/bin/activate
python app.py
```

**终端 2 - 前端：**
```bash
cd frontend
npm run dev
```

## 第五步：访问系统

- **前端界面**: http://localhost:5173
- **后端 API**: http://localhost:5000

## 使用流程

### 1. 查看小说

访问 http://localhost:5173，可以看到预创建的小说《代码掘金者》

### 2. 生成章节大纲

1. 进入小说详情页
2. 点击"批量生成大纲"按钮
3. 等待 AI 生成大纲

### 3. 生成章节内容

1. 在章节列表中找到草稿章节
2. 点击"AI生成"按钮
3. 等待生成完成

### 4. 编辑和润色

1. 点击"编辑"进入编辑器
2. 可以手动修改内容
3. 也可以点击"AI润色"让 AI 优化文笔

### 5. 本地阅读

1. 点击"开始阅读"
2. 选择章节开始阅读
3. 支持调整字体大小和主题

## 常见问题

### Q: API Key 无效？

检查以下几点：
1. API Key 是否正确复制
2. DeepSeek 账号是否有余额
3. `.env` 文件是否在 `backend/` 目录下

### Q: 前端无法连接后端？

1. 确认后端服务已启动（端口 5000）
2. 检查 CORS 配置
3. 尝试重启后端服务

### Q: 章节生成失败？

1. 检查 API Key 是否有效
2. 检查网络连接
3. 查看后端日志错误信息

## 下一步

- 配置番茄小说账号，实现自动发布
- 调整 AI 提示词，优化生成质量
- 自定义小说世界观和人物设定

## 技术支持

- GitHub Issues: https://github.com/yeyaping-a/ai-novel-system/issues
- 文档: 见 `docs/` 目录
