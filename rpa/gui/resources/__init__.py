"""
资源管理模块
"""
import os
from pathlib import Path

# 资源目录
RESOURCES_DIR = Path(__file__).parent
ICONS_DIR = RESOURCES_DIR / 'icons'

def get_icon_path(icon_name: str) -> str:
    """获取图标路径"""
    # 如果图标不存在，返回空字符串
    icon_path = ICONS_DIR / icon_name
    if icon_path.exists():
        return str(icon_path)
    return ""

def ensure_icons_exist():
    """确保图标存在，不存在则创建默认图标"""
    if not ICONS_DIR.exists():
        ICONS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 检查是否有图标，没有则创建
    if not any(ICONS_DIR.iterdir()):
        try:
            from .generate_icons import generate_all_icons
            generate_all_icons()
        except Exception as e:
            print(f"Warning: Could not generate icons: {e}")
