---
title: "Developer Guide"
description: "Comprehensive guide for developing, testing, and publishing Knowledge Capsules including development tools, best practices, and certification process"
weight: 250
---

# Knowledge Capsule Developer Guide

This comprehensive guide provides everything developers need to create, test, and publish high-quality Knowledge Capsules for the AIMatrix ecosystem. From initial setup to marketplace publication, this guide covers all aspects of capsule development.

## Development Environment Setup

### Prerequisites and Tools

Before starting Knowledge Capsule development, ensure you have the required tools and environment:

```bash
# Install AIMatrix CLI
npm install -g @aimatrix/cli

# Install Capsule Development Kit (CDK)
npm install -g @aimatrix/capsule-cdk

# Verify installation
aimatrix version
capsule-cdk version
```

### Development Environment Configuration

```typescript
// aimatrix.config.ts
export default {
  capsule: {
    development: {
      runtime: 'node18',
      environment: 'sandbox',
      debugging: true,
      hotReload: true,
      testDatabase: 'postgresql://localhost:5432/capsule_dev',
      vectorStore: 'local', // or 'supabase' for remote development
    },
    build: {
      outputDir: './dist',
      minify: true,
      treeshaking: true,
      sourceMap: true,
      bundleAnalysis: true
    },
    deployment: {
      registry: 'https://marketplace.aimatrix.com',
      organization: 'your-org',
      visibility: 'private' // or 'public'
    }
  }
};
```

### Project Structure

The CDK generates a standardized project structure:

```
my-knowledge-capsule/
├── manifest.json              # Capsule metadata and configuration
├── README.md                  # Documentation
├── LICENSE                    # License file
├── CHANGELOG.md              # Version history
├── aimatrix.config.ts        # Development configuration
├── src/                      # Source code
│   ├── index.ts             # Main entry point
│   ├── handlers/            # Event handlers
│   │   ├── install.ts       # Installation hooks
│   │   ├── update.ts        # Update hooks
│   │   └── lifecycle.ts     # Lifecycle management
│   ├── services/            # Core services
│   │   ├── knowledge.ts     # Knowledge processing
│   │   ├── api.ts          # API endpoints
│   │   └── data.ts         # Data management
│   ├── types/               # TypeScript type definitions
│   └── utils/               # Utility functions
├── knowledge/               # Knowledge assets
│   ├── rules/              # Business rules
│   ├── schemas/            # Data schemas
│   ├── workflows/          # Process definitions
│   └── embeddings/         # Vector embeddings
├── tests/                   # Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── fixtures/           # Test data
├── docs/                    # Additional documentation
└── examples/                # Usage examples
```

## Capsule Development Kit (CDK)

### Creating a New Capsule

```bash
# Create a new capsule project
capsule-cdk init my-knowledge-capsule --template=typescript

# Available templates
capsule-cdk list-templates
# - typescript (default)
# - python
# - javascript
# - mixed-language

cd my-knowledge-capsule

# Install dependencies
npm install
```

### Manifest Configuration

The manifest.json file defines your capsule's metadata, dependencies, and capabilities:

