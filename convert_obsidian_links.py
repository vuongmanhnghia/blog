import os
import re
import glob
import yaml  # pyright: ignore[reportMissingModuleSource]

def slugify(text):
    """Convert text to URL-friendly slug - only lowercase and replace spaces with hyphens"""
    # Convert to lowercase
    text = text.lower()
    
    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)
    
    # Replace multiple hyphens with a single one
    text = re.sub(r'-+', '-', text)
    
    # Remove leading/trailing hyphens
    return text.strip('-')

def convert_obsidian_links(content, title_map=None, content_directory="content"):
    title_map = title_map or {}
    
    def replace_simple_link(match):
        link_text = match.group(1)
        
        # Use the actual post title for display
        display_text = title_map.get(slugify(link_text), link_text)
        
        # Create URL slug - just lowercase and replace spaces
        url_slug = slugify(link_text)
        
        print(f"Converting link: '{link_text}' → '{url_slug}/' → '{display_text}'")
        
        # Add trailing slash
        return f'[{display_text}](posts/{url_slug}/)'
    
    def replace_aliased_link(match):
        link_url = match.group(1)
        display_text = match.group(2)
        
        # Create URL slug - just lowercase and replace spaces
        url_slug = slugify(link_url)
        
        # Print debugging info
        print(f"Converting aliased link: '{link_url}|{display_text}' → '{url_slug}/'")
        
        # Add trailing slash
        return f'[{display_text}](posts/{url_slug}/)'
    
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
    """Create a mapping of slugified titles to actual post titles"""
    title_map = {}
    
    for filepath in glob.glob(f"{directory}/**/*.md", recursive=True):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            frontmatter = extract_frontmatter(content)
            if 'title' in frontmatter:
                title = frontmatter['title']
                title_slug = slugify(title)
                
                # Map the slugified title to the actual title
                title_map[title_slug] = title
                
                print(f"Mapped '{title}' → '{title_slug}'")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    return title_map

def process_markdown_files(directory):
    # First, build the title map
    title_map = get_post_titles(directory)
    
    for filepath in glob.glob(f"{directory}/**/*.md", recursive=True):
        print(f"Processing: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            original_content = file.read()
        
        converted_content = convert_obsidian_links(original_content, title_map, directory)
        
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