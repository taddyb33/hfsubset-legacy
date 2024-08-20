from pathlib import Path

def find_repo_root(current_path: Path = None) -> Path:
    """
    Find the root directory of the repository.
    
    This function looks for a .git directory or a specific file/directory
    that marks the root of your repository.
    
    :param current_path: The path to start searching from. If None, uses the current file's location.
    :return: Path object pointing to the repository root.
    """
    if current_path is None:
        current_path = Path(__file__).resolve()
    
    root_markers = ['.git', 'requirements.txt', 'setup.py']
    
    for parent in current_path.parents:
        if any((parent / marker).exists() for marker in root_markers):
            return parent
    
    raise FileNotFoundError("Could not find repository root.")
