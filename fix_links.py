import os
import re

# Comprehensive list of extensionless URL cleanup
TARGET_DIR = r"c:\Users\HP\AndroidStudioProjects\ResidueSafeWeb"

def clean_file(file_path):
    if not file_path.endswith('.html'):
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find href links and window.location redirects
    # Finds pattern like 'href="role.html"' or 'href="role.html?role=farmer"' or 'window.location.href = "role.html"'
    pattern_href = r'([Hh][Rr][Ee][Ff]\s*=\s*["\'])([a-z0-9_]+)\.html'
    pattern_js = r'(window\.location\.href\s*=\s*["\'])([a-z0-9_]+)\.html'

    # Add a leading slash if missing to make it absolute (required for extensionless URLs to work correctly in all folders)
    # We replace: href="role.html"  -->  href="/role"
    new_content = re.sub(pattern_href, r'\1/\2', content)
    new_content = re.sub(pattern_js, r'\1/\2', new_content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Cleaned {file_path}")

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"Error: Directory {TARGET_DIR} not found.")
        return
        
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith('.html'):
            clean_file(os.path.join(TARGET_DIR, filename))

if __name__ == "__main__":
    main()