```json
{
  "id": "com.example.my-knowledge-capsule",
  "name": "My Knowledge Capsule",
  "version": "1.0.0",
  "description": "A comprehensive knowledge capsule for domain-specific tasks",
  "author": {
    "name": "Developer Name",
    "email": "developer@example.com",
    "organization": "Example Corp",
    "website": "https://example.com"
  },
  "license": "MIT",
  "keywords": ["knowledge", "ai", "domain-specific"],
  
  "aimatrixVersion": "^2.0.0",
  "nodeVersion": ">=18.0.0",
  
  "dependencies": {
    "com.aimatrix.core.nlp": "^1.2.0",
    "com.aimatrix.data.postgres": "^2.1.0"
  },
  
  "peerDependencies": {
    "com.aimatrix.vector.embeddings": "^1.0.0"
  },
  
  "resources": {
    "memory": {
      "min": "128MB",
      "recommended": "256MB",
      "max": "512MB"
    },
    "cpu": {
      "min": 0.1,
      "recommended": 0.5
    },
    "storage": {
      "persistent": "1GB",
      "temporary": "500MB"
    }
  },
  
  "permissions": [
    {
      "resource": "supabase.table.knowledge_base",
      "actions": ["read", "write"],
      "conditions": [
        {
          "field": "organization_id",
          "operator": "equals",
          "value": "${organization.id}"
        }
      ]
    },
    {
      "resource": "aimatrix.vector.search",
      "actions": ["query", "embed"]
    }
  ],
  
  "endpoints": [
    {
      "path": "/api/v1/process",
      "method": "POST",
      "handler": "src/handlers/process.ts",
      "description": "Process knowledge queries"
    }
  ],
  
  "eventHandlers": [
    {
      "event": "knowledge.updated",
      "handler": "src/handlers/knowledge-updated.ts"
    }
  ],
  
  "hooks": {
    "preInstall": "src/hooks/pre-install.ts",
    "postInstall": "src/hooks/post-install.ts",
    "preUpdate": "src/hooks/pre-update.ts",
    "postUpdate": "src/hooks/post-update.ts",
    "preRemove": "src/hooks/pre-remove.ts"
  },
  
  "knowledgeAssets": {
    "schemas": ["knowledge/schemas/*.json"],
    "rules": ["knowledge/rules/*.yaml"],
    "workflows": ["knowledge/workflows/*.bpmn"],
    "embeddings": ["knowledge/embeddings/*.jsonl"]
  }
}
```

### Core Implementation

#### Main Entry Point

```typescript
// src/index.ts
import { CapsuleRuntime, CapsuleContext } from '@aimatrix/capsule-runtime';
import { KnowledgeService } from './services/knowledge';
import { APIService } from './services/api';
import { DataService } from './services/data';

export class MyKnowledgeCapsule {
  private knowledgeService: KnowledgeService;
  private apiService: APIService;
  private dataService: DataService;
  
  constructor(private context: CapsuleContext) {
    this.initializeServices();
  }
  
  async initialize(): Promise<void> {
    // Initialize services in dependency order
    await this.dataService.initialize();
    await this.knowledgeService.initialize();
    await this.apiService.initialize();
    
    // Register event handlers
    this.registerEventHandlers();
    
    // Setup monitoring
    this.setupMonitoring();
    
    console.log(`${this.context.capsule.name} v${this.context.capsule.version} initialized`);
  }
  
  async shutdown(): Promise<void> {
    // Graceful shutdown sequence
    await this.apiService.shutdown();
    await this.knowledgeService.shutdown();
    await this.dataService.shutdown();
    
    console.log('Capsule shutdown complete');
  }
  
  private initializeServices(): void {
    this.dataService = new DataService(this.context);
    this.knowledgeService = new KnowledgeService(this.context, this.dataService);
    this.apiService = new APIService(this.context, this.knowledgeService);
  }
  
  private registerEventHandlers(): void {
    this.context.events.on('knowledge.updated', async (event) => {
      await this.knowledgeService.handleKnowledgeUpdate(event);
    });
    
    this.context.events.on('organization.settings.changed', async (event) => {
      await this.handleOrganizationSettingsChange(event);
    });
  }
  
  private setupMonitoring(): void {
    // Performance monitoring
    this.context.metrics.gauge('capsule.memory_usage', () => process.memoryUsage().heapUsed);
    this.context.metrics.gauge('capsule.active_requests', () => this.apiService.getActiveRequestCount());
    
    // Health checks
    this.context.health.register('database', () => this.dataService.healthCheck());
    this.context.health.register('knowledge_base', () => this.knowledgeService.healthCheck());
  }
}

// Export the capsule class for runtime loading
export default MyKnowledgeCapsule;
```

#### Knowledge Service Implementation

