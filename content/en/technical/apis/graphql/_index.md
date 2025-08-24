---
title: "GraphQL API"
weight: 20
---

AIMatrix GraphQL API provides a flexible, efficient way to query and mutate data with strong typing and introspection capabilities.

## Overview

The GraphQL API offers several advantages over REST:
- **Single endpoint** for all operations
- **Flexible queries** - request exactly the data you need
- **Strong typing** with schema introspection
- **Real-time subscriptions** for live updates
- **Batched requests** with automatic query optimization
- **Federation support** for distributed schemas

## Endpoint

```
GraphQL Endpoint: https://api.aimatrix.com/graphql
WebSocket (Subscriptions): wss://api.aimatrix.com/graphql
GraphQL Playground: https://api.aimatrix.com/graphql/playground
```

## Authentication

Include your API key in the Authorization header:

```javascript
const headers = {
  'Authorization': 'Bearer YOUR_API_KEY',
  'Content-Type': 'application/json'
};
```

## Schema Overview

### Core Types

#### Agent
```graphql
type Agent {
  id: ID!
  name: String!
  type: AgentType!
  status: AgentStatus!
  description: String
  capabilities: [String!]!
  configuration: AgentConfiguration
  knowledgeBases: [KnowledgeBase!]!
  tools: [Tool!]!
  executions: [Execution!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

enum AgentType {
  ASSISTANT
  ANALYZER
  GENERATOR
  CLASSIFIER
  CUSTOM
}

enum AgentStatus {
  ACTIVE
  INACTIVE
  TRAINING
  ERROR
}

type AgentConfiguration {
  model: String
  temperature: Float
  maxTokens: Int
  systemPrompt: String
  parameters: JSON
}
```

#### KnowledgeBase
```graphql
type KnowledgeBase {
  id: ID!
  name: String!
  type: KnowledgeType!
  description: String
  status: ProcessingStatus!
  sources: [DataSource!]!
  documents: [Document!]!
  agents: [Agent!]!
  vectorCount: Int
  lastIndexed: DateTime
  createdAt: DateTime!
  updatedAt: DateTime!
}

enum KnowledgeType {
  DOCUMENTATION
  FAQ
  KNOWLEDGE_GRAPH
  CUSTOM
}

type DataSource {
  id: ID!
  type: SourceType!
  url: String
  fileId: String
  configuration: JSON
  lastSynced: DateTime
}

enum SourceType {
  URL
  FILE
  DATABASE
  API
  RSS
}
```

#### DigitalTwin
```graphql
type DigitalTwin {
  id: ID!
  name: String!
  type: TwinType!
  description: String
  status: TwinStatus!
  dataSources: [TwinDataSource!]!
  models: [SimulationModel!]!
  simulations: [Simulation!]!
  metrics: [TwinMetric!]!
  lastUpdated: DateTime
  createdAt: DateTime!
  updatedAt: DateTime!
}

enum TwinType {
  BUSINESS_PROCESS
  SUPPLY_CHAIN
  CUSTOMER_JOURNEY
  FINANCIAL_MODEL
  OPERATIONAL
}

type Simulation {
  id: ID!
  scenario: String!
  parameters: JSON!
  status: SimulationStatus!
  results: SimulationResults
  startedAt: DateTime!
  completedAt: DateTime
}
```

## Queries

### Basic Queries

#### Get Agent
```graphql
query GetAgent($id: ID!) {
  agent(id: $id) {
    id
    name
    type
    status
    description
    capabilities
    configuration {
      model
      temperature
      maxTokens
    }
    knowledgeBases {
      id
      name
      type
    }
    createdAt
    updatedAt
  }
}
```

#### List Agents with Filtering
```graphql
query ListAgents($filter: AgentFilter, $pagination: PaginationInput) {
  agents(filter: $filter, pagination: $pagination) {
    data {
      id
      name
      type
      status
      description
      capabilities
      createdAt
    }
    pagination {
      page
      perPage
      total
      pages
    }
  }
}
```

Variables:
```json
{
  "filter": {
    "type": "ASSISTANT",
    "status": "ACTIVE",
    "search": "customer"
  },
  "pagination": {
    "page": 1,
    "perPage": 20
  }
}
```

