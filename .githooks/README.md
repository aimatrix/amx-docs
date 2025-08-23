# Git Hooks

This directory contains git hooks to maintain code quality.

## Setup

To enable these hooks, run:

```bash
git config core.hooksPath .githooks
```

## Available Hooks

### pre-commit
- Checks for duplicate headers in markdown files
- Prevents commits where the front matter title matches an H1 heading

## To Bypass (Emergency Only)

If you absolutely need to commit despite warnings:

```bash
git commit --no-verify -m "Your message"
```

But please fix the issues first!