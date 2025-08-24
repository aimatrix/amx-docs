---
title: "API Examples"
weight: 60
---

Real-world API integration examples for common use cases and scenarios with the AIMatrix platform.

## Complete Integration Examples

### E-commerce AI Assistant

This example shows how to build a complete e-commerce AI assistant that handles customer inquiries, product recommendations, and order processing.

#### 1. Setup and Configuration

```javascript
// Setup AIMatrix client
const AIMatrixClient = require('@aimatrix/sdk');

const client = new AIMatrixClient({
  apiKey: process.env.AIMATRIX_API_KEY,
  environment: 'production'
});

// Create specialized agents for different functions
const setupEcommerceAgents = async () => {
  // Product recommendation agent
  const productAgent = await client.agents.create({
    name: 'Product Recommendation Agent',
    type: 'assistant',
    description: 'Provides personalized product recommendations',
    capabilities: ['text_processing', 'knowledge_query', 'recommendation_engine'],
    configuration: {
      model: 'gpt-4',
      temperature: 0.7,
      systemPrompt: `You are a helpful product recommendation assistant. 
        Use customer preferences and purchase history to suggest relevant products.
        Always explain why you're recommending specific items.`
    }
  });

  // Customer support agent
  const supportAgent = await client.agents.create({
    name: 'Customer Support Agent',
    type: 'assistant',
    description: 'Handles customer service inquiries',
    capabilities: ['text_processing', 'knowledge_query', 'order_management'],
    configuration: {
      model: 'gpt-4',
      temperature: 0.5,
      systemPrompt: `You are a professional customer support agent.
        Help customers with orders, returns, and product questions.
        Always be polite and solution-focused.`
    }
  });

  return { productAgent, supportAgent };
};
```

#### 2. Knowledge Base Setup

```javascript
// Create product knowledge base
const setupProductKnowledge = async () => {
  const productKB = await client.knowledge.create({
    name: 'Product Catalog',
    type: 'documentation',
    description: 'Complete product catalog with specifications and features',
    sources: [
      {
        type: 'database',
        connection: {
          type: 'postgresql',
          host: 'db.company.com',
          database: 'products',
          table: 'product_catalog'
        }
      },
      {
        type: 'api',
        endpoint: 'https://api.company.com/products',
        headers: { 'Authorization': 'Bearer API_TOKEN' }
      }
    ],
    processingOptions: {
      chunkSize: 1000,
      overlap: 200,
      extractMetadata: true,
      enableSemantic: true
    }
  });

  // Customer service knowledge base
  const serviceKB = await client.knowledge.create({
    name: 'Customer Service Knowledge',
    type: 'faq',
    sources: [
      { type: 'url', url: 'https://company.com/help' },
      { type: 'file', fileId: 'policies_document_123' }
    ]
  });

  return { productKB, serviceKB };
};
```

#### 3. Customer Interaction Handler

```javascript
// Main interaction handler
class EcommerceAssistant {
  constructor(agents, knowledgeBases) {
    this.agents = agents;
    this.knowledgeBases = knowledgeBases;
  }

  async handleCustomerQuery(query, context) {
    // Determine intent
    const intent = await this.classifyIntent(query);
    
    switch (intent.type) {
      case 'product_inquiry':
        return await this.handleProductInquiry(query, context);
      case 'recommendation':
        return await this.handleRecommendation(query, context);
      case 'support':
        return await this.handleSupport(query, context);
      case 'order_status':
        return await this.handleOrderStatus(query, context);
      default:
        return await this.handleGeneral(query, context);
    }
  }

  async handleProductInquiry(query, context) {
    // Search product knowledge base
    const searchResults = await this.knowledgeBases.productKB.query({
      query: query,
      options: {
        maxResults: 5,
        includeMetadata: true,
        rerank: true
      }
    });

    // Generate response with product agent
    const response = await this.agents.productAgent.execute({
      query: query,
      context: {
        ...context,
        searchResults: searchResults,
        customerProfile: await this.getCustomerProfile(context.userId)
      }
    });

    return {
      response: response.text,
      products: this.extractProducts(searchResults),
      confidence: response.confidence
    };
  }

