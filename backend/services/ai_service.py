import os
from openai import OpenAI
from config.settings import config
from models import db, Novel, Chapter, Character

class AIService:
    """AI 服务类"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=config.AI_API_KEY,
            base_url=config.AI_API_BASE
        )
        self.model = config.AI_MODEL
    
    def generate_outline(self, novel_id, volume_id, chapter_count, theme):
        """生成章节大纲"""
        novel = Novel.query.get(novel_id)
        if not novel:
            raise ValueError(f"小说 {novel_id} 不存在")
        
        prompt = f"""你是一个专业的网络小说策划师。请为以下小说生成 {chapter_count} 个章节的大纲。

小说标题：{novel.title}
小说类型：{novel.genre}
主题：{theme or novel.theme}
世界观设定：
{novel.world_setting}

人物设定：
{novel.character_settings}

请按照以下格式输出：
第一章：章节标题
- 章节大纲（100-200字）

第二章：章节标题
- 章节大纲（100-200字）

...

要求：
1. 每章都要有明确的情节推进
2. 包含冲突、转折和高潮
3. 留有悬念，吸引读者
4. 人物行为符合设定
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的网络小说策划师。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content
        
        # 解析大纲并创建章节
        chapters = self._parse_outline(content, novel_id, volume_id)
        
        return {
            'outline': content,
            'chapters': chapters,
            'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0
        }
    
    def _parse_outline(self, outline_text, novel_id, volume_id):
        """解析大纲文本并创建章节"""
        import re
        
        chapters = []
        lines = outline_text.split('\n')
        current_chapter = None
        
        for line in lines:
            # 匹配章节标题
            match = re.match(r'第(\d+)章[：:]\s*(.+)', line)
            if match:
                if current_chapter:
                    chapters.append(current_chapter)
                
                current_chapter = {
                    'chapter_number': int(match.group(1)),
                    'title': match.group(2).strip(),
                    'outline': ''
                }
            # 匹配大纲内容
            elif current_chapter and line.strip().startswith('-'):
                current_chapter['outline'] += line.strip()[1:].strip() + '\n'
        
        if current_chapter:
            chapters.append(current_chapter)
        
        return chapters
    
    def generate_chapter_content(self, chapter_id):
        """生成章节内容"""
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            raise ValueError(f"章节 {chapter_id} 不存在")
        
        novel = Novel.query.get(chapter.novel_id)
        
        # 获取上一章内容（如果存在）
        prev_chapter = Chapter.query.filter(
            Chapter.novel_id == chapter.novel_id,
            Chapter.chapter_number < chapter.chapter_number
        ).order_by(Chapter.chapter_number.desc()).first()
        
        prev_summary = ""
        if prev_chapter and prev_chapter.content:
            # 简要总结上一章
            prev_summary = f"\n上一章概要：\n{prev_chapter.content[:500]}...\n"
        
        prompt = f"""你是一个专业的网络小说作家。请根据以下设定生成章节内容。

小说标题：{novel.title}
小说类型：{novel.genre}
世界观设定：
{novel.world_setting}

{prev_summary}

本章标题：第{chapter.chapter_number}章 {chapter.title}
本章大纲：
{chapter.outline}

写作要求：
1. 字数：2000-3000字
2. 风格：网文爽文节奏，快节奏推进
3. 要素：至少包含一个爽点或冲突
4. 结尾：留有悬念，吸引读者追更
5. 对话：自然流畅，符合人物性格
6. 描写：简洁有力，避免啰嗦

请直接输出正文内容，不要有任何前缀说明。
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的网络小说作家，擅长创作引人入胜的故事。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content
        
        return {
            'content': content,
            'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0,
            'model': self.model
        }
    
    def polish_content(self, content):
        """润色内容"""
        prompt = f"""请对以下小说章节内容进行润色优化：

{content}

润色要求：
1. 优化文笔，使语言更流畅
2. 增强细节描写
3. 去除AI生成的痕迹，使内容更自然
4. 保持原有情节和人物设定不变
5. 保持字数相近

请直接输出润色后的内容。
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的文字编辑。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        polished_content = response.choices[0].message.content
        
        return {
            'content': polished_content,
            'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0
        }
    
    def check_consistency(self, novel_id, chapter_id):
        """检查章节一致性"""
        novel = Novel.query.get(novel_id)
        chapter = Chapter.query.get(chapter_id)
        
        # 获取前5章内容
        prev_chapters = Chapter.query.filter(
            Chapter.novel_id == novel_id,
            Chapter.chapter_number < chapter.chapter_number,
            Chapter.status.in_(['generated', 'published'])
        ).order_by(Chapter.chapter_number.desc()).limit(5).all()
        
        prev_content = "\n\n".join([
            f"第{c.chapter_number}章 {c.title}:\n{c.content[:1000]}..."
            for c in reversed(prev_chapters)
        ])
        
        prompt = f"""请检查以下章节是否存在前后矛盾或不一致的地方。

小说标题：{novel.title}
人物设定：{novel.character_settings}

前几章内容摘要：
{prev_content}

当前章节：
第{chapter.chapter_number}章 {chapter.title}
{chapter.content}

请检查：
1. 人物名称是否一致
2. 人物性格是否前后矛盾
3. 时间线是否合理
4. 情节是否有冲突
5. 设定是否前后矛盾

如有问题，请列出具体问题。如无问题，请回复"内容一致，无明显矛盾"。
"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的小说审稿编辑。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content
        
        return {
            'consistent': '无明显矛盾' in result,
            'analysis': result,
            'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0
        }
