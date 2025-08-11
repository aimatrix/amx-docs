+++
title = "Getting Started"
weight = 10
+++

# Getting Started with BigLedger

Welcome to BigLedger! This guide will help you understand what BigLedger is, how it works, and how to get your first instance up and running.

## What is BigLedger?

BigLedger is a comprehensive Business Operating System (BOS) that reimagines enterprise resource planning for the modern digital age. Built from the ground up with cloud-native principles, BigLedger provides:

- **Unified Platform**: All business operations in one integrated system
- **Modular Architecture**: Use only what you need, scale as you grow
- **Real-time Processing**: Instant insights and operations
- **Global Ready**: Multi-language, multi-currency, multi-tax support
- **API-First**: Everything accessible programmatically
- **Applet Ecosystem**: Extend with third-party solutions

## Core Concepts

### Business Operating System (BOS)

Unlike traditional ERP systems that focus on resource planning, BigLedger functions as a complete operating system for your business:

1. **Core Kernel**: Essential business functions (GL, AR, AP)
2. **Module Layer**: Specialized business modules (POS, WMS, CRM)
3. **Applet Layer**: Custom and third-party extensions
4. **API Layer**: Integration and automation capabilities
5. **UI Layer**: Web, mobile, and terminal interfaces

### Data Hub Architecture

BigLedger acts as a central data hub for your entire business ecosystem:

```
┌─────────────────────────────────────────┐
│          BigLedger Data Hub             │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────┐  │
│  │   POS    │  │   ERP    │  │ CRM  │  │
│  └──────────┘  └──────────┘  └──────┘  │
│  ┌──────────┐  ┌──────────┐  ┌──────┐  │
│  │   WMS    │  │ E-Comm   │  │ B2B  │  │
│  └──────────┘  └──────────┘  └──────┘  │
├─────────────────────────────────────────┤
│         Unified Data Model              │
├─────────────────────────────────────────┤
│      Analytics & Intelligence           │
└─────────────────────────────────────────┘
```

### Multi-Tenant Architecture

BigLedger supports true multi-tenancy:
- **Isolation**: Complete data separation between tenants
- **Customization**: Per-tenant configurations and applets
- **Scalability**: Automatic resource allocation
- **Security**: Bank-grade encryption and compliance

## Quick Start Guide

### Prerequisites

Before installing BigLedger, ensure you have:

1. **Hardware Requirements**:
   - Minimum: 4 CPU cores, 8GB RAM, 50GB SSD
   - Recommended: 8 CPU cores, 16GB RAM, 200GB SSD
   - Production: 16+ CPU cores, 32GB+ RAM, 500GB+ SSD

2. **Software Requirements**:
   - Operating System: Linux (Ubuntu 20.04+, RHEL 8+), macOS 11+, Windows Server 2019+
   - Container Runtime: Docker 20.10+ or Kubernetes 1.21+
   - Database: PostgreSQL 13+ or MySQL 8.0+
   - Cache: Redis 6.0+

3. **Network Requirements**:
   - Stable internet connection
   - Open ports: 80 (HTTP), 443 (HTTPS), 5432 (PostgreSQL), 6379 (Redis)

### Installation Methods

#### 1. Docker Compose (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/bigledger/bigledger.git
cd bigledger

# Copy environment template
cp .env.example .env

# Edit configuration
nano .env

# Start services
docker-compose up -d

# Check status
docker-compose ps

# Access BigLedger at http://localhost:8080
```

#### 2. Kubernetes (Recommended for Production)

```bash
# Add BigLedger Helm repository
helm repo add bigledger https://charts.bigledger.com
helm repo update

# Install BigLedger
helm install bigledger bigledger/bigledger \
  --namespace bigledger \
  --create-namespace \
  --values values.yaml

# Check deployment
kubectl get pods -n bigledger

# Get access URL
kubectl get ingress -n bigledger
```

#### 3. Cloud Marketplace

BigLedger is available on major cloud platforms:
- **AWS Marketplace**: One-click deployment on AWS
- **Azure Marketplace**: Deploy on Azure
- **Google Cloud Marketplace**: GCP deployment
- **DigitalOcean Marketplace**: Simple cloud deployment

### Initial Configuration

#### Step 1: Access Admin Panel

Navigate to `https://your-domain/admin` and log in with default credentials:
- Username: `admin`
- Password: `changeme`