  async handleRecommendation(query, context) {
    const customerProfile = await this.getCustomerProfile(context.userId);
    const purchaseHistory = await this.getPurchaseHistory(context.userId);
    
    const response = await this.agents.productAgent.execute({
      query: query,
      context: {
        ...context,
        customerProfile,
        purchaseHistory,
        currentBrowsing: context.currentPage
      }
    });

    return {
      response: response.text,
      recommendations: response.recommendations,
      reasoning: response.reasoning
    };
  }

  async getCustomerProfile(userId) {
    // Fetch from your customer database
    const profile = await fetch(`https://api.company.com/customers/${userId}`, {
      headers: { 'Authorization': 'Bearer API_TOKEN' }
    });
    return profile.json();
  }
}
```

#### 4. WebSocket Real-time Integration

```javascript
// Real-time chat integration
const WebSocket = require('ws');

class RealtimeChatHandler {
  constructor(assistant) {
    this.assistant = assistant;
    this.connections = new Map();
  }

  setupWebSocketServer(server) {
    const wss = new WebSocket.Server({ server });

    wss.on('connection', (ws, request) => {
      const userId = this.extractUserId(request);
      this.connections.set(userId, ws);

      ws.on('message', async (data) => {
        const message = JSON.parse(data);
        await this.handleMessage(userId, message, ws);
      });

      ws.on('close', () => {
        this.connections.delete(userId);
      });
    });
  }

  async handleMessage(userId, message, ws) {
    const context = {
      userId: userId,
      sessionId: message.sessionId,
      timestamp: new Date().toISOString()
    };

    try {
      const response = await this.assistant.handleCustomerQuery(
        message.text, 
        context
      );

      ws.send(JSON.stringify({
        type: 'response',
        data: response,
        timestamp: new Date().toISOString()
      }));

      // Log conversation for analytics
      await this.logConversation(userId, message, response);
      
    } catch (error) {
      ws.send(JSON.stringify({
        type: 'error',
        message: 'I apologize, but I encountered an error. Please try again.',
        error: error.message
      }));
    }
  }
}
```

### CRM Integration Example

This example demonstrates integrating AIMatrix with a CRM system for automated lead qualification and customer insights.

#### 1. CRM Data Sync

```python
import asyncio
import aiohttp
from aimatrix import AIMatrixClient

class CRMIntegration:
    def __init__(self, aimatrix_key, crm_config):
        self.aimatrix = AIMatrixClient(api_key=aimatrix_key)
        self.crm_config = crm_config
        
    async def sync_crm_data(self):
        """Sync CRM data to AIMatrix knowledge base"""
        
        # Fetch CRM data
        crm_data = await self.fetch_crm_contacts()
        
        # Create or update knowledge base
        knowledge_base = await self.aimatrix.knowledge.create_or_update({
            'name': 'CRM Customer Data',
            'type': 'customer_data',
            'data': crm_data
        })
        
        return knowledge_base
    
    async def fetch_crm_contacts(self):
        """Fetch contacts from CRM system"""
        async with aiohttp.ClientSession() as session:
            headers = {
                'Authorization': f"Bearer {self.crm_config['api_key']}",
                'Content-Type': 'application/json'
            }
            
            contacts = []
            page = 1
            
            while True:
                async with session.get(
                    f"{self.crm_config['base_url']}/contacts",
                    headers=headers,
                    params={'page': page, 'per_page': 100}
                ) as response:
                    data = await response.json()
                    
                    if not data.get('contacts'):
                        break
                        
                    contacts.extend(data['contacts'])
                    page += 1
                    
            return contacts

    async def qualify_lead(self, lead_data):
        """Use AI to qualify incoming leads"""
        
        # Create lead qualification agent if not exists
        agent = await self.get_or_create_qualification_agent()
        
        # Execute qualification
        result = await agent.execute({
            'query': f"Qualify this lead based on our criteria: {lead_data}",
            'context': {
                'lead_data': lead_data,
                'qualification_criteria': await self.get_qualification_criteria()
            }
        })
        
        # Update CRM with qualification results
        await self.update_crm_lead(lead_data['id'], {
            'ai_qualification_score': result.score,
            'ai_qualification_notes': result.notes,
            'recommended_actions': result.actions
        })
        
        return result

    async def get_or_create_qualification_agent(self):
        """Get or create lead qualification agent"""
        try:
            agent = await self.aimatrix.agents.get('lead-qualification-agent')
        except:
            agent = await self.aimatrix.agents.create({
                'name': 'Lead Qualification Agent',
                'type': 'analyzer',
                'capabilities': ['data_analysis', 'scoring', 'recommendation'],
                'configuration': {
                    'model': 'gpt-4',
                    'temperature': 0.3,
                    'system_prompt': '''
                        You are a lead qualification specialist. 
                        Analyze lead data and score leads from 1-100 based on:
                        - Company size and industry fit
                        - Budget indicators
                        - Decision making authority
                        - Timeline urgency
                        Provide specific recommendations for follow-up.
                    '''
                }
            })
        
        return agent
