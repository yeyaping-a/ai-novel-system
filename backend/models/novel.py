from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Novel(db.Model):
    """小说信息表"""
    __tablename__ = 'novels'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, comment='小说标题')
    author = db.Column(db.String(100), nullable=False, default='AI', comment='作者')
    genre = db.Column(db.String(50), comment='类型')
    theme = db.Column(db.String(200), comment='主题')
    summary = db.Column(db.Text, comment='简介')
    world_setting = db.Column(db.Text, comment='世界观设定')
    character_settings = db.Column(db.Text, comment='人物设定')
    total_chapters = db.Column(db.Integer, default=0, comment='总章节数')
    total_words = db.Column(db.Integer, default=0, comment='总字数')
    status = db.Column(db.String(20), default='draft', comment='状态: draft/publishing/completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关联
    volumes = db.relationship('Volume', backref='novel', lazy='dynamic', cascade='all, delete-orphan')
    chapters = db.relationship('Chapter', backref='novel', lazy='dynamic', cascade='all, delete-orphan')


class Volume(db.Model):
    """卷信息表"""
    __tablename__ = 'volumes'
    
    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False, comment='小说ID')
    volume_number = db.Column(db.Integer, nullable=False, comment='卷号')
    title = db.Column(db.String(200), nullable=False, comment='卷标题')
    summary = db.Column(db.Text, comment='卷简介')
    chapter_count = db.Column(db.Integer, default=0, comment='章节数')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    # 关联
    chapters = db.relationship('Chapter', backref='volume', lazy='dynamic', cascade='all, delete-orphan')


class Chapter(db.Model):
    """章节表"""
    __tablename__ = 'chapters'
    
    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False, comment='小说ID')
    volume_id = db.Column(db.Integer, db.ForeignKey('volumes.id'), comment='卷ID')
    chapter_number = db.Column(db.Integer, nullable=False, comment='章节序号')
    title = db.Column(db.String(200), nullable=False, comment='章节标题')
    outline = db.Column(db.Text, comment='章节大纲')
    content = db.Column(db.Text, comment='章节内容')
    word_count = db.Column(db.Integer, default=0, comment='字数')
    status = db.Column(db.String(20), default='draft', comment='状态: draft/generated/published')
    publish_time = db.Column(db.DateTime, comment='发布时间')
    fanqie_chapter_id = db.Column(db.String(100), comment='番茄小说章节ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关联
    publish_logs = db.relationship('PublishLog', backref='chapter', lazy='dynamic', cascade='all, delete-orphan')


class Character(db.Model):
    """人物表"""
    __tablename__ = 'characters'
    
    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False, comment='小说ID')
    name = db.Column(db.String(100), nullable=False, comment='姓名')
    role = db.Column(db.String(50), comment='角色: protagonist/antagonist/supporting')
    age = db.Column(db.Integer, comment='年龄')
    occupation = db.Column(db.String(100), comment='职业')
    personality = db.Column(db.Text, comment='性格')
    background = db.Column(db.Text, comment='背景故事')
    first_appear_chapter = db.Column(db.Integer, comment='首次出现章节')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')


class PublishLog(db.Model):
    """发布日志表"""
    __tablename__ = 'publish_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False, comment='章节ID')
    platform = db.Column(db.String(50), default='fanqie', comment='平台')
    action = db.Column(db.String(50), comment='操作: publish/update/delete')
    status = db.Column(db.String(20), comment='状态: success/failed')
    message = db.Column(db.Text, comment='消息')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')


class GenerationTask(db.Model):
    """AI生成任务表"""
    __tablename__ = 'generation_tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), comment='章节ID')
    task_type = db.Column(db.String(50), comment='任务类型: outline/content/polish')
    prompt = db.Column(db.Text, comment='提示词')
    result = db.Column(db.Text, comment='生成结果')
    model = db.Column(db.String(50), comment='使用的模型')
    tokens_used = db.Column(db.Integer, comment='使用token数')
    status = db.Column(db.String(20), default='pending', comment='状态: pending/processing/completed/failed')
    error_message = db.Column(db.Text, comment='错误信息')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    completed_at = db.Column(db.DateTime, comment='完成时间')
