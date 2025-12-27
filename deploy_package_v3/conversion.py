#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path

def add_load_static(content):
    """Add {% load static %} at the top of the template if it doesn't exist."""
    if "{% load static %}" not in content:
        # Check if there's a DOCTYPE or html tag at the beginning
        if content.lstrip().startswith("<!DOCTYPE") or content.lstrip().startswith("<html"):
            # Insert after the first line
            lines = content.split('\n', 1)
            return lines[0] + '\n{% load static %}\n' + (lines[1] if len(lines) > 1 else '')
        else:
            return "{% load static %}\n" + content
    return content

def convert_static_references(content):
    """Convert all static file references to use Django's static template tag."""

    # Process <link> tags for CSS
    content = re.sub(
        r'(<link\s+[^>]*href=["\']((?!http|https|//|{% static).*?)["\']([^>]*?)>)',
        lambda m: m.group(0).replace(m.group(2), "{% static '" + m.group(2) + "' %}"),
        content
    )

    # Process <script> tags for JS
    content = re.sub(
        r'(<script\s+[^>]*src=["\']((?!http|https|//|{% static).*?)["\']([^>]*?)>)',
        lambda m: m.group(0).replace(m.group(2), "{% static '" + m.group(2) + "' %}"),
        content
    )

    # Process <img> tags
    content = re.sub(
        r'(<img\s+[^>]*src=["\']((?!http|https|//|{% static|data:).*?)["\']([^>]*?)>)',
        lambda m: m.group(0).replace(m.group(2), "{% static '" + m.group(2) + "' %}"),
        content
    )

    # Process inline style with background-image and other url() references
    content = re.sub(
        r'url\(["\']?((?!http|https|//|{% static|data:).*?)["\']?\)',
        r'url({% static "\1" %})',
        content
    )

    # Process <audio> and <video> src attributes
    for tag in ['audio', 'video']:
        content = re.sub(
            r'(<' + tag + r'\s+[^>]*src=["\']((?!http|https|//|{% static|data:).*?)["\']([^>]*?)>)',
            lambda m: m.group(0).replace(m.group(2), "{% static '" + m.group(2) + "' %}"),
            content
        )

    # Process <source> tags
    content = re.sub(
        r'(<source\s+[^>]*src=["\']((?!http|https|//|{% static|data:).*?)["\']([^>]*?)>)',
        lambda m: m.group(0).replace(m.group(2), "{% static '" + m.group(2) + "' %}"),
        content
    )

    # Process <embed> tags
    content = re.sub(
        r'(<embed\s+[^>]*src=["\']((?!http|https|//|{% static|data:).*?)["\']([^>]*?)>)',
        lambda m: m.group(0).replace(m.group(2), "{% static '" + m.group(2) + "' %}"),
        content
    )

    # Process href for downloadable files
    content = re.sub(
        r'(<a\s+[^>]*href=["\']((?!http|https|//|{% static|data:|#|mailto:|tel:).*?\.(pdf|doc|docx|xls|xlsx|zip|rar|csv|txt))["\']([^>]*?)>)',
        lambda m: m.group(0).replace(m.group(2), "{% static '" + m.group(2) + "' %}"),
        content
    )

    # Process <object> tags
    content = re.sub(
        r'(<object\s+[^>]*data=["\']((?!http|https|//|{% static|data:).*?)["\']([^>]*?)>)',
        lambda m: m.group(0).replace(m.group(2), "{% static '" + m.group(2) + "' %}"),
        content
    )

    # Process favicon links specifically
    content = re.sub(
        r'(<link\s+[^>]*rel=["\'](?:shortcut )?icon["\'][^>]*href=["\']((?!http|https|//|{% static).*?)["\']([^>]*?)>)',
        lambda m: m.group(0).replace(m.group(2), "{% static '" + m.group(2) + "' %}"),
        content
    )

    return content

def process_file(file_path, backup=True):
    """Process a single file to convert static references."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Add {% load static %} if needed
        content = add_load_static(content)

        # Convert static references
        content = convert_static_references(content)

        # Only write if changes were made
        if content != original_content:
            if backup:
                # Create backup
                backup_path = str(file_path) + '.bak'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                print(f"Created backup at {backup_path}")

            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {file_path}")
            return True
        else:
            print(f"No changes needed for {file_path}")
            return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def process_directory(dir_path, extensions=None, recursive=True, backup=True):
    """Process all template files in a directory."""
    if extensions is None:
        extensions = ['.html', '.htm', '.djhtml', '.django']

    count = 0
    modified = 0

    for entry in os.scandir(dir_path):
        if entry.is_file():
            file_ext = os.path.splitext(entry.name)[1].lower()
            if file_ext in extensions:
                count += 1
                if process_file(entry.path, backup):
                    modified += 1
        elif entry.is_dir() and recursive:
            c, m = process_directory(entry.path, extensions, recursive, backup)
            count += c
            modified += m

    return count, modified

def main():
    parser = argparse.ArgumentParser(description='Convert static file references to Django static template tags')
    parser.add_argument('path', help='Path to template file or directory containing templates')
    parser.add_argument('--no-backup', action='store_true', help='Do not create backup files')
    parser.add_argument('--no-recursive', action='store_true', help='Do not process subdirectories')
    parser.add_argument('--extensions', default='.html,.htm,.djhtml,.django',
                        help='Comma-separated list of file extensions to process (default: .html,.htm,.djhtml,.django)')

    args = parser.parse_args()

    path = Path(args.path)
    backup = not args.no_backup
    recursive = not args.no_recursive
    extensions = ['.' + ext.strip('.') for ext in args.extensions.split(',')]

    if path.is_file():
        if process_file(path, backup):
            print("\nSuccessfully updated 1 file.")
        else:
            print("\nNo changes were needed for the file.")
    elif path.is_dir():
        print(f"Processing templates in {path}...")
        count, modified = process_directory(path, extensions, recursive, backup)
        print(f"\nProcessed {count} template files.")
        print(f"Updated {modified} files with static references.")
        if modified > 0:
            print(f"\nSuccessfully converted static references to Django's static template tags!")
            if backup:
                print("Backup files with .bak extension were created for modified files.")
        else:
            print("\nNo files needed updates.")
    else:
        print(f"Error: {path} is not a valid file or directory.")

if __name__ == "__main__":
    main()
