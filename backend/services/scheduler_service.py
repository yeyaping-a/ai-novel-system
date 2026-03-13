"""
自动化调度服务
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app
from models import db, Novel, Chapter, GenerationTask
from services.ai_service import AIService
from config.settings import config


class SchedulerService:
    """自动化调度服务"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.ai_service = AIService()
    
    def start(self):
        """启动调度器"""
        # 每天定时生成新章节
        generate_time = config.AUTO_GENERATE_TIME.split(':')
        self.scheduler.add_job(
            self.auto_generate_chapter,
            CronTrigger(
                hour=int(generate_time[0]),
                minute=int(generate_time[1])
            ),
            id='auto_generate',
            replace_existing=True
        )
        
        # 每天定时发布
        publish_time = config.AUTO_PUBLISH_TIME.split(':')
        self.scheduler.add_job(
            self.auto_publish_chapter,
            CronTrigger(
                hour=int(publish_time[0]),
                minute=int(publish_time[1])
            ),
            id='auto_publish',
            replace_existing=True
        )
        
        self.scheduler.start()
        print(f"✅ 调度器已启动")
        print(f"   - 自动生成时间: {config.AUTO_GENERATE_TIME}")
        print(f"   - 自动发布时间: {config.AUTO_PUBLISH_TIME}")
    
    def stop(self):
        """停止调度器"""
        self.scheduler.shutdown()
        print("调度器已停止")
    
    def auto_generate_chapter(self):
        """自动生成新章节"""
        with app.app_context():
            print(f"[{datetime.now()}] 开始自动生成章节...")
            
            # 找到需要生成的章节
            draft_chapter = Chapter.query.filter_by(status='draft').order_by(Chapter.chapter_number).first()
            
            if not draft_chapter:
                print("没有需要生成的草稿章节")
                return
            
            try:
                # 创建任务
                task = GenerationTask(
                    chapter_id=draft_chapter.id,
                    task_type='content',
                    status='processing'
                )
                db.session.add(task)
                db.session.commit()
                
                # 生成内容
                result = self.ai_service.generate_chapter_content(draft_chapter.id)
                
                # 更新章节
                draft_chapter.content = result['content']
                draft_chapter.word_count = len(result['content'])
                draft_chapter.status = 'generated'
                
                # 更新任务
                task.status = 'completed'
                task.result = result['content']
                task.tokens_used = result.get('tokens_used', 0)
                task.model = result.get('model', 'unknown')
                task.completed_at = datetime.utcnow()
                
                db.session.commit()
                
                print(f"✅ 章节 {draft_chapter.chapter_number} 生成成功！")
                print(f"   - 字数: {draft_chapter.word_count}")
                print(f"   - Tokens: {task.tokens_used}")
                
            except Exception as e:
                print(f"❌ 生成失败: {str(e)}")
                task.status = 'failed'
                task.error_message = str(e)
                db.session.commit()
    
    def auto_publish_chapter(self):
        """自动发布章节到番茄小说"""
        with app.app_context():
            print(f"[{datetime.now()}] 开始自动发布章节...")
            
            # 找到已生成但未发布的章节
            chapter_to_publish = Chapter.query.filter_by(status='generated').order_by(Chapter.chapter_number).first()
            
            if not chapter_to_publish:
                print("没有需要发布的章节")
                return
            
            # TODO: 实现番茄小说发布逻辑
            print(f"⚠️  章节 {chapter_to_publish.chapter_number} 待发布")
            print(f"   - 番茄小说发布功能待实现")


# 全局调度器实例
scheduler_service = None


def init_scheduler():
    """初始化调度器"""
    global scheduler_service
    scheduler_service = SchedulerService()
    scheduler_service.start()
    return scheduler_service