```typescript
// src/services/knowledge.ts
import { CapsuleContext } from '@aimatrix/capsule-runtime';
import { VectorSearch, Embedding } from '@aimatrix/vector-search';
import { RuleEngine } from '@aimatrix/rule-engine';
import { DataService } from './data';

export class KnowledgeService {
  private vectorSearch: VectorSearch;
  private ruleEngine: RuleEngine;
  private embeddings: Map<string, Embedding>;
  
  constructor(
    private context: CapsuleContext,
    private dataService: DataService
  ) {
    this.vectorSearch = new VectorSearch(context.supabase);
    this.ruleEngine = new RuleEngine();
    this.embeddings = new Map();
  }
  
  async initialize(): Promise<void> {
    // Load knowledge rules
    await this.loadKnowledgeRules();
    
    // Load embeddings
    await this.loadEmbeddings();
    
    // Initialize vector search
    await this.vectorSearch.initialize();
    
    // Subscribe to knowledge updates
    this.subscribeToUpdates();
  }
  
  async processQuery(query: string, context?: Record<string, any>): Promise<KnowledgeResponse> {
    const startTime = Date.now();
    
    try {
      // 1. Generate query embedding
      const queryEmbedding = await this.context.ai.generateEmbedding(query);
      
      // 2. Vector search for relevant knowledge
      const searchResults = await this.vectorSearch.search(queryEmbedding, {
        limit: 10,
        threshold: 0.7,
        filter: {
          capsule_id: this.context.capsule.id,
          organization_id: this.context.organization.id
        }
      });
      
      // 3. Apply business rules
      const ruleContext = {
        query,
        searchResults,
        userContext: context,
        organization: this.context.organization
      };
      
      const ruleResults = await this.ruleEngine.evaluate(ruleContext);
      
      // 4. Generate response
      const response = await this.generateResponse(query, searchResults, ruleResults);
      
      // 5. Log metrics
      this.context.metrics.histogram('knowledge.query_duration', Date.now() - startTime);
      this.context.metrics.counter('knowledge.queries_processed').inc();
      
      return response;
      
    } catch (error) {
      this.context.metrics.counter('knowledge.query_errors').inc();
      this.context.logger.error('Knowledge query processing failed', { query, error });
      throw error;
    }
  }
  
  private async loadKnowledgeRules(): Promise<void> {
    const ruleFiles = await this.context.assets.glob('knowledge/rules/*.yaml');
    
    for (const ruleFile of ruleFiles) {
      const ruleContent = await this.context.assets.readText(ruleFile);
      const rules = this.parseRuleFile(ruleContent);
      
      for (const rule of rules) {
        this.ruleEngine.addRule(rule);
      }
    }
    
    this.context.logger.info(`Loaded ${this.ruleEngine.getRuleCount()} knowledge rules`);
  }
  
  private async loadEmbeddings(): Promise<void> {
    const embeddingFiles = await this.context.assets.glob('knowledge/embeddings/*.jsonl');
    
    for (const embeddingFile of embeddingFiles) {
      const lines = await this.context.assets.readLines(embeddingFile);
      
      for (const line of lines) {
        const embedding = JSON.parse(line) as Embedding;
        this.embeddings.set(embedding.id, embedding);
        
        // Store in vector database
        await this.vectorSearch.upsert({
          id: embedding.id,
          vector: embedding.vector,
          metadata: {
            capsule_id: this.context.capsule.id,
            content: embedding.content,
            tags: embedding.tags
          }
        });
      }
    }
    
    this.context.logger.info(`Loaded ${this.embeddings.size} embeddings`);
  }
  
  async updateKnowledge(updates: KnowledgeUpdate[]): Promise<void> {
    const transaction = await this.dataService.beginTransaction();
    
    try {
      for (const update of updates) {
        switch (update.type) {
          case 'rule':
            await this.updateRule(update, transaction);
            break;
          case 'embedding':
            await this.updateEmbedding(update, transaction);
            break;
          case 'schema':
            await this.updateSchema(update, transaction);
            break;
        }
      }
      
      await transaction.commit();
      
      // Emit update event
      this.context.events.emit('knowledge.updated', {
        capsuleId: this.context.capsule.id,
        updates: updates.length
      });
      
    } catch (error) {
      await transaction.rollback();
      throw error;
    }
  }
  
  async healthCheck(): Promise<boolean> {
    try {
      // Check vector search connectivity
      await this.vectorSearch.healthCheck();
      
      // Check rule engine status
      const ruleCount = this.ruleEngine.getRuleCount();
      if (ruleCount === 0) {
        throw new Error('No rules loaded');
      }
      
      // Check embedding availability
      if (this.embeddings.size === 0) {
        throw new Error('No embeddings loaded');
      }
      
      return true;
    } catch (error) {
      this.context.logger.error('Knowledge service health check failed', { error });
      return false;
    }
  }
}
```

