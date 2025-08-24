---
title: "AMX Engine - Technical Data Sheet"
description: "Comprehensive technical specifications for AMX Engine digital twin factory and agent orchestration platform"
weight: 3
---

## Executive Summary

AMX Engine is the core computational platform powering the AIMatrix ecosystem, serving as both a digital twin factory and agent orchestration engine. Built with Ktor framework and Kotlin, it processes data and executes workflows locally or in the cloud, reading knowledge artifacts from local workspace files. It provides discrete event simulation capabilities through the integrated Kalasim engine, comprehensive agent design and workflow management, and universal connectivity through MCP (Model Context Protocol) and A2A (Agent-to-Agent) servers.

## Technical Specifications

| Specification | Details |
|---------------|---------|
| **Product Name** | AMX Engine |
| **Version** | 3.0+ |
| **Framework** | Ktor (Kotlin Async Web Framework) |
| **Language** | Kotlin/JVM |
| **Simulation Engine** | Kalasim (Discrete Event Simulation) |
| **Database** | PostgreSQL with Supabase |
| **Message Queue** | Apache Kafka / RabbitMQ |
| **Container Support** | Docker, Kubernetes, Podman |
| **API Standards** | REST, GraphQL, WebSocket, gRPC |

### Performance Specifications
| Metric | Specification |
|--------|--------------|
| **Concurrent Agents** | 10,000+ agents per instance |
| **Simulation Events** | 1M+ events per second |
| **API Throughput** | 50,000+ requests per second |
| **Database Connections** | 1,000+ concurrent connections |
| **Memory Usage** | 2-16 GB (configurable) |
| **Response Time** | <100ms (99th percentile) |
| **Uptime SLA** | 99.9% availability |

## System Requirements

### Minimum Requirements
| Component | Specification |
|-----------|---------------|
| **Operating System** | Linux (Ubuntu 20.04+), Windows Server 2019+, macOS 11+ |
| **JVM** | OpenJDK 17+ or Oracle JDK 17+ |
| **CPU** | 2 cores, 2.4 GHz |
| **RAM** | 4 GB |
| **Storage** | 20 GB SSD |
| **Network** | 100 Mbps |
| **Database** | PostgreSQL 13+ |

### Recommended Production
| Component | Specification |
|-----------|---------------|
| **Operating System** | Linux (Ubuntu 22.04 LTS) |
| **JVM** | OpenJDK 21 LTS |
| **CPU** | 8+ cores, 3.2 GHz |
| **RAM** | 32 GB |
| **Storage** | 500 GB NVMe SSD |
| **Network** | 1 Gbps |
| **Database** | PostgreSQL 15+ with connection pooling |

### High-Availability Enterprise
| Component | Specification |
|-----------|---------------|
| **Load Balancer** | HAProxy, NGINX, or cloud load balancer |
| **Application Servers** | 3+ instances (active-active) |
| **Database** | PostgreSQL cluster (primary + 2 replicas) |
| **Cache Layer** | Redis Cluster (3+ nodes) |
| **Message Queue** | Kafka cluster (3+ brokers) |
| **Storage** | Distributed storage (Ceph, GlusterFS) |
| **Monitoring** | Prometheus + Grafana |

## Key Features & Capabilities

### Digital Twin Factory

#### Business Process Modeling
| Feature | Description |
|---------|-------------|
| **Process Designer** | Visual workflow editor with drag-drop interface |
| **Resource Modeling** | Equipment, personnel, and material resource definition |
| **Capacity Planning** | Bottleneck analysis and optimization |
| **Process Templates** | Industry-standard process libraries |
| **Custom Logic** | Kotlin DSL for complex business rules |
| **Real-Time Sync** | Live data integration from ERP/MES systems |

#### Simulation Capabilities
| Feature | Description |
|---------|-------------|
| **Discrete Event Simulation** | Time-based event processing with Kalasim |
| **Monte Carlo Analysis** | Statistical uncertainty modeling |
| **What-If Scenarios** | Parameter variation and sensitivity analysis |
| **Batch Processing** | Multiple simulation runs with parameter sweeps |
| **Historical Replay** | Past event recreation and analysis |
| **Predictive Modeling** | Future state forecasting |

### Agent Orchestration Platform

#### Agent Design Studio
| Component | Capabilities |
|-----------|-------------|
| **Visual Designer** | Drag-and-drop agent behavior composition |
| **Skill Library** | Pre-built agent capabilities and templates |
| **Training Pipeline** | Machine learning model training and deployment |
| **Behavior Trees** | Hierarchical decision-making structures |
| **State Machines** | Complex agent state management |
| **Performance Tuning** | A/B testing and optimization tools |

