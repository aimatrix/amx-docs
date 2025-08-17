---
title: AIMatrix Products
description: Three powerful products that work together to deliver complete AI transformation
weight: 2
---

# The AIMatrix Product Suite

Three integrated products that create a complete AI ecosystem for businesses, developers, and end users.

## Product Overview

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 40px 0;">

  <div style="border: 2px solid #00ff00; padding: 30px; border-radius: 10px;">
    <h2>🖥️ AIMatrix CLI</h2>
    <p><strong>For Developers & Power Users</strong></p>
    <p>Command-line tool for building, testing, and deploying AI agents locally</p>
    <ul>
      <li>Workspace management</li>
      <li>Local agent development</li>
      <li>P2P compute sharing</li>
      <li>Credential management</li>
    </ul>
    <a href="#aimatrix-cli" style="color: #00ff00;">Learn More →</a>
  </div>

  <div style="border: 2px solid #00ff00; padding: 30px; border-radius: 10px;">
    <h2>☁️ Studio.AIMatrix.com</h2>
    <p><strong>For Teams & Organizations</strong></p>
    <p>Cloud platform for collaboration, deployment, and management</p>
    <ul>
      <li>GitHub for AI projects</li>
      <li>Knowledge capsules</li>
      <li>Cloud runtime</li>
      <li>Team collaboration</li>
    </ul>
    <a href="#studio-aimatrix" style="color: #00ff00;">Learn More →</a>
  </div>

  <div style="border: 2px solid #00ff00; padding: 30px; border-radius: 10px;">
    <h2>💬 AIMatrix Console</h2>
    <p><strong>For End Users</strong></p>
    <p>Beautiful chat interface for AI interaction on all platforms</p>
    <ul>
      <li>Unified chat UI</li>
      <li>iOS, Android, Desktop, Web</li>
      <li>Voice & vision in chat</li>
      <li>Compose Multiplatform</li>
    </ul>
    <a href="#aimatrix-console" style="color: #00ff00;">Learn More →</a>
  </div>

</div>

---

## AIMatrix CLI

### The Developer's AI Workspace

Think of AIMatrix CLI as **git meets npm meets docker** for AI development. It's your local command center for building, testing, and deploying intelligent agents.

### Core Concepts

#### 🏗️ Workspace Management
Just like git manages source code, AIMatrix CLI manages AI projects:
```bash
# Initialize a new AI workspace
aimatrix init my-ai-project

# Clone from Studio
aimatrix clone studio://company/sales-agent

# Check workspace status
aimatrix status
```

#### 🤖 Agent Orchestration
Run a master agent that coordinates multiple AI services:
```bash
# Start the master agent (like 'ng serve' for Angular)
aimatrix serve

# The master agent then manages:
# - Claude CLI instances
# - Gemini agents
# - OpenAI Codex
# - AutoGen frameworks
# - Custom agents
```

#### 🔑 Credential Management
Securely manage API keys and credentials:
```bash
# Add credentials
aimatrix auth add openai
aimatrix auth add anthropic
aimatrix auth add bigledger

# Credentials are encrypted and isolated per workspace
```

#### 💰 P2P Compute Network
Share your computing resources and earn credits:
```bash
# Join the compute network
aimatrix compute join

# Set resource limits
aimatrix compute config --cpu=4 --memory=8GB --gpu=1

# Monitor earnings
aimatrix compute earnings
```

### Key Features

#### Development Environment
- **Local Testing**: Test agents without cloud costs
- **Hot Reload**: Changes reflect immediately
- **Debug Mode**: Step through agent execution
- **Performance Profiling**: Optimize token usage

#### Agent Management
```bash
# Create new agent
aimatrix agent create expense-processor

# Test agent locally
aimatrix agent test --input="process this receipt" --image=receipt.jpg

# Deploy to Studio
aimatrix agent deploy --env=production
```

#### Integration Tools
```bash
# Generate MCP server
aimatrix mcp init --api=rest --url=https://api.company.com

# Connect to BigLedger
aimatrix connect bigledger --instance=https://erp.company.com

# Add data sources
aimatrix data add --type=gdrive --path=/company-docs
```

### Installation

```bash
# NPM (Node.js)
npm install -g @aimatrix/cli

# Homebrew (macOS)
brew install aimatrix-cli

# Direct download
curl -L https://get.aimatrix.com | bash
```

### Example Workflow

```bash
# 1. Create workspace
aimatrix init sales-automation
cd sales-automation

# 2. Add agents
aimatrix agent add voice-order-taker
aimatrix agent add inventory-checker
aimatrix agent add order-processor

# 3. Configure connections
aimatrix connect bigledger
aimatrix auth add openai

# 4. Start development server
aimatrix serve

# 5. Test locally
aimatrix test scenarios/new-order.yaml

# 6. Deploy to Studio
aimatrix deploy --studio=company/sales-automation
```

