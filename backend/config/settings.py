import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """应用配置"""
    
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///../data/database/novel.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI 模型配置
    AI_MODEL = os.getenv('AI_MODEL', 'deepseek-chat')
    AI_API_KEY = os.getenv('AI_API_KEY', '')
    AI_API_BASE = os.getenv('AI_API_BASE', 'https://api.deepseek.com/v1')
    
    # 小说配置
    NOVEL_TITLE = os.getenv('NOVEL_TITLE', '代码掘金者')
    NOVEL_GENRE = os.getenv('NOVEL_GENRE', '科幻')
    CHAPTERS_PER_DAY = int(os.getenv('CHAPTERS_PER_DAY', '1'))
    
    # 自动化配置
    AUTO_GENERATE_TIME = os.getenv('AUTO_GENERATE_TIME', '10:00')
    AUTO_PUBLISH_TIME = os.getenv('AUTO_PUBLISH_TIME', '20:00')
    
    # 番茄小说配置
    FANQIE_USERNAME = os.getenv('FANQIE_USERNAME', '')
    FANQIE_PASSWORD = os.getenv('FANQIE_PASSWORD', '')
    FANQIE_BOOK_ID = os.getenv('FANQIE_BOOK_ID', '')
    
    # 文件路径
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB


config = Config()
