"""
生成简单的图标资源文件
使用Python PIL生成基础图标
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(name, text, color, size=64):
    """创建简单图标"""
    img = Image.new('RGBA', (size, size), color)
    draw = ImageDraw.Draw(img)
    
    # 尝试使用默认字体
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    except:
        font = ImageFont.load_default()
    
    # 计算文字位置居中
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 5
    
    # 绘制文字（白色）
    draw.text((x, y), text, fill='white', font=font)
    
    return img

def generate_all_icons():
    """生成所有图标"""
    icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
    os.makedirs(icons_dir, exist_ok=True)
    
    icons = [
        ('app.png', '🤖', '#3498db'),
        ('dashboard.png', '📊', '#9b59b6'),
        ('flow.png', '📝', '#3498db'),
        ('history.png', '⏱️', '#f39c12'),
        ('template.png', '📦', '#e74c3c'),
        ('plugin.png', '🔌', '#2ecc71'),
        ('settings.png', '⚙️', '#95a5a6'),
        ('new.png', '➕', '#2ecc71'),
        ('open.png', '📂', '#f39c12'),
        ('save.png', '💾', '#3498db'),
        ('run.png', '▶️', '#2ecc71'),
        ('stop.png', '⏹️', '#e74c3c'),
        ('debug.png', '🐛', '#9b59b6'),
        ('success.png', '✅', '#27ae60'),
    ]
    
    for name, text, color in icons:
        img = create_icon(name, text, color)
        img.save(os.path.join(icons_dir, name))
        print(f"Created: {name}")

if __name__ == '__main__':
    generate_all_icons()
    print("All icons generated!")
