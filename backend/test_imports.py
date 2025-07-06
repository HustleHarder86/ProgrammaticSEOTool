"""Test all imports in the backend to find issues before deployment"""
import ast
import os
from pathlib import Path

def check_imports(file_path):
    """Check if a Python file has valid imports"""
    with open(file_path, 'r') as f:
        try:
            tree = ast.parse(f.read())
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}" if module else alias.name)
            return True, imports
        except SyntaxError as e:
            return False, f"Syntax Error: {e}"

# Check all Python files
issues = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py') and file != 'test_imports.py':
            file_path = os.path.join(root, file)
            success, result = check_imports(file_path)
            if not success:
                issues.append((file_path, result))
            else:
                # Check for problematic imports
                for imp in result:
                    if imp.startswith('backend.'):
                        issues.append((file_path, f"Import issue: '{imp}' - should not use 'backend.' prefix"))

if issues:
    print("Found issues:")
    for file_path, issue in issues:
        print(f"\n{file_path}:")
        print(f"  {issue}")
else:
    print("No import issues found!")

# Check for circular imports by looking at __init__.py files
print("\n\nChecking __init__.py files for potential circular imports:")
for root, dirs, files in os.walk('.'):
    if '__init__.py' in files:
        init_path = os.path.join(root, '__init__.py')
        with open(init_path, 'r') as f:
            content = f.read()
            if content.strip():  # Not empty
                print(f"\n{init_path}:")
                print(content[:200] + "..." if len(content) > 200 else content)