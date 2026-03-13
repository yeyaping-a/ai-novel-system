from flask import Blueprint, jsonify
from models import Novel, Chapter, Volume

reader_bp = Blueprint('reader', __name__)


@reader_bp.route('/novel/<int:novel_id>', methods=['GET'])
def get_novel_for_reader(novel_id):
    """获取小说信息用于阅读器"""
    novel = Novel.query.get_or_404(novel_id)
    chapters = Chapter.query.filter_by(novel_id=novel_id).order_by(Chapter.chapter_number).all()
    
    return jsonify({
        'success': True,
        'data': {
            'id': novel.id,
            'title': novel.title,
            'author': novel.author,
            'summary': novel.summary,
            'total_chapters': len(chapters),
            'chapters': [{
                'id': c.id,
                'chapter_number': c.chapter_number,
                'title': c.title,
                'word_count': c.word_count,
                'status': c.status
            } for c in chapters]
        }
    })


@reader_bp.route('/chapter/<int:chapter_id>', methods=['GET'])
def read_chapter(chapter_id):
    """阅读章节"""
    chapter = Chapter.query.get_or_404(chapter_id)
    
    # 获取上一章和下一章
    prev_chapter = Chapter.query.filter(
        Chapter.novel_id == chapter.novel_id,
        Chapter.chapter_number < chapter.chapter_number
    ).order_by(Chapter.chapter_number.desc()).first()
    
    next_chapter = Chapter.query.filter(
        Chapter.novel_id == chapter.novel_id,
        Chapter.chapter_number > chapter.chapter_number
    ).order_by(Chapter.chapter_number).first()
    
    return jsonify({
        'success': True,
        'data': {
            'id': chapter.id,
            'novel_id': chapter.novel_id,
            'chapter_number': chapter.chapter_number,
            'title': chapter.title,
            'content': chapter.content,
            'word_count': chapter.word_count,
            'prev_chapter_id': prev_chapter.id if prev_chapter else None,
            'next_chapter_id': next_chapter.id if next_chapter else None
        }
    })


@reader_bp.route('/toc/<int:novel_id>', methods=['GET'])
def get_table_of_contents(novel_id):
    """获取目录"""
    novel = Novel.query.get_or_404(novel_id)
    volumes = Volume.query.filter_by(novel_id=novel_id).order_by(Volume.volume_number).all()
    
    result = []
    for volume in volumes:
        chapters = Chapter.query.filter_by(
            volume_id=volume.id
        ).order_by(Chapter.chapter_number).all()
        
        result.append({
            'volume_id': volume.id,
            'volume_number': volume.volume_number,
            'volume_title': volume.title,
            'chapters': [{
                'id': c.id,
                'chapter_number': c.chapter_number,
                'title': c.title,
                'word_count': c.word_count,
                'status': c.status
            } for c in chapters]
        })
    
    # 未分卷的章节
    ungrouped_chapters = Chapter.query.filter_by(
        novel_id=novel_id,
        volume_id=None
    ).order_by(Chapter.chapter_number).all()
    
    if ungrouped_chapters:
        result.append({
            'volume_id': None,
            'volume_number': 0,
            'volume_title': '正文',
            'chapters': [{
                'id': c.id,
                'chapter_number': c.chapter_number,
                'title': c.title,
                'word_count': c.word_count,
                'status': c.status
            } for c in ungrouped_chapters]
        })
    
    return jsonify({
        'success': True,
        'data': {
            'novel_id': novel_id,
            'novel_title': novel.title,
            'toc': result
        }
    })
