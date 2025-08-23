---
title: AIMatrix Products
description: Complete AI platform with CLI tools, console applications, simulation engine, and collaboration hub
weight: 2
---

# The AIMatrix Product Suite

Four integrated products that create a complete AI ecosystem for businesses, developers, and end users.

## Product Overview

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin: 40px 0;">

  <div style="border: 2px solid #00ff00; padding: 30px; border-radius: 10px;">
    <h2>🖥️ AIMatrix CLI</h2>
    <p><strong>Free Developer Tools</strong></p>
    <p>Command-line application for setting up and managing AIMatrix environments</p>
    <ul>
      <li>Local environment setup</li>
      <li>Desktop app launcher</li>
      <li>Engine installation & updates</li>
      <li>User account management</li>
      <li>Built with Kotlin + Clikt</li>
    </ul>
    <a href="#aimatrix-cli" style="color: #00ff00;">Learn More →</a>
  </div>

  <div style="border: 2px solid #00ff00; padding: 30px; border-radius: 10px;">
    <h2>💬 AMX Console</h2>
    <p><strong>Universal User Interface</strong></p>
    <p>Native apps for all platforms with conversational and graphical UI</p>
    <ul>
      <li>iOS, Android, Windows, Mac, Linux</li>
      <li>Conversational + graphical UI</li>
      <li>Todo lists & conversations</li>
      <li>Multi-channel agent monitoring</li>
      <li>Compose Multiplatform</li>
    </ul>
    <a href="#amx-console" style="color: #00ff00;">Learn More →</a>
  </div>

  <div style="border: 2px solid #00ff00; padding: 30px; border-radius: 10px;">
    <h2>⚙️ AMX Engine</h2>
    <p><strong>AI & Simulation Core</strong></p>
    <p>The digital twin factory and agent orchestration engine</p>
    <ul>
      <li>Digital twin simulations</li>
      <li>Agent design & workflows</li>
      <li>MCP & A2A servers</li>
      <li>Kalasim simulation engine</li>
      <li>Built with Ktor</li>
    </ul>
    <a href="#amx-engine" style="color: #00ff00;">Learn More →</a>
  </div>

  <div style="border: 2px solid #00ff00; padding: 30px; border-radius: 10px;">
    <h2>🌐 AMX Hub</h2>
    <p><strong>Collaboration Platform</strong></p>
    <p>GitHub-like platform for hosting workspaces and orchestrating engines</p>
    <ul>
      <li>Workspace hosting</li>
      <li>Webhook integrations</li>
      <li>Engine orchestration</li>
      <li>License & subscriptions</li>
      <li>Spring Cloud + Angular</li>
    </ul>
    <a href="#amx-hub" style="color: #00ff00;">Learn More →</a>
  </div>

</div>

---

## AIMatrix CLI

### Free Command-Line Tools for Everyone

AIMatrix CLI is your starting point - a free command-line application that anyone can download and use. Think of it as the Swiss Army knife for AIMatrix, similar to how `git` manages repositories or `ng` manages Angular projects.

### Core Functions

#### 🏗️ Environment Management
```bash
# Initialize AIMatrix in your project
aimatrix init

# Set up your local development environment
aimatrix setup

# Check system status
aimatrix status
```

#### 🚀 Application Launcher
```bash
# Launch the desktop version of AMX Console
aimatrix console

# Start the local AMX Engine
aimatrix engine start

# Run in development mode
aimatrix dev
```

#### ⚙️ Engine Management
```bash
# Install AMX Engine locally
aimatrix engine install

# Update to latest version
aimatrix engine update

# Configure engine settings
aimatrix engine config
```

#### 👤 Account Management
```bash
# Register new account
aimatrix auth register

# Sign in to your account
aimatrix auth login

# Connect to AMX Hub
aimatrix hub connect
```

### Technical Architecture
- **Language**: Kotlin
- **Framework**: Clikt (Command Line Interface for Kotlin)
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Distribution**: Free download from aimatrix.com

### Why Free CLI?
- Lower barrier to entry for developers
- Community-driven adoption
- Local development without cloud costs
- Foundation for desktop applications

---

## AMX Console

### The Universal Interface for Everyone

AMX Console is the user-facing application that employees, customers, and suppliers use to interact with AIMatrix. It combines conversational UI with traditional graphical interfaces, available natively on every platform.

