# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Important Instructions

- **NEVER** add "Co-Authored-By: Claude" or any Claude/AI references in git commit messages
- **NEVER** add "Generated with Claude Code" or similar attribution in commits
- Keep commit messages professional and focused on the changes made

## Task Management Strategy

**ALWAYS use sub-agents for complex, long-running tasks:**
- When given multiple files to create or extensive content to generate
- When tasks involve analyzing and processing large amounts of information
- When implementing features that span multiple files or sections
- This keeps the main agent's context window available for understanding user requests and coordinating work

**How to use sub-agents effectively:**
1. Break down complex tasks into smaller, focused sub-tasks
2. Spin up multiple sub-agents in parallel when possible
3. Use the main agent to coordinate and review sub-agent outputs
4. Keep the main agent free to respond to user queries and maintain overall context

## Critical: Prevent Duplicate Headers

**NEVER create markdown files with duplicate headers!**

The Hextra theme automatically displays the `title` from front matter as the page heading. 
Adding an H1 (`#`) with the same text creates an ugly duplicate.

### ❌ WRONG (Creates Duplicate):
```markdown
---
title: "Project Management AI (PMAI)"
---

# Project Management AI (PMAI)  ← This creates a duplicate!
```

### ✅ CORRECT:
```markdown
---
title: "Project Management AI (PMAI)"
---

AIMatrix Project Management AI revolutionizes...  ← Start with content directly
```

**Rule**: If a file has a `title` in front matter, NEVER start the content with an H1 that matches it.

## Project Overview

AIMatrix Documentation site built with Hugo and Hextra theme, featuring a Matrix-style digital rain effect.

## Key Features

- Black background with white fonts
- Digital rain effect with Greek letters and "aimatrix.com"
- Multi-language support (EN, ZH, AR, MS, ID, RU)
- Hextra theme with FlexSearch functionality
- Custom branding with AIMatrix logo

## Development

- Run `hugo server` to start local development server
- Digital rain effect is implemented in `layouts/partials/custom/head-end.html`
- Custom styles in `assets/css/custom.css`
- Homepage layout override in `layouts/hextra-home.html`

## Deployment

**IMPORTANT**: Always deploy through GitHub Actions, NEVER directly from local machine to AWS S3

1. Commit changes: `git add -A && git commit -m "Your message"`
2. Push to GitHub: `git push origin main`
3. GitHub Actions will automatically:
   - Build the Hugo site
   - Deploy to S3 bucket
   - Invalidate CloudFront cache
4. Monitor deployment: `gh run list --limit=1`

**✅ FIXED**: Clean URLs now work correctly
- ✅ Works: https://docs.aimatrix.com/developers/
- ✅ Works: https://docs.aimatrix.com/investors/
- ✅ Works: https://docs.aimatrix.com/products/
- Solution: Updated CloudFront to use S3 static website endpoint