```

#### 2. Automated Lead Scoring

```python
async def automated_lead_processing():
    """Process new leads automatically"""
    crm_integration = CRMIntegration(
        aimatrix_key=os.getenv('AIMATRIX_API_KEY'),
        crm_config={
            'base_url': 'https://api.hubspot.com',
            'api_key': os.getenv('HUBSPOT_API_KEY')
        }
    )
    
    # Set up webhook listener for new leads
    from flask import Flask, request
    app = Flask(__name__)
    
    @app.route('/webhooks/new-lead', methods=['POST'])
    async def handle_new_lead():
        lead_data = request.json
        
        # Qualify the lead
        qualification = await crm_integration.qualify_lead(lead_data)
        
        # Trigger appropriate actions based on score
        if qualification.score >= 80:
            await trigger_immediate_followup(lead_data)
        elif qualification.score >= 60:
            await schedule_nurture_campaign(lead_data)
        else:
            await add_to_general_newsletter(lead_data)
        
        return {'status': 'processed', 'score': qualification.score}
```

### Healthcare AI Assistant

Example of a healthcare AI assistant that handles patient inquiries while maintaining HIPAA compliance.

#### 1. HIPAA-Compliant Setup

```javascript
const express = require('express');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

class HealthcareAssistant {
  constructor() {
    this.client = new AIMatrixClient({
      apiKey: process.env.AIMATRIX_API_KEY,
      environment: 'production',
      compliance: {
        mode: 'HIPAA',
        encryption: true,
        auditLogging: true
      }
    });
    
    this.app = express();
    this.setupSecurity();
    this.setupAgents();
  }

