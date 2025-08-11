# AIMatrix Documentation

Comprehensive documentation for AIMatrix - The Business Operating System for Modern Enterprises.

## Overview

This repository contains the source files for the AIMatrix documentation website, built with Hugo and the Docsy theme. The documentation is designed to be:

- **Multi-lingual**: Supporting 6 languages (EN, ZH, AR, MS, ID, RU)
- **Version-controlled**: Multiple versions of documentation maintained simultaneously
- **LLM-optimized**: Structured for AI/ML consumption, RAG, and GraphRAG systems
- **Comprehensive**: Covering all modules, APIs, and use cases
- **Enterprise-ready**: Following documentation standards from SAP, Oracle, Microsoft, and other leaders

## Documentation Structure

```
content/
├── en/                   # English (primary language)
│   ├── docs/            # Main documentation
│   │   ├── getting-started/
│   │   ├── modules/     # All AIMatrix modules
│   │   │   ├── pos/
│   │   │   ├── financial-accounting/
│   │   │   ├── inventory/
│   │   │   └── ...
│   │   ├── user-guides/ # Role-based guides
│   │   ├── industry-solutions/
│   │   ├── administration/
│   │   ├── developer/
│   │   └── best-practices/
│   ├── api/             # API reference
│   ├── tutorials/       # Step-by-step tutorials
│   └── community/       # Community resources
├── zh/                  # Chinese
├── ar/                  # Arabic
├── ms/                  # Malay
├── id/                  # Indonesian
└── ru/                  # Russian
```

## Key Features

### Modules Covered

- **Core ERP**: General Ledger, AR/AP, Financial Reporting
- **Point of Sales (POS)**: Retail and hospitality management
- **Supply Chain**: Procure-to-Pay, Order-to-Cash, Inventory
- **E-Commerce**: Online store integration
- **Warehouse Management**: WMS with barcode/RFID
- **Manufacturing**: MRP, production planning
- **CRM**: Customer relationship management
- **HR**: Human resources and payroll
- **B2B Portal**: Business-to-business transactions
- **Mobile Apps**: iOS and Android applications
- **Applet Store**: Third-party extensions
- **And many more...**

### Target Audiences

1. **Business Users**: Step-by-step guides for daily operations
2. **Administrators**: System configuration and management
3. **Developers**: API documentation and integration guides
4. **Implementation Partners**: Deployment and customization
5. **Business Owners**: Strategic insights and ROI analysis

## Quick Start

### Prerequisites

- Hugo Extended v0.110.0 or later
- Node.js v16 or later
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/aimatrix/amx-docs.git
cd amx-docs

# Initialize submodules (Docsy theme)
git submodule update --init --recursive

# Install Node dependencies
npm install

# Start local development server
hugo server --buildDrafts
```

The site will be available at http://localhost:1313

### Building for Production

```bash
# Build the site
npm run build

# Output will be in the 'public' directory
# Deploy the 'public' directory to your web server
```

## Contributing

We welcome contributions to improve our documentation!

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b improve-inventory-docs`)
3. Make your changes
4. Test locally (`hugo server`)
5. Commit your changes (`git commit -am 'Improve inventory documentation'`)
6. Push to the branch (`git push origin improve-inventory-docs`)
7. Create a Pull Request

### Content Guidelines

- Write in clear, simple English
- Use active voice
- Include practical examples
- Add screenshots where helpful
- Follow the existing structure
- Test all code examples
- Optimize for LLM consumption

### Translation Guidelines

- Primary content is written in English
- Translations should maintain technical accuracy
- Preserve all code examples as-is
- Adapt cultural references appropriately
- Maintain consistent terminology

## Documentation Philosophy

### LLM Optimization

Our documentation is specifically optimized for Large Language Model consumption:

- **Structured Metadata**: Clear frontmatter with categories and tags
- **Semantic HTML**: Proper heading hierarchy and semantic markup
- **Rich Examples**: Comprehensive code samples and use cases
- **Cross-references**: Extensive linking between related topics
- **Consistent Formatting**: Predictable structure for parsing
- **RAG-Ready**: Chunked content suitable for retrieval
- **GraphRAG Compatible**: Clear entity relationships

### Comparison with Competitors

| Feature | AIMatrix | Odoo | SAP | QuickBooks |
|---------|-----------|------|-----|------------|
| Architecture | Microservices | Monolithic | Hybrid | Cloud-only |
| Language | Go | Python | ABAP/Java | Proprietary |
| Customization | Applets | Code mods | Modules | Limited |
| Upgrade Path | Seamless | Complex | Expensive | Automatic |
| API Coverage | 100% | Partial | Limited | Basic |
| Open Source | Partial | Yes | No | No |

## Directory Structure

```
.
├── archetypes/          # Hugo archetypes
├── assets/              # SCSS and other assets
├── build/               # Build artifacts (git-ignored)
├── content/             # Documentation content
├── data/                # Data files for Hugo
├── layouts/             # Custom layouts
├── static/              # Static files (images, etc.)
├── themes/              # Hugo themes (Docsy)
├── tmp/                 # Temporary files (git-ignored)
├── hugo.toml            # Hugo configuration
├── package.json         # Node.js dependencies
└── README.md            # This file
```

## Technology Stack

- **Static Site Generator**: Hugo (Go-based)
- **Theme**: Google Docsy
- **Search**: Lunr.js (client-side)
- **Analytics**: Google Analytics (optional)
- **Version Control**: Git
- **CI/CD**: GitHub Actions
- **Hosting**: Netlify/Vercel/AWS S3

## Deployment

### Automated Deployment

The documentation automatically deploys on:
- Push to `main` branch (production)
- Pull request (preview deployment)

### Manual Deployment

```bash
# Build the site
hugo --minify

# Deploy to S3
aws s3 sync public/ s3://docs.aimatrix.com --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id ABCD1234 --paths "/*"
```

## Versioning

Documentation versions are maintained in branches:
- `main`: Current version (v1.0)
- `v0.9`: Previous stable version
- `develop`: Next version (v1.1)

## License

This documentation is licensed under the Apache License 2.0. See [LICENSE](LICENSE) file for details.

## Support

- **Documentation Issues**: [GitHub Issues](https://github.com/aimatrix/amx-docs/issues)
- **Community Forum**: [forum.aimatrix.com](https://forum.aimatrix.com)
- **Email**: docs@aimatrix.com
- **Slack**: [AIMatrix Community](https://aimatrix.slack.com)

## Roadmap

### Q1 2024
- [ ] Add interactive API explorer
- [ ] Implement versioned API docs
- [ ] Add more video tutorials
- [ ] Enhance search functionality

### Q2 2024
- [ ] Add more languages (Spanish, French, German)
- [ ] Implement AI-powered documentation assistant
- [ ] Create industry-specific guides
- [ ] Add certification programs

### Q3 2024
- [ ] GraphQL playground integration
- [ ] Advanced code examples repository
- [ ] Community contributions portal
- [ ] Documentation feedback system

## Acknowledgments

- Hugo Static Site Generator
- Google Docsy Theme
- Our amazing community contributors
- Open source projects that inspire us

---

**AIMatrix Documentation** - Empowering businesses with comprehensive, accessible knowledge.
