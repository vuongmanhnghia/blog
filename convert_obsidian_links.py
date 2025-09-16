import os
import re
import glob
import unicodedata
from pathlib import Path

def slugify(text):
    """Convert text to URL-friendly slug"""
    text = unicodedata.normalize('NFKD', text)
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

class ObsidianToHugoConverter:
    def __init__(self, content_dir="content"):
        self.content_dir = content_dir
        self.file_mapping = {}
        self.build_file_mapping()
    
    def build_file_mapping(self):
        """Build mapping from filename to relative URL path"""
        for filepath in glob.glob(f"{self.content_dir}/**/*.md", recursive=True):
            path_obj = Path(filepath)
            
            # Get relative path from content directory
            rel_path = path_obj.relative_to(self.content_dir)
            
            # Remove .md extension
            url_path = str(rel_path.with_suffix(''))
            
            # Get just the filename for mapping
            filename = path_obj.stem
            
            # Store mapping: filename -> URL path
            self.file_mapping[filename] = url_path
            
            # Also store with spaces converted to hyphens
            slug_filename = slugify(filename)
            if slug_filename != filename:
                self.file_mapping[slug_filename] = url_path
    
    def find_target_url(self, link_text):
        """Find the target URL for a given link text"""
        # Try exact match first
        if link_text in self.file_mapping:
            return self.file_mapping[link_text]
        
        # Try slugified version
        slug = slugify(link_text)
        if slug in self.file_mapping:
            return self.file_mapping[slug]
        
        # If not found, try partial matching
        for filename, url_path in self.file_mapping.items():
            if slugify(filename) == slug:
                return url_path
        
        # If still not found, return slugified version as fallback
        return slug
    
    def convert_obsidian_links(self, content, current_file_path):
        """Convert Obsidian links to Hugo format"""
        def replace_simple_link(match):
            link_text = match.group(1)
            target_url = self.find_target_url(link_text)
            
            # Make relative URL
            if not target_url.startswith('/'):
                target_url = '/' + target_url
                
            return f'[{link_text}]({target_url})'
        
        def replace_aliased_link(match):
            link_url = match.group(1)
            display_text = match.group(2)
            target_url = self.find_target_url(link_url)
            
            # Make relative URL
            if not target_url.startswith('/'):
                target_url = '/' + target_url
                
            return f'[{display_text}]({target_url})'
        
        # Convert [[Link|Alias]] first
        content = re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', replace_aliased_link, content)
        
        # Then convert [[Link]]
        content = re.sub(r'\[\[([^\]]+)\]\]', replace_simple_link, content)
        
        return content
    
    def process_all_files(self):
        """Process all markdown files"""
        processed_count = 0
        
        for filepath in glob.glob(f"{self.content_dir}/**/*.md", recursive=True):
            print(f"Processing: {filepath}")
            
            with open(filepath, 'r', encoding='utf-8') as file:
                original_content = file.read()
            
            converted_content = self.convert_obsidian_links(original_content, filepath)
            
            if original_content != converted_content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(converted_content)
                print(f"✓ Converted links in: {filepath}")
                processed_count += 1
            else:
                print(f"- No changes needed: {filepath}")
        
        print(f"\nProcessed {processed_count} files with link conversions")
        
        # Print file mapping for debugging
        print("\nFile mapping:")
        for filename, url_path in sorted(self.file_mapping.items()):
            print(f"  {filename} -> /{url_path}")

if __name__ == "__main__":
    converter = ObsidianToHugoConverter("content")
    converter.process_all_files()