---

## Studio.AIMatrix.com

### The GitHub for AI Projects

Studio is where AI projects live, collaborate, and scale. It's your cloud platform for managing, sharing, and deploying AI agents at enterprise scale.

### Core Capabilities

#### 📦 Knowledge Capsules
Like GitHub Apps, but for AI knowledge:
- **Install & Share**: One-click knowledge installation
- **Version Control**: Track knowledge evolution
- **Private/Public**: Control knowledge visibility
- **Marketplace**: Discover pre-built capabilities

#### 🏃 Runtime Environments
Like GitHub Codespaces, but for AI:
- **Cloud Workspaces**: Full AIMatrix environment in browser
- **Instant Deployment**: Zero-config agent deployment
- **Auto-scaling**: Handle any workload
- **Multi-cloud**: Deploy to AWS, Google Cloud, Azure, Alibaba

#### 🔄 GitHub Integration
Seamless connection with your development workflow:
```yaml
# .github/aimatrix.yml
on:
  issues:
    types: [opened]
jobs:
  process:
    runs-on: aimatrix
    steps:
      - uses: aimatrix/analyze-issue
      - uses: aimatrix/suggest-solution
      - uses: aimatrix/create-pr
```

### Platform Features

#### Project Management
- **Workspaces**: Organize agents, knowledge, and configurations
- **Teams**: Collaborate with role-based permissions
- **Versioning**: Track all changes with rollback capability
- **Branching**: Test changes before production

#### Knowledge Management
- **RAG Pipelines**: Automated document processing
- **Vector Stores**: Managed vector databases
- **Knowledge Graphs**: Visual relationship mapping
- **Fine-tuning**: Custom model training

#### Deployment Options
```yaml
# studio.aimatrix.yaml
deployment:
  provider: aws
  region: us-east-1
  scaling:
    min: 2
    max: 100
  model_config:
    primary: gpt-4
    fallback: claude-3
```

#### Monitoring & Analytics
- **Real-time Dashboard**: Track agent performance
- **Cost Analytics**: Monitor and optimize spending
- **Usage Metrics**: Understand user patterns
- **Error Tracking**: Automated issue detection

### Collaboration Features

#### Team Workspaces
- Shared agent development
- Knowledge base collaboration
- Credential management
- Audit logging

#### Knowledge Marketplace
- Browse thousands of capsules
- Industry-specific solutions
- Certified integrations
- Community contributions

### Pricing Tiers

#### Free Tier
- 3 workspaces
- 10,000 API calls/month
- Community support
- Public repositories only

#### Pro ($49/month)
- Unlimited workspaces
- 100,000 API calls/month
- Private repositories
- Priority support

#### Enterprise (Custom)
- Dedicated infrastructure
- Unlimited everything
- SLA guarantees
- White-label options

---

## AIMatrix Console

### AI for Everyone, Everywhere

The AIMatrix Console is the beautiful, intuitive chat interface that makes AI accessible to everyone. Built with Compose Multiplatform, it provides a consistent experience across all devices - no technical knowledge required.

### One Codebase, Every Platform

Using **Compose Multiplatform**, we deliver native performance everywhere:

#### 📱 Mobile Apps
**iOS & Android (Native Performance)**
- Unified chat interface
- Voice-first interaction
- Camera integration for visual AI
- Push notifications
- Offline capabilities

#### 💻 Desktop Applications
**Windows, macOS, Linux (Native Desktop)**
- Same familiar chat interface
- Screen capture & automation
- Keyboard shortcuts
- System tray integration
- Multi-window support

#### 🌐 Web Console
**Browser-based Access (Compose for Web)**
- No installation required
- Same UI/UX as native apps
- Real-time sync
- Progressive web app
- Works on any device

### The Chat-First Experience

#### Unified Interface Design
The Console is fundamentally a **chat interface** that works the same everywhere:
- Clean, modern chat UI inspired by messaging apps
- Consistent experience across all platforms
- Rich message types (text, images, voice, files)
- Real-time streaming responses
- Conversation history and context

#### Natural Interaction
```
User: "Process yesterday's receipts"
AI: "I found 12 receipts from yesterday. Processing now..."
AI: "Complete. 10 expenses created, 2 need your review."
User: "Show me the ones that need review"
```

#### Multi-Modal Chat
Beyond text, the chat interface supports:
- **📸 Image Messages**: Drag & drop or capture photos
- **🎤 Voice Messages**: Talk instead of type
- **📎 File Attachments**: Documents, spreadsheets, PDFs
- **📊 Rich Responses**: Charts, tables, interactive elements
- **🔗 Deep Links**: Click to navigate to specific functions

### Business Features

#### For Retail Staff
- Voice-controlled POS
- Visual inventory counts
- Customer service assistant
- Price checking