#### Complex Nested Query
```graphql
query GetAgentWithDetails($id: ID!) {
  agent(id: $id) {
    id
    name
    type
    status
    knowledgeBases {
      id
      name
      type
      documents(limit: 5) {
        id
        title
        content
        metadata
      }
      vectorCount
    }
    tools {
      id
      name
      type
      configuration
    }
    executions(limit: 10, orderBy: { field: CREATED_AT, direction: DESC }) {
      id
      query
      response
      status
      duration
      createdAt
    }
  }
}
```

### Knowledge Base Queries

#### Search Knowledge
```graphql
query SearchKnowledge($query: String!, $kbIds: [ID!], $options: SearchOptions) {
  searchKnowledge(query: $query, knowledgeBaseIds: $kbIds, options: $options) {
    results {
      id
      score
      document {
        id
        title
        content
        metadata
        knowledgeBase {
          id
          name
        }
      }
      highlights {
        field
        snippets
      }
    }
    aggregations {
      knowledgeBases {
        id
        name
        count
      }
      documentTypes {
        type
        count
      }
    }
    totalResults
    queryTime
  }
}
```

Variables:
```json
{
  "query": "API integration examples",
  "kbIds": ["kb_1", "kb_2"],
  "options": {
    "maxResults": 10,
    "minScore": 0.7,
    "includeHighlights": true,
    "rerank": true
  }
}
```

### Digital Twin Queries

#### Get Twin with Simulations
```graphql
query GetTwinWithSimulations($id: ID!) {
  digitalTwin(id: $id) {
    id
    name
    type
    description
    status
    dataSources {
      id
      type
      configuration
      lastSynced
    }
    simulations(limit: 5, orderBy: { field: STARTED_AT, direction: DESC }) {
      id
      scenario
      parameters
      status
      results {
        summary
        metrics
        recommendations
      }
      startedAt
      completedAt
    }
    metrics(timeRange: LAST_24_HOURS) {
      name
      value
      unit
      timestamp
    }
  }
}
```

## Mutations

### Agent Mutations

#### Create Agent
```graphql
mutation CreateAgent($input: CreateAgentInput!) {
  createAgent(input: $input) {
    id
    name
    type
    status
    description
    capabilities
    createdAt
  }
}
```

Variables:
```json
{
  "input": {
    "name": "Customer Support Agent",
    "type": "ASSISTANT",
    "description": "Handles customer inquiries and support requests",
    "capabilities": ["text_processing", "knowledge_query"],
    "configuration": {
      "model": "gpt-4",
      "temperature": 0.7,
      "maxTokens": 2000,
      "systemPrompt": "You are a helpful customer support agent."
    },
    "knowledgeBaseIds": ["kb_123", "kb_456"]
  }
}
```

#### Update Agent
```graphql
mutation UpdateAgent($id: ID!, $input: UpdateAgentInput!) {
  updateAgent(id: $id, input: $input) {
    id
    name
    description
    configuration {
      model
      temperature
      maxTokens
    }
    updatedAt
  }
}
```

#### Execute Agent
```graphql
mutation ExecuteAgent($id: ID!, $input: ExecutionInput!) {
  executeAgent(id: $id, input: $input) {
    id
    response
    status
    metadata {
      tokensUsed
      duration
      model
    }
    createdAt
  }
}
```

Variables:
```json
{
  "id": "agent_123",
  "input": {
    "query": "How do I integrate the API?",
    "context": {
      "userId": "user_456",
      "sessionId": "session_789",
      "metadata": {
        "source": "chat_widget",
        "page": "/docs/api"
      }
    },
    "options": {
      "stream": false,
      "maxTokens": 1000,
      "includeMetadata": true
    }
  }
}
```

### Knowledge Base Mutations

#### Create Knowledge Base
```graphql
mutation CreateKnowledgeBase($input: CreateKnowledgeBaseInput!) {
  createKnowledgeBase(input: $input) {
    id
    name
    type
    status
    sources {
      id
      type
      url
      configuration
    }
    createdAt
  }
}
```

