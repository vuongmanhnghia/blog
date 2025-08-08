#!/run/current-system/sw/bin/bash

if [ "`git status -s`" ]
then
    echo "The working directory is dirty. Please commit any pending changes."
    exit 1;
fi

echo "Deleting old publication"
rm -rf public
mkdir public
git worktree prune
rm -rf .git/worktrees/public/

echo "Deleting old images"
rm -rf /home/nagih/blog/static/images/*

echo "Syncing post from obsidian"
rsync -av --delete "/home/nagih/Documents/Obsidian Vault/posts/" "/home/nagih/blog/content/post/"

echo "Syncing images"
python images.py

echo "Checking out deploy branch into public"
git worktree add -B deploy public origin/deploy

echo "Removing existing files"
rm -rf public/*

echo "Generating site"
env HUGO_ENV="production" hugo -t github-style

echo "Updating deploy branch"
cd public && git add --all && git commit -m "Publishing to deploy (publish.sh)"

echo "Pushing to github"
git push --all
