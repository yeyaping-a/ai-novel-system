"""
初始化脚本：创建默认小说《代码掘金者》
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app
from models import db, Novel, Volume, Character

def init_novel():
    """初始化默认小说"""
    with app.app_context():
        # 检查是否已存在
        existing = Novel.query.filter_by(title='代码掘金者').first()
        if existing:
            print("小说已存在，跳过初始化")
            return
        
        # 创建小说
        novel = Novel(
            title='代码掘金者',
            author='AI',
            genre='科幻',
            theme='一个普通人如何通过AI赚了第一桶金',
            summary='2025年，AI大爆发时代。林晨，一个创业失败的程序员，偶然获得了一个早期版本的AI助手。在这个充满机遇与挑战的时代，他如何利用AI逆袭人生，赚取第一桶金？',
            world_setting='''时代背景：2025年的中国，AI大爆发时代

科技水平：
- AI模型已经非常成熟，能够完成大部分文字、图像、编程工作
- 自动驾驶开始普及
- 智能助手成为生活必需品
- AI创业成为热门领域

社会环境：
- 传统行业面临巨大冲击
- 新的就业机会不断涌现
- 贫富差距进一步拉大
- 人们对AI既期待又恐惧''',
            character_settings='''主角：林晨
- 年龄：28岁
- 职业：前程序员，现创业失败
- 性格：务实、坚韧、有商业头脑
- 现状：负债50万，寻找翻身机会
- 特长：编程、产品思维、快速学习

配角：
1. 王磊 - 林晨的前同事，现AI公司技术总监
2. 张静 - 林晨的前女友，现投资公司分析师
3. 陈明 - 创业孵化器负责人
4. 刘强 - 互联网巨头高管，林晨的主要对手''',
            status='draft'
        )
        
        db.session.add(novel)
        db.session.flush()
        
        # 创建卷
        volumes = [
            {
                'volume_number': 1,
                'title': '觉醒篇',
                'summary': '跌入谷底，偶然获得AI助手，发现第一桶金的机会'
            },
            {
                'volume_number': 2,
                'title': '搏杀篇',
                'summary': '进入AI领域创业，遭遇巨头打压，寻找突破口'
            },
            {
                'volume_number': 3,
                'title': '登顶篇',
                'summary': '找到独特商业模式，与巨头博弈，最终成功'
            }
        ]
        
        for vol_data in volumes:
            volume = Volume(
                novel_id=novel.id,
                **vol_data
            )
            db.session.add(volume)
        
        # 创建人物
        characters = [
            {
                'name': '林晨',
                'role': 'protagonist',
                'age': 28,
                'occupation': '创业者',
                'personality': '务实、坚韧、有商业头脑、善于学习',
                'background': '前程序员，创业失败后负债50万，不甘心就此沉沦'
            },
            {
                'name': '王磊',
                'role': 'supporting',
                'age': 29,
                'occupation': 'AI公司技术总监',
                'personality': '技术极客、理想主义者',
                'background': '林晨的前同事，现就职于一家AI创业公司'
            },
            {
                'name': '张静',
                'role': 'supporting',
                'age': 27,
                'occupation': '投资分析师',
                'personality': '理性、果断、有洞察力',
                'background': '林晨的前女友，因创业问题分手'
            },
            {
                'name': '刘强',
                'role': 'antagonist',
                'age': 35,
                'occupation': '互联网巨头高管',
                'personality': '野心勃勃、不择手段',
                'background': '互联网巨头的高管，负责AI业务线'
            }
        ]
        
        for char_data in characters:
            character = Character(
                novel_id=novel.id,
                **char_data
            )
            db.session.add(character)
        
        db.session.commit()
        print(f"✅ 小说《{novel.title}》创建成功！")
        print(f"   - ID: {novel.id}")
        print(f"   - 卷数: {len(volumes)}")
        print(f"   - 人物: {len(characters)}")


if __name__ == '__main__':
    init_novel()