## Testing Framework

### Unit Testing

```typescript
// tests/unit/knowledge.service.test.ts
import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import { createMockContext } from '@aimatrix/capsule-testing';
import { KnowledgeService } from '../../src/services/knowledge';
import { DataService } from '../../src/services/data';

describe('KnowledgeService', () => {
  let knowledgeService: KnowledgeService;
  let mockContext: any;
  let mockDataService: DataService;
  
  beforeEach(async () => {
    mockContext = createMockContext({
      capsule: {
        id: 'test-capsule',
        name: 'Test Capsule',
        version: '1.0.0'
      }
    });
    
    mockDataService = new DataService(mockContext);
    knowledgeService = new KnowledgeService(mockContext, mockDataService);
    
    await knowledgeService.initialize();
  });
  
  afterEach(async () => {
    await knowledgeService.shutdown();
  });
  
  test('should process simple queries', async () => {
    const query = 'What is the refund policy?';
    const response = await knowledgeService.processQuery(query);
    
    expect(response).toBeDefined();
    expect(response.confidence).toBeGreaterThan(0.5);
    expect(response.sources).toHaveLength.toBeGreaterThan(0);
  });
  
  test('should handle knowledge updates', async () => {
    const updates = [
      {
        type: 'rule',
        id: 'new-rule',
        content: 'IF customer_tier = "premium" THEN priority = "high"'
      }
    ];
    
    await expect(knowledgeService.updateKnowledge(updates)).resolves.not.toThrow();
  });
  
  test('should pass health checks', async () => {
    const isHealthy = await knowledgeService.healthCheck();
    expect(isHealthy).toBe(true);
  });
});
```

### Integration Testing

```typescript
// tests/integration/capsule.integration.test.ts
import { describe, test, expect, beforeAll, afterAll } from '@jest/globals';
import { CapsuleTestRunner } from '@aimatrix/capsule-testing';
import MyKnowledgeCapsule from '../../src/index';

describe('Capsule Integration Tests', () => {
  let testRunner: CapsuleTestRunner;
  let capsule: MyKnowledgeCapsule;
  
  beforeAll(async () => {
    testRunner = new CapsuleTestRunner({
      capsuleClass: MyKnowledgeCapsule,
      testDatabase: process.env.TEST_DATABASE_URL,
      supabaseUrl: process.env.TEST_SUPABASE_URL,
      supabaseKey: process.env.TEST_SUPABASE_ANON_KEY
    });
    
    await testRunner.setup();
    capsule = await testRunner.createCapsule();
  });
  
  afterAll(async () => {
    await testRunner.teardown();
  });
  
  test('should install successfully', async () => {
    const result = await testRunner.install(capsule);
    expect(result.success).toBe(true);
  });
  
  test('should handle API requests', async () => {
    const response = await testRunner.request('/api/v1/process', {
      method: 'POST',
      body: {
        query: 'Test query',
        context: { user_id: 'test-user' }
      }
    });
    
    expect(response.status).toBe(200);
    expect(response.data).toHaveProperty('result');
  });
  
  test('should process knowledge queries end-to-end', async () => {
    const query = 'What are the business hours?';
    
    const response = await testRunner.processKnowledgeQuery(query);
    
    expect(response.confidence).toBeGreaterThan(0.7);
    expect(response.result).toContain('hours');
  });
});
```

