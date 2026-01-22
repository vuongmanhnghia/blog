#!/usr/bin/env bash

set -e

echo "🏗️  Building site locally..."
hugo --minify

echo ""
echo "✅ Build complete!"
echo "📂 Built files in: public/"
echo ""
echo "🔍 To preview locally:"
echo "  hugo server -D"
echo ""
echo "🚀 To deploy:"
echo "  ./deploy.sh"
echo "  git add . && git commit -m 'Update content'"
echo "  git push origin main"