  setupSecurity() {
    // Security headers
    this.app.use(helmet({
      hsts: { maxAge: 31536000, includeSubDomains: true },
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'self'", "'unsafe-inline'"],
          styleSrc: ["'self'", "'unsafe-inline'"]
        }
      }
    }));

    // Rate limiting
    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 100 // limit each IP to 100 requests per windowMs
    });
    this.app.use(limiter);

    // Input validation middleware
    this.app.use(express.json({ limit: '10mb' }));
    this.app.use(this.validateInput.bind(this));
  }

  async setupAgents() {
    // General health information agent
    this.healthInfoAgent = await this.client.agents.create({
      name: 'Health Information Assistant',
      type: 'assistant',
      capabilities: ['medical_information', 'symptom_guidance'],
      configuration: {
        model: 'gpt-4',
        temperature: 0.3,
        systemPrompt: `
          You are a healthcare information assistant. 
          IMPORTANT: You can only provide general health information.
          Always recommend consulting healthcare professionals for medical advice.
          Never attempt to diagnose or prescribe treatments.
          Be empathetic but maintain professional boundaries.
        `,
        complianceFilters: ['HIPAA', 'medical_disclaimer']
      }
    });

    // Appointment scheduling agent
    this.schedulingAgent = await this.client.agents.create({
      name: 'Appointment Scheduling Assistant',
      type: 'assistant',
      capabilities: ['scheduling', 'calendar_integration'],
      configuration: {
        model: 'gpt-3.5-turbo',
        temperature: 0.1,
        systemPrompt: 'Help patients schedule appointments efficiently.'
      }
    });
  }

  async handlePatientQuery(query, patientContext) {
    // Log all interactions for HIPAA compliance
    const interactionId = await this.logInteraction({
      query: this.sanitizeForLogging(query),
      patientId: patientContext.patientId,
      timestamp: new Date().toISOString(),
      ipAddress: patientContext.ipAddress
    });

    try {
      // Classify query type
      const classification = await this.classifyHealthQuery(query);
      
      let response;
      switch (classification.type) {
        case 'general_health_info':
          response = await this.handleHealthInformation(query, patientContext);
          break;
        case 'appointment_request':
          response = await this.handleAppointmentRequest(query, patientContext);
          break;
        case 'prescription_inquiry':
          response = await this.handlePrescriptionInquiry(query, patientContext);
          break;
        default:
          response = await this.handleGeneralInquiry(query, patientContext);
      }

      // Log response
      await this.logResponse(interactionId, response);
      
      return response;
      
    } catch (error) {
      await this.logError(interactionId, error);
      return {
        message: "I apologize, but I'm unable to process your request right now. Please contact our office directly.",
        requiresHumanIntervention: true
      };
    }
  }

  sanitizeForLogging(text) {
    // Remove potential PHI from logs
    const phiPatterns = [
      /\b\d{3}-\d{2}-\d{4}\b/g, // SSN
      /\b\d{10,}\b/g, // Phone numbers
      /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g // Emails
    ];
    
    let sanitized = text;
    phiPatterns.forEach(pattern => {
      sanitized = sanitized.replace(pattern, '[REDACTED]');
    });
    
    return sanitized;
  }
}
```

### Financial Services Integration

Example showing integration with financial systems for automated reporting and compliance.

#### 1. Financial Data Processing

```python
from decimal import Decimal
import pandas as pd
from aimatrix import AIMatrixClient

class FinancialAIIntegration:
    def __init__(self, api_key):
        self.client = AIMatrixClient(api_key=api_key)
        self.compliance_agent = None
        self.analysis_agent = None
        
    async def setup_financial_agents(self):
        """Setup specialized financial agents"""
        
        # Compliance monitoring agent
        self.compliance_agent = await self.client.agents.create({
            'name': 'Financial Compliance Monitor',
            'type': 'analyzer',
            'capabilities': ['compliance_checking', 'risk_assessment'],
            'configuration': {
                'model': 'gpt-4',
                'temperature': 0.1,  # Very conservative for compliance
                'system_prompt': '''
                    You are a financial compliance specialist.
                    Monitor transactions for suspicious activity, regulatory compliance,
                    and risk indicators. Flag any anomalies for human review.
                    Always err on the side of caution.
                '''
            }
        })
        
        # Financial analysis agent
        self.analysis_agent = await self.client.agents.create({
            'name': 'Financial Data Analyst',
            'type': 'analyzer',
            'capabilities': ['data_analysis', 'trend_identification', 'reporting'],
            'configuration': {
                'model': 'gpt-4',
                'temperature': 0.3,
                'system_prompt': '''
                    You are a financial data analyst. Analyze financial data,
                    identify trends, generate insights, and create reports.
                    Focus on accuracy and actionable recommendations.
                '''
            }
        })

    async def process_transaction_batch(self, transactions):
        """Process a batch of transactions for compliance and analysis"""
        
        results = {
            'processed': 0,
            'flagged': 0,
            'insights': [],
            'alerts': []
        }
        
        for transaction in transactions:
            # Compliance check
            compliance_result = await self.compliance_agent.execute({
                'query': f'Analyze this transaction for compliance: {transaction}',
                'context': {
                    'transaction': transaction,
                    'account_history': await self.get_account_history(transaction['account_id'])
                }
            })
            
            if compliance_result.risk_level == 'HIGH':
                results['alerts'].append({
                    'transaction_id': transaction['id'],
                    'risk_factors': compliance_result.risk_factors,
                    'recommended_actions': compliance_result.actions
                })
                results['flagged'] += 1
            
            results['processed'] += 1
        
        # Generate batch insights
        batch_analysis = await self.analysis_agent.execute({
            'query': 'Analyze this batch of transactions for patterns and insights',
            'context': {
                'transactions': transactions,
                'batch_summary': self.create_batch_summary(transactions)
            }
        })
        
        results['insights'] = batch_analysis.insights
        
        return results

    async def generate_compliance_report(self, period='monthly'):
        """Generate automated compliance reports"""
        
        # Fetch transaction data for period
        transactions = await self.fetch_transactions_for_period(period)
        
        # Process through AI analysis
        report_data = await self.analysis_agent.execute({
            'query': f'Generate a {period} compliance report from this transaction data',
            'context': {
                'transactions': transactions,
                'period': period,
                'regulatory_requirements': await self.get_regulatory_requirements()
            }
        })
        
        # Format report
        report = {
            'period': period,
            'generated_at': pd.Timestamp.now().isoformat(),
            'summary': report_data.summary,
            'metrics': report_data.metrics,
            'recommendations': report_data.recommendations,
            'appendices': {
                'transaction_count': len(transactions),
                'total_volume': sum(t['amount'] for t in transactions),
                'flagged_transactions': report_data.flagged_count
            }
        }
        
        # Store report
        await self.store_compliance_report(report)
        
        return report
