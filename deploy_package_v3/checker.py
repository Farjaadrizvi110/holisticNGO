import os
import re
from pathlib import Path
import argparse


def find_html_files(directory):
    """Find all HTML files in the given directory and its subdirectories."""
    html_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.html', '.htm')):
                html_files.append(os.path.join(root, file))
    return html_files


def update_html_links(file_path, url_mapping):
    """Update href attributes in HTML files to use Django URL template tags."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Keep track of replacements for reporting
        replacements = []

        # Replace mappings based on exact matches first
        for old_url, new_url in url_mapping.items():
            # Don't convert URLs that are already in Django template tag format
            pattern = fr'href=["\']({re.escape(old_url)})["\']'
            if re.search(pattern, content):
                new_content = re.sub(pattern, f'href="{new_url}"', content)
                if new_content != content:
                    replacements.append(f"{old_url} → {new_url}")
                    content = new_content

        # If content was modified, write it back to the file
        if replacements:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {file_path}")
            for replacement in replacements:
                print(f"  - {replacement}")
        else:
            print(f"No changes made to {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


def create_url_mapping():
    """Create mapping from static URLs to Django URL template tags."""
    # Define basic URL mappings based on the provided urlpatterns
    url_mapping = {
        'index.html': '{% url "home" %}',
        './': '{% url "home" %}',
        'about.html': '{% url "about" %}',
        'services.html': '{% url "services" %}',
        'testimonials.html': '{% url "testimonials" %}',
        'contact.html': '{% url "contact" %}',
        'donation.html': '{% url "donation" %}',
        'faqs.html': '{% url "faqs" %}',
        'team.html': '{% url "team" %}',
        'blog.html': '{% url "blog" %}',

        # Include service-specific pages to be removed or updated
        'service-holistic-care.html': '{% url "services" %}',
        'service-education.html': '{% url "services" %}',
        'service-healthcare.html': '{% url "services" %}',
        'service-emotional-support.html': '{% url "services" %}',
        'service-skills.html': '{% url "services" %}',
        'service-community.html': '{% url "services" %}',

        # Also handle absolute URLs to the same site
        'https://holisticfostercare.org/': '{% url "home" %}',
        'https://holisticfostercare.org/about.html': '{% url "about" %}',
        'https://holisticfostercare.org/services.html': '{% url "services" %}',
        'https://holisticfostercare.org/testimonials.html': '{% url "testimonials" %}',
        'https://holisticfostercare.org/contact.html': '{% url "contact" %}',
        'https://holisticfostercare.org/donation.html': '{% url "donation" %}',
        'https://holisticfostercare.org/faqs.html': '{% url "faqs" %}',
        'https://holisticfostercare.org/team.html': '{% url "team" %}',
        'https://holisticfostercare.org/blog.html': '{% url "blog" %}',
    }

    return url_mapping


def main():
    parser = argparse.ArgumentParser(description='Update HTML href links to Django URL template tags')
    parser.add_argument('directory', help='Directory containing HTML templates')
    args = parser.parse_args()

    directory = args.directory

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        return

    url_mapping = create_url_mapping()
    html_files = find_html_files(directory)

    print(f"Found {len(html_files)} HTML file(s) in {directory}")

    for file_path in html_files:
        update_html_links(file_path, url_mapping)

    print("\nURL replacement complete!")
    print("Note: Some URLs may still need manual review, especially for dynamic URLs with parameters.")


if __name__ == "__main__":
    main()