## Quality Assurance Requirements

### Code Quality Standards

All capsules must meet the following quality standards:

```typescript
// .eslintrc.js
module.exports = {
  extends: ['@aimatrix/eslint-config-capsule'],
  rules: {
    // Security rules
    'security/detect-object-injection': 'error',
    'security/detect-non-literal-require': 'error',
    
    // Performance rules
    'unicorn/no-abusive-eslint-disable': 'error',
    'sonarjs/cognitive-complexity': ['error', 15],
    
    // Code quality rules
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn',
    
    // AIMatrix specific rules
    'aimatrix/no-direct-database-access': 'error',
    'aimatrix/require-permission-checks': 'error',
    'aimatrix/validate-knowledge-assets': 'error'
  }
};
```

### Security Scanning

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security audit
        run: |
          npm audit --audit-level high
          
      - name: Snyk security scan
        run: |
          npx snyk test --severity-threshold=medium
          
      - name: CodeQL analysis
        uses: github/codeql-action/analyze@v2
        with:
          languages: typescript
          
      - name: AIMatrix security validation
        run: |
          capsule-cdk validate --security
```

### Performance Requirements

```typescript
// Performance benchmarks that must be met
const PERFORMANCE_REQUIREMENTS = {
  // Response time requirements (95th percentile)
  api: {
    simpleQuery: 100, // ms
    complexQuery: 500, // ms
    knowledgeUpdate: 1000 // ms
  },
  
  // Resource usage limits
  memory: {
    idle: 50 * 1024 * 1024, // 50MB
    peak: 256 * 1024 * 1024 // 256MB
  },
  
  // Throughput requirements
  throughput: {
    queries_per_second: 100,
    concurrent_users: 50
  }
};
```

## Certification Process

### Certification Levels

The AIMatrix ecosystem offers three certification levels:

1. **Basic Certification**: Functional correctness and security
2. **Advanced Certification**: Performance, scalability, and integration
3. **Enterprise Certification**: Full production readiness

### Certification Checklist

```typescript
// Certification requirements checklist
interface CertificationRequirements {
  basic: {
    functionality: boolean;     // All tests pass
    security: boolean;          // Security scan passes
    documentation: boolean;     // Complete documentation
    manifest: boolean;          // Valid manifest
  };
  
  advanced: {
    performance: boolean;       // Meets performance benchmarks
    integration: boolean;       // Integration tests pass
    monitoring: boolean;        // Proper monitoring setup
    errorHandling: boolean;     // Comprehensive error handling
  };
  
  enterprise: {
    scalability: boolean;       // Load testing passes
    reliability: boolean;       // High availability design
    observability: boolean;     // Full observability stack
    compliance: boolean;        // Regulatory compliance
  };
}
```

### Automated Certification

```bash
# Run certification process
capsule-cdk certify --level=basic

# Output example:
✓ Functionality tests: PASSED (127/127 tests)
✓ Security scan: PASSED (0 high, 2 medium, 5 low issues)
✓ Documentation: PASSED (95% coverage)
✓ Manifest validation: PASSED
✓ Performance benchmarks: PASSED (avg: 45ms, p95: 120ms)
✓ Integration tests: PASSED (23/23 tests)

🎉 Certification PASSED - Ready for Basic certification
```

## Publishing Workflow

### Pre-publication Checklist

```bash
#!/bin/bash
# pre-publish.sh

set -e

echo "🔍 Running pre-publication checks..."

# 1. Version validation
echo "📋 Validating version..."
capsule-cdk validate-version

# 2. Build and test
echo "🔧 Building capsule..."
npm run build

