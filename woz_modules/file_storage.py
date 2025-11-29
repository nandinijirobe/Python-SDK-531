"""
File Storage Module
Handles persistent storage of script files using JSON
"""

import json

def load_script_files():
    """Load script files from persistent storage"""
    try:
        with open('script_files.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_script_files(script_files):
    """Save script files to persistent storage"""
    with open('script_files.json', 'w') as f:
        json.dump(script_files, f, indent=2)

def get_script_files(script_name):
    """Get files for a specific marketing script"""
    script_files = load_script_files()
    return script_files.get(script_name, [])

def add_script_file(script_name, filename):
    """Add a file to a specific marketing script"""
    script_files = load_script_files()
    if script_name not in script_files:
        script_files[script_name] = []
    if filename not in script_files[script_name]:
        script_files[script_name].append(filename)
        save_script_files(script_files)
        return True
    return False

def remove_script_file(script_name, filename):
    """Remove a file from a specific marketing script"""
    script_files = load_script_files()
    if script_name in script_files and filename in script_files[script_name]:
        script_files[script_name].remove(filename)
        save_script_files(script_files)
        return True
    return False