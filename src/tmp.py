import os

def get_project_tree(root_path, prefix=''):
    """生成项目文件结构树，自动忽略以'.'开头的文件/文件夹
    
    Args:
        root_path (str): 根目录路径
        prefix (str): 用于递归的内部参数，无需手动设置
    
    Returns:
        str: 格式化的文件结构树字符串
    """
    lines = []
    if prefix == '':  # 根目录
        lines.append(os.path.basename(root_path.rstrip(os.sep)))
    
    # 过滤掉以 '.' 开头的文件/文件夹，并按字母排序
    items = sorted(
        [item for item in os.listdir(root_path) if not item.startswith('.')],
        key=lambda x: (not os.path.isdir(os.path.join(root_path, x)), x)  # 目录优先
    )
    
    for index, item in enumerate(items):
        full_path = os.path.join(root_path, item)
        is_last = index == len(items) - 1
        
        if os.path.isdir(full_path):
            # 目录处理
            lines.append(f"{prefix}{'└── ' if is_last else '├── '}{item}/")
            new_prefix = prefix + ('    ' if is_last else '│   ')
            lines.append(get_project_tree(full_path, new_prefix).lstrip())
        else:
            # 文件处理
            lines.append(f"{prefix}{'└── ' if is_last else '├── '}{item}")
    
    return '\n'.join(line for line in lines if line)  # 过滤掉空行

# 使用示例
PROJECT_ROOT = "d:/home/projects/orbitExpert"
project_tree = get_project_tree(PROJECT_ROOT)
print(project_tree)