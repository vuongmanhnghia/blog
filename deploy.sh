#!/run/current-system/sw/bin/bash

echo "Deleting old publication"
rm -rf public
mkdir public
git worktree prune
rm -rf .git/worktrees/public/

echo "Syncing post from obsidian"
rsync -av --delete "/home/nagih/Documents/blog/posts/" "/home/nagih/hugo/content/posts/"

echo "Syncing thumbnails from obsidian"
rsync -av --delete "/home/nagih/Documents/blog/thumb/" "/home/nagih/hugo/static/thumb/"

echo "Syncing images"
python images.py

echo "Converting obsidian links"
python convert_obsidian_links.py

echo "Checking out deploy branch into public"
git worktree add -B deploy public origin/deploy

echo "Generating site"
env HUGO_ENV="production" hugo -t PaperMod --minify

echo "Create file CNAME"
echo "blog.nagih.io.vn" > public/CNAME

# Check if there are uncommitted changes (excluding public directory)
if [ "`git status -s | grep -v '^?? public/' | grep -v '^D  public/'`" ]
then
    echo "The working directory has uncommitted changes. Please commit any pending changes."
    echo "Do you want to continue? (y/n)"
    read answer
    if [ "$answer" != "y" ]; then
        exit 1
    fi
    echo "Adding all files to git (excluding public directory)..."
    git add --all
    git reset public/
    echo "Committing all files to git"
    git commit -m "Publishing to deploy (deploy.sh)"
fi

echo "Updating deploy branch"
cd public
git add --all
if git diff --cached --quiet; then
    git commit --allow-empty -m "Trigger deploy (no content change)"
else
    git commit -m "Publishing to deploy (deploy.sh)"
fi
git push origin deploy -f
cd ..