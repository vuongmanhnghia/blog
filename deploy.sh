#!/usr/bin/env bash

set -e

echo "🔄 Syncing posts from Obsidian..."
rsync -av --delete "/home/nagih/Documents/blog/posts/" "/home/nagih/hugo/content/posts/"

echo "🖼️  Syncing thumbnails..."
rsync -av --delete "/home/nagih/Documents/blog/thumb/" "/home/nagih/hugo/static/thumb/"

echo "📸 Processing images..."
python images.py

echo "🔗 Converting Obsidian links..."
python convert_obsidian_links.py

echo "📁 Generating section indexes..."
# bash generate_index.sh

echo ""
echo "✅ Content prepared successfully!"
echo ""

git add .
git commit -m "Update content"
git push origin main

echo "Update content successfully!"
echo ""
echo ""
# echo "📋 Next steps:"
# echo "  1. Review changes:    git status"
# echo "  2. Stage changes:     git add ."
# echo "  3. Commit:            git commit -m 'Update content'"
# echo "  4. Deploy:            git push origin main"
echo ""
echo "💡 GitHub Actions will automatically build and deploy to the deploy branch"
echo "🌐 Site will be live at: https://nagih.nooblearn2code.com"