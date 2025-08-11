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

## 🚀 Quick Start

### Prerequisites
- Hugo Extended (latest version)
- Node.js 18+ (optional, for additional processing)
- Git

### Local Development

1. Clone the repository:
```bash
# Clone the repository
git clone https://github.com/aimatrix/amx-docs.git
cd amx-docs
```

2. Install dependencies (if using npm packages):
```bash
npm install
```

3. Start the Hugo development server:
```bash
hugo server -D
```

4. Visit `http://localhost:1313` to view the site.

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

## 📁 Project Structure

```
.
├── .github/workflows/     # GitHub Actions for CI/CD
├── content/              # Documentation content
│   ├── en/              # English content
│   ├── zh/              # Chinese content
│   ├── ar/              # Arabic content
│   ├── ms/              # Malay content
│   ├── id/              # Indonesian content
│   └── ru/              # Russian content
├── themes/relearn/       # Hugo Relearn theme
├── hugo.toml            # Hugo configuration
└── package.json         # Node.js dependencies (if any)
```

## 🌐 Multi-Language Support

The documentation supports 6 languages:
- 🇬🇧 English (`/en/`)
- 🇨🇳 Chinese (`/zh/`)
- 🇸🇦 Arabic (`/ar/`)
- 🇲🇾 Malay (`/ms/`)
- 🇮🇩 Indonesian (`/id/`)
- 🇷🇺 Russian (`/ru/`)

Each language has its own content directory and can be edited independently.

## 🔧 Configuration

### Hugo Configuration
The main configuration is in `hugo.toml`. Key settings include:
- Base URL: `https://docs.aimatrix.com/`
- Theme: Relearn
- Multi-language support
- Edit URLs pointing to this GitHub repository

### GitHub Actions Deployment

The repository includes two GitHub Actions workflows:

#### Simple Deployment (`deploy.yml`)
- Builds Hugo site
- Deploys to S3
- Basic caching strategy

#### Advanced Deployment (`deploy-advanced.yml`)
- Optimized caching for different file types
- CORS configuration
- Website configuration
- Deployment verification
- Better error handling

Both workflows are triggered on push to the `main` branch.

### Required Secrets

The following secrets must be configured in the GitHub repository settings:

- `AWS_ACCESS_KEY_ID_S3_DOCS_AIMATRIX_COM` - AWS access key
- `AWS_SECRET_ACCESS_KEY_S3_DOCS_AIMATRIX_COM` - AWS secret key
- `AWS_REGION_S3_DOCS_AIMATRIX_COM` - AWS region (e.g., `ap-southeast-5`)

The S3 bucket name is hardcoded as `docs.aimatrix.com`.

## ✍️ Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `hugo server`
5. Commit and push your changes
6. Create a pull request

### Content Guidelines

- Use clear, concise language
- Include code examples where appropriate
- Follow the existing structure and formatting
- Test all links and references
- Add content to appropriate language directories

## 📦 Deployment

### Automatic Deployment
- Push to `main` branch triggers automatic deployment
- GitHub Actions builds and deploys to S3
- Site is available at https://docs.aimatrix.com

### Manual Deployment
```bash
# Build the site
hugo --minify --environment production

# Deploy to S3
aws s3 sync public/ s3://docs.aimatrix.com --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id ABCD1234 --paths "/*"
```

## 🔍 Troubleshooting

### Build Issues
- Ensure Hugo Extended is installed
- Check for syntax errors in Markdown files
- Verify all internal links are correct

### Deployment Issues
- Check AWS credentials in GitHub secrets
- Verify S3 bucket exists and is accessible
- Check GitHub Actions logs for specific errors

## 📞 Support

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