#### For Field Workers
- Photo-based reporting
- Voice notes to tasks
- Offline sync
- GPS integration

#### For Office Workers
- Email assistant
- Meeting transcription
- Document processing
- Calendar management

#### For Executives
- Voice-driven analytics
- Natural language reports
- Real-time alerts
- Decision support

### Consumer Features

#### Personal Assistant
- Expense tracking
- Shopping assistance
- Travel planning
- Health monitoring

#### Home Integration
- Smart home control
- Family organization
- Recipe assistance
- Entertainment

### Security & Privacy

#### Data Protection
- End-to-end encryption
- Biometric authentication
- Local processing option
- GDPR compliant

#### User Control
- Data deletion rights
- Processing transparency
- Opt-in features
- Privacy dashboard

### Technical Architecture

#### Compose Multiplatform
The Console shares its codebase with AIMatrix CLI, using **Kotlin Multiplatform** and **Compose Multiplatform**:
- **Shared Business Logic**: One codebase for all platforms
- **Native Performance**: Compiles to native code
- **Platform-Specific Features**: Access native APIs when needed
- **Consistent UI/UX**: Same components everywhere

#### Relationship with CLI
```
AIMatrix Repository
├── cli/                 # Command-line interface
├── console/            # GUI/Chat interface (Compose)
├── shared/             # Shared business logic
└── platform/           # Platform-specific code
```

While technically part of the same codebase:
- **CLI**: For developers and automation
- **Console**: For end users and chat interaction
- Both can be installed independently
- Share core agent runtime and capabilities

### Getting Started

#### For End Users (Console)
```
# Mobile
iOS: App Store → "AIMatrix Console"
Android: Play Store → "AIMatrix Console"

# Desktop
macOS/Windows/Linux: Download from aimatrix.com/console
```

#### For Developers (CLI + Console)
```bash
# Install complete AIMatrix suite
npm install -g @aimatrix/cli

# This includes:
# - CLI tools for development
# - Console GUI application
# - Local agent runtime
# - P2P compute capabilities
```

---

## How They Work Together

### The Complete Ecosystem

```
┌─────────────────────────────────────────────────┐
│            AIMatrix Console                     │
│         (Chat Interface - GUI)                  │
│    Compose Multiplatform Application            │
│   iOS | Android | Desktop | Web                 │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│         Studio.AIMatrix.com                     │
│         (Cloud Platform)                        │
│   Knowledge Store | Runtime | Collaboration     │
└────────────────┬────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────┐
│            AIMatrix CLI                         │
│      (Developer Tools & Runtime)                │
│   Command Line | Agent Runtime | P2P Network    │
│                                                 │
│  Note: CLI and Console share same codebase     │
│  using Compose Multiplatform                   │
└─────────────────────────────────────────────────┘
```

### Technical & Marketing Perspective

#### From Technical View (Single Codebase)
```
AIMatrix (Compose Multiplatform)
├── CLI Module (Terminal Interface)
├── Console Module (Chat GUI)
├── Shared Core (Agent Runtime)
└── Platform Adapters (iOS/Android/Desktop/Web)
```

#### From Marketing View (Three Products)
1. **CLI** → Developers love command-line tools
2. **Console** → End users want beautiful apps
3. **Studio** → Teams need cloud collaboration

### Typical Workflow

1. **Developer** uses CLI to build agent locally
2. **Developer** tests with Console GUI locally
3. **Developer** deploys to Studio for team access
4. **Team** collaborates on Studio to refine
5. **Organization** deploys to production via Studio
6. **End Users** interact through Console apps
7. **P2P Network** (via CLI) provides distributed compute

### Integration Example

```bash
# Developer creates agent locally
aimatrix init customer-service
aimatrix agent create chat-handler

# Deploy to Studio
aimatrix deploy --studio=company/customer-service

# Studio automatically:
# - Versions the agent
# - Runs tests
# - Deploys to production
# - Makes available to Console apps

# End users immediately see:
# "New capability available: Improved customer service"
```

---

## Start Your Journey

<div style="display: flex; gap: 20px; margin: 40px 0; flex-wrap: wrap; justify-content: center;">
  <a href="/docs/cli/quickstart" style="padding: 15px 30px; background: #00ff00; color: #000; text-decoration: none; border-radius: 8px; font-weight: bold;">
    Install CLI →
  </a>
  <a href="https://studio.aimatrix.com/signup" style="padding: 15px 30px; background: #00ff00; color: #000; text-decoration: none; border-radius: 8px; font-weight: bold;">
    Try Studio →
  </a>
  <a href="/downloads" style="padding: 15px 30px; background: #00ff00; color: #000; text-decoration: none; border-radius: 8px; font-weight: bold;">
    Get Console →
  </a>
</div>

---

*AIMatrix - Complete AI Platform for Business Transformation*