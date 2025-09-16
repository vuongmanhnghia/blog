import re
import glob

def convert_obsidian_links(content, content_directory="content"):
    def replace_simple_link(match):
        link_text = match.group(1)
        
        # Keep the original link text for display
        display_text = link_text
        
        print(f"Converting link: '{link_text}' → filename: '{link_text}'")
        
        # Use filename directly since permalink is now /:filename/
        return f'[{display_text}]({link_text}/)'
    
    def replace_aliased_link(match):
        link_url = match.group(1)
        display_text = match.group(2)
        
        print(f"Converting aliased link: '{link_url}|{display_text}' → filename: '{link_url}'")
        
        # Use filename directly since permalink is now /:filename/
        return f'[{display_text}]({link_url}/)'
    
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
        
        converted_content = convert_obsidian_links(original_content, directory)
        
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