#### Workflow Specification Engine
| Feature | Description |
|---------|-------------|
| **BPMN 2.0 Support** | Standard workflow notation compatibility |
| **Event-Driven Architecture** | Reactive workflow triggers |
| **Conditional Logic** | Complex branching and routing rules |
| **Human-in-the-Loop** | Manual approval and intervention points |
| **SLA Management** | Service level agreement enforcement |
| **Escalation Policies** | Automated escalation and fallback procedures |

### Integration Architecture

#### MCP Servers (Model Context Protocol)
| Integration Type | Supported Systems |
|------------------|-------------------|
| **ERP Systems** | SAP, Oracle EBS, Microsoft Dynamics |
| **CRM Platforms** | Salesforce, HubSpot, Microsoft CRM |
| **Databases** | PostgreSQL, MySQL, Oracle, SQL Server |
| **File Systems** | Local, NFS, S3, Azure Blob |
| **APIs** | REST, SOAP, GraphQL, gRPC |
| **Message Queues** | Kafka, RabbitMQ, ActiveMQ, AWS SQS |

#### A2A Servers (Agent-to-Agent Communication)
| Feature | Description |
|---------|-------------|
| **Protocol Stack** | Custom protocol optimized for agent communication |
| **Discovery Service** | Automatic agent registration and discovery |
| **Load Balancing** | Intelligent agent workload distribution |
| **Fault Tolerance** | Automatic failover and recovery |
| **Security Layer** | End-to-end encryption and authentication |
| **Performance Monitoring** | Real-time agent performance metrics |

## Architecture Overview

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AMX Console   │    │    AMX CLI      │    │    AMX Hub      │
│   (Frontend)    │────│  (Management)   │────│ (Orchestration) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AMX Engine                               │
├─────────────────┬─────────────────┬─────────────────────────────┤
│ Agent           │ Simulation      │ Integration                 │
│ Orchestration   │ Engine          │ Layer                       │
│ - Workflow Mgmt │ - Kalasim Core  │ - MCP Servers              │
│ - Agent Design  │ - Process Model │ - A2A Servers              │
│ - State Mgmt    │ - Event Engine  │ - API Gateway              │
└─────────────────┴─────────────────┴─────────────────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Kafka       │    │     Redis       │
│   Database      │    │  Message Queue  │    │     Cache       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Microservices Architecture
```
AMX Engine Core
├── API Gateway Service (Ktor)
├── Agent Management Service
├── Simulation Service (Kalasim)
├── Workflow Engine Service
├── Integration Service (MCP/A2A)
├── Authentication Service
├── Monitoring Service
└── Configuration Service
```

## Deployment Options

### Local Development (Workspace-Aware)
```bash
# Via AIMatrix CLI (in workspace directory)
cd my-workspace/
aimatrix engine install
aimatrix engine start

# Engine automatically reads workspace structure:
# my-workspace/
# ├── .aimatrix/
# ├── knowledge/
# │   ├── capsules/     # Knowledge files
# │   ├── volumes/      # Knowledge files
# │   └── libraries/    # Knowledge files
# ├── agents/           # Agent configs
# ├── workflows/        # Workflow definitions
# └── models/           # Custom models

# Engine processes these local files
# Access at http://localhost:8080
```

### Cloud Deployment

#### AWS Deployment
```yaml
# ECS Service Definition
Services:
  - AMX Engine (ECS/Fargate)
  - Application Load Balancer
  - RDS PostgreSQL
  - ElastiCache Redis
  - MSK Kafka

# Auto Scaling:
  - CPU > 70%: Scale up
  - CPU < 30%: Scale down
  - Min: 2 instances
  - Max: 20 instances
```

#### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: amx-engine
spec:
  replicas: 3
  selector:
    matchLabels:
      app: amx-engine
  template:
    spec:
      containers:
      - name: amx-engine
        image: aimatrix/amx-engine:3.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

### On-Premise Installation
```bash
# Production Installation Script
#!/bin/bash
# Download and install AMX Engine
curl -fsSL https://install.aimatrix.com/engine | bash

# System service installation
sudo systemctl enable amx-engine
sudo systemctl start amx-engine

# Configuration
amx-engine config set database.url postgresql://localhost:5432/amx
amx-engine config set server.port 8080
amx-engine config set auth.enabled true

# Health check
amx-engine health-check
```

## Security Features

### Authentication & Authorization
| Feature | Implementation |
|---------|----------------|
| **Multi-Factor Authentication** | TOTP, SMS, Email verification |
| **Single Sign-On (SSO)** | SAML 2.0, OAuth 2.0, OpenID Connect |
| **Role-Based Access Control** | Granular permissions per resource |
| **API Key Management** | Rotating keys with expiration |
| **JWT Tokens** | Stateless authentication with refresh |
| **Audit Logging** | Complete access and action logging |

