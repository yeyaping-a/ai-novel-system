import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config.settings import config

# 创建 Flask 应用
app = Flask(__name__)
app.config.from_object(config)

# 启用 CORS
CORS(app)

# 初始化数据库
from models import db
db.init_app(app)

# 注册路由
from routes.novel_routes import novel_bp
from routes.chapter_routes import chapter_bp
from routes.generation_routes import generation_bp
from routes.reader_routes import reader_bp

app.register_blueprint(novel_bp, url_prefix='/api/novels')
app.register_blueprint(chapter_bp, url_prefix='/api/chapters')
app.register_blueprint(generation_bp, url_prefix='/api/generate')
app.register_blueprint(reader_bp, url_prefix='/api/reader')


@app.route('/')
def index():
    return {
        'message': 'AI 小说自动化系统 API',
        'version': '1.0.0',
        'status': 'running'
    }


@app.route('/api/health')
def health():
    return {'status': 'healthy'}


def init_db():
    """初始化数据库"""
    with app.app_context():
        db.create_all()
        print("数据库初始化完成！")


if __name__ == '__main__':
    # 确保数据库目录存在
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'database')
    os.makedirs(db_path, exist_ok=True)
    
    # 初始化数据库
    init_db()
    
    # 启动应用
    app.run(host='0.0.0.0', port=5000, debug=config.DEBUG)
