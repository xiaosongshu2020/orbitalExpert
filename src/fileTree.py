import os
from pathlib import Path


def get_file_tree(folder_path):
    """
    Generate a tree structure for the given folder path.
    
    Args:
        folder_path (str): Path to the folder to generate tree for
        
    Returns:
        str: String representation of the file tree structure
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        return f"Error: Path '{folder_path}' does not exist."
    
    if not folder_path.is_dir():
        return f"Error: Path '{folder_path}' is not a directory."
    
    result = []
    
    def explore_directory(dir_path, indent=0):
        items = []
        prefix = "  " * indent
        
        try:
            # Get all items in directory and sort them
            all_items = list(dir_path.iterdir())
            dirs = [item for item in all_items if item.is_dir()]
            files = [item for item in all_items if item.is_file()]
            
            dirs.sort(key=lambda x: x.name.lower())
            files.sort(key=lambda x: x.name.lower())
            
            # Display directories
            for dir_item in dirs:
                if not dir_item.name.startswith('.'):  # Skip hidden directories
                    items.append(f"{prefix}📁 {dir_item.name}/")
                    # Recursively display subdirectories
                    sub_items = explore_directory(dir_item, indent + 1)
                    items.extend(sub_items)
            
            # Display files
            for file_item in files:
                if not file_item.name.startswith('.'):  # Skip hidden files
                    try:
                        file_size = file_item.stat().st_size
                        # Format file size
                        if file_size < 1024:
                            size_str = f"{file_size}B"
                        elif file_size < 1024 * 1024:
                            size_str = f"{file_size/1024:.1f}KB"
                        elif file_size < 1024 * 1024 * 1024:
                            size_str = f"{file_size/(1024*1024):.1f}MB"
                        else:
                            size_str = f"{file_size/(1024*1024*1024):.1f}GB"
                        items.append(f"{prefix}📄 {file_item.name} ({size_str})")
                    except Exception as e:
                        items.append(f"{prefix}📄 {file_item.name} (Unable to get info: {str(e)})")
            
            return items
            
        except PermissionError:
            return [f"{prefix}❌ No permission to access directory"]
        except Exception as e:
            return [f"{prefix}❌ Error accessing directory: {str(e)}"]
    
    # Add the root folder to the result
    result.append(f"📁 {folder_path.name}/")
    
    # Start exploring
    file_structure = explore_directory(folder_path, 1)
    result.extend(file_structure)
    
    return "\n".join(result)


# If running this file directly, test the tool functionality
if __name__ == "__main__":
    # Test the function with current directory
    print("File tree for current directory:")
    print(get_file_tree("."))
