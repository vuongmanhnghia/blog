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

def convert_obsidian_links(content, title_map=None, url_map=None, content_directory="content"):
    title_map = title_map or {}
    url_map = url_map or {}
    
    def replace_simple_link(match):
        link_text = match.group(1)
        file_slug = slugify(link_text)
        
        # Keep the original link text for display
        display_text = link_text
        
        # Use URL from title if available, otherwise use the link text
        url_slug = url_map.get(file_slug, file_slug)
        
        print(f"Converting link: '{link_text}' → URL: '{url_slug}/'")
        
        # Add trailing slash
        return f'[{display_text}](posts/{url_slug}/)'
    
    def replace_aliased_link(match):
        link_url = match.group(1)
        display_text = match.group(2)
        
        file_slug = slugify(link_url)
        
        # Use URL from title if available, otherwise use the link text
        url_slug = url_map.get(file_slug, file_slug)
        
        # Print debugging info
        print(f"Converting aliased link: '{link_url}|{display_text}' → URL: '{url_slug}/'")
        
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

def get_post_titles_and_urls(directory):
    """Create mappings for post titles and URLs"""
    title_map = {}  # Maps file slug to actual title
    url_map = {}    # Maps file slug to URL slug from title
    
    for filepath in glob.glob(f"{directory}/**/*.md", recursive=True):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            frontmatter = extract_frontmatter(content)
            if 'title' in frontmatter:
                title = frontmatter['title']
                filename = os.path.splitext(os.path.basename(filepath))[0]
                file_slug = slugify(filename)
                title_slug = slugify(title)
                
                # Map filename slug to actual title for display
                title_map[file_slug] = title
                
                # Map filename slug to title slug for URL
                url_map[file_slug] = title_slug
                
                print(f"File: '{filename}' → URL: '{title_slug}' → Title: '{title}'")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    return title_map, url_map

def process_markdown_files(directory):
    # First, build the title and URL maps
    title_map, url_map = get_post_titles_and_urls(directory)
    
    for filepath in glob.glob(f"{directory}/**/*.md", recursive=True):
        print(f"Processing: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            original_content = file.read()
        
        converted_content = convert_obsidian_links(original_content, title_map, url_map, directory)
        
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