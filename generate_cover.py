#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成小红书封面图
风格: 种草+实用,简洁大方
"""

from PIL import Image, ImageDraw, ImageFont
import os

def generate_cover_image():
    """生成小红书笔记封面图"""
    
    # 小红书推荐尺寸: 1242 x 1660 (3:4 比例)
    width = 1242
    height = 1660
    
    # 创建画布 - 使用渐变背景
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    
    # 创建渐变背景 (粉色系 - 种草风格)
    for y in range(height):
        # 从浅粉色到浅橙色的渐变
        r = int(255 - (y / height) * 30)
        g = int(240 + (y / height) * 20)
        b = int(245 + (y / height) * 10)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
    
    # 添加装饰圆圈
    # 大圆圈
    draw.ellipse([100, 100, 500, 500], fill=(255, 255, 255, 80))
    draw.ellipse([800, 1100, 1200, 1500], fill=(255, 255, 255, 60))
    
    # 小圆圈
    draw.ellipse([900, 200, 1000, 300], fill=(255, 200, 200, 100))
    draw.ellipse([200, 1300, 300, 1400], fill=(255, 220, 180, 80))
    
    # 尝试加载中文字体
    font_large = None
    font_medium = None
    font_small = None
    
    # 常见的中文字体路径
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',  # macOS 系统字体
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/Helvetica.ttc',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',  # Linux
        'C:\\Windows\\Fonts\\simhei.ttf',  # Windows
        'C:\\Windows\\Fonts\\msyh.ttc',
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font_large = ImageFont.truetype(font_path, 100)
                font_medium = ImageFont.truetype(font_path, 60)
                font_small = ImageFont.truetype(font_path, 40)
                break
            except:
                continue
    
    # 如果没有找到中文字体,使用默认字体
    if font_large is None:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
        print("警告: 未找到中文字体,使用默认字体")
    
    # 添加标题文字
    title = "AI帮我运营小红书"
    subtitle = "3个月涨粉1万+的真相"
    
    # 计算文字位置 - 居中
    # 标题
    bbox = draw.textbbox((0, 0), title, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = 400
    draw.text((x, y), title, fill=(255, 255, 255), font=font_large, stroke_width=3, stroke_fill=(200, 150, 150))
    
    # 副标题
    bbox = draw.textbbox((0, 0), subtitle, font=font_medium)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = y + text_height + 40
    draw.text((x, y), subtitle, fill=(255, 255, 255), font=font_medium, stroke_width=2, stroke_fill=(200, 150, 150))
    
    # 添加标签
    tags = ["干货", "AI工具", "博主经验"]
    y_start = 1000
    x_start = 200
    tag_width = 250
    tag_height = 80
    spacing = 50
    
    tag_colors = [(255, 100, 100), (255, 150, 50), (100, 200, 100)]
    for i, (tag, color) in enumerate(zip(tags, tag_colors)):
        x = x_start + i * (tag_width + spacing)
        # 标签背景
        draw.rounded_rectangle([x, y_start, x + tag_width, y_start + tag_height], radius=20, fill=color)
        # 标签文字
        bbox = draw.textbbox((0, 0), tag, font=font_small)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x + (tag_width - text_width) // 2
        text_y = y_start + (tag_height - text_height) // 2
        draw.text((text_x, text_y), tag, fill=(255, 255, 255), font=font_small)
    
    # 添加底部提示文字
    tip = "真实分享 · 实用干货"
    bbox = draw.textbbox((0, 0), tip, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = 1400
    draw.text((x, y), tip, fill=(255, 220, 220), font=font_small)
    
    return img

def main():
    """主函数"""
    output_path = '/Users/yeyaping/WorkBuddy/20260313143721/cover.jpg'
    
    print("正在生成小红书封面图...")
    img = generate_cover_image()
    
    # 保存图片
    img.save(output_path, 'JPEG', quality=95)
    print(f"✓ 封面图已生成: {output_path}")
    print(f"  尺寸: {img.size[0]} x {img.size[1]}")

if __name__ == '__main__':
    main()