```

### Multi-channel Customer Support

Example of a comprehensive customer support system using multiple AIMatrix APIs.

#### 1. Unified Support Platform

```typescript
interface SupportChannel {
  id: string;
  type: 'chat' | 'email' | 'phone' | 'social';
  agent: any;
  knowledgeBase: any;
}

class UnifiedSupportPlatform {
  private client: AIMatrixClient;
  private channels: Map<string, SupportChannel> = new Map();
  private escalationRules: EscalationRule[] = [];

  constructor(apiKey: string) {
    this.client = new AIMatrixClient({ apiKey });
  }

  async initialize(): Promise<void> {
    // Setup different agents for different channels
    const chatAgent = await this.client.agents.create({
      name: 'Chat Support Agent',
      type: 'assistant',
      capabilities: ['text_processing', 'quick_response', 'escalation'],
      configuration: {
        model: 'gpt-3.5-turbo',
        temperature: 0.7,
        maxTokens: 500,
        systemPrompt: 'Provide quick, helpful responses for chat support. Be concise but friendly.'
      }
    });

    const emailAgent = await this.client.agents.create({
      name: 'Email Support Agent', 
      type: 'assistant',
      capabilities: ['text_processing', 'detailed_response', 'research'],
      configuration: {
        model: 'gpt-4',
        temperature: 0.5,
        maxTokens: 2000,
        systemPrompt: 'Provide detailed, professional email responses. Research thoroughly before responding.'
      }
    });

    // Setup knowledge bases
    const generalKB = await this.client.knowledge.create({
      name: 'General Support Knowledge',
      type: 'faq',
      sources: [
        { type: 'url', url: 'https://company.com/help' },
        { type: 'file', fileId: 'support_docs_123' }
      ]
    });

    const technicalKB = await this.client.knowledge.create({
      name: 'Technical Documentation',
      type: 'documentation',
      sources: [
        { type: 'url', url: 'https://docs.company.com' },
        { type: 'api', endpoint: 'https://api.company.com/docs' }
      ]
    });

    // Register channels
    this.channels.set('chat', {
      id: 'chat',
      type: 'chat',
      agent: chatAgent,
      knowledgeBase: generalKB
    });

    this.channels.set('email', {
      id: 'email',
      type: 'email', 
      agent: emailAgent,
      knowledgeBase: technicalKB
    });

    // Setup escalation rules
    this.escalationRules = [
      {
        condition: (context) => context.sentiment < 0.3,
        action: 'escalate_to_human',
        priority: 'high'
      },
      {
        condition: (context) => context.complexity > 0.8,
        action: 'escalate_to_specialist',
        priority: 'medium'  
      }
    ];
  }

