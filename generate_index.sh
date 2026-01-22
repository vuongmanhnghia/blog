#!/run/current-system/sw/bin/bash

# Script to automatically generate _index.md files for all subdirectories in content/posts
# This enables Hugo to recognize subdirectories as sections for proper URL structure

POSTS_DIR="/home/nagih/hugo/content/posts"

echo "Generating _index.md files for sections..."

# Find all directories (excluding the posts root itself)
find "$POSTS_DIR" -type d | while read -r dir; do
    # Skip the root posts directory
    if [ "$dir" = "$POSTS_DIR" ]; then
        continue
    fi
    
    # Check if _index.md already exists
    if [ ! -f "$dir/_index.md" ]; then
        # Get the directory name for the title
        dirname=$(basename "$dir")
        # Capitalize first letter
        title=$(echo "$dirname" | sed 's/\b\(.\)/\u\1/g')
        
        # Create _index.md
        cat > "$dir/_index.md" << EOF
---
title: "$title"
---
EOF
        echo "Created: $dir/_index.md"
    fi
done

echo "Done generating _index.md files."
