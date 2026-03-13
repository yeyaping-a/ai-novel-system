from flask import Blueprint, request, jsonify
from models import db, Chapter, Volume

chapter_bp = Blueprint('chapter', __name__)


@chapter_bp.route('/', methods=['GET'])
def get_chapters():
    """获取章节列表"""
    novel_id = request.args.get('novel_id', type=int)
    volume_id = request.args.get('volume_id', type=int)
    status = request.args.get('status')
    
    query = Chapter.query
    
    if novel_id:
        query = query.filter_by(novel_id=novel_id)
    if volume_id:
        query = query.filter_by(volume_id=volume_id)
    if status:
        query = query.filter_by(status=status)
    
    chapters = query.order_by(Chapter.chapter_number).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': c.id,
            'novel_id': c.novel_id,
            'volume_id': c.volume_id,
            'chapter_number': c.chapter_number,
            'title': c.title,
            'word_count': c.word_count,
            'status': c.status,
            'publish_time': c.publish_time.isoformat() if c.publish_time else None,
            'created_at': c.created_at.isoformat()
        } for c in chapters]
    })


@chapter_bp.route('/<int:chapter_id>', methods=['GET'])
def get_chapter(chapter_id):
    """获取章节详情"""
    chapter = Chapter.query.get_or_404(chapter_id)
    
    return jsonify({
        'success': True,
        'data': {
            'id': chapter.id,
            'novel_id': chapter.novel_id,
            'volume_id': chapter.volume_id,
            'chapter_number': chapter.chapter_number,
            'title': chapter.title,
            'outline': chapter.outline,
            'content': chapter.content,
            'word_count': chapter.word_count,
            'status': chapter.status,
            'publish_time': chapter.publish_time.isoformat() if chapter.publish_time else None,
            'created_at': chapter.created_at.isoformat(),
            'updated_at': chapter.updated_at.isoformat()
        }
    })


@chapter_bp.route('/', methods=['POST'])
def create_chapter():
    """创建新章节"""
    data = request.get_json()
    
    chapter = Chapter(
        novel_id=data.get('novel_id'),
        volume_id=data.get('volume_id'),
        chapter_number=data.get('chapter_number'),
        title=data.get('title'),
        outline=data.get('outline'),
        content=data.get('content'),
        status=data.get('status', 'draft')
    )
    
    # 计算字数
    if chapter.content:
        chapter.word_count = len(chapter.content)
    
    db.session.add(chapter)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '章节创建成功',
        'data': {'id': chapter.id}
    }), 201


@chapter_bp.route('/<int:chapter_id>', methods=['PUT'])
def update_chapter(chapter_id):
    """更新章节"""
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.get_json()
    
    for key in ['volume_id', 'chapter_number', 'title', 'outline', 'content', 'status']:
        if key in data:
            setattr(chapter, key, data[key])
    
    # 更新字数
    if 'content' in data and data['content']:
        chapter.word_count = len(data['content'])
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '章节更新成功'
    })


@chapter_bp.route('/<int:chapter_id>', methods=['DELETE'])
def delete_chapter(chapter_id):
    """删除章节"""
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '章节删除成功'
    })


@chapter_bp.route('/<int:chapter_id>/publish', methods=['POST'])
def publish_chapter(chapter_id):
    """发布章节到番茄小说"""
    chapter = Chapter.query.get_or_404(chapter_id)
    
    # TODO: 实现番茄小说发布逻辑
    
    return jsonify({
        'success': False,
        'message': '番茄小说发布功能待实现'
    })


@chapter_bp.route('/batch', methods=['POST'])
def batch_create_chapters():
    """批量创建章节大纲"""
    data = request.get_json()
    chapters_data = data.get('chapters', [])
    
    created_ids = []
    for chapter_data in chapters_data:
        chapter = Chapter(
            novel_id=chapter_data.get('novel_id'),
            volume_id=chapter_data.get('volume_id'),
            chapter_number=chapter_data.get('chapter_number'),
            title=chapter_data.get('title'),
            outline=chapter_data.get('outline'),
            status='draft'
        )
        db.session.add(chapter)
        db.session.flush()  # 获取 ID
        created_ids.append(chapter.id)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'成功创建 {len(created_ids)} 个章节',
        'data': {'ids': created_ids}
    }), 201
