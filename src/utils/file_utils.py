# src/utils/file_utils.py
import os

def ensure_dir(path):
    """Ensure that the directory for the given path exists."""
    if not os.path.exists(path):
        os.makedirs(path)

def save_file(path, content):
    """Save text or binary content to a file."""
    ensure_dir(os.path.dirname(path))
    mode = 'w'
    if isinstance(content, bytes):
        mode = 'wb'
    with open(path, mode) as f:
        f.write(content)

def tamper_file(original_path, tampered_path, new_content=None):
    """
    Create a tampered version of a file.
    If new_content is provided, write it; otherwise append 'tampered' to the original content.
    """
    ensure_dir(os.path.dirname(tampered_path))
    with open(original_path, 'rb') as f:
        data = f.read()
    if new_content:
        tampered_data = new_content.encode() if isinstance(new_content, str) else new_content
    else:
        tampered_data = data + b" -- tampered"
    with open(tampered_path, 'wb') as f:
        f.write(tampered_data)