### Key Features

#### 💬 Hybrid Interface
**Conversational UI**: Chat naturally with AI agents
**Graphical UI**: Traditional interface for structured tasks
**Seamless Integration**: Switch between modes effortlessly

#### 📱 True Multi-Platform
Using **Compose Multiplatform**, one codebase delivers:
- **Mobile**: Native iOS and Android apps
- **Desktop**: Native Windows, macOS, Linux applications
- **Performance**: True native performance, not web wrappers

#### 🎯 Core Capabilities

**Todo Management**:
- View and manage task lists
- AI-generated todos from conversations
- Priority and deadline tracking
- Team collaboration

**Conversation Hub**:
- All AI conversations in one place
- Multi-channel view (email, chat, voice)
- Context preservation across sessions
- Conversation history and search

**Agent Monitoring**:
- See AI agents responding to customers
- Monitor agent performance
- Override or intervene when needed
- Training feedback loop

**Multi-Channel Integration**:
- WhatsApp, Telegram, Email
- Voice calls and SMS
- Social media channels
- Custom integrations

### User Scenarios

#### For Employees
- Morning: Check AI-prioritized todo list
- Communicate: Natural language commands
- Monitor: Watch AI handle routine tasks
- Intervene: Take over complex situations

#### For Customers
- Support: 24/7 intelligent assistance
- Orders: Voice or text ordering
- Tracking: Real-time updates
- Feedback: Direct communication channel

#### For Suppliers
- Orders: Automated purchase orders
- Updates: Inventory level notifications
- Coordination: Delivery scheduling
- Payments: Invoice management

### Technical Stack
- **Framework**: Compose Multiplatform
- **Language**: Kotlin
- **Platforms**: iOS, Android, Windows, macOS, Linux
- **Architecture**: MVVM with reactive streams

---

## AMX Engine

### The Brain Behind Everything

AMX Engine is where the magic happens - it's the digital twin factory and agent orchestration platform that runs simulations, manages agents, and handles all the heavy lifting. Think of it as the engine room of a ship.

### Core Components

#### 🎮 Digital Twin Factory
**What It Does**: Creates virtual copies of your business
**How It Works**: 
- Models business processes
- Runs predictive simulations
- Tests scenarios risk-free
- Optimizes operations

**Powered By**: Kalasim simulation engine
- Discrete event simulation
- Process modeling
- What-if analysis
- Monte Carlo simulations

#### 🤖 Agent Orchestration
**Agent Design Studio**:
- Visual agent builder
- Behavior programming
- Skill assignment
- Performance tuning

**Workflow Specification**:
- Define agent interactions
- Set trigger conditions
- Configure automation rules
- Manage escalations

#### 🔌 Integration Servers

**MCP Servers** (Model Context Protocol):
- Universal translators for business systems
- Connect any ERP, CRM, database
- Real-time data synchronization
- Protocol translation

**A2A Servers** (Agent-to-Agent):
- Inter-agent communication
- Coordination protocols
- Knowledge sharing
- Collective intelligence

#### 🏃 Runtime Modes

**Cloud Deployment**:
- Fully managed service
- Auto-scaling capabilities
- High availability
- Global distribution

**On-Premise Installation**:
- Run on your servers
- Complete data control
- Compliance friendly
- Air-gapped options

**Background Daemon**:
- Runs as system service
- Always-on availability
- Resource efficient
- Auto-start on boot

### Deployment Options

#### For Development
```bash
# Install locally via CLI
aimatrix engine install

# Run in development mode
aimatrix engine dev

# Access at http://localhost:8080
```

#### For Production
- **Cloud**: Hosted on AMX Hub
- **Private Cloud**: Your AWS/Azure/GCP
- **On-Premise**: Your data center
- **Hybrid**: Mix of cloud and local

### Technical Architecture
- **Framework**: Ktor (Kotlin async web framework)
- **Simulation**: Kalasim engine
- **Database**: PostgreSQL with Supabase
- **Message Queue**: Kafka/RabbitMQ
- **Container**: Docker/Kubernetes ready

---

## AMX Hub

### Your GitHub for AI Workspaces

AMX Hub (hub.aimatrix.com) is the collaboration and orchestration platform where businesses host their AI workspaces, similar to how GitHub hosts code repositories. It's the central nervous system for the AIMatrix ecosystem.

### Core Functions