  async handleSupportRequest(request: SupportRequest): Promise<SupportResponse> {
    const channel = this.channels.get(request.channel);
    if (!channel) {
      throw new Error(`Unsupported channel: ${request.channel}`);
    }

    // Analyze request context
    const context = await this.analyzeRequestContext(request);
    
    // Check escalation rules
    const escalation = this.checkEscalationRules(context);
    if (escalation) {
      return await this.handleEscalation(request, escalation);
    }

    // Search knowledge base
    const searchResults = await channel.knowledgeBase.query({
      query: request.message,
      options: {
        maxResults: 3,
        minScore: 0.7
      }
    });

    // Generate response
    const response = await channel.agent.execute({
      query: request.message,
      context: {
        ...context,
        searchResults,
        channel: request.channel,
        customerHistory: await this.getCustomerHistory(request.customerId)
      }
    });

    // Track metrics
    await this.trackSupportMetrics(request, response, context);

    return {
      message: response.text,
      confidence: response.confidence,
      sources: searchResults,
      escalated: false,
      followUpRequired: response.metadata?.followUpRequired || false
    };
  }

  private async analyzeRequestContext(request: SupportRequest): Promise<RequestContext> {
    const analysisAgent = await this.getAnalysisAgent();
    
    const analysis = await analysisAgent.execute({
      query: `Analyze this support request: ${request.message}`,
      context: {
        channel: request.channel,
        customerId: request.customerId,
        timestamp: request.timestamp
      }
    });

    return {
      sentiment: analysis.sentiment,
      complexity: analysis.complexity,
      urgency: analysis.urgency,
      category: analysis.category,
      requiredExpertise: analysis.requiredExpertise
    };
  }
}
```

## API Testing Examples

### Comprehensive Test Suite

```javascript
// Jest test suite for AIMatrix API integration
describe('AIMatrix API Integration Tests', () => {
  let client;
  let testAgent;

  beforeAll(async () => {
    client = new AIMatrixClient({
      apiKey: process.env.AIMATRIX_TEST_API_KEY,
      environment: 'test'
    });

    // Create test agent
    testAgent = await client.agents.create({
      name: 'Test Agent',
      type: 'assistant',
      capabilities: ['text_processing']
    });
  });

  afterAll(async () => {
    // Cleanup test resources
    if (testAgent) {
      await client.agents.delete(testAgent.id);
    }
  });

  describe('Agent Operations', () => {
    test('should create agent successfully', async () => {
      const agent = await client.agents.create({
        name: 'Integration Test Agent',
        type: 'assistant',
        capabilities: ['text_processing']
      });

      expect(agent.id).toBeDefined();
      expect(agent.name).toBe('Integration Test Agent');
      expect(agent.type).toBe('assistant');

      // Cleanup
      await client.agents.delete(agent.id);
    });

    test('should execute agent with context', async () => {
      const result = await testAgent.execute({
        query: 'Hello, how are you?',
        context: {
          userId: 'test_user_123',
          sessionId: 'test_session_456'
        }
      });

      expect(result.response).toBeDefined();
      expect(result.metadata).toBeDefined();
      expect(result.metadata.tokensUsed).toBeGreaterThan(0);
    });

    test('should handle rate limiting gracefully', async () => {
      const promises = Array.from({ length: 20 }, () =>
        testAgent.execute({ query: 'Test query' })
      );

      const results = await Promise.allSettled(promises);
      const rejected = results.filter(r => r.status === 'rejected');

      if (rejected.length > 0) {
        expect(rejected[0].reason.message).toContain('rate limit');
      }
    });
  });

  describe('Knowledge Base Operations', () => {
    let testKB;

    beforeEach(async () => {
      testKB = await client.knowledge.create({
        name: 'Test Knowledge Base',
        type: 'documentation',
        sources: [
          {
            type: 'text',
            content: 'This is test documentation content.'
          }
        ]
      });
    });

    afterEach(async () => {
      if (testKB) {
        await client.knowledge.delete(testKB.id);
      }
    });

    test('should create and query knowledge base', async () => {
      // Wait for processing
      await new Promise(resolve => setTimeout(resolve, 2000));

      const results = await testKB.query({
        query: 'test documentation',
        options: { maxResults: 5 }
      });

      expect(results.results).toBeDefined();
      expect(Array.isArray(results.results)).toBe(true);
    });

    test('should handle empty query results', async () => {
      const results = await testKB.query({
        query: 'nonexistent content that should not match',
        options: { maxResults: 5 }
      });

      expect(results.results).toBeDefined();
      expect(results.results.length).toBe(0);
    });
  });

  describe('Error Handling', () => {
    test('should handle invalid agent ID', async () => {
      await expect(
        client.agents.get('invalid_agent_id')
      ).rejects.toThrow(/not found/i);
    });

    test('should handle malformed requests', async () => {
      await expect(
        client.agents.create({
          // Missing required fields
          type: 'assistant'
        })
      ).rejects.toThrow(/validation/i);
    });

    test('should handle network errors', async () => {
      const offlineClient = new AIMatrixClient({
        apiKey: 'test_key',
        baseURL: 'https://nonexistent-api.example.com'
      });

      await expect(
        offlineClient.agents.list()
      ).rejects.toThrow(/network/i);
    });
  });
});
```

### Load Testing Example

```python
# Load testing with asyncio and aiohttp
import asyncio
import aiohttp
import time
from statistics import mean, median

