import os
import re
import glob
import unicodedata
import yaml  # pyright: ignore[reportMissingModuleSource]

def slugify(text):
    """Convert text to URL-friendly slug"""
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    # Remove leading/trailing hyphens
    return text.strip('-')

def convert_obsidian_links(content, title_map=None):
    title_map = title_map or {}
    
    def replace_simple_link(match):
        link_text = match.group(1)
        url_slug = slugify(link_text)
        
        # Use the actual post title if available
        display_text = title_map.get(url_slug, link_text)
        
        # Use just the slug, let Hugo handle the full path
        return f'[{display_text}](posts/{url_slug})'
    
    def replace_aliased_link(match):
        link_url = match.group(1)
        display_text = match.group(2)
        url_slug = slugify(link_url)
        
        # For aliased links, keep the alias as is
        # (no need to replace with title since the user explicitly chose a display text)
        
        # Use just the slug, let Hugo handle the full path
        return f'[{display_text}](posts/{url_slug})'
    
    # Convert [[Link|Alias]] first
    content = re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', replace_aliased_link, content)
    
    # Then convert [[Link]]
    content = re.sub(r'\[\[([^\]]+)\]\]', replace_simple_link, content)
    
    return content

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    if content.startswith('---'):
        end_marker = content.find('---', 3)
        if end_marker != -1:
            frontmatter_yaml = content[3:end_marker].strip()
            try:
                return yaml.safe_load(frontmatter_yaml)
            except yaml.YAMLError:
                return {}
    return {}

def get_post_titles(directory):
    """Create a mapping of slugified names to actual post titles"""
    title_map = {}
    
    for filepath in glob.glob(f"{directory}/**/*.md", recursive=True):
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
        
        frontmatter = extract_frontmatter(content)
        if 'title' in frontmatter:
            title = frontmatter['title']
            slug = slugify(os.path.splitext(os.path.basename(filepath))[0])
            title_map[slug] = title
    
    return title_map

def process_markdown_files(directory):
    # First, build the title map
    title_map = get_post_titles(directory)
    
    for filepath in glob.glob(f"{directory}/**/*.md", recursive=True):
        print(f"Processing: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            original_content = file.read()
        
        converted_content = convert_obsidian_links(original_content, title_map)
        
        # Only write if there are changes
        if original_content != converted_content:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(converted_content)
            print(f"✓ Converted links in: {filepath}")
        else:
            print(f"- No changes needed: {filepath}")

if __name__ == "__main__":
    content_directory = "content"
    process_markdown_files(content_directory)