import re
import glob
import unicodedata

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

def convert_obsidian_links(content):
    def replace_simple_link(match):
        link_text = match.group(1)
        url_slug = slugify(link_text)
        # Use just the slug, let Hugo handle the full path
        return f'[{link_text}](posts/{url_slug})'
    
    def replace_aliased_link(match):
        link_url = match.group(1)
        display_text = match.group(2)
        url_slug = slugify(link_url)
        # Use just the slug, let Hugo handle the full path
        return f'[{display_text}](posts/{url_slug})'
    
    # Convert [[Link|Alias]] first
    content = re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', replace_aliased_link, content)
    
    # Then convert [[Link]]
    content = re.sub(r'\[\[([^\]]+)\]\]', replace_simple_link, content)
    
    return content

def process_markdown_files(directory):
    for filepath in glob.glob(f"{directory}/**/*.md", recursive=True):
        print(f"Processing: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as file:
            original_content = file.read()
        
        converted_content = convert_obsidian_links(original_content)
        
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