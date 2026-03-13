from flask import Blueprint, request, jsonify
from models import db, Novel, Volume, Character

novel_bp = Blueprint('novel', __name__)


@novel_bp.route('/', methods=['GET'])
def get_novels():
    """获取所有小说列表"""
    novels = Novel.query.all()
    return jsonify({
        'success': True,
        'data': [{
            'id': n.id,
            'title': n.title,
            'author': n.author,
            'genre': n.genre,
            'total_chapters': n.total_chapters,
            'total_words': n.total_words,
            'status': n.status,
            'created_at': n.created_at.isoformat()
        } for n in novels]
    })


@novel_bp.route('/<int:novel_id>', methods=['GET'])
def get_novel(novel_id):
    """获取单个小说详情"""
    novel = Novel.query.get_or_404(novel_id)
    volumes = Volume.query.filter_by(novel_id=novel_id).order_by(Volume.volume_number).all()
    characters = Character.query.filter_by(novel_id=novel_id).all()
    
    return jsonify({
        'success': True,
        'data': {
            'id': novel.id,
            'title': novel.title,
            'author': novel.author,
            'genre': novel.genre,
            'theme': novel.theme,
            'summary': novel.summary,
            'world_setting': novel.world_setting,
            'character_settings': novel.character_settings,
            'total_chapters': novel.total_chapters,
            'total_words': novel.total_words,
            'status': novel.status,
            'volumes': [{
                'id': v.id,
                'volume_number': v.volume_number,
                'title': v.title,
                'chapter_count': v.chapter_count
            } for v in volumes],
            'characters': [{
                'id': c.id,
                'name': c.name,
                'role': c.role,
                'age': c.age,
                'occupation': c.occupation
            } for c in characters],
            'created_at': novel.created_at.isoformat()
        }
    })


@novel_bp.route('/', methods=['POST'])
def create_novel():
    """创建新小说"""
    data = request.get_json()
    
    novel = Novel(
        title=data.get('title'),
        author=data.get('author', 'AI'),
        genre=data.get('genre'),
        theme=data.get('theme'),
        summary=data.get('summary'),
        world_setting=data.get('world_setting'),
        character_settings=data.get('character_settings')
    )
    
    db.session.add(novel)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '小说创建成功',
        'data': {'id': novel.id}
    }), 201


@novel_bp.route('/<int:novel_id>', methods=['PUT'])
def update_novel(novel_id):
    """更新小说信息"""
    novel = Novel.query.get_or_404(novel_id)
    data = request.get_json()
    
    for key in ['title', 'author', 'genre', 'theme', 'summary', 'world_setting', 'character_settings', 'status']:
        if key in data:
            setattr(novel, key, data[key])
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '小说更新成功'
    })


@novel_bp.route('/<int:novel_id>', methods=['DELETE'])
def delete_novel(novel_id):
    """删除小说"""
    novel = Novel.query.get_or_404(novel_id)
    db.session.delete(novel)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '小说删除成功'
    })


@novel_bp.route('/<int:novel_id>/volumes', methods=['GET'])
def get_volumes(novel_id):
    """获取小说的所有卷"""
    volumes = Volume.query.filter_by(novel_id=novel_id).order_by(Volume.volume_number).all()
    return jsonify({
        'success': True,
        'data': [{
            'id': v.id,
            'volume_number': v.volume_number,
            'title': v.title,
            'summary': v.summary,
            'chapter_count': v.chapter_count
        } for v in volumes]
    })


@novel_bp.route('/<int:novel_id>/volumes', methods=['POST'])
def create_volume(novel_id):
    """创建新卷"""
    data = request.get_json()
    
    volume = Volume(
        novel_id=novel_id,
        volume_number=data.get('volume_number'),
        title=data.get('title'),
        summary=data.get('summary')
    )
    
    db.session.add(volume)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '卷创建成功',
        'data': {'id': volume.id}
    }), 201


@novel_bp.route('/<int:novel_id>/characters', methods=['GET'])
def get_characters(novel_id):
    """获取小说的所有人物"""
    characters = Character.query.filter_by(novel_id=novel_id).all()
    return jsonify({
        'success': True,
        'data': [{
            'id': c.id,
            'name': c.name,
            'role': c.role,
            'age': c.age,
            'occupation': c.occupation,
            'personality': c.personality,
            'background': c.background
        } for c in characters]
    })


@novel_bp.route('/<int:novel_id>/characters', methods=['POST'])
def create_character(novel_id):
    """创建新人物"""
    data = request.get_json()
    
    character = Character(
        novel_id=novel_id,
        name=data.get('name'),
        role=data.get('role'),
        age=data.get('age'),
        occupation=data.get('occupation'),
        personality=data.get('personality'),
        background=data.get('background'),
        first_appear_chapter=data.get('first_appear_chapter')
    )
    
    db.session.add(character)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '人物创建成功',
        'data': {'id': character.id}
    }), 201


@novel_bp.route('/<int:novel_id>/stats', methods=['GET'])
def get_stats(novel_id):
    """获取小说统计信息"""
    novel = Novel.query.get_or_404(novel_id)
    
    from models import Chapter
    chapters = Chapter.query.filter_by(novel_id=novel_id).all()
    
    total_words = sum(c.word_count for c in chapters if c.word_count)
    published_count = len([c for c in chapters if c.status == 'published'])
    draft_count = len([c for c in chapters if c.status == 'draft'])
    generated_count = len([c for c in chapters if c.status == 'generated'])
    
    return jsonify({
        'success': True,
        'data': {
            'total_chapters': len(chapters),
            'total_words': total_words,
            'published_count': published_count,
            'draft_count': draft_count,
            'generated_count': generated_count,
            'average_words': total_words // len(chapters) if chapters else 0
        }
    })
