import os
import re

def run_security_scan(root_dir):
    """Runs a security scan on the specified directory."""
    results = {}
    
    # Step 1: Find executable files in root
    executable_extensions = ['.js', '.py', '.ts', '.sh', '.bat']
    root_files = []
    for item in os.listdir(root_dir):
        if os.path.isfile(os.path.join(root_dir, item)) and any(item.endswith(ext) for ext in executable_extensions):
            root_files.append(f'./{item}')
    results['root_files'] = root_files
    
    # Step 2: Credential scan
    credential_pattern = re.compile(r'password|secret|token|api.*key|admin:admin|10\.|192\.168\.', re.IGNORECASE)
    credential_matches = []
    for dirpath, _, filenames in os.walk(root_dir):
        if 'node_modules' in dirpath or 'dist' in dirpath:
            continue
        for filename in filenames:
            if any(filename.endswith(ext) for ext in ['.js', '.ts', '.py', '.json']):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r') as f:
                    for i, line in enumerate(f, 1):
                        if credential_pattern.search(line):
                            credential_matches.append(f'{file_path}:{i}:{line.strip()}')
    results['credentials'] = credential_matches
    
    # Step 3: Production URL scan
    url_pattern = re.compile(r'https://.*\.(46|85)\.')
    url_matches = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if any(filename.endswith(ext) for ext in ['.js', '.ts']):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r') as f:
                    for i, line in enumerate(f, 1):
                        if url_pattern.search(line):
                            url_matches.append(f'{file_path}:{i}:{line.strip()}')
    results['production_urls'] = url_matches
    
    return results