async def load_test_agents():
    """Load test agent execution endpoints"""
    
    client = AIMatrixClient(api_key='test_key')
    
    # Create test agent
    agent = await client.agents.create({
        'name': 'Load Test Agent',
        'type': 'assistant',
        'capabilities': ['text_processing']
    })
    
    # Test scenarios
    scenarios = [
        {'concurrent_users': 10, 'requests_per_user': 50},
        {'concurrent_users': 25, 'requests_per_user': 20},
        {'concurrent_users': 50, 'requests_per_user': 10}
    ]
    
    results = []
    
    for scenario in scenarios:
        print(f"Testing {scenario['concurrent_users']} concurrent users, {scenario['requests_per_user']} requests each")
        
        start_time = time.time()
        
        # Create tasks for concurrent execution
        tasks = []
        for user in range(scenario['concurrent_users']):
            for request in range(scenario['requests_per_user']):
                task = execute_agent_request(agent, f"Test query {user}-{request}")
                tasks.append(task)
        
        # Execute all tasks concurrently
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        
        # Analyze results
        successful = [r for r in responses if not isinstance(r, Exception)]
        failed = [r for r in responses if isinstance(r, Exception)]
        
        response_times = [r.get('response_time', 0) for r in successful if isinstance(r, dict)]
        
        scenario_result = {
            'scenario': scenario,
            'total_requests': len(tasks),
            'successful_requests': len(successful),
            'failed_requests': len(failed),
            'total_time': end_time - start_time,
            'requests_per_second': len(tasks) / (end_time - start_time),
            'avg_response_time': mean(response_times) if response_times else 0,
            'median_response_time': median(response_times) if response_times else 0
        }
        
        results.append(scenario_result)
        print(f"Results: {len(successful)} successful, {len(failed)} failed")
        print(f"RPS: {scenario_result['requests_per_second']:.2f}")
        print(f"Avg response time: {scenario_result['avg_response_time']:.2f}s")
        print("-" * 50)
    
    # Cleanup
    await client.agents.delete(agent.id)
    
    return results

async def execute_agent_request(agent, query):
    """Execute single agent request and measure response time"""
    start_time = time.time()
    
    try:
        result = await agent.execute({
            'query': query,
            'context': {'test': True}
        })
        
        response_time = time.time() - start_time
        
        return {
            'success': True,
            'response_time': response_time,
            'result': result
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'response_time': time.time() - start_time
        }

# Run load test
if __name__ == "__main__":
    results = asyncio.run(load_test_agents())
    
    # Generate report
    print("Load Test Summary:")
    print("=" * 60)
    for result in results:
        print(f"Scenario: {result['scenario']}")
        print(f"Success Rate: {result['successful_requests']/result['total_requests']*100:.1f}%")
        print(f"Requests/Second: {result['requests_per_second']:.2f}")
        print(f"Average Response Time: {result['avg_response_time']:.3f}s")
        print()
```

---

These comprehensive examples demonstrate real-world integration patterns with the AIMatrix platform. For more specific use cases or custom implementations, refer to our [API Documentation](/reference/apis/) or contact our support team.