#### 📦 Workspace Hosting
**Like GitHub Repositories**:
- Host multiple workspaces
- Version control for configurations
- Branching and merging
- Collaboration tools

**Workspace Contains**:
- Agent definitions
- Workflow configurations
- Integration settings
- Simulation models

#### 🔗 Integration Gateway
**Webhook Reservoir**:
- Centralized webhook endpoints
- Third-party integrations (Telegram, WhatsApp)
- Event routing and processing
- Secure credential storage

**API Gateway**:
- Unified API endpoint
- Rate limiting and throttling
- Authentication and authorization
- Request routing

#### 🚀 Engine Orchestration
**Like GitHub Actions**:
- Spin up AMX Engines on-demand
- Run simulations in the cloud
- Execute batch processes
- Scheduled automation

**Compute Resources**:
- Elastic scaling
- Resource allocation
- Cost optimization
- Performance monitoring

#### 💼 Business Services

**User Management**:
- Registration and authentication
- Team and organization management
- Role-based access control
- SSO integration

**Subscription & Licensing**:
- Software license management
- Subscription billing
- Usage tracking
- Payment processing

**Backup & Recovery**:
- Automatic workspace backups
- Point-in-time recovery
- Disaster recovery
- Data redundancy

### Hub Features

#### For Individuals
- Free tier with basic workspace
- Community sharing
- Public templates
- Learning resources

#### For Teams
- Private workspaces
- Team collaboration
- Shared resources
- Activity tracking

#### For Enterprises
- Unlimited workspaces
- Dedicated resources
- SLA guarantees
- Priority support

### Technical Stack
- **Backend**: Spring Cloud Gateway (Reactive Kotlin)
- **Frontend**: Angular (only component using Angular)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Storage**: S3-compatible object storage

### Integration Ecosystem

**Supported Integrations**:
- Communication: Telegram, WhatsApp, Slack
- ERP: BigLedger, SAP, Oracle
- CRM: Salesforce, HubSpot
- Email: Gmail, Outlook
- Custom: Any REST API

---

## How Products Work Together

### The Complete Flow

```
1. Developer downloads AIMatrix CLI (free)
   ↓
2. CLI installs and configures AMX Engine locally
   ↓
3. Users download AMX Console on their devices
   ↓
4. Console connects to local or cloud Engine
   ↓
5. Workspaces are synced with AMX Hub
   ↓
6. Hub orchestrates cloud Engines as needed
```

### Typical Deployment Scenarios

#### Small Business (Local)
- AIMatrix CLI on owner's computer
- AMX Engine running locally
- AMX Console on employee phones
- Backup to AMX Hub (free tier)

#### Medium Business (Hybrid)
- AIMatrix CLI for development
- AMX Engine on company server
- AMX Console for all staff
- AMX Hub for cloud burst capacity

#### Enterprise (Full Cloud)
- AIMatrix CLI for developers
- AMX Engine cluster in cloud
- AMX Console company-wide
- AMX Hub for orchestration

### Product Synergy

**CLI + Engine**: CLI manages Engine lifecycle
**Console + Engine**: Console is the UI for Engine
**Engine + Hub**: Hub orchestrates multiple Engines
**Hub + CLI**: CLI deploys workspaces to Hub

---

## Pricing Strategy

### AIMatrix CLI
**Free Forever**
- Full functionality
- No limitations
- Community support
- Regular updates

### AMX Console
**Free for End Users**
- Employees: Free
- Customers: Free
- Suppliers: Free
- Premium features for businesses

### AMX Engine
**Flexible Licensing**
- Community: Free (limited resources)
- Professional: $99/month per instance
- Enterprise: Custom pricing
- On-premise: One-time license

### AMX Hub
**Usage-Based Pricing**
- Free: 1 workspace, 100 runs/month
- Starter: $29/month, 5 workspaces
- Business: $99/month, unlimited workspaces
- Enterprise: Custom pricing

---

## Getting Started

### For Developers
1. Download AIMatrix CLI
2. Run `aimatrix init`
3. Install local Engine
4. Start building

### For Businesses
1. Contact sales for demo
2. Pilot deployment
3. Train team on Console
4. Scale gradually

### For Enterprises
1. Architecture review
2. Security assessment
3. Pilot program
4. Full deployment

---

*AIMatrix - Four Products, One Vision: Complete Business Automation*