**Important**: Change the default password immediately!

#### Step 2: Company Setup

1. Navigate to **Settings → Company**
2. Enter your company information:
   - Company Name
   - Tax ID
   - Address
   - Contact Information
3. Configure regional settings:
   - Currency
   - Time Zone
   - Language
   - Tax Configuration

#### Step 3: User Management

1. Go to **Settings → Users**
2. Create user accounts for your team
3. Assign roles and permissions:
   - **Admin**: Full system access
   - **Manager**: Module-level management
   - **User**: Operational access
   - **Viewer**: Read-only access

#### Step 4: Module Activation

1. Navigate to **Modules**
2. Activate the modules you need:
   - Start with core modules (GL, AR, AP)
   - Add operational modules (POS, Inventory)
   - Enable specialized modules as needed

#### Step 5: Data Import

1. Go to **Settings → Import**
2. Download import templates
3. Prepare your data in CSV format
4. Import in this order:
   - Chart of Accounts
   - Customers
   - Vendors
   - Products
   - Opening Balances

## First Steps

### Create Your First Invoice

1. Navigate to **Sales → Invoices**
2. Click **New Invoice**
3. Select or create a customer
4. Add line items
5. Review and save
6. Send to customer

### Process Your First Payment

1. Go to **Finance → Payments**
2. Click **Receive Payment**
3. Select customer and invoice
4. Enter payment details
5. Process and reconcile

### Generate Your First Report

1. Navigate to **Reports**
2. Select report type (P&L, Balance Sheet, etc.)
3. Set date range
4. Generate and export

## Learning Resources

### Documentation

- [User Guides](/docs/user-guides/): Role-specific tutorials
- [Module Documentation](/docs/modules/): Detailed module guides
- [API Reference](/api/): Developer documentation
- [Video Tutorials](/tutorials/): Step-by-step video guides

### Training

- **BigLedger Academy**: Online training courses
- **Webinars**: Weekly feature demonstrations
- **Certification**: Professional certification programs
- **Partner Training**: Implementation partner resources

### Support

- **Community Forum**: https://forum.bigledger.com
- **Knowledge Base**: https://kb.bigledger.com
- **Support Portal**: https://support.bigledger.com
- **Emergency Support**: +1-800-BIGLEDGER

## Next Steps

Now that you have BigLedger running:

1. 📚 **Explore Modules**: Learn about available [modules](/docs/modules/)
2. 🎓 **Take Training**: Enroll in [BigLedger Academy](https://academy.bigledger.com)
3. 🔧 **Configure System**: Fine-tune [system settings](/docs/administration/)
4. 🚀 **Deploy Applets**: Browse the [Applet Store](https://appstore.bigledger.com)
5. 🤝 **Join Community**: Connect with other users in our [forum](https://forum.bigledger.com)

## Frequently Asked Questions

### Q: How is BigLedger different from other ERP systems?

BigLedger is built on modern cloud-native architecture with:
- Stateless microservices (vs monolithic architecture)
- Go programming language (vs Python/Java)
- API-first design (vs UI-first)
- Continuous updates (vs version lock-in)
- Applet ecosystem (vs custom code modifications)

### Q: Can I migrate from my existing ERP?

Yes! BigLedger provides migration tools for:
- QuickBooks
- Xero
- Odoo
- SAP Business One
- Microsoft Dynamics
- Custom systems (via API/CSV)

### Q: What about data security?

BigLedger implements enterprise-grade security:
- End-to-end encryption
- Role-based access control
- Audit trails
- GDPR/CCPA compliance
- SOC 2 Type II certified
- ISO 27001 compliant

### Q: How does pricing work?

BigLedger offers flexible pricing:
- **SaaS**: Monthly/annual subscriptions
- **On-Premise**: Perpetual license
- **Private Cloud**: Dedicated instances
- **Usage-Based**: Pay for what you use

Contact sales for detailed pricing: sales@bigledger.com

---

*Ready to transform your business? Let's get started with BigLedger!*