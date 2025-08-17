# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Important Instructions

- **NEVER** add "Co-Authored-By: Claude" or any Claude/AI references in git commit messages
- **NEVER** add "Generated with Claude Code" or similar attribution in commits
- Keep commit messages professional and focused on the changes made

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