echo "🧪 Running tests..."
npm test

# 3. Security scan
echo "🔒 Security scanning..."
capsule-cdk security-scan

# 4. Performance testing
echo "⚡ Performance testing..."
npm run test:performance

# 5. Integration testing
echo "🔗 Integration testing..."
npm run test:integration

# 6. Documentation validation
echo "📚 Documentation validation..."
capsule-cdk validate-docs

# 7. License check
echo "⚖️ License validation..."
capsule-cdk validate-license

echo "✅ All pre-publication checks passed!"
```

### Publication Process

```bash
# Build production package
npm run build:production

# Package for distribution
capsule-cdk package

# Upload to marketplace (requires authentication)
capsule-cdk publish --registry=https://marketplace.aimatrix.com

# Example output:
📦 Packaging capsule...
   ✓ Manifest validation
   ✓ Asset compression
   ✓ Dependency resolution
   ✓ Security signing

🚀 Publishing to AIMatrix Marketplace...
   ✓ Authentication verified
   ✓ Package uploaded (2.4MB)
   ✓ Automated testing initiated
   ✓ Security review queued

🎉 Publication successful!
   Package ID: pkg_abc123def456
   Review status: https://marketplace.aimatrix.com/review/pkg_abc123def456
   Expected approval: 2-5 business days
```

## Monetization Options

### Revenue Models

The AIMatrix Marketplace supports multiple monetization strategies:

```typescript
// Revenue model configuration
interface RevenueModel {
  type: 'free' | 'freemium' | 'subscription' | 'usage' | 'enterprise';
  pricing?: {
    free_tier?: {
      requests_per_month: number;
      features: string[];
    };
    paid_tiers?: Array<{
      name: string;
      price_monthly: number;
      price_yearly: number;
      requests_per_month: number;
      features: string[];
    }>;
    usage_pricing?: {
      per_request: number;
      per_gb_storage: number;
      per_cpu_hour: number;
    };
  };
  revenue_share: number; // AIMatrix platform fee (typically 20-30%)
}
```

### Revenue Tracking

```typescript
// Built-in revenue tracking
export class RevenueTracker {
  async trackUsage(
    capsuleId: string,
    organizationId: string,
    event: UsageEvent
  ): Promise<void> {
    await this.context.billing.recordUsage({
      capsule_id: capsuleId,
      organization_id: organizationId,
      event_type: event.type,
      quantity: event.quantity,
      unit_price: this.getPricing(event.type),
      timestamp: new Date()
    });
  }
  
  async generateInvoice(
    period: BillingPeriod
  ): Promise<Invoice> {
    return await this.context.billing.generateInvoice({
      capsule_id: this.context.capsule.id,
      period,
      line_items: await this.calculateLineItems(period)
    });
  }
}
```

## Best Practices

### Development Best Practices

1. **Modular Design**: Keep services loosely coupled
2. **Error Handling**: Implement comprehensive error handling
3. **Logging**: Use structured logging with appropriate levels
4. **Monitoring**: Include health checks and metrics
5. **Security**: Validate all inputs and implement proper permissions
6. **Performance**: Optimize for the specified resource limits
7. **Documentation**: Maintain up-to-date documentation

### Knowledge Asset Best Practices

1. **Embeddings**: Use high-quality, domain-specific embeddings
2. **Rules**: Keep rules simple and testable
3. **Schemas**: Design flexible, extensible schemas
4. **Workflows**: Model real-world business processes accurately

### Deployment Best Practices

1. **Versioning**: Use semantic versioning consistently
2. **Testing**: Comprehensive test coverage including edge cases
3. **Monitoring**: Set up proper monitoring and alerting
4. **Documentation**: Provide clear installation and usage instructions
5. **Support**: Offer responsive developer support

This developer guide provides a comprehensive foundation for creating high-quality Knowledge Capsules that integrate seamlessly with the AIMatrix ecosystem while meeting the platform's standards for security, performance, and reliability.