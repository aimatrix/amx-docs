# AIMatrix Documentation

This repository contains the source code for the AIMatrix documentation website, built with Hugo and automatically deployed to AWS S3.

## 🚀 Quick Start

### Prerequisites
- Hugo Extended (latest version)
- Node.js 18+ (optional, for additional processing)
- Git

### Local Development

1. Clone the repository:
```bash
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

# Deploy to S3 (requires AWS CLI configured)
aws s3 sync public/ s3://docs.aimatrix.com/ --delete
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

- 📖 [Hugo Documentation](https://gohugo.io/documentation/)
- 🎨 [Relearn Theme Docs](https://mcshelby.github.io/hugo-theme-relearn/)
- 💬 [GitHub Issues](https://github.com/aimatrix/amx-docs/issues)

---

Built with ❤️ using [Hugo](https://gohugo.io/) and the [Relearn](https://github.com/McShelby/hugo-theme-relearn) theme.