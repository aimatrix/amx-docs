# Contributing to AIMatrix Documentation

## Important: Preventing Duplicate Headers

### ❌ DON'T DO THIS:
```markdown
---
title: "Project Management AI (PMAI)"
---

# Project Management AI (PMAI)  ← This creates a duplicate!

Content here...
```

### ✅ DO THIS INSTEAD:
```markdown
---
title: "Project Management AI (PMAI)"
---

Content starts here directly...
```

## Rule: Never repeat the title as an H1

The Hugo/Hextra theme automatically displays the `title` from the front matter as the page heading. Adding an H1 (`#`) with the same text creates an ugly duplicate.

**Key Points:**
1. The `title` in front matter becomes the page's H1 automatically
2. Start your content with regular text or an H2 (`##`) subheading
3. Never use H1 (`#`) if it matches or is similar to your front matter title

## Examples

### For index pages:
```markdown
---
title: "Sales Funnel AI (SFAI)"
description: "Transform your sales process..."
---

AIMatrix Sales Funnel AI revolutionizes...  ← Start with content, not H1

## Overview  ← Use H2 for sections
```

### For sub-pages:
```markdown
---
title: "Implementation Guide"
---

This guide walks you through...  ← Start with content

## Prerequisites  ← Use H2 for sections
```

## Quick Checklist Before Committing

- [ ] Check: Does your front matter have a `title`?
- [ ] Check: Is your first heading an H1 that matches the title?
- [ ] Fix: Remove the H1 or change it to H2 if needed
- [ ] Verify: Preview the page to ensure no duplicate headers appear

## Automated Prevention

A pre-commit hook can be added to check for this pattern. To enable it:

```bash
# Create the pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Check for duplicate headers in markdown files

files=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$')

for file in $files; do
    if [ -f "$file" ]; then
        # Extract title from front matter
        title=$(awk '/^---$/,/^---$/ {if (/^title:/) print}' "$file" | sed 's/title: *//; s/"//g; s/'"'"'//g')
        
        # Check for matching H1
        if [ ! -z "$title" ]; then
            h1=$(grep "^# " "$file" | head -1 | sed 's/^# *//')
            
            if [ "$title" = "$h1" ]; then
                echo "ERROR: Duplicate header found in $file"
                echo "  Front matter title: '$title'"
                echo "  H1 heading: '$h1'"
                echo "  Remove the H1 heading to fix this issue."
                exit 1
            fi
        fi
    fi
done

exit 0
EOF

chmod +x .git/hooks/pre-commit
```

This hook will prevent commits with duplicate headers from being created.