### Network Security
| Feature | Implementation |
|---------|----------------|
| **TLS Termination** | TLS 1.3 for all external communications |
| **Certificate Management** | Automatic Let's Encrypt integration |
| **API Rate Limiting** | Per-user and per-endpoint limits |
| **IP Whitelisting** | Network-level access control |
| **VPN Integration** | IPsec and WireGuard support |
| **Firewall Rules** | Port and service restrictions |

### Data Protection
| Feature | Implementation |
|---------|----------------|
| **Encryption at Rest** | AES-256 database and file encryption |
| **Encryption in Transit** | TLS 1.3 for all data transmission |
| **Key Management** | HashiCorp Vault integration |
| **Data Masking** | PII protection in logs and exports |
| **Backup Encryption** | Encrypted backup storage |
| **Secure Deletion** | Cryptographic data wiping |

## Integration Points

### Enterprise Systems Integration

#### ERP Systems
| System | Integration Method | Features |
|--------|-------------------|----------|
| **SAP** | RFC, REST APIs | Real-time data sync, transaction processing |
| **Oracle EBS** | PL/SQL APIs, web services | Financial data, inventory management |
| **Microsoft Dynamics** | OData, REST APIs | CRM integration, workflow automation |
| **NetSuite** | SuiteScript, REST APIs | E-commerce, financial reporting |

#### Database Connectivity
```kotlin
// Example MCP Server Configuration
mcpServer {
    name = "primary-db"
    type = DatabaseMCP
    config {
        url = "postgresql://db.company.com:5432/production"
        driver = "postgresql"
        pool {
            minSize = 5
            maxSize = 50
            timeout = 30.seconds
        }
        encryption = true
        ssl = SSLMode.REQUIRE
    }
}
```

#### Message Queue Integration
```kotlin
// Kafka Integration Example
kafkaConfig {
    bootstrapServers = listOf("kafka-1:9092", "kafka-2:9092")
    topics {
        register("agent-events") {
            partitions = 12
            replicationFactor = 3
            compression = CompressionType.LZ4
        }
        register("simulation-results") {
            partitions = 6
            replicationFactor = 2
        }
    }
    security {
        protocol = SecurityProtocol.SASL_SSL
        saslMechanism = SaslMechanism.PLAIN
    }
}
```

## Monitoring & Observability

### Metrics & Analytics
| Category | Metrics |
|----------|---------|
| **Performance** | Response time, throughput, error rates |
| **Resources** | CPU, memory, disk, network utilization |
| **Business** | Agent efficiency, simulation accuracy |
| **Custom** | User-defined KPIs and business metrics |

### Logging & Tracing
```yaml
Logging Framework: Logback with structured JSON
Log Levels: ERROR, WARN, INFO, DEBUG, TRACE
Log Retention: 90 days (configurable)
Distributed Tracing: Jaeger/Zipkin compatible
Metrics Export: Prometheus format
Alerting: AlertManager integration
```

### Health Checks
```bash
# Health check endpoints
GET /health          # Overall system health
GET /health/db       # Database connectivity
GET /health/cache    # Redis cache status  
GET /health/queue    # Message queue health
GET /health/agents   # Agent system status
GET /health/sim      # Simulation engine status
```

## Licensing & Pricing

### Community Edition (Free)
| Feature | Limitation |
|---------|------------|
| **Agents** | Up to 100 active agents |
| **Simulations** | 10,000 events per run |
| **Integrations** | 3 MCP connections |
| **Storage** | 1 GB database |
| **Support** | Community forums |
| **Updates** | Major versions only |

### Professional Edition
| Tier | Price | Features |
|------|-------|----------|
| **Starter** | $99/month | 1,000 agents, 100K events |
| **Business** | $299/month | 5,000 agents, 1M events |
| **Enterprise** | $999/month | 20,000 agents, 10M events |
| **Unlimited** | Custom | No limits, dedicated support |

### Enterprise Licensing
- **Per-Core Licensing**: $500 per CPU core annually
- **Site License**: Unlimited deployment within organization
- **OEM License**: Redistribution rights for software vendors
- **Government**: Special pricing and terms available
- **Volume Discounts**: 20% off 10+ instances, 35% off 50+ instances

## Support & Maintenance

### Support Tiers
| Tier | Response Time | Channels | Price |
|------|---------------|----------|-------|
| **Community** | Best effort | Forums, GitHub | Free |
| **Professional** | 24 hours | Email, Chat | $199/month |
| **Enterprise** | 4 hours | Email, Chat, Phone | $499/month |
| **Mission Critical** | 1 hour | Dedicated support | $1,999/month |