#### Add Knowledge Source
```graphql
mutation AddKnowledgeSource($kbId: ID!, $input: DataSourceInput!) {
  addKnowledgeSource(knowledgeBaseId: $kbId, input: $input) {
    id
    type
    url
    configuration
    status
    lastSynced
  }
}
```

### Digital Twin Mutations

#### Create Digital Twin
```graphql
mutation CreateDigitalTwin($input: CreateDigitalTwinInput!) {
  createDigitalTwin(input: $input) {
    id
    name
    type
    description
    status
    dataSources {
      id
      type
      configuration
    }
    createdAt
  }
}
```

#### Run Simulation
```graphql
mutation RunSimulation($twinId: ID!, $input: SimulationInput!) {
  runSimulation(digitalTwinId: $twinId, input: $input) {
    id
    scenario
    parameters
    status
    startedAt
  }
}
```

Variables:
```json
{
  "twinId": "twin_123",
  "input": {
    "scenario": "demand_spike",
    "parameters": {
      "increasePercentage": 30,
      "durationDays": 7,
      "affectedRegions": ["US", "EU"]
    },
    "options": {
      "runAsync": true,
      "notificationWebhook": "https://your-app.com/webhooks/simulation"
    }
  }
}
```

## Subscriptions

### Real-time Agent Executions
```graphql
subscription AgentExecutions($agentId: ID!) {
  agentExecutions(agentId: $agentId) {
    id
    query
    response
    status
    metadata {
      tokensUsed
      duration
    }
    createdAt
  }
}
```

### Knowledge Base Updates
```graphql
subscription KnowledgeBaseUpdates($kbId: ID!) {
  knowledgeBaseUpdates(knowledgeBaseId: $kbId) {
    type
    knowledgeBase {
      id
      name
      status
      vectorCount
      lastIndexed
    }
    documents {
      id
      title
      status
    }
  }
}
```

### Simulation Progress
```graphql
subscription SimulationProgress($simulationId: ID!) {
  simulationProgress(simulationId: $simulationId) {
    id
    status
    progress
    currentStep
    estimatedCompletion
    partialResults {
      metrics
      insights
    }
  }
}
```

## Advanced Features

### Fragments
```graphql
fragment AgentDetails on Agent {
  id
  name
  type
  status
  description
  capabilities
  createdAt
  updatedAt
}

fragment KnowledgeBaseInfo on KnowledgeBase {
  id
  name
  type
  status
  vectorCount
  lastIndexed
}

query GetAgentWithKnowledge($id: ID!) {
  agent(id: $id) {
    ...AgentDetails
    knowledgeBases {
      ...KnowledgeBaseInfo
    }
  }
}
```

### Variables and Directives
```graphql
query GetAgent($id: ID!, $includeExecutions: Boolean = false) {
  agent(id: $id) {
    id
    name
    type
    status
    executions @include(if: $includeExecutions) {
      id
      query
      response
      createdAt
    }
  }
}
```

### Aliases
```graphql
query GetMultipleAgents {
  supportAgent: agent(id: "agent_support") {
    id
    name
    type
  }
  salesAgent: agent(id: "agent_sales") {
    id
    name
    type
  }
}
```

## Error Handling

### GraphQL Errors
```json
{
  "data": null,
  "errors": [
    {
      "message": "Agent not found",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ],
      "path": ["agent"],
      "extensions": {
        "code": "AGENT_NOT_FOUND",
        "details": {
          "agentId": "agent_invalid"
        }
      }
    }
  ]
}
```

### Partial Errors
```json
{
  "data": {
    "agent": {
      "id": "agent_123",
      "name": "Support Agent",
      "knowledgeBases": null
    }
  },
  "errors": [
    {
      "message": "Failed to load knowledge bases",
      "path": ["agent", "knowledgeBases"],
      "extensions": {
        "code": "KNOWLEDGE_BASE_ERROR"
      }
    }
  ]
}
```

## Code Examples

### JavaScript/Apollo Client
```javascript
import { ApolloClient, InMemoryCache, gql } from '@apollo/client';
import { createHttpLink } from '@apollo/client/link/http';
import { setContext } from '@apollo/client/link/context';

const httpLink = createHttpLink({
  uri: 'https://api.aimatrix.com/graphql',
});

const authLink = setContext((_, { headers }) => {
  return {
    headers: {
      ...headers,
      authorization: `Bearer ${YOUR_API_KEY}`,
    }
  }
});

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache()
});

// Query
const GET_AGENT = gql`
  query GetAgent($id: ID!) {
    agent(id: $id) {
      id
      name
      type
      status
      capabilities
    }
  }
