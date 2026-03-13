from flask import Blueprint, request, jsonify
from models import db, Chapter, GenerationTask
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from services.ai_service import AIService

generation_bp = Blueprint('generation', __name__)


@generation_bp.route('/outline', methods=['POST'])
def generate_outline():
    """生成章节大纲"""
    data = request.get_json()
    novel_id = data.get('novel_id')
    volume_id = data.get('volume_id')
    chapter_count = data.get('chapter_count', 10)
    theme = data.get('theme', '')
    
    ai_service = AIService()
    
    try:
        result = ai_service.generate_outline(
            novel_id=novel_id,
            volume_id=volume_id,
            chapter_count=chapter_count,
            theme=theme
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@generation_bp.route('/chapter/<int:chapter_id>', methods=['POST'])
def generate_chapter_content(chapter_id):
    """生成章节内容"""
    chapter = Chapter.query.get_or_404(chapter_id)
    
    data = request.get_json() or {}
    force_regenerate = data.get('force', False)
    
    # 检查是否已生成
    if chapter.status == 'generated' and not force_regenerate:
        return jsonify({
            'success': False,
            'message': '章节已生成，如需重新生成请设置 force=true'
        })
    
    # 创建生成任务
    task = GenerationTask(
        chapter_id=chapter_id,
        task_type='content',
        status='processing'
    )
    db.session.add(task)
    db.session.commit()
    
    try:
        ai_service = AIService()
        result = ai_service.generate_chapter_content(
            chapter_id=chapter_id
        )
        
        # 更新章节
        chapter.content = result['content']
        chapter.word_count = len(result['content'])
        chapter.status = 'generated'
        
        # 更新任务
        task.status = 'completed'
        task.result = result['content']
        task.tokens_used = result.get('tokens_used', 0)
        task.model = result.get('model', 'unknown')
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '章节生成成功',
            'data': {
                'chapter_id': chapter_id,
                'word_count': chapter.word_count,
                'tokens_used': result.get('tokens_used', 0)
            }
        })
    except Exception as e:
        task.status = 'failed'
        task.error_message = str(e)
        db.session.commit()
        
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@generation_bp.route('/polish/<int:chapter_id>', methods=['POST'])
def polish_chapter(chapter_id):
    """润色章节"""
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if not chapter.content:
        return jsonify({
            'success': False,
            'message': '章节内容为空，无法润色'
        }), 400
    
    try:
        ai_service = AIService()
        result = ai_service.polish_content(chapter.content)
        
        # 返回润色后的内容，不直接保存
        return jsonify({
            'success': True,
            'data': {
                'original': chapter.content,
                'polished': result['content'],
                'tokens_used': result.get('tokens_used', 0)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@generation_bp.route('/check-consistency/<int:chapter_id>', methods=['POST'])
def check_consistency(chapter_id):
    """检查章节一致性"""
    chapter = Chapter.query.get_or_404(chapter_id)
    
    if not chapter.content:
        return jsonify({
            'success': False,
            'message': '章节内容为空'
        }), 400
    
    try:
        ai_service = AIService()
        result = ai_service.check_consistency(
            novel_id=chapter.novel_id,
            chapter_id=chapter_id
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@generation_bp.route('/tasks', methods=['GET'])
def get_generation_tasks():
    """获取生成任务列表"""
    tasks = GenerationTask.query.order_by(GenerationTask.created_at.desc()).limit(50).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': t.id,
            'chapter_id': t.chapter_id,
            'task_type': t.task_type,
            'model': t.model,
            'tokens_used': t.tokens_used,
            'status': t.status,
            'error_message': t.error_message,
            'created_at': t.created_at.isoformat(),
            'completed_at': t.completed_at.isoformat() if t.completed_at else None
        } for t in tasks]
    })
