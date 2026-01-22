---
title: Completely restore Git commits (Orphan Branch)
description: How to completely reset the Git commit history (Orphan Branch)
date: 2026-01-22
image:
categories:
  - instruction
tags:
  - git
draft: false
---
---
## Step 1: Create a temporary branch (Orphan)

An **orphan** branch is a special branch, it has no commit history but still keeps all files in the workspace

```bash
git checkout --orphan latest_commit
```

## Step 2: Add all files and commit

At this time, all file are "staged" status (ready to commit)

```bash
git add -A
git commit -m "Init commit"
```

## Step 3: Delete the old `main` branch

```bash
git branch -D main
```

## Step 4: Rename current branch to `main`

```bash
git branch -m main
```

## Step 5: Update the remote repository

If you have pushed code, you must "force push" to replace the old history on the server

```bash
git push origin main -f
```