`;

const { data, loading, error } = useQuery(GET_AGENT, {
  variables: { id: 'agent_123' }
});

// Mutation
const CREATE_AGENT = gql`
  mutation CreateAgent($input: CreateAgentInput!) {
    createAgent(input: $input) {
      id
      name
      type
      status
    }
  }
`;

const [createAgent] = useMutation(CREATE_AGENT);

const handleCreateAgent = async () => {
  try {
    const { data } = await createAgent({
      variables: {
        input: {
          name: 'New Agent',
          type: 'ASSISTANT',
          capabilities: ['text_processing']
        }
      }
    });
    console.log('Agent created:', data.createAgent);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### Python/GQL
```python
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(
    url="https://api.aimatrix.com/graphql",
    headers={"Authorization": "Bearer YOUR_API_KEY"}
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Query
query = gql("""
    query GetAgent($id: ID!) {
        agent(id: $id) {
            id
            name
            type
            status
            capabilities
            knowledgeBases {
                id
                name
                type
            }
        }
    }
""")

result = client.execute(query, variable_values={"id": "agent_123"})
print(result)

# Mutation
mutation = gql("""
    mutation CreateAgent($input: CreateAgentInput!) {
        createAgent(input: $input) {
            id
            name
            type
            status
        }
    }
""")

variables = {
    "input": {
        "name": "Python Agent",
        "type": "ASSISTANT",
        "capabilities": ["text_processing", "knowledge_query"]
    }
}

result = client.execute(mutation, variable_values=variables)
print(result)
```

### Subscriptions with WebSocket
```javascript
import { GraphQLWsLink } from '@apollo/client/link/subscriptions';
import { createClient } from 'graphql-ws';

const wsLink = new GraphQLWsLink(createClient({
  url: 'wss://api.aimatrix.com/graphql',
  connectionParams: {
    Authorization: `Bearer ${YOUR_API_KEY}`,
  },
}));

const AGENT_EXECUTIONS_SUBSCRIPTION = gql`
  subscription AgentExecutions($agentId: ID!) {
    agentExecutions(agentId: $agentId) {
      id
      query
      response
      status
      createdAt
    }
  }
`;

const { data, loading } = useSubscription(AGENT_EXECUTIONS_SUBSCRIPTION, {
  variables: { agentId: 'agent_123' }
});
```

## Performance Optimization

### Query Optimization
1. **Use fragments** to avoid duplication
2. **Request only needed fields** to reduce payload size
3. **Implement pagination** for large datasets
4. **Use aliases** to batch multiple queries
5. **Cache queries** with proper cache policies

### Caching Strategy
```javascript
const client = new ApolloClient({
  cache: new InMemoryCache({
    typePolicies: {
      Agent: {
        fields: {
          executions: {
            merge(existing = [], incoming) {
              return [...existing, ...incoming];
            }
          }
        }
      }
    }
  })
});
```

### DataLoader Pattern
```javascript
const knowledgeBaseLoader = new DataLoader(async (ids) => {
  const query = gql`
    query GetKnowledgeBases($ids: [ID!]!) {
      knowledgeBases(ids: $ids) {
        id
        name
        type
      }
    }
  `;
  
  const result = await client.query({ query, variables: { ids } });
  return ids.map(id => result.data.knowledgeBases.find(kb => kb.id === id));
});
```

## Schema Introspection

### Get Schema Information
```graphql
query IntrospectionQuery {
  __schema {
    types {
      name
      kind
      description
      fields {
        name
        type {
          name
          kind
        }
      }
    }
  }
}
```

### Get Type Information
```graphql
query GetTypeInfo {
  __type(name: "Agent") {
    name
    kind
    description
    fields {
      name
      type {
        name
        kind
      }
      description
    }
  }
}
```

---

For more examples and advanced GraphQL patterns, see our [GraphQL Examples](/reference/apis/examples/#graphql-examples) section.