### Professional Services
| Service | Description | Price |
|---------|-------------|-------|
| **Architecture Review** | System design consultation | $5,000 |
| **Implementation Services** | Deployment and configuration | $15,000+ |
| **Training Programs** | Technical team training | $3,000/day |
| **Custom Development** | Bespoke features and integrations | $250/hour |
| **Performance Optimization** | System tuning and optimization | $10,000+ |

### Maintenance & Updates
- **Security Updates**: Monthly security patches
- **Feature Updates**: Quarterly feature releases
- **Major Versions**: Annual major version releases
- **LTS Support**: 3-year support for LTS versions
- **Migration Assistance**: Upgrade support and guidance

## Getting Started Guide

### Quick Start Installation

#### Prerequisites
```bash
# Java 17+ (OpenJDK recommended)
java --version

# PostgreSQL 13+
psql --version

# Docker (optional but recommended)
docker --version
```

#### Local Installation
```bash
# Download and install via script
curl -fsSL https://install.aimatrix.com/engine | bash

# Or via Docker
docker run -d --name amx-engine \
  -p 8080:8080 \
  -p 5432:5432 \
  -e POSTGRES_DB=amx \
  -e POSTGRES_USER=amx \
  -e POSTGRES_PASSWORD=secure_password \
  aimatrix/amx-engine:latest

# Verify installation
curl http://localhost:8080/health
```

#### Configuration
```yaml
# config/application.yml
server:
  port: 8080
  ssl:
    enabled: false

database:
  url: postgresql://localhost:5432/amx
  username: amx
  password: ${DATABASE_PASSWORD}
  pool:
    maximum: 50
    minimum: 5

simulation:
  engine: kalasim
  max_events: 1000000
  threads: 4

agents:
  max_concurrent: 1000
  heartbeat_interval: 30s
  
security:
  jwt:
    secret: ${JWT_SECRET}
    expiration: 24h
  cors:
    enabled: true
    origins: "*"
```

### Development Workflow

#### Creating Your First Agent
```kotlin
// Agent Definition
class CustomerServiceAgent : Agent {
    override suspend fun initialize() {
        // Agent initialization logic
        registerSkill(EmailHandling())
        registerSkill(OrderProcessing())
        registerSkill(CustomerLookup())
    }
    
    override suspend fun processMessage(message: AgentMessage): AgentResponse {
        return when (message.intent) {
            "order_inquiry" -> handleOrderInquiry(message)
            "product_question" -> handleProductQuestion(message)
            else -> handleGeneral(message)
        }
    }
}

// Agent Registration
agentRegistry.register("customer-service") {
    factory = { CustomerServiceAgent() }
    maxInstances = 10
    scalingPolicy = AutoScaling.CPU_BASED
}
```

#### Creating Simulations
```kotlin
// Process Simulation
simulation("order-fulfillment") {
    resources {
        resource("warehouse-staff", capacity = 5)
        resource("shipping-dock", capacity = 2)
    }
    
    process("order-processing") {
        delay(exponential(5.minutes))
        request("warehouse-staff") {
            delay(uniform(10.minutes, 20.minutes))
        }
        request("shipping-dock") {
            delay(triangular(15.minutes, 30.minutes, 45.minutes))
        }
    }
    
    arrival {
        generator = poisson(2.per(hour))
        until = 8.hours
    }
}
```

### API Usage Examples

#### Agent Management API
```bash
# Create new agent
curl -X POST http://localhost:8080/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "support-agent-001",
    "type": "customer-service",
    "config": {
      "language": "en",
      "skills": ["email", "chat", "phone"]
    }
  }'

# Start agent
curl -X POST http://localhost:8080/api/agents/support-agent-001/start

# Get agent status
curl http://localhost:8080/api/agents/support-agent-001/status
```

#### Simulation API
```bash
# Run simulation
curl -X POST http://localhost:8080/api/simulations/run \
  -H "Content-Type: application/json" \
  -d '{
    "model": "order-fulfillment",
    "duration": "24h",
    "replications": 10,
    "parameters": {
      "arrival_rate": 2.5,
      "warehouse_capacity": 6
    }
  }'

# Get simulation results
curl http://localhost:8080/api/simulations/{simulationId}/results
```

---

**Download AMX Engine**: [engine.aimatrix.com](https://engine.aimatrix.com)  
**Documentation**: [docs.aimatrix.com/engine](https://docs.aimatrix.com/engine)  
**Support**: [support@aimatrix.com](mailto:support@aimatrix.com)