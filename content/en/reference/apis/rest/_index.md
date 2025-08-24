---
title: "REST API"
weight: 10
---

AIMatrix REST APIs follow RESTful principles and provide comprehensive access to all platform capabilities through HTTP endpoints.

## Overview

The REST API is the primary interface for integrating with AIMatrix. It provides:
- **Resource-based URLs** following REST conventions
- **HTTP methods** for different operations (GET, POST, PUT, DELETE)
- **JSON payloads** for request and response data
- **Standard HTTP status codes** for operation results
- **Comprehensive error handling** with detailed error messages

## Base Configuration

### Endpoints
```
Production:  https://api.aimatrix.com/v1
Staging:     https://api-staging.aimatrix.com/v1
Development: https://api-dev.aimatrix.com/v1
```

### Request Headers
```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
Accept: application/json
User-Agent: YourApp/1.0
```

## Core Resources

### Agents API

#### List Agents
```http
GET /v1/agents
```

**Query Parameters:**
- `page` (integer): Page number (default: 1)
- `per_page` (integer): Items per page (default: 20, max: 100)
- `type` (string): Filter by agent type
- `status` (string): Filter by status (active, inactive, training)
- `search` (string): Search by name or description

**Response:**
```json
{
  "data": [
    {
      "id": "agent_12345",
      "name": "Customer Support Agent",
      "type": "assistant",
      "status": "active",
      "description": "Handles customer inquiries",
      "capabilities": ["text_processing", "knowledge_query"],
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5
  }
}
```

#### Create Agent
```http
POST /v1/agents
```

**Request Body:**
```json
{
  "name": "New Agent",
  "type": "assistant",
  "description": "Agent description",
  "capabilities": ["text_processing"],
  "configuration": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000
  }
}
```

#### Get Agent
```http
GET /v1/agents/{agent_id}
```

#### Update Agent
```http
PUT /v1/agents/{agent_id}
```

#### Delete Agent
```http
DELETE /v1/agents/{agent_id}
```

#### Execute Agent
```http
POST /v1/agents/{agent_id}/execute
```

**Request Body:**
```json
{
  "query": "How can I help you?",
  "context": {
    "user_id": "user_123",
    "session_id": "session_456",
    "metadata": {}
  },
  "options": {
    "stream": false,
    "max_tokens": 1000
  }
}
```

### Knowledge API

#### List Knowledge Bases
```http
GET /v1/knowledge
```

#### Create Knowledge Base
```http
POST /v1/knowledge
```

**Request Body:**
```json
{
  "name": "Product Documentation",
  "type": "documentation",
  "description": "Company product documentation",
  "sources": [
    {
      "type": "url",
      "url": "https://docs.company.com"
    },
    {
      "type": "file",
      "file_id": "file_123"
    }
  ],
  "processing_options": {
    "chunk_size": 1000,
    "overlap": 200,
    "extract_metadata": true
  }
}
```

#### Query Knowledge Base
```http
POST /v1/knowledge/{kb_id}/query
```

**Request Body:**
```json
{
  "query": "How do I install the SDK?",
  "options": {
    "max_results": 5,
    "min_score": 0.7,
    "include_metadata": true,
    "rerank": true
  }
}
```

### Digital Twins API

#### List Digital Twins
```http
GET /v1/twins
```

#### Create Digital Twin
```http
POST /v1/twins
```

**Request Body:**
```json
{
  "name": "Supply Chain Twin",
  "type": "logistics",
  "description": "Digital twin of supply chain operations",
  "data_sources": [
    {
      "type": "database",
      "connection_string": "postgresql://...",
      "tables": ["orders", "inventory", "suppliers"]
    }
  ],
  "update_frequency": "real-time",
  "simulation_models": ["demand_forecast", "capacity_planning"]
}
```

#### Run Simulation
```http
POST /v1/twins/{twin_id}/simulate
```

**Request Body:**
```json
{
  "scenario": "demand_spike",
  "parameters": {
    "increase_percentage": 30,
    "duration_days": 7,
    "affected_regions": ["US", "EU"]
  },
  "options": {
    "run_async": true,
    "notification_webhook": "https://your-app.com/webhooks/simulation"
  }
}
```

## Advanced Features

### Filtering and Searching

#### Complex Filters
```http
GET /v1/agents?filter[type]=assistant&filter[status]=active&filter[created_at][gte]=2024-01-01
```

#### Full-text Search
```http
GET /v1/knowledge/search?q=installation%20guide&type=documentation
```

### Pagination

#### Cursor-based Pagination
```http
GET /v1/agents?cursor=eyJpZCI6IjEyMyJ9&limit=50
```

#### Offset-based Pagination
```http
GET /v1/agents?page=2&per_page=25
```

### Sorting
```http
GET /v1/agents?sort=name&order=asc
GET /v1/agents?sort=-created_at  # Descending
```

### Field Selection
```http
GET /v1/agents?fields=id,name,type,status
```

### Expanding Relations
```http
GET /v1/agents?expand=knowledge_bases,tools
```

## Bulk Operations

### Batch Requests
```http
POST /v1/batch
```

**Request Body:**
```json
{
  "operations": [
    {
      "method": "POST",
      "path": "/v1/agents",
      "body": {"name": "Agent 1", "type": "assistant"}
    },
    {
      "method": "POST", 
      "path": "/v1/agents",
      "body": {"name": "Agent 2", "type": "analyzer"}
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "status": 201,
      "body": {"id": "agent_123", "name": "Agent 1"}
    },
    {
      "status": 201,
      "body": {"id": "agent_124", "name": "Agent 2"}
    }
  ]
}
```

### Bulk Updates
```http
PATCH /v1/agents/bulk
```

**Request Body:**
```json
{
  "filter": {"type": "assistant"},
  "updates": {"status": "active"}
}
```

## Error Handling

### Error Response Format
```json
{
  "error": {
    "type": "ValidationError",
    "code": "INVALID_REQUEST",
    "message": "The request is invalid",
    "details": [
      {
        "field": "name",
        "code": "REQUIRED",
        "message": "Name is required"
      }
    ],
    "request_id": "req_1234567890",
    "timestamp": "2024-01-01T12:00:00Z",
    "documentation_url": "https://docs.aimatrix.com/errors#INVALID_REQUEST"
  }
}
```

### Common Error Codes
- `400` - Bad Request: Invalid request format
- `401` - Unauthorized: Invalid or missing API key
- `403` - Forbidden: Insufficient permissions
- `404` - Not Found: Resource doesn't exist
- `409` - Conflict: Resource already exists
- `422` - Unprocessable Entity: Validation failed
- `429` - Too Many Requests: Rate limit exceeded
- `500` - Internal Server Error: Server error

## Code Examples

### JavaScript/Node.js
```javascript
const axios = require('axios');

const client = axios.create({
  baseURL: 'https://api.aimatrix.com/v1',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  }
});

// Create an agent
const createAgent = async () => {
  try {
    const response = await client.post('/agents', {
      name: 'Support Agent',
      type: 'assistant',
      capabilities: ['text_processing']
    });
    
    console.log('Agent created:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
  }
};

// Execute agent
const executeAgent = async (agentId, query) => {
  try {
    const response = await client.post(`/agents/${agentId}/execute`, {
      query: query,
      context: {
        user_id: 'user_123',
        session_id: 'session_456'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Execution error:', error.response?.data);
  }
};
```

### Python
```python
import requests
import json

class AIMatrixAPI:
    def __init__(self, api_key):
        self.base_url = 'https://api.aimatrix.com/v1'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    def create_agent(self, name, agent_type, capabilities):
        url = f'{self.base_url}/agents'
        data = {
            'name': name,
            'type': agent_type,
            'capabilities': capabilities
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def execute_agent(self, agent_id, query, context=None):
        url = f'{self.base_url}/agents/{agent_id}/execute'
        data = {
            'query': query,
            'context': context or {}
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

# Usage
api = AIMatrixAPI('your_api_key')

# Create agent
agent = api.create_agent(
    name='Customer Support',
    agent_type='assistant',
    capabilities=['text_processing', 'knowledge_query']
)

# Execute agent
result = api.execute_agent(
    agent_id=agent['id'],
    query='How can I help you?',
    context={'user_id': 'user_123'}
)
```

### cURL Examples
```bash
# Create Agent
curl -X POST https://api.aimatrix.com/v1/agents \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Support Agent",
    "type": "assistant",
    "capabilities": ["text_processing"]
  }'

# List Agents
curl -X GET "https://api.aimatrix.com/v1/agents?page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Execute Agent
curl -X POST https://api.aimatrix.com/v1/agents/agent_123/execute \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Hello, how can I help?",
    "context": {"user_id": "user_123"}
  }'
```

## Performance Considerations

### Rate Limiting
- Free tier: 1,000 requests/hour
- Pro tier: 10,000 requests/hour  
- Enterprise tier: 100,000 requests/hour

### Optimization Tips
1. **Use field selection** to reduce response size
2. **Implement caching** for frequently accessed data
3. **Use batch operations** for multiple related requests
4. **Enable compression** with Accept-Encoding: gzip
5. **Implement retry logic** with exponential backoff

### Response Caching
```http
GET /v1/agents/agent_123
If-None-Match: "etag_value"
```

Response with caching headers:
```http
HTTP/1.1 200 OK
ETag: "etag_value_123"
Cache-Control: private, max-age=300
Last-Modified: Mon, 01 Jan 2024 12:00:00 GMT
```

## Testing

### Sandbox Environment
Use the sandbox environment for testing:
```
Base URL: https://api-sandbox.aimatrix.com/v1
API Key: test_key_1234567890
```

### Test Data
The sandbox includes sample agents, knowledge bases, and digital twins for testing all API endpoints without affecting production data.

---

For more examples and advanced use cases, see the [API Examples](/reference/apis/examples/) section.