---
title: AIMatrix SDKs
description: Comprehensive SDK documentation for Kotlin, Python, TypeScript, C#, and Java - build intelligent agents and digital twins with first-class language support.
weight: 10
---

Build intelligent agents and digital twins with AIMatrix's comprehensive SDK suite. Our SDKs provide first-class support across five major programming languages, enabling you to create powerful AI applications regardless of your technology stack.

## Supported Languages

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin: 30px 0;">
  
  <div style="border: 2px solid #00ff00; padding: 20px; border-radius: 8px;">
    <h3>🎯 Kotlin (First-Class)</h3>
    <p><strong>Primary SDK with full feature set</strong></p>
    <ul style="list-style: none; padding: 0; margin: 10px 0;">
      <li>✅ Complete API coverage</li>
      <li>✅ Coroutines support</li>
      <li>✅ Type-safe builders</li>
      <li>✅ Android/JVM compatible</li>
    </ul>
    <a href="#kotlin-sdk" style="color: #00ff00;">→ Get Started</a>
  </div>

  <div style="border: 1px solid #00ff00; padding: 20px; border-radius: 8px;">
    <h3>🐍 Python</h3>
    <p>Full-featured with async support</p>
    <ul style="list-style: none; padding: 0; margin: 10px 0;">
      <li>✅ AsyncIO integration</li>
      <li>✅ Pydantic models</li>
      <li>✅ Type hints</li>
      <li>✅ Jupyter support</li>
    </ul>
    <a href="#python-sdk" style="color: #00ff00;">→ Get Started</a>
  </div>

  <div style="border: 1px solid #00ff00; padding: 20px; border-radius: 8px;">
    <h3>⚡ TypeScript</h3>
    <p>Modern JS/TS with full type safety</p>
    <ul style="list-style: none; padding: 0; margin: 10px 0;">
      <li>✅ Promise-based APIs</li>
      <li>✅ Browser & Node.js</li>
      <li>✅ ESM & CommonJS</li>
      <li>✅ React hooks</li>
    </ul>
    <a href="#typescript-sdk" style="color: #00ff00;">→ Get Started</a>
  </div>

  <div style="border: 1px solid #00ff00; padding: 20px; border-radius: 8px;">
    <h3>🔷 C#</h3>
    <p>.NET ecosystem integration</p>
    <ul style="list-style: none; padding: 0; margin: 10px 0;">
      <li>✅ Task-based async</li>
      <li>✅ .NET 6+ support</li>
      <li>✅ Dependency injection</li>
      <li>✅ Unity3D compatible</li>
    </ul>
    <a href="#csharp-sdk" style="color: #00ff00;">→ Get Started</a>
  </div>

  <div style="border: 1px solid #00ff00; padding: 20px; border-radius: 8px;">
    <h3>☕ Java</h3>
    <p>Enterprise-ready JVM integration</p>
    <ul style="list-style: none; padding: 0; margin: 10px 0;">
      <li>✅ CompletableFuture</li>
      <li>✅ Spring Boot</li>
      <li>✅ Maven/Gradle</li>
      <li>✅ Jakarta EE</li>
    </ul>
    <a href="#java-sdk" style="color: #00ff00;">→ Get Started</a>
  </div>

</div>

## Core SDK Features

All SDKs provide consistent APIs for:

- **Agent Management**: Create, configure, and orchestrate AI agents
- **TwinML Integration**: Build and deploy digital twins with machine learning
- **Workspace Operations**: Manage development environments and deployments  
- **Hub Integration**: Connect to the AIMatrix Hub ecosystem
- **Real-time Communication**: WebSocket and event-driven architectures
- **Authentication**: Secure API key and OAuth2 flows

---

# Kotlin SDK {#kotlin-sdk}

**First-class SDK with complete feature coverage and idiomatic Kotlin design patterns.**

## Installation & Setup

### Gradle (Kotlin DSL)
```kotlin
dependencies {
    implementation("com.aimatrix:kotlin-sdk:2.0.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
}
```

### Maven
```xml
<dependency>
    <groupId>com.aimatrix</groupId>
    <artifactId>kotlin-sdk</artifactId>
    <version>2.0.0</version>
</dependency>
```

### Quick Start

```kotlin
import com.aimatrix.sdk.AIMatrixClient
import com.aimatrix.sdk.agent.AgentBuilder
import com.aimatrix.sdk.auth.ApiKeyAuth
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    // Initialize client with authentication
    val client = AIMatrixClient {
        authentication = ApiKeyAuth("your-api-key")
        environment = Environment.PRODUCTION
        timeout = 30.seconds
    }
    
    // Create your first agent
    val agent = client.agents.create {
        name = "business-assistant"
        description = "Intelligent business operations assistant"
        model = "gpt-4"
        capabilities = listOf(
            Capability.VISION,
            Capability.FUNCTION_CALLING,
            Capability.REAL_TIME_PROCESSING
        )
    }
    
    println("Agent created: ${agent.id}")
}
```

## Core API Classes

### AIMatrixClient

Primary entry point for all SDK operations:

```kotlin
class AIMatrixClient private constructor(
    val agents: AgentManager,
    val twins: TwinManager,
    val workspace: WorkspaceManager,
    val hub: HubManager,
    val auth: AuthenticationManager
) {
    companion object {
        operator fun invoke(configure: ClientBuilder.() -> Unit): AIMatrixClient
    }
}

// Usage
val client = AIMatrixClient {
    authentication = ApiKeyAuth("your-key")
    retryPolicy = RetryPolicy.exponentialBackoff(maxRetries = 3)
    logging = LogLevel.INFO
}
```

### AgentManager

Manage AI agent lifecycle and operations:

```kotlin
interface AgentManager {
    suspend fun create(configure: AgentBuilder.() -> Unit): Agent
    suspend fun get(agentId: String): Agent?
    suspend fun list(filter: AgentFilter = AgentFilter.ALL): List<Agent>
    suspend fun update(agentId: String, configure: AgentBuilder.() -> Unit): Agent
    suspend fun delete(agentId: String): Boolean
    suspend fun invoke(agentId: String, request: InvocationRequest): InvocationResult
}
```

### TwinManager

Digital twin operations with TwinML integration:

```kotlin
interface TwinManager {
    suspend fun create(configure: TwinBuilder.() -> Unit): DigitalTwin
    suspend fun train(twinId: String, dataset: Dataset): TrainingJob
    suspend fun predict(twinId: String, input: TwinInput): PredictionResult
    suspend fun deploy(twinId: String, environment: DeploymentEnvironment): Deployment
}
```

## Agent Creation & Management

### Creating Agents

```kotlin
// Simple agent creation
val chatAgent = client.agents.create {
    name = "customer-service"
    description = "24/7 customer support assistant"
    model = "claude-3-sonnet"
    
    // Configure capabilities
    capabilities {
        +Capability.MULTIMODAL_VISION
        +Capability.FUNCTION_CALLING
        +Capability.MEMORY
    }
    
    // Add tools
    tools {
        +tool("get_order_status") {
            description = "Retrieve customer order status"
            parameters = jsonSchema {
                string("order_id") { description = "Order identifier" }
            }
            implementation = ::getOrderStatus
        }
    }
    
    // System prompt
    systemPrompt = """
        You are a helpful customer service assistant.
        Always be polite and provide accurate information.
    """.trimIndent()
}
```

### Advanced Agent Configuration

```kotlin
val complexAgent = client.agents.create {
    name = "data-analyst"
    description = "Advanced data analysis and reporting"
    
    // Model configuration
    model {
        provider = ModelProvider.OPENAI
        name = "gpt-4"
        temperature = 0.2
        maxTokens = 4000
    }
    
    // Memory configuration
    memory {
        type = MemoryType.CONVERSATION
        maxSize = 10000
        persistenceStrategy = PersistenceStrategy.DATABASE
    }
    
    // Workspace integration
    workspace {
        workspaceId = "analytics-workspace"
        tools = listOf("python-executor", "chart-generator")
        dataAccess = DataAccess.READ_WRITE
    }
    
    // Security settings
    security {
        accessLevel = AccessLevel.RESTRICTED
        allowedDomains = listOf("company.com", "api.company.com")
        rateLimits {
            requestsPerMinute = 100
            tokensPerMinute = 50000
        }
    }
}
```

### Agent Invocation

```kotlin
// Simple invocation
val result = client.agents.invoke(agentId = "customer-service") {
    message = "What's the status of order #12345?"
    context {
        userId = "user123"
        sessionId = "session456"
    }
}

println("Response: ${result.message}")

// Streaming invocation
client.agents.invokeStream(agentId = "data-analyst") {
    message = "Analyze sales data for Q4 2024"
    onToken { token -> print(token) }
    onComplete { result -> println("\nAnalysis complete: ${result.summary}") }
    onError { error -> println("Error: ${error.message}") }
}
```

## TwinML Integration

### Digital Twin Creation

```kotlin
val productTwin = client.twins.create {
    name = "inventory-predictor"
    description = "Predict inventory needs based on historical data"
    
    // Model configuration
    model {
        type = TwinModelType.REGRESSION
        algorithm = Algorithm.RANDOM_FOREST
        features = listOf(
            "sales_history",
            "seasonal_patterns", 
            "market_trends",
            "promotion_calendar"
        )
        target = "required_inventory"
    }
    
    // Data sources
    dataSources {
        +dataSource("sales-db") {
            type = DataSourceType.POSTGRESQL
            connectionString = "postgresql://localhost/sales"
            tables = listOf("sales", "products", "inventory")
        }
        
        +dataSource("market-api") {
            type = DataSourceType.REST_API
            endpoint = "https://api.marketdata.com/trends"
            authentication = BearerToken("token")
        }
    }
    
    // Training configuration
    training {
        splitStrategy = SplitStrategy.TIME_BASED
        trainRatio = 0.8
        validationRatio = 0.2
        hyperparameters {
            "n_estimators" to 100
            "max_depth" to 10
            "min_samples_split" to 5
        }
    }
}
```

### Training Digital Twins

```kotlin
// Prepare training dataset
val dataset = Dataset.builder()
    .fromQuery("SELECT * FROM sales_with_features WHERE date >= '2023-01-01'")
    .withFeatures(listOf("sales_volume", "season", "promotion", "price"))
    .withTarget("inventory_needed")
    .build()

// Start training job
val trainingJob = client.twins.train(productTwin.id, dataset)

// Monitor training progress
val job = client.twins.getTrainingJob(trainingJob.id)
when (job.status) {
    TrainingStatus.RUNNING -> println("Training in progress: ${job.progress}%")
    TrainingStatus.COMPLETED -> {
        println("Training completed!")
        println("Accuracy: ${job.metrics.accuracy}")
        println("R² Score: ${job.metrics.r2Score}")
    }
    TrainingStatus.FAILED -> println("Training failed: ${job.error}")
}
```

### Making Predictions

```kotlin
// Single prediction
val prediction = client.twins.predict(productTwin.id) {
    features {
        "sales_volume" to 1500
        "season" to "winter"
        "promotion" to true
        "price" to 29.99
    }
}

println("Predicted inventory needed: ${prediction.value}")
println("Confidence: ${prediction.confidence}")

// Batch predictions
val batchPredictions = client.twins.predictBatch(productTwin.id) {
    inputs = listOf(
        twinInput {
            "sales_volume" to 1500
            "season" to "winter"
            "promotion" to true
        },
        twinInput {
            "sales_volume" to 2000
            "season" to "spring"
            "promotion" to false
        }
    )
}
```

## Workspace Operations

### Workspace Management

```kotlin
// Create development workspace
val workspace = client.workspace.create {
    name = "ml-experiments"
    description = "Machine learning experimentation environment"
    
    // Runtime configuration
    runtime {
        type = RuntimeType.PYTHON
        version = "3.11"
        packages = listOf(
            "tensorflow==2.13.0",
            "pandas==2.1.0",
            "scikit-learn==1.3.0"
        )
    }
    
    // Resource allocation
    resources {
        cpu = "4 cores"
        memory = "16GB"
        gpu = GpuType.T4
        storage = "100GB"
    }
    
    // Access control
    access {
        +member("user@company.com", Role.OWNER)
        +member("team@company.com", Role.COLLABORATOR)
    }
}

// Deploy to workspace
val deployment = client.workspace.deploy(workspace.id) {
    artifact = "my-model-v1.0.jar"
    environment = mapOf(
        "MODEL_PATH" to "/models/inventory-predictor",
        "API_KEY" to client.auth.apiKey
    )
    scaling {
        minInstances = 1
        maxInstances = 10
        targetCpuUtilization = 70
    }
}
```

### Code Execution

```kotlin
// Execute Python code in workspace
val result = client.workspace.execute(workspace.id) {
    language = Language.PYTHON
    code = """
        import pandas as pd
        import numpy as np
        
        # Load data
        data = pd.read_csv('/data/sales.csv')
        
        # Analyze trends
        monthly_trends = data.groupby('month').sum()
        print(f"Average monthly sales: {monthly_trends.mean()}")
        
        monthly_trends
    """.trimIndent()
}

when (result) {
    is ExecutionResult.Success -> {
        println("Output: ${result.output}")
        println("Variables: ${result.variables}")
    }
    is ExecutionResult.Error -> {
        println("Execution failed: ${result.error}")
        println("Stack trace: ${result.stackTrace}")
    }
}
```

## Hub Integration

### Publishing to Hub

```kotlin
// Publish agent to AIMatrix Hub
val publication = client.hub.publish {
    artifact = HubArtifact.AGENT
    agentId = chatAgent.id
    
    metadata {
        title = "Customer Service Assistant"
        description = "Intelligent 24/7 customer support"
        category = HubCategory.BUSINESS
        tags = listOf("customer-service", "support", "chatbot")
        pricing = PricingModel.FREE
    }
    
    documentation {
        readme = "README.md"
        examples = listOf("examples/basic-usage.kt", "examples/advanced.kt")
        apiDocs = "docs/api.md"
    }
    
    requirements {
        minimumVersion = "2.0.0"
        requiredCapabilities = listOf(Capability.FUNCTION_CALLING)
    }
}

// Check publication status
val status = client.hub.getPublicationStatus(publication.id)
when (status) {
    PublicationStatus.PENDING -> println("Under review")
    PublicationStatus.APPROVED -> println("Published successfully!")
    PublicationStatus.REJECTED -> println("Rejected: ${status.reason}")
}
```

### Installing from Hub

```kotlin
// Browse Hub marketplace
val searchResults = client.hub.search {
    query = "data analysis"
    category = HubCategory.ANALYTICS
    pricing = PricingModel.FREE
    minRating = 4.0
}

// Install agent from Hub
val installedAgent = client.hub.install("marketplace://data-analyst-pro") {
    workspace = "analytics-workspace"
    configuration {
        "max_processing_time" to "300s"
        "output_format" to "json"
    }
}
```

## Authentication

### API Key Authentication

```kotlin
val client = AIMatrixClient {
    authentication = ApiKeyAuth("amx_sk_your_secret_key")
    environment = Environment.PRODUCTION
}
```

### OAuth2 Flow

```kotlin
// OAuth2 with PKCE
val oauthClient = AIMatrixClient {
    authentication = OAuth2Auth {
        clientId = "your-client-id"
        redirectUri = "https://myapp.com/callback"
        scopes = listOf("agents:read", "agents:write", "twins:manage")
        usePkce = true
    }
    environment = Environment.PRODUCTION
}

// Handle OAuth flow
val authUrl = oauthClient.auth.getAuthorizationUrl()
println("Visit: $authUrl")

// After user authorizes, exchange code for tokens
val tokens = oauthClient.auth.exchangeCodeForTokens("authorization_code")
```

### Service Account Authentication

```kotlin
val serviceClient = AIMatrixClient {
    authentication = ServiceAccountAuth {
        serviceAccountId = "service-account@project.iam.gserviceaccount.com"
        privateKeyPath = "path/to/service-account-key.json"
        scopes = listOf("https://www.googleapis.com/auth/aimatrix")
    }
}
```

## Code Examples

### Multi-Modal Agent

```kotlin
val visionAgent = client.agents.create {
    name = "document-processor"
    capabilities = listOf(Capability.VISION, Capability.OCR)
    
    tools {
        +tool("extract_text") { image: ByteArray ->
            // OCR implementation
            ocrService.extractText(image)
        }
        
        +tool("analyze_layout") { image: ByteArray ->
            // Document layout analysis
            layoutAnalyzer.analyze(image)
        }
    }
}

// Process document image
val result = client.agents.invoke(visionAgent.id) {
    message = "Extract all text and analyze the document structure"
    attachments = listOf(
        Attachment.image("document.pdf", imageBytes)
    )
}
```

### Real-time Streaming

```kotlin
// Set up real-time agent communication
val streamingSession = client.agents.createStream(agentId) {
    onMessage { message -> 
        println("Agent: ${message.content}")
    }
    
    onFunctionCall { call ->
        println("Calling function: ${call.name}")
        // Handle function execution
    }
    
    onError { error ->
        println("Stream error: ${error.message}")
    }
}

// Send messages to agent
streamingSession.send("Analyze the current market trends")
streamingSession.send("Generate a summary report")
```

### Batch Operations

```kotlin
// Process multiple requests in parallel
val requests = listOf(
    InvocationRequest("Summarize document 1", attachments = listOf(doc1)),
    InvocationRequest("Summarize document 2", attachments = listOf(doc2)),
    InvocationRequest("Summarize document 3", attachments = listOf(doc3))
)

val results = client.agents.invokeBatch(agentId, requests) {
    concurrency = 3
    timeout = 60.seconds
    retryPolicy = RetryPolicy.exponentialBackoff()
}

results.forEach { result ->
    when (result) {
        is BatchResult.Success -> println("Summary: ${result.response.message}")
        is BatchResult.Failure -> println("Failed: ${result.error.message}")
    }
}
```

## Best Practices

### Error Handling

```kotlin
// Comprehensive error handling
try {
    val result = client.agents.invoke(agentId) {
        message = "Process this request"
        timeout = 30.seconds
    }
    
    when (result.status) {
        InvocationStatus.SUCCESS -> handleSuccess(result)
        InvocationStatus.PARTIAL_SUCCESS -> handlePartialSuccess(result)
        InvocationStatus.TIMEOUT -> handleTimeout(result)
    }
    
} catch (e: AIMatrixException) {
    when (e) {
        is AuthenticationException -> refreshTokensAndRetry()
        is RateLimitException -> backoffAndRetry(e.retryAfter)
        is ValidationException -> handleValidationError(e.errors)
        is ServiceUnavailableException -> useCircuitBreaker()
        else -> logAndAlert(e)
    }
}
```

### Resource Management

```kotlin
// Use resource management for cleanup
AIMatrixClient {
    authentication = ApiKeyAuth("key")
}.use { client ->
    // Perform operations
    val agent = client.agents.create { /* config */ }
    
    // Resources automatically cleaned up
}

// Manual resource management
val client = AIMatrixClient { /* config */ }
try {
    // Operations
} finally {
    client.close()
}
```

### Configuration Management

```kotlin
// Environment-based configuration
val client = AIMatrixClient {
    when (System.getenv("ENVIRONMENT")) {
        "development" -> {
            environment = Environment.DEVELOPMENT
            logging = LogLevel.DEBUG
            timeout = 60.seconds
        }
        "staging" -> {
            environment = Environment.STAGING  
            logging = LogLevel.INFO
            timeout = 30.seconds
        }
        "production" -> {
            environment = Environment.PRODUCTION
            logging = LogLevel.WARN
            timeout = 15.seconds
            retryPolicy = RetryPolicy.exponentialBackoff(maxRetries = 3)
        }
    }
    
    authentication = ApiKeyAuth(System.getenv("AIMATRIX_API_KEY"))
}
```

---

# Python SDK {#python-sdk}

**Full-featured Python SDK with async support, type hints, and Pydantic models.**

## Installation & Setup

```bash
# Install from PyPI
pip install aimatrix

# With optional dependencies
pip install aimatrix[async,vision,audio]

# Development version
pip install git+https://github.com/aimatrix/python-sdk.git
```

### Quick Start

```python
import asyncio
from aimatrix import AIMatrixClient, Agent, Capability

async def main():
    # Initialize client
    async with AIMatrixClient("your-api-key") as client:
        # Create agent
        agent = await client.agents.create(
            name="business-assistant",
            description="Intelligent business operations assistant",
            model="gpt-4",
            capabilities=[Capability.VISION, Capability.FUNCTION_CALLING]
        )
        
        # Invoke agent
        result = await client.agents.invoke(
            agent.id,
            message="What's the status of our Q4 sales?"
        )
        
        print(f"Response: {result.message}")

# Run the async function
asyncio.run(main())
```

## Core API Classes

### AIMatrixClient

```python
from aimatrix import AIMatrixClient
from aimatrix.auth import ApiKeyAuth, OAuth2Auth
from aimatrix.config import Environment, RetryPolicy

# Basic initialization
client = AIMatrixClient("your-api-key")

# Advanced configuration
client = AIMatrixClient(
    auth=ApiKeyAuth("your-api-key"),
    environment=Environment.PRODUCTION,
    timeout=30.0,
    retry_policy=RetryPolicy.exponential_backoff(max_retries=3),
    base_url="https://api.aimatrix.com/v1"
)
```

### Agent Management

```python
from aimatrix.agents import AgentManager, AgentBuilder
from aimatrix.models import Agent, InvocationRequest
from typing import List, Optional

class AIMatrixClient:
    def __init__(self, api_key: str):
        self.agents = AgentManager(api_key)
        self.twins = TwinManager(api_key) 
        self.workspace = WorkspaceManager(api_key)
        self.hub = HubManager(api_key)

# Agent operations
async def agent_example():
    async with AIMatrixClient("key") as client:
        # Create agent with type-safe builder
        agent = await client.agents.create(
            name="customer-service",
            description="24/7 support assistant",
            model="claude-3-sonnet",
            capabilities=[Capability.MULTIMODAL_VISION],
            tools=[
                {
                    "name": "get_order_status",
                    "description": "Retrieve order status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {"type": "string"}
                        }
                    }
                }
            ]
        )
        
        # List agents with filtering
        agents: List[Agent] = await client.agents.list(
            filter_by_capability=Capability.VISION,
            limit=10
        )
        
        # Update agent configuration
        updated_agent = await client.agents.update(
            agent.id,
            description="Enhanced customer service with vision",
            model="gpt-4-vision-preview"
        )
```

### TwinML Integration

```python
from aimatrix.twins import DigitalTwin, Dataset, TrainingJob
from aimatrix.models import TwinModelType, Algorithm
import pandas as pd

# Create digital twin
async def create_inventory_twin():
    async with AIMatrixClient("key") as client:
        twin = await client.twins.create(
            name="inventory-predictor",
            description="Predict inventory needs",
            model_config={
                "type": TwinModelType.REGRESSION,
                "algorithm": Algorithm.RANDOM_FOREST,
                "features": [
                    "sales_history",
                    "seasonal_patterns", 
                    "market_trends"
                ],
                "target": "required_inventory"
            },
            data_sources=[
                {
                    "name": "sales-db",
                    "type": "postgresql",
                    "connection_string": "postgresql://localhost/sales"
                }
            ]
        )
        
        return twin

# Train the twin
async def train_twin(twin_id: str):
    async with AIMatrixClient("key") as client:
        # Load training data
        df = pd.read_csv("sales_data.csv")
        dataset = Dataset.from_dataframe(
            df,
            features=["sales_volume", "season", "promotion"],
            target="inventory_needed"
        )
        
        # Start training
        job = await client.twins.train(twin_id, dataset)
        
        # Monitor progress
        while job.status == "running":
            await asyncio.sleep(5)
            job = await client.twins.get_training_job(job.id)
            print(f"Training progress: {job.progress}%")
        
        if job.status == "completed":
            print(f"Training completed! Accuracy: {job.metrics.accuracy}")
            return job
        else:
            raise Exception(f"Training failed: {job.error}")

# Make predictions
async def predict_inventory(twin_id: str, features: dict):
    async with AIMatrixClient("key") as client:
        prediction = await client.twins.predict(
            twin_id,
            features=features
        )
        return prediction
```

## Workspace Operations

```python
from aimatrix.workspace import Workspace, Runtime, ExecutionResult

async def workspace_operations():
    async with AIMatrixClient("key") as client:
        # Create workspace
        workspace = await client.workspace.create(
            name="ml-experiments",
            runtime=Runtime(
                type="python",
                version="3.11",
                packages=["tensorflow==2.13.0", "pandas==2.1.0"]
            ),
            resources={
                "cpu": "4 cores",
                "memory": "16GB", 
                "gpu": "T4"
            }
        )
        
        # Execute code
        result = await client.workspace.execute(
            workspace.id,
            code="""
import pandas as pd
data = pd.read_csv('/data/sales.csv')
print(f"Loaded {len(data)} records")
data.head()
            """,
            language="python"
        )
        
        if result.success:
            print(f"Output: {result.output}")
        else:
            print(f"Error: {result.error}")
```

## Hub Integration

```python
from aimatrix.hub import HubArtifact, HubCategory, PricingModel

async def hub_operations():
    async with AIMatrixClient("key") as client:
        # Publish agent to Hub
        publication = await client.hub.publish(
            artifact_type=HubArtifact.AGENT,
            agent_id="agent-123",
            metadata={
                "title": "Customer Service Assistant",
                "description": "24/7 intelligent support",
                "category": HubCategory.BUSINESS,
                "tags": ["customer-service", "support"],
                "pricing": PricingModel.FREE
            }
        )
        
        # Search Hub marketplace
        results = await client.hub.search(
            query="data analysis",
            category=HubCategory.ANALYTICS,
            min_rating=4.0
        )
        
        # Install from Hub
        agent = await client.hub.install(
            "marketplace://data-analyst-pro",
            workspace="analytics-workspace"
        )
```

## Authentication

```python
from aimatrix.auth import ApiKeyAuth, OAuth2Auth, ServiceAccountAuth

# API Key authentication
client = AIMatrixClient(auth=ApiKeyAuth("amx_sk_your_key"))

# OAuth2 flow
oauth_client = AIMatrixClient(
    auth=OAuth2Auth(
        client_id="your-client-id",
        redirect_uri="https://myapp.com/callback",
        scopes=["agents:read", "agents:write"]
    )
)

# Get authorization URL
auth_url = await oauth_client.auth.get_authorization_url()
print(f"Visit: {auth_url}")

# Exchange code for tokens
tokens = await oauth_client.auth.exchange_code("auth_code")

# Service account
service_client = AIMatrixClient(
    auth=ServiceAccountAuth(
        service_account_file="service-account.json",
        scopes=["https://www.googleapis.com/auth/aimatrix"]
    )
)
```

## Code Examples

### Streaming Responses

```python
async def streaming_example():
    async with AIMatrixClient("key") as client:
        # Stream agent responses
        async for chunk in client.agents.stream(
            agent_id="agent-123",
            message="Analyze quarterly sales data"
        ):
            if chunk.type == "message":
                print(chunk.content, end="")
            elif chunk.type == "function_call":
                print(f"\nCalling: {chunk.function_name}")
            elif chunk.type == "error":
                print(f"\nError: {chunk.error}")
```

### Batch Processing

```python
from aimatrix.batch import BatchProcessor

async def batch_example():
    async with AIMatrixClient("key") as client:
        processor = BatchProcessor(client, concurrency=5)
        
        requests = [
            {"message": "Summarize document 1", "attachments": [doc1]},
            {"message": "Summarize document 2", "attachments": [doc2]},
            {"message": "Summarize document 3", "attachments": [doc3]},
        ]
        
        async for result in processor.process_batch(
            agent_id="summarizer",
            requests=requests
        ):
            if result.success:
                print(f"Summary: {result.response.message}")
            else:
                print(f"Failed: {result.error}")
```

### Error Handling

```python
from aimatrix.exceptions import (
    AIMatrixException,
    AuthenticationException,
    RateLimitException,
    ValidationException
)

async def error_handling_example():
    async with AIMatrixClient("key") as client:
        try:
            result = await client.agents.invoke(
                "agent-123",
                message="Process this request",
                timeout=30.0
            )
        except AuthenticationException:
            # Refresh tokens and retry
            await client.auth.refresh_tokens()
        except RateLimitException as e:
            # Backoff and retry
            await asyncio.sleep(e.retry_after)
        except ValidationException as e:
            # Handle validation errors
            for error in e.errors:
                print(f"Validation error: {error}")
        except AIMatrixException as e:
            # Handle general API errors
            print(f"API error: {e.message}")
```

## Best Practices

### Async Context Management

```python
# Always use async context manager
async with AIMatrixClient("key") as client:
    # Automatic cleanup
    agent = await client.agents.create(...)

# Manual cleanup if needed
client = AIMatrixClient("key")
try:
    # operations
    pass
finally:
    await client.close()
```

### Type Hints and Validation

```python
from typing import List, Optional
from pydantic import BaseModel

class AgentRequest(BaseModel):
    message: str
    context: Optional[dict] = None
    attachments: List[str] = []

async def typed_invoke(
    client: AIMatrixClient,
    agent_id: str, 
    request: AgentRequest
) -> InvocationResult:
    return await client.agents.invoke(
        agent_id,
        message=request.message,
        context=request.context,
        attachments=request.attachments
    )
```

---

# TypeScript SDK {#typescript-sdk}

**Modern JavaScript/TypeScript SDK with full type safety and promise-based APIs.**

## Installation & Setup

```bash
# NPM
npm install @aimatrix/sdk

# Yarn
yarn add @aimatrix/sdk

# PNPM
pnpm add @aimatrix/sdk
```

### Quick Start

```typescript
import { AIMatrixClient, Capability } from '@aimatrix/sdk';

// Initialize client
const client = new AIMatrixClient({
  apiKey: 'your-api-key',
  environment: 'production'
});

// Create and invoke agent
async function main() {
  const agent = await client.agents.create({
    name: 'business-assistant',
    description: 'Intelligent business operations assistant',
    model: 'gpt-4',
    capabilities: [Capability.VISION, Capability.FUNCTION_CALLING]
  });

  const result = await client.agents.invoke(agent.id, {
    message: "What's our current sales performance?"
  });

  console.log('Response:', result.message);
}

main().catch(console.error);
```

## Core Types & Interfaces

```typescript
// Client configuration
interface AIMatrixConfig {
  apiKey?: string;
  baseUrl?: string;
  environment?: 'development' | 'staging' | 'production';
  timeout?: number;
  retryPolicy?: RetryPolicy;
  auth?: AuthProvider;
}

// Agent interface
interface Agent {
  id: string;
  name: string;
  description: string;
  model: string;
  capabilities: Capability[];
  tools: Tool[];
  created_at: string;
  updated_at: string;
}

// Agent creation parameters
interface CreateAgentParams {
  name: string;
  description: string;
  model: string;
  capabilities?: Capability[];
  tools?: ToolDefinition[];
  system_prompt?: string;
  memory?: MemoryConfig;
  security?: SecurityConfig;
}
```

## Agent Management

```typescript
import { 
  AIMatrixClient, 
  Agent, 
  CreateAgentParams,
  InvocationRequest,
  InvocationResult 
} from '@aimatrix/sdk';

class AgentManager {
  constructor(private client: AIMatrixClient) {}

  // Create agent with comprehensive configuration
  async createAdvancedAgent(): Promise<Agent> {
    return await this.client.agents.create({
      name: 'customer-service',
      description: '24/7 customer support assistant',
      model: 'claude-3-sonnet',
      capabilities: [Capability.MULTIMODAL_VISION, Capability.FUNCTION_CALLING],
      
      tools: [
        {
          name: 'get_order_status',
          description: 'Retrieve customer order status',
          parameters: {
            type: 'object',
            properties: {
              order_id: { type: 'string', description: 'Order identifier' }
            },
            required: ['order_id']
          }
        },
        {
          name: 'create_support_ticket',
          description: 'Create a new support ticket',
          parameters: {
            type: 'object',
            properties: {
              title: { type: 'string' },
              description: { type: 'string' },
              priority: { type: 'string', enum: ['low', 'medium', 'high'] }
            },
            required: ['title', 'description']
          }
        }
      ],
      
      system_prompt: `
        You are a helpful customer service assistant.
        Always be polite and provide accurate information.
        Escalate complex issues to human agents when necessary.
      `,
      
      memory: {
        type: 'conversation',
        max_size: 10000,
        persistence: 'database'
      },
      
      security: {
        access_level: 'restricted',
        allowed_domains: ['company.com'],
        rate_limits: {
          requests_per_minute: 100,
          tokens_per_minute: 50000
        }
      }
    });
  }

  // Invoke agent with streaming
  async streamingInvocation(agentId: string): Promise<void> {
    const stream = await this.client.agents.stream(agentId, {
      message: 'Analyze our Q4 performance',
      context: {
        user_id: 'user123',
        session_id: 'session456'
      }
    });

    for await (const chunk of stream) {
      switch (chunk.type) {
        case 'message':
          process.stdout.write(chunk.content);
          break;
        case 'function_call':
          console.log(`\nCalling function: ${chunk.function_name}`);
          break;
        case 'error':
          console.error(`\nError: ${chunk.error}`);
          break;
      }
    }
  }
}
```

## Digital Twin Operations

```typescript
import { 
  DigitalTwin, 
  TwinModelType, 
  Algorithm,
  Dataset,
  TrainingJob 
} from '@aimatrix/sdk';

interface TwinConfig {
  name: string;
  description: string;
  model: {
    type: TwinModelType;
    algorithm: Algorithm;
    features: string[];
    target: string;
  };
  dataSources: DataSource[];
}

class TwinManager {
  constructor(private client: AIMatrixClient) {}

  async createInventoryTwin(): Promise<DigitalTwin> {
    return await this.client.twins.create({
      name: 'inventory-predictor',
      description: 'Predict inventory needs based on historical data',
      
      model: {
        type: TwinModelType.REGRESSION,
        algorithm: Algorithm.RANDOM_FOREST,
        features: [
          'sales_history',
          'seasonal_patterns',
          'market_trends',
          'promotion_calendar'
        ],
        target: 'required_inventory'
      },
      
      dataSources: [
        {
          name: 'sales-db',
          type: 'postgresql',
          connectionString: 'postgresql://localhost/sales',
          tables: ['sales', 'products', 'inventory']
        },
        {
          name: 'market-api',
          type: 'rest_api',
          endpoint: 'https://api.marketdata.com/trends',
          authentication: {
            type: 'bearer',
            token: process.env.MARKET_API_TOKEN
          }
        }
      ],
      
      training: {
        splitStrategy: 'time_based',
        trainRatio: 0.8,
        validationRatio: 0.2,
        hyperparameters: {
          n_estimators: 100,
          max_depth: 10,
          min_samples_split: 5
        }
      }
    });
  }

  async trainTwin(twinId: string, dataset: Dataset): Promise<TrainingJob> {
    const job = await this.client.twins.train(twinId, dataset);
    
    // Monitor training progress
    const monitor = setInterval(async () => {
      const status = await this.client.twins.getTrainingJob(job.id);
      
      switch (status.status) {
        case 'running':
          console.log(`Training progress: ${status.progress}%`);
          break;
        case 'completed':
          console.log('Training completed!');
          console.log(`Accuracy: ${status.metrics.accuracy}`);
          console.log(`R² Score: ${status.metrics.r2Score}`);
          clearInterval(monitor);
          break;
        case 'failed':
          console.error(`Training failed: ${status.error}`);
          clearInterval(monitor);
          break;
      }
    }, 5000);
    
    return job;
  }

  async makePrediction(twinId: string, features: Record<string, any>) {
    const prediction = await this.client.twins.predict(twinId, { features });
    
    return {
      value: prediction.value,
      confidence: prediction.confidence,
      explanation: prediction.explanation
    };
  }
}
```

## Workspace Management

```typescript
import { Workspace, Runtime, ExecutionResult } from '@aimatrix/sdk';

interface WorkspaceConfig {
  name: string;
  description: string;
  runtime: {
    type: 'python' | 'node' | 'r';
    version: string;
    packages: string[];
  };
  resources: {
    cpu: string;
    memory: string;
    gpu?: string;
    storage: string;
  };
}

class WorkspaceManager {
  constructor(private client: AIMatrixClient) {}

  async createMLWorkspace(): Promise<Workspace> {
    return await this.client.workspace.create({
      name: 'ml-experiments',
      description: 'Machine learning experimentation environment',
      
      runtime: {
        type: 'python',
        version: '3.11',
        packages: [
          'tensorflow==2.13.0',
          'pandas==2.1.0',
          'scikit-learn==1.3.0',
          'matplotlib==3.7.0'
        ]
      },
      
      resources: {
        cpu: '4 cores',
        memory: '16GB',
        gpu: 'T4',
        storage: '100GB'
      },
      
      access: [
        { email: 'user@company.com', role: 'owner' },
        { email: 'team@company.com', role: 'collaborator' }
      ]
    });
  }

  async executeCode(workspaceId: string, code: string): Promise<ExecutionResult> {
    return await this.client.workspace.execute(workspaceId, {
      language: 'python',
      code: `
        import pandas as pd
        import numpy as np
        
        # Load data
        data = pd.read_csv('/data/sales.csv')
        
        # Analyze trends
        monthly_trends = data.groupby('month').sum()
        print(f"Average monthly sales: {monthly_trends.mean()}")
        
        monthly_trends
      `
    });
  }

  async deployModel(workspaceId: string, modelPath: string) {
    return await this.client.workspace.deploy(workspaceId, {
      artifact: modelPath,
      environment: {
        MODEL_PATH: '/models/inventory-predictor',
        API_KEY: process.env.AIMATRIX_API_KEY
      },
      scaling: {
        minInstances: 1,
        maxInstances: 10,
        targetCpuUtilization: 70
      }
    });
  }
}
```

## Hub Integration

```typescript
import { 
  HubArtifact, 
  HubCategory, 
  PricingModel,
  Publication 
} from '@aimatrix/sdk';

class HubManager {
  constructor(private client: AIMatrixClient) {}

  async publishAgent(agentId: string): Promise<Publication> {
    return await this.client.hub.publish({
      artifactType: HubArtifact.AGENT,
      agentId,
      
      metadata: {
        title: 'Customer Service Assistant',
        description: 'Intelligent 24/7 customer support with vision capabilities',
        category: HubCategory.BUSINESS,
        tags: ['customer-service', 'support', 'chatbot', 'vision'],
        pricing: PricingModel.FREE,
        license: 'MIT'
      },
      
      documentation: {
        readme: 'README.md',
        examples: ['examples/basic-usage.ts', 'examples/advanced.ts'],
        apiDocs: 'docs/api.md'
      },
      
      requirements: {
        minimumVersion: '2.0.0',
        requiredCapabilities: [Capability.FUNCTION_CALLING]
      }
    });
  }

  async searchHub(query: string) {
    const results = await this.client.hub.search({
      query,
      category: HubCategory.ANALYTICS,
      pricing: PricingModel.FREE,
      minRating: 4.0,
      limit: 20
    });

    return results.map(item => ({
      id: item.id,
      title: item.title,
      description: item.description,
      rating: item.rating,
      downloads: item.downloadCount,
      author: item.author
    }));
  }

  async installFromHub(marketplaceId: string, workspace?: string) {
    return await this.client.hub.install(marketplaceId, {
      workspace,
      configuration: {
        max_processing_time: '300s',
        output_format: 'json'
      }
    });
  }
}
```

## Authentication

```typescript
import { 
  ApiKeyAuth, 
  OAuth2Auth, 
  ServiceAccountAuth,
  AuthProvider 
} from '@aimatrix/sdk';

// API Key authentication
const client = new AIMatrixClient({
  auth: new ApiKeyAuth('amx_sk_your_secret_key'),
  environment: 'production'
});

// OAuth2 flow
const oauthClient = new AIMatrixClient({
  auth: new OAuth2Auth({
    clientId: 'your-client-id',
    redirectUri: 'https://myapp.com/callback',
    scopes: ['agents:read', 'agents:write', 'twins:manage'],
    usePkce: true
  })
});

// Handle OAuth flow
async function handleOAuth() {
  const authUrl = await oauthClient.auth.getAuthorizationUrl();
  console.log(`Visit: ${authUrl}`);
  
  // After user authorizes
  const tokens = await oauthClient.auth.exchangeCodeForTokens('auth_code');
  console.log('Access token:', tokens.accessToken);
}

// Service Account
const serviceClient = new AIMatrixClient({
  auth: new ServiceAccountAuth({
    serviceAccountKey: require('./service-account.json'),
    scopes: ['https://www.googleapis.com/auth/aimatrix']
  })
});
```

## React Integration

```typescript
import React, { createContext, useContext, useState, useEffect } from 'react';
import { AIMatrixClient, Agent } from '@aimatrix/sdk';

// Context for AIMatrix client
const AIMatrixContext = createContext<AIMatrixClient | null>(null);

export const AIMatrixProvider: React.FC<{ apiKey: string; children: React.ReactNode }> = ({ 
  apiKey, 
  children 
}) => {
  const [client] = useState(() => new AIMatrixClient({ apiKey }));
  
  return (
    <AIMatrixContext.Provider value={client}>
      {children}
    </AIMatrixContext.Provider>
  );
};

// Custom hooks
export const useAIMatrix = () => {
  const client = useContext(AIMatrixContext);
  if (!client) throw new Error('useAIMatrix must be used within AIMatrixProvider');
  return client;
};

export const useAgent = (agentId: string) => {
  const client = useAIMatrix();
  const [agent, setAgent] = useState<Agent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    client.agents.get(agentId)
      .then(setAgent)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [client, agentId]);

  const invoke = async (message: string) => {
    if (!agent) return;
    return await client.agents.invoke(agent.id, { message });
  };

  return { agent, loading, error, invoke };
};

// Component example
const ChatInterface: React.FC<{ agentId: string }> = ({ agentId }) => {
  const { agent, loading, error, invoke } = useAgent(agentId);
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || !invoke) return;

    const result = await invoke(message);
    setResponse(result.message);
    setMessage('');
  };

  if (loading) return <div>Loading agent...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!agent) return <div>Agent not found</div>;

  return (
    <div>
      <h2>{agent.name}</h2>
      <p>{agent.description}</p>
      
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={message}
          onChange={e => setMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
      
      {response && (
        <div>
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
};
```

## Best Practices

### Error Handling

```typescript
import { 
  AIMatrixError,
  AuthenticationError,
  RateLimitError,
  ValidationError 
} from '@aimatrix/sdk';

async function robustInvocation(client: AIMatrixClient, agentId: string, message: string) {
  try {
    return await client.agents.invoke(agentId, { 
      message,
      timeout: 30000 
    });
  } catch (error) {
    if (error instanceof AuthenticationError) {
      // Refresh tokens and retry
      await client.auth.refreshTokens();
      return client.agents.invoke(agentId, { message });
    } else if (error instanceof RateLimitError) {
      // Backoff and retry
      await new Promise(resolve => setTimeout(resolve, error.retryAfter * 1000));
      return client.agents.invoke(agentId, { message });
    } else if (error instanceof ValidationError) {
      // Handle validation errors
      console.error('Validation errors:', error.errors);
      throw error;
    } else if (error instanceof AIMatrixError) {
      // Handle other API errors
      console.error('API error:', error.message);
      throw error;
    } else {
      // Handle unexpected errors
      console.error('Unexpected error:', error);
      throw error;
    }
  }
}
```

### Configuration Management

```typescript
interface Config {
  apiKey: string;
  environment: 'development' | 'staging' | 'production';
  baseUrl?: string;
  timeout?: number;
}

function createClient(config: Config): AIMatrixClient {
  return new AIMatrixClient({
    apiKey: config.apiKey,
    environment: config.environment,
    baseUrl: config.baseUrl || getDefaultBaseUrl(config.environment),
    timeout: config.timeout || getDefaultTimeout(config.environment),
    retryPolicy: {
      maxRetries: config.environment === 'production' ? 3 : 1,
      backoffFactor: 2
    }
  });
}

function getDefaultBaseUrl(env: string): string {
  switch (env) {
    case 'development': return 'https://api.dev.aimatrix.com/v1';
    case 'staging': return 'https://api.staging.aimatrix.com/v1';
    case 'production': return 'https://api.aimatrix.com/v1';
    default: throw new Error(`Unknown environment: ${env}`);
  }
}
```

---

# C# SDK {#csharp-sdk}

**.NET ecosystem integration with Task-based async, dependency injection, and Unity3D compatibility.**

## Installation & Setup

```xml
<!-- Package Manager Console -->
Install-Package AIMatrix.SDK

<!-- PackageReference -->
<PackageReference Include="AIMatrix.SDK" Version="2.0.0" />

<!-- .NET CLI -->
dotnet add package AIMatrix.SDK
```

### Quick Start

```csharp
using AIMatrix.SDK;
using AIMatrix.SDK.Models;

// Initialize client
var client = new AIMatrixClient("your-api-key");

// Create and invoke agent
var agent = await client.Agents.CreateAsync(new CreateAgentRequest
{
    Name = "business-assistant",
    Description = "Intelligent business operations assistant",
    Model = "gpt-4",
    Capabilities = new[] { Capability.Vision, Capability.FunctionCalling }
});

var result = await client.Agents.InvokeAsync(agent.Id, new InvocationRequest
{
    Message = "What's our current sales performance?"
});

Console.WriteLine($"Response: {result.Message}");
```

## Core Classes & Interfaces

```csharp
using AIMatrix.SDK.Configuration;
using AIMatrix.SDK.Authentication;

public class AIMatrixClient : IDisposable
{
    public IAgentManager Agents { get; }
    public ITwinManager Twins { get; }
    public IWorkspaceManager Workspace { get; }
    public IHubManager Hub { get; }
    public IAuthenticationManager Auth { get; }

    public AIMatrixClient(string apiKey) : this(new AIMatrixConfig
    {
        Authentication = new ApiKeyAuth(apiKey),
        Environment = Environment.Production
    })
    { }

    public AIMatrixClient(AIMatrixConfig config)
    {
        // Implementation
    }
}

// Configuration
public class AIMatrixConfig
{
    public IAuthProvider Authentication { get; set; }
    public Environment Environment { get; set; } = Environment.Production;
    public string BaseUrl { get; set; }
    public TimeSpan Timeout { get; set; } = TimeSpan.FromSeconds(30);
    public RetryPolicy RetryPolicy { get; set; }
    public LogLevel LogLevel { get; set; } = LogLevel.Information;
}
```

## Agent Management

```csharp
using AIMatrix.SDK.Agents;
using AIMatrix.SDK.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

public interface IAgentManager
{
    Task<Agent> CreateAsync(CreateAgentRequest request, CancellationToken cancellationToken = default);
    Task<Agent> GetAsync(string agentId, CancellationToken cancellationToken = default);
    Task<IEnumerable<Agent>> ListAsync(AgentFilter filter = null, CancellationToken cancellationToken = default);
    Task<Agent> UpdateAsync(string agentId, UpdateAgentRequest request, CancellationToken cancellationToken = default);
    Task<bool> DeleteAsync(string agentId, CancellationToken cancellationToken = default);
    Task<InvocationResult> InvokeAsync(string agentId, InvocationRequest request, CancellationToken cancellationToken = default);
    IAsyncEnumerable<StreamChunk> StreamAsync(string agentId, InvocationRequest request, CancellationToken cancellationToken = default);
}

// Advanced agent creation
public class BusinessAgentExample
{
    private readonly AIMatrixClient _client;

    public BusinessAgentExample(AIMatrixClient client)
    {
        _client = client;
    }

    public async Task<Agent> CreateCustomerServiceAgent()
    {
        var request = new CreateAgentRequest
        {
            Name = "customer-service",
            Description = "24/7 customer support assistant with vision capabilities",
            Model = "claude-3-sonnet",
            Capabilities = new[]
            {
                Capability.MultimodalVision,
                Capability.FunctionCalling,
                Capability.Memory
            },
            
            Tools = new[]
            {
                new ToolDefinition
                {
                    Name = "get_order_status",
                    Description = "Retrieve customer order status",
                    Parameters = new
                    {
                        type = "object",
                        properties = new
                        {
                            order_id = new { type = "string", description = "Order identifier" }
                        },
                        required = new[] { "order_id" }
                    }
                },
                new ToolDefinition
                {
                    Name = "create_support_ticket",
                    Description = "Create a new support ticket",
                    Parameters = new
                    {
                        type = "object",
                        properties = new
                        {
                            title = new { type = "string" },
                            description = new { type = "string" },
                            priority = new { type = "string", @enum = new[] { "low", "medium", "high" } }
                        },
                        required = new[] { "title", "description" }
                    }
                }
            },
            
            SystemPrompt = @"
                You are a helpful customer service assistant.
                Always be polite and provide accurate information.
                Escalate complex issues to human agents when necessary.
            ",
            
            Memory = new MemoryConfig
            {
                Type = MemoryType.Conversation,
                MaxSize = 10000,
                PersistenceStrategy = PersistenceStrategy.Database
            },
            
            Security = new SecurityConfig
            {
                AccessLevel = AccessLevel.Restricted,
                AllowedDomains = new[] { "company.com" },
                RateLimits = new RateLimits
                {
                    RequestsPerMinute = 100,
                    TokensPerMinute = 50000
                }
            }
        };

        return await _client.Agents.CreateAsync(request);
    }

    public async Task<InvocationResult> InvokeWithStreaming(string agentId, string message)
    {
        var request = new InvocationRequest
        {
            Message = message,
            Context = new Dictionary<string, object>
            {
                ["user_id"] = "user123",
                ["session_id"] = "session456"
            }
        };

        await foreach (var chunk in _client.Agents.StreamAsync(agentId, request))
        {
            switch (chunk.Type)
            {
                case ChunkType.Message:
                    Console.Write(chunk.Content);
                    break;
                case ChunkType.FunctionCall:
                    Console.WriteLine($"\nCalling function: {chunk.FunctionName}");
                    break;
                case ChunkType.Error:
                    Console.WriteLine($"\nError: {chunk.Error}");
                    break;
            }
        }

        return new InvocationResult(); // Final result
    }
}
```

## Digital Twin Operations

```csharp
using AIMatrix.SDK.Twins;
using AIMatrix.SDK.Models.Twins;

public interface ITwinManager
{
    Task<DigitalTwin> CreateAsync(CreateTwinRequest request, CancellationToken cancellationToken = default);
    Task<TrainingJob> TrainAsync(string twinId, Dataset dataset, CancellationToken cancellationToken = default);
    Task<PredictionResult> PredictAsync(string twinId, TwinInput input, CancellationToken cancellationToken = default);
    Task<Deployment> DeployAsync(string twinId, DeploymentEnvironment environment, CancellationToken cancellationToken = default);
}

public class InventoryTwinExample
{
    private readonly AIMatrixClient _client;

    public InventoryTwinExample(AIMatrixClient client)
    {
        _client = client;
    }

    public async Task<DigitalTwin> CreateInventoryPredictor()
    {
        var request = new CreateTwinRequest
        {
            Name = "inventory-predictor",
            Description = "Predict inventory needs based on historical data",
            
            ModelConfig = new TwinModelConfig
            {
                Type = TwinModelType.Regression,
                Algorithm = Algorithm.RandomForest,
                Features = new[]
                {
                    "sales_history",
                    "seasonal_patterns",
                    "market_trends",
                    "promotion_calendar"
                },
                Target = "required_inventory"
            },
            
            DataSources = new[]
            {
                new DataSource
                {
                    Name = "sales-db",
                    Type = DataSourceType.PostgreSQL,
                    ConnectionString = "Server=localhost;Database=sales;",
                    Tables = new[] { "sales", "products", "inventory" }
                },
                new DataSource
                {
                    Name = "market-api",
                    Type = DataSourceType.RestApi,
                    Endpoint = "https://api.marketdata.com/trends",
                    Authentication = new BearerTokenAuth("your-token")
                }
            },
            
            TrainingConfig = new TrainingConfig
            {
                SplitStrategy = SplitStrategy.TimeBased,
                TrainRatio = 0.8m,
                ValidationRatio = 0.2m,
                Hyperparameters = new Dictionary<string, object>
                {
                    ["n_estimators"] = 100,
                    ["max_depth"] = 10,
                    ["min_samples_split"] = 5
                }
            }
        };

        return await _client.Twins.CreateAsync(request);
    }

    public async Task<TrainingJob> TrainTwin(string twinId)
    {
        // Load data from CSV file
        var dataset = Dataset.FromCsv("sales_data.csv", new DatasetConfig
        {
            Features = new[] { "sales_volume", "season", "promotion" },
            Target = "inventory_needed",
            HasHeader = true
        });

        var job = await _client.Twins.TrainAsync(twinId, dataset);

        // Monitor training progress
        while (job.Status == TrainingStatus.Running)
        {
            await Task.Delay(5000);
            job = await _client.Twins.GetTrainingJobAsync(job.Id);
            Console.WriteLine($"Training progress: {job.Progress}%");
        }

        switch (job.Status)
        {
            case TrainingStatus.Completed:
                Console.WriteLine("Training completed!");
                Console.WriteLine($"Accuracy: {job.Metrics.Accuracy}");
                Console.WriteLine($"R² Score: {job.Metrics.R2Score}");
                break;
            case TrainingStatus.Failed:
                throw new Exception($"Training failed: {job.Error}");
        }

        return job;
    }

    public async Task<PredictionResult> PredictInventory(string twinId, Dictionary<string, object> features)
    {
        var input = new TwinInput { Features = features };
        return await _client.Twins.PredictAsync(twinId, input);
    }
}
```

## Workspace Operations

```csharp
using AIMatrix.SDK.Workspace;
using AIMatrix.SDK.Models.Workspace;

public interface IWorkspaceManager
{
    Task<Workspace> CreateAsync(CreateWorkspaceRequest request, CancellationToken cancellationToken = default);
    Task<ExecutionResult> ExecuteAsync(string workspaceId, CodeExecutionRequest request, CancellationToken cancellationToken = default);
    Task<Deployment> DeployAsync(string workspaceId, DeploymentRequest request, CancellationToken cancellationToken = default);
}

public class WorkspaceExample
{
    private readonly AIMatrixClient _client;

    public WorkspaceExample(AIMatrixClient client)
    {
        _client = client;
    }

    public async Task<Workspace> CreateMLWorkspace()
    {
        var request = new CreateWorkspaceRequest
        {
            Name = "ml-experiments",
            Description = "Machine learning experimentation environment",
            
            Runtime = new Runtime
            {
                Type = RuntimeType.Python,
                Version = "3.11",
                Packages = new[]
                {
                    "tensorflow==2.13.0",
                    "pandas==2.1.0",
                    "scikit-learn==1.3.0",
                    "matplotlib==3.7.0"
                }
            },
            
            Resources = new ResourceAllocation
            {
                Cpu = "4 cores",
                Memory = "16GB",
                Gpu = GpuType.T4,
                Storage = "100GB"
            },
            
            Access = new[]
            {
                new AccessControl { Email = "user@company.com", Role = Role.Owner },
                new AccessControl { Email = "team@company.com", Role = Role.Collaborator }
            }
        };

        return await _client.Workspace.CreateAsync(request);
    }

    public async Task<ExecutionResult> ExecutePythonCode(string workspaceId)
    {
        var request = new CodeExecutionRequest
        {
            Language = Language.Python,
            Code = @"
                import pandas as pd
                import numpy as np
                
                # Load data
                data = pd.read_csv('/data/sales.csv')
                
                # Analyze trends
                monthly_trends = data.groupby('month').sum()
                print(f'Average monthly sales: {monthly_trends.mean()}')
                
                monthly_trends
            "
        };

        return await _client.Workspace.ExecuteAsync(workspaceId, request);
    }

    public async Task<Deployment> DeployModel(string workspaceId, string modelPath)
    {
        var request = new DeploymentRequest
        {
            Artifact = modelPath,
            Environment = new Dictionary<string, string>
            {
                ["MODEL_PATH"] = "/models/inventory-predictor",
                ["API_KEY"] = Environment.GetEnvironmentVariable("AIMATRIX_API_KEY")
            },
            Scaling = new ScalingConfig
            {
                MinInstances = 1,
                MaxInstances = 10,
                TargetCpuUtilization = 70
            }
        };

        return await _client.Workspace.DeployAsync(workspaceId, request);
    }
}
```

## Hub Integration

```csharp
using AIMatrix.SDK.Hub;
using AIMatrix.SDK.Models.Hub;

public interface IHubManager
{
    Task<Publication> PublishAsync(PublishRequest request, CancellationToken cancellationToken = default);
    Task<IEnumerable<HubItem>> SearchAsync(SearchRequest request, CancellationToken cancellationToken = default);
    Task<Agent> InstallAsync(string marketplaceId, InstallRequest request = null, CancellationToken cancellationToken = default);
}

public class HubExample
{
    private readonly AIMatrixClient _client;

    public HubExample(AIMatrixClient client)
    {
        _client = client;
    }

    public async Task<Publication> PublishAgent(string agentId)
    {
        var request = new PublishRequest
        {
            ArtifactType = HubArtifact.Agent,
            AgentId = agentId,
            
            Metadata = new PublicationMetadata
            {
                Title = "Customer Service Assistant",
                Description = "Intelligent 24/7 customer support with vision capabilities",
                Category = HubCategory.Business,
                Tags = new[] { "customer-service", "support", "chatbot", "vision" },
                Pricing = PricingModel.Free,
                License = "MIT"
            },
            
            Documentation = new Documentation
            {
                ReadmePath = "README.md",
                ExamplePaths = new[] { "examples/basic-usage.cs", "examples/advanced.cs" },
                ApiDocsPath = "docs/api.md"
            },
            
            Requirements = new Requirements
            {
                MinimumVersion = new Version(2, 0, 0),
                RequiredCapabilities = new[] { Capability.FunctionCalling }
            }
        };

        return await _client.Hub.PublishAsync(request);
    }

    public async Task<IEnumerable<HubItem>> SearchHub(string query)
    {
        var request = new SearchRequest
        {
            Query = query,
            Category = HubCategory.Analytics,
            Pricing = PricingModel.Free,
            MinRating = 4.0f,
            Limit = 20
        };

        return await _client.Hub.SearchAsync(request);
    }

    public async Task<Agent> InstallFromHub(string marketplaceId, string workspace = null)
    {
        var request = new InstallRequest
        {
            Workspace = workspace,
            Configuration = new Dictionary<string, object>
            {
                ["max_processing_time"] = "300s",
                ["output_format"] = "json"
            }
        };

        return await _client.Hub.InstallAsync(marketplaceId, request);
    }
}
```

## Authentication

```csharp
using AIMatrix.SDK.Authentication;

// API Key authentication
var client = new AIMatrixClient(new AIMatrixConfig
{
    Authentication = new ApiKeyAuth("amx_sk_your_secret_key"),
    Environment = Environment.Production
});

// OAuth2 flow
var oauthClient = new AIMatrixClient(new AIMatrixConfig
{
    Authentication = new OAuth2Auth
    {
        ClientId = "your-client-id",
        RedirectUri = "https://myapp.com/callback",
        Scopes = new[] { "agents:read", "agents:write", "twins:manage" },
        UsePkce = true
    }
});

// Handle OAuth flow
public async Task HandleOAuthFlow()
{
    var authUrl = await oauthClient.Auth.GetAuthorizationUrlAsync();
    Console.WriteLine($"Visit: {authUrl}");
    
    // After user authorizes
    var tokens = await oauthClient.Auth.ExchangeCodeForTokensAsync("authorization_code");
    Console.WriteLine($"Access token: {tokens.AccessToken}");
}

// Service Account
var serviceClient = new AIMatrixClient(new AIMatrixConfig
{
    Authentication = new ServiceAccountAuth
    {
        ServiceAccountKeyPath = "service-account.json",
        Scopes = new[] { "https://www.googleapis.com/auth/aimatrix" }
    }
});
```

## Dependency Injection

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Configuration;
using AIMatrix.SDK.Extensions;

// Startup.cs or Program.cs
public void ConfigureServices(IServiceCollection services)
{
    // Add AIMatrix SDK
    services.AddAIMatrix(options =>
    {
        options.ApiKey = Configuration.GetValue<string>("AIMatrix:ApiKey");
        options.Environment = Configuration.GetValue<Environment>("AIMatrix:Environment");
        options.Timeout = TimeSpan.FromSeconds(30);
    });
    
    // Register your services
    services.AddScoped<ICustomerServiceAgent, CustomerServiceAgent>();
}

// Service implementation
public interface ICustomerServiceAgent
{
    Task<string> ProcessCustomerInquiry(string inquiry);
}

public class CustomerServiceAgent : ICustomerServiceAgent
{
    private readonly AIMatrixClient _client;
    private readonly ILogger<CustomerServiceAgent> _logger;
    private const string AgentId = "customer-service-agent";

    public CustomerServiceAgent(AIMatrixClient client, ILogger<CustomerServiceAgent> logger)
    {
        _client = client;
        _logger = logger;
    }

    public async Task<string> ProcessCustomerInquiry(string inquiry)
    {
        try
        {
            var result = await _client.Agents.InvokeAsync(AgentId, new InvocationRequest
            {
                Message = inquiry,
                Context = new Dictionary<string, object>
                {
                    ["timestamp"] = DateTime.UtcNow,
                    ["source"] = "web-portal"
                }
            });

            _logger.LogInformation("Successfully processed customer inquiry");
            return result.Message;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to process customer inquiry");
            return "I apologize, but I'm experiencing technical difficulties. Please try again later.";
        }
    }
}
```

## Unity3D Integration

```csharp
using UnityEngine;
using AIMatrix.SDK;
using System.Threading.Tasks;

public class AIMatrixUnityClient : MonoBehaviour
{
    [SerializeField] private string apiKey;
    [SerializeField] private string agentId;
    
    private AIMatrixClient _client;

    void Start()
    {
        _client = new AIMatrixClient(apiKey);
    }

    public async Task<string> ProcessVoiceCommand(AudioClip audioClip)
    {
        try
        {
            // Convert AudioClip to bytes (implementation depends on your audio system)
            byte[] audioData = ConvertAudioClipToBytes(audioClip);
            
            var result = await _client.Agents.InvokeAsync(agentId, new InvocationRequest
            {
                Message = "Process this voice command",
                Attachments = new[]
                {
                    new Attachment
                    {
                        Type = AttachmentType.Audio,
                        Data = audioData,
                        MimeType = "audio/wav"
                    }
                }
            });

            return result.Message;
        }
        catch (System.Exception ex)
        {
            Debug.LogError($"Failed to process voice command: {ex.Message}");
            return "Voice command processing failed";
        }
    }

    private byte[] ConvertAudioClipToBytes(AudioClip clip)
    {
        // Implementation for converting AudioClip to byte array
        // This is a placeholder - actual implementation depends on your audio pipeline
        return new byte[0];
    }

    void OnDestroy()
    {
        _client?.Dispose();
    }
}

// Unity coroutine wrapper for async operations
public class AsyncUnityWrapper : MonoBehaviour
{
    private AIMatrixClient _client;

    void Start()
    {
        _client = new AIMatrixClient("your-api-key");
        StartCoroutine(ProcessAgentRequest());
    }

    private IEnumerator ProcessAgentRequest()
    {
        var task = _client.Agents.InvokeAsync("agent-id", new InvocationRequest
        {
            Message = "Hello from Unity!"
        });

        yield return new WaitUntil(() => task.IsCompleted);

        if (task.Exception != null)
        {
            Debug.LogError(task.Exception);
        }
        else
        {
            Debug.Log($"Agent response: {task.Result.Message}");
        }
    }
}
```

## Best Practices

### Error Handling & Resilience

```csharp
using AIMatrix.SDK.Exceptions;
using Polly;
using Polly.Extensions.Http;

public class ResilientAIMatrixService
{
    private readonly AIMatrixClient _client;
    private readonly IAsyncPolicy<InvocationResult> _retryPolicy;

    public ResilientAIMatrixService(AIMatrixClient client)
    {
        _client = client;
        
        _retryPolicy = Policy
            .Handle<RateLimitException>()
            .Or<ServiceUnavailableException>()
            .WaitAndRetryAsync(
                retryCount: 3,
                sleepDurationProvider: retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
                onRetry: (outcome, timespan, retryCount, context) =>
                {
                    Console.WriteLine($"Retry {retryCount} after {timespan} seconds");
                });
    }

    public async Task<InvocationResult> InvokeWithResilience(string agentId, string message)
    {
        return await _retryPolicy.ExecuteAsync(async () =>
        {
            try
            {
                return await _client.Agents.InvokeAsync(agentId, new InvocationRequest
                {
                    Message = message,
                    Timeout = TimeSpan.FromSeconds(30)
                });
            }
            catch (AuthenticationException)
            {
                // Refresh tokens and retry
                await _client.Auth.RefreshTokensAsync();
                throw; // Re-throw to trigger retry
            }
            catch (ValidationException ex)
            {
                // Don't retry validation errors
                Console.WriteLine($"Validation errors: {string.Join(", ", ex.Errors)}");
                throw;
            }
        });
    }
}
```

### Configuration & Environment Management

```csharp
// appsettings.json
{
  "AIMatrix": {
    "ApiKey": "your-api-key",
    "Environment": "Production",
    "BaseUrl": "https://api.aimatrix.com/v1",
    "Timeout": "00:00:30",
    "RetryPolicy": {
      "MaxRetries": 3,
      "BackoffFactor": 2
    },
    "Logging": {
      "Level": "Information"
    }
  }
}

// Configuration binding
public class AIMatrixOptions
{
    public string ApiKey { get; set; }
    public Environment Environment { get; set; }
    public string BaseUrl { get; set; }
    public TimeSpan Timeout { get; set; }
    public RetryPolicyOptions RetryPolicy { get; set; }
    public LoggingOptions Logging { get; set; }
}

public class RetryPolicyOptions
{
    public int MaxRetries { get; set; }
    public int BackoffFactor { get; set; }
}

// Extension method for DI
public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddAIMatrix(
        this IServiceCollection services, 
        IConfiguration configuration)
    {
        services.Configure<AIMatrixOptions>(configuration.GetSection("AIMatrix"));
        
        services.AddSingleton<AIMatrixClient>(provider =>
        {
            var options = provider.GetRequiredService<IOptions<AIMatrixOptions>>().Value;
            return new AIMatrixClient(new AIMatrixConfig
            {
                Authentication = new ApiKeyAuth(options.ApiKey),
                Environment = options.Environment,
                BaseUrl = options.BaseUrl,
                Timeout = options.Timeout,
                RetryPolicy = new RetryPolicy
                {
                    MaxRetries = options.RetryPolicy.MaxRetries,
                    BackoffFactor = options.RetryPolicy.BackoffFactor
                }
            });
        });

        return services;
    }
}
```

---

# Java SDK {#java-sdk}

**Enterprise-ready JVM integration with CompletableFuture, Spring Boot, and Jakarta EE support.**

## Installation & Setup

### Maven
```xml
<dependency>
    <groupId>com.aimatrix</groupId>
    <artifactId>java-sdk</artifactId>
    <version>2.0.0</version>
</dependency>
```

### Gradle
```groovy
implementation 'com.aimatrix:java-sdk:2.0.0'
```

### Quick Start

```java
import com.aimatrix.sdk.AIMatrixClient;
import com.aimatrix.sdk.models.Agent;
import com.aimatrix.sdk.models.CreateAgentRequest;
import com.aimatrix.sdk.models.InvocationRequest;
import com.aimatrix.sdk.models.Capability;

import java.util.concurrent.CompletableFuture;

public class QuickStart {
    public static void main(String[] args) {
        // Initialize client
        AIMatrixClient client = new AIMatrixClient("your-api-key");
        
        // Create agent
        CompletableFuture<Agent> agentFuture = client.agents().create(
            CreateAgentRequest.builder()
                .name("business-assistant")
                .description("Intelligent business operations assistant")
                .model("gpt-4")
                .capabilities(Capability.VISION, Capability.FUNCTION_CALLING)
                .build()
        );
        
        // Invoke agent
        agentFuture.thenCompose(agent -> 
            client.agents().invoke(agent.getId(), 
                InvocationRequest.builder()
                    .message("What's our current sales performance?")
                    .build()
            )
        ).thenAccept(result -> 
            System.out.println("Response: " + result.getMessage())
        ).join();
    }
}
```

## Core Classes & Interfaces

```java
package com.aimatrix.sdk;

import com.aimatrix.sdk.auth.AuthProvider;
import com.aimatrix.sdk.config.AIMatrixConfig;
import com.aimatrix.sdk.config.Environment;

public class AIMatrixClient implements AutoCloseable {
    private final AgentManager agentManager;
    private final TwinManager twinManager;
    private final WorkspaceManager workspaceManager;
    private final HubManager hubManager;
    private final AuthenticationManager authManager;

    public AIMatrixClient(String apiKey) {
        this(AIMatrixConfig.builder()
            .apiKey(apiKey)
            .environment(Environment.PRODUCTION)
            .build());
    }

    public AIMatrixClient(AIMatrixConfig config) {
        // Implementation
    }

    public AgentManager agents() { return agentManager; }
    public TwinManager twins() { return twinManager; }
    public WorkspaceManager workspace() { return workspaceManager; }
    public HubManager hub() { return hubManager; }
    public AuthenticationManager auth() { return authManager; }

    @Override
    public void close() {
        // Cleanup resources
    }
}

// Configuration
public class AIMatrixConfig {
    private final AuthProvider authentication;
    private final Environment environment;
    private final String baseUrl;
    private final Duration timeout;
    private final RetryPolicy retryPolicy;
    private final LogLevel logLevel;

    private AIMatrixConfig(Builder builder) {
        this.authentication = builder.authentication;
        this.environment = builder.environment;
        this.baseUrl = builder.baseUrl;
        this.timeout = builder.timeout;
        this.retryPolicy = builder.retryPolicy;
        this.logLevel = builder.logLevel;
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        // Builder implementation
    }
}
```

## Agent Management

```java
package com.aimatrix.sdk.agents;

import com.aimatrix.sdk.models.*;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Stream;

public interface AgentManager {
    CompletableFuture<Agent> create(CreateAgentRequest request);
    CompletableFuture<Agent> get(String agentId);
    CompletableFuture<List<Agent>> list(AgentFilter filter);
    CompletableFuture<Agent> update(String agentId, UpdateAgentRequest request);
    CompletableFuture<Boolean> delete(String agentId);
    CompletableFuture<InvocationResult> invoke(String agentId, InvocationRequest request);
    Stream<StreamChunk> stream(String agentId, InvocationRequest request);
}

// Advanced agent creation example
public class BusinessAgentExample {
    private final AIMatrixClient client;

    public BusinessAgentExample(AIMatrixClient client) {
        this.client = client;
    }

    public CompletableFuture<Agent> createCustomerServiceAgent() {
        CreateAgentRequest request = CreateAgentRequest.builder()
            .name("customer-service")
            .description("24/7 customer support assistant with vision capabilities")
            .model("claude-3-sonnet")
            .capabilities(
                Capability.MULTIMODAL_VISION,
                Capability.FUNCTION_CALLING,
                Capability.MEMORY
            )
            .tools(
                ToolDefinition.builder()
                    .name("get_order_status")
                    .description("Retrieve customer order status")
                    .parameters(JsonSchema.object()
                        .property("order_id", JsonSchema.string()
                            .description("Order identifier"))
                        .required("order_id")
                        .build())
                    .build(),
                
                ToolDefinition.builder()
                    .name("create_support_ticket")
                    .description("Create a new support ticket")
                    .parameters(JsonSchema.object()
                        .property("title", JsonSchema.string())
                        .property("description", JsonSchema.string())
                        .property("priority", JsonSchema.stringEnum("low", "medium", "high"))
                        .required("title", "description")
                        .build())
                    .build()
            )
            .systemPrompt("""
                You are a helpful customer service assistant.
                Always be polite and provide accurate information.
                Escalate complex issues to human agents when necessary.
                """)
            .memory(MemoryConfig.builder()
                .type(MemoryType.CONVERSATION)
                .maxSize(10000)
                .persistenceStrategy(PersistenceStrategy.DATABASE)
                .build())
            .security(SecurityConfig.builder()
                .accessLevel(AccessLevel.RESTRICTED)
                .allowedDomains("company.com")
                .rateLimits(RateLimits.builder()
                    .requestsPerMinute(100)
                    .tokensPerMinute(50000)
                    .build())
                .build())
            .build();

        return client.agents().create(request);
    }

    public CompletableFuture<InvocationResult> invokeWithContext(String agentId, String message) {
        InvocationRequest request = InvocationRequest.builder()
            .message(message)
            .context(Map.of(
                "user_id", "user123",
                "session_id", "session456"
            ))
            .build();

        return client.agents().invoke(agentId, request);
    }

    public void streamingInvocation(String agentId, String message) {
        InvocationRequest request = InvocationRequest.builder()
            .message(message)
            .build();

        client.agents().stream(agentId, request)
            .forEach(chunk -> {
                switch (chunk.getType()) {
                    case MESSAGE:
                        System.out.print(chunk.getContent());
                        break;
                    case FUNCTION_CALL:
                        System.out.println("\nCalling function: " + chunk.getFunctionName());
                        break;
                    case ERROR:
                        System.out.println("\nError: " + chunk.getError());
                        break;
                }
            });
    }
}
```

## Digital Twin Operations

```java
package com.aimatrix.sdk.twins;

import com.aimatrix.sdk.models.twins.*;
import java.util.concurrent.CompletableFuture;

public interface TwinManager {
    CompletableFuture<DigitalTwin> create(CreateTwinRequest request);
    CompletableFuture<TrainingJob> train(String twinId, Dataset dataset);
    CompletableFuture<PredictionResult> predict(String twinId, TwinInput input);
    CompletableFuture<Deployment> deploy(String twinId, DeploymentEnvironment environment);
}

public class InventoryTwinExample {
    private final AIMatrixClient client;

    public InventoryTwinExample(AIMatrixClient client) {
        this.client = client;
    }

    public CompletableFuture<DigitalTwin> createInventoryPredictor() {
        CreateTwinRequest request = CreateTwinRequest.builder()
            .name("inventory-predictor")
            .description("Predict inventory needs based on historical data")
            .modelConfig(TwinModelConfig.builder()
                .type(TwinModelType.REGRESSION)
                .algorithm(Algorithm.RANDOM_FOREST)
                .features("sales_history", "seasonal_patterns", "market_trends", "promotion_calendar")
                .target("required_inventory")
                .build())
            .dataSources(
                DataSource.builder()
                    .name("sales-db")
                    .type(DataSourceType.POSTGRESQL)
                    .connectionString("jdbc:postgresql://localhost/sales")
                    .tables("sales", "products", "inventory")
                    .build(),
                
                DataSource.builder()
                    .name("market-api")
                    .type(DataSourceType.REST_API)
                    .endpoint("https://api.marketdata.com/trends")
                    .authentication(BearerTokenAuth.of("your-token"))
                    .build()
            )
            .trainingConfig(TrainingConfig.builder()
                .splitStrategy(SplitStrategy.TIME_BASED)
                .trainRatio(0.8)
                .validationRatio(0.2)
                .hyperparameters(Map.of(
                    "n_estimators", 100,
                    "max_depth", 10,
                    "min_samples_split", 5
                ))
                .build())
            .build();

        return client.twins().create(request);
    }

    public CompletableFuture<TrainingJob> trainTwin(String twinId) {
        // Load dataset from CSV
        Dataset dataset = Dataset.fromCsv("sales_data.csv", DatasetConfig.builder()
            .features("sales_volume", "season", "promotion")
            .target("inventory_needed")
            .hasHeader(true)
            .build());

        return client.twins().train(twinId, dataset)
            .thenCompose(job -> monitorTrainingProgress(job.getId()));
    }

    private CompletableFuture<TrainingJob> monitorTrainingProgress(String jobId) {
        return CompletableFuture.supplyAsync(() -> {
            try {
                TrainingJob job;
                do {
                    Thread.sleep(5000);
                    job = client.twins().getTrainingJob(jobId).join();
                    System.out.println("Training progress: " + job.getProgress() + "%");
                } while (job.getStatus() == TrainingStatus.RUNNING);

                switch (job.getStatus()) {
                    case COMPLETED:
                        System.out.println("Training completed!");
                        System.out.println("Accuracy: " + job.getMetrics().getAccuracy());
                        System.out.println("R² Score: " + job.getMetrics().getR2Score());
                        break;
                    case FAILED:
                        throw new RuntimeException("Training failed: " + job.getError());
                }

                return job;
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException(e);
            }
        });
    }

    public CompletableFuture<PredictionResult> predictInventory(String twinId, Map<String, Object> features) {
        TwinInput input = TwinInput.builder()
            .features(features)
            .build();
        
        return client.twins().predict(twinId, input);
    }
}
```

## Workspace Operations

```java
package com.aimatrix.sdk.workspace;

import com.aimatrix.sdk.models.workspace.*;
import java.util.concurrent.CompletableFuture;

public interface WorkspaceManager {
    CompletableFuture<Workspace> create(CreateWorkspaceRequest request);
    CompletableFuture<ExecutionResult> execute(String workspaceId, CodeExecutionRequest request);
    CompletableFuture<Deployment> deploy(String workspaceId, DeploymentRequest request);
}

public class WorkspaceExample {
    private final AIMatrixClient client;

    public WorkspaceExample(AIMatrixClient client) {
        this.client = client;
    }

    public CompletableFuture<Workspace> createMLWorkspace() {
        CreateWorkspaceRequest request = CreateWorkspaceRequest.builder()
            .name("ml-experiments")
            .description("Machine learning experimentation environment")
            .runtime(Runtime.builder()
                .type(RuntimeType.PYTHON)
                .version("3.11")
                .packages(
                    "tensorflow==2.13.0",
                    "pandas==2.1.0", 
                    "scikit-learn==1.3.0",
                    "matplotlib==3.7.0"
                )
                .build())
            .resources(ResourceAllocation.builder()
                .cpu("4 cores")
                .memory("16GB")
                .gpu(GpuType.T4)
                .storage("100GB")
                .build())
            .access(
                AccessControl.builder()
                    .email("user@company.com")
                    .role(Role.OWNER)
                    .build(),
                AccessControl.builder()
                    .email("team@company.com")
                    .role(Role.COLLABORATOR)
                    .build()
            )
            .build();

        return client.workspace().create(request);
    }

    public CompletableFuture<ExecutionResult> executePythonCode(String workspaceId) {
        CodeExecutionRequest request = CodeExecutionRequest.builder()
            .language(Language.PYTHON)
            .code("""
                import pandas as pd
                import numpy as np
                
                # Load data
                data = pd.read_csv('/data/sales.csv')
                
                # Analyze trends
                monthly_trends = data.groupby('month').sum()
                print(f'Average monthly sales: {monthly_trends.mean()}')
                
                monthly_trends
                """)
            .build();

        return client.workspace().execute(workspaceId, request);
    }

    public CompletableFuture<Deployment> deployModel(String workspaceId, String modelPath) {
        DeploymentRequest request = DeploymentRequest.builder()
            .artifact(modelPath)
            .environment(Map.of(
                "MODEL_PATH", "/models/inventory-predictor",
                "API_KEY", System.getenv("AIMATRIX_API_KEY")
            ))
            .scaling(ScalingConfig.builder()
                .minInstances(1)
                .maxInstances(10)
                .targetCpuUtilization(70)
                .build())
            .build();

        return client.workspace().deploy(workspaceId, request);
    }
}
```

## Hub Integration

```java
package com.aimatrix.sdk.hub;

import com.aimatrix.sdk.models.hub.*;
import java.util.List;
import java.util.concurrent.CompletableFuture;

public interface HubManager {
    CompletableFuture<Publication> publish(PublishRequest request);
    CompletableFuture<List<HubItem>> search(SearchRequest request);
    CompletableFuture<Agent> install(String marketplaceId, InstallRequest request);
}

public class HubExample {
    private final AIMatrixClient client;

    public HubExample(AIMatrixClient client) {
        this.client = client;
    }

    public CompletableFuture<Publication> publishAgent(String agentId) {
        PublishRequest request = PublishRequest.builder()
            .artifactType(HubArtifact.AGENT)
            .agentId(agentId)
            .metadata(PublicationMetadata.builder()
                .title("Customer Service Assistant")
                .description("Intelligent 24/7 customer support with vision capabilities")
                .category(HubCategory.BUSINESS)
                .tags("customer-service", "support", "chatbot", "vision")
                .pricing(PricingModel.FREE)
                .license("MIT")
                .build())
            .documentation(Documentation.builder()
                .readmePath("README.md")
                .examplePaths("examples/basic-usage.java", "examples/advanced.java")
                .apiDocsPath("docs/api.md")
                .build())
            .requirements(Requirements.builder()
                .minimumVersion("2.0.0")
                .requiredCapabilities(Capability.FUNCTION_CALLING)
                .build())
            .build();

        return client.hub().publish(request);
    }

    public CompletableFuture<List<HubItem>> searchHub(String query) {
        SearchRequest request = SearchRequest.builder()
            .query(query)
            .category(HubCategory.ANALYTICS)
            .pricing(PricingModel.FREE)
            .minRating(4.0f)
            .limit(20)
            .build();

        return client.hub().search(request);
    }

    public CompletableFuture<Agent> installFromHub(String marketplaceId, String workspace) {
        InstallRequest request = InstallRequest.builder()
            .workspace(workspace)
            .configuration(Map.of(
                "max_processing_time", "300s",
                "output_format", "json"
            ))
            .build();

        return client.hub().install(marketplaceId, request);
    }
}
```

## Authentication

```java
package com.aimatrix.sdk.auth;

// API Key authentication
AIMatrixClient client = new AIMatrixClient(
    AIMatrixConfig.builder()
        .authentication(new ApiKeyAuth("amx_sk_your_secret_key"))
        .environment(Environment.PRODUCTION)
        .build()
);

// OAuth2 flow
AIMatrixClient oauthClient = new AIMatrixClient(
    AIMatrixConfig.builder()
        .authentication(OAuth2Auth.builder()
            .clientId("your-client-id")
            .redirectUri("https://myapp.com/callback")
            .scopes("agents:read", "agents:write", "twins:manage")
            .usePkce(true)
            .build())
        .build()
);

// Handle OAuth flow
public CompletableFuture<String> handleOAuthFlow() {
    return oauthClient.auth().getAuthorizationUrl()
        .thenAccept(authUrl -> System.out.println("Visit: " + authUrl))
        .thenCompose(v -> {
            // After user authorizes, get the authorization code
            String authCode = "authorization_code"; // From callback
            return oauthClient.auth().exchangeCodeForTokens(authCode);
        })
        .thenApply(tokens -> tokens.getAccessToken());
}

// Service Account
AIMatrixClient serviceClient = new AIMatrixClient(
    AIMatrixConfig.builder()
        .authentication(ServiceAccountAuth.builder()
            .serviceAccountKeyFile("service-account.json")
            .scopes("https://www.googleapis.com/auth/aimatrix")
            .build())
        .build()
);
```

## Spring Boot Integration

```java
// Configuration
@Configuration
@EnableConfigurationProperties(AIMatrixProperties.class)
public class AIMatrixConfiguration {

    @Bean
    @ConditionalOnMissingBean
    public AIMatrixClient aiMatrixClient(AIMatrixProperties properties) {
        return new AIMatrixClient(
            AIMatrixConfig.builder()
                .apiKey(properties.getApiKey())
                .environment(properties.getEnvironment())
                .baseUrl(properties.getBaseUrl())
                .timeout(properties.getTimeout())
                .retryPolicy(RetryPolicy.builder()
                    .maxRetries(properties.getRetryPolicy().getMaxRetries())
                    .backoffFactor(properties.getRetryPolicy().getBackoffFactor())
                    .build())
                .build()
        );
    }

    @Bean
    public CustomerServiceAgent customerServiceAgent(AIMatrixClient client) {
        return new CustomerServiceAgent(client);
    }
}

// Properties
@ConfigurationProperties(prefix = "aimatrix")
@Data
public class AIMatrixProperties {
    private String apiKey;
    private Environment environment = Environment.PRODUCTION;
    private String baseUrl;
    private Duration timeout = Duration.ofSeconds(30);
    private RetryPolicyProperties retryPolicy = new RetryPolicyProperties();

    @Data
    public static class RetryPolicyProperties {
        private int maxRetries = 3;
        private int backoffFactor = 2;
    }
}

// Service implementation
@Service
public class CustomerServiceAgent {
    private final AIMatrixClient client;
    private final Logger logger = LoggerFactory.getLogger(CustomerServiceAgent.class);
    private static final String AGENT_ID = "customer-service-agent";

    public CustomerServiceAgent(AIMatrixClient client) {
        this.client = client;
    }

    public CompletableFuture<String> processCustomerInquiry(String inquiry) {
        return client.agents().invoke(AGENT_ID, 
            InvocationRequest.builder()
                .message(inquiry)
                .context(Map.of(
                    "timestamp", Instant.now().toString(),
                    "source", "web-portal"
                ))
                .build()
        )
        .thenApply(InvocationResult::getMessage)
        .exceptionally(throwable -> {
            logger.error("Failed to process customer inquiry", throwable);
            return "I apologize, but I'm experiencing technical difficulties. Please try again later.";
        });
    }
}

// Controller
@RestController
@RequestMapping("/api/customer-service")
public class CustomerServiceController {
    private final CustomerServiceAgent agent;

    public CustomerServiceController(CustomerServiceAgent agent) {
        this.agent = agent;
    }

    @PostMapping("/inquiry")
    public CompletableFuture<ResponseEntity<String>> handleInquiry(@RequestBody String inquiry) {
        return agent.processCustomerInquiry(inquiry)
            .thenApply(response -> ResponseEntity.ok(response))
            .exceptionally(throwable -> ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Service temporarily unavailable"));
    }
}
```

## Best Practices

### Error Handling & Resilience

```java
import com.aimatrix.sdk.exceptions.*;
import io.github.resilience4j.retry.Retry;
import io.github.resilience4j.circuitbreaker.CircuitBreaker;

public class ResilientAIMatrixService {
    private final AIMatrixClient client;
    private final Retry retry;
    private final CircuitBreaker circuitBreaker;

    public ResilientAIMatrixService(AIMatrixClient client) {
        this.client = client;
        
        this.retry = Retry.ofDefaults("aimatrix-retry");
        this.circuitBreaker = CircuitBreaker.ofDefaults("aimatrix-circuit-breaker");
    }

    public CompletableFuture<InvocationResult> invokeWithResilience(String agentId, String message) {
        Supplier<CompletableFuture<InvocationResult>> supplier = () -> {
            try {
                return client.agents().invoke(agentId, 
                    InvocationRequest.builder()
                        .message(message)
                        .timeout(Duration.ofSeconds(30))
                        .build()
                );
            } catch (AuthenticationException e) {
                // Refresh tokens and retry
                return client.auth().refreshTokens()
                    .thenCompose(v -> client.agents().invoke(agentId, 
                        InvocationRequest.builder().message(message).build()));
            } catch (RateLimitException e) {
                // Backoff and retry
                return CompletableFuture.failedFuture(e);
            } catch (ValidationException e) {
                // Don't retry validation errors
                logger.error("Validation errors: {}", e.getErrors());
                return CompletableFuture.failedFuture(e);
            }
        };

        return Retry.decorateCompletionStage(retry, 
                CircuitBreaker.decorateCompletionStage(circuitBreaker, supplier))
            .get()
            .toCompletableFuture();
    }
}
```

### Resource Management

```java
// Try-with-resources
public void processWithAutoClose() {
    try (AIMatrixClient client = new AIMatrixClient("api-key")) {
        CompletableFuture<InvocationResult> result = client.agents().invoke("agent-id", 
            InvocationRequest.builder().message("Hello").build());
        
        // Process result
        result.join();
        
        // Client automatically closed
    }
}

// Manual resource management
public class ManagedAIMatrixService implements AutoCloseable {
    private final AIMatrixClient client;

    public ManagedAIMatrixService(String apiKey) {
        this.client = new AIMatrixClient(apiKey);
    }

    public CompletableFuture<String> processMessage(String message) {
        return client.agents().invoke("agent-id", 
            InvocationRequest.builder().message(message).build())
            .thenApply(InvocationResult::getMessage);
    }

    @Override
    public void close() {
        client.close();
    }
}
```

---

## Summary

AIMatrix provides comprehensive SDK support across five major programming languages, with Kotlin receiving first-class treatment and full feature coverage. Each SDK maintains consistent APIs while leveraging language-specific idioms and patterns.

### Key Features Across All SDKs:

- **Complete Agent Management** - Create, configure, and orchestrate AI agents
- **TwinML Integration** - Build and deploy digital twins with machine learning
- **Workspace Operations** - Manage development environments and code execution
- **Hub Ecosystem** - Publish and install agents from the marketplace
- **Real-time Communication** - WebSocket streaming and event-driven architectures
- **Robust Authentication** - API keys, OAuth2, and service account support

### Language-Specific Strengths:

- **Kotlin** - Coroutines, type-safe builders, null safety, Android compatibility
- **Python** - AsyncIO, Pydantic models, Jupyter integration, scientific computing
- **TypeScript** - Full type safety, React hooks, Node.js/browser support
- **C#** - Task-based async, dependency injection, Unity3D, enterprise features  
- **Java** - CompletableFuture, Spring Boot, Jakarta EE, enterprise patterns

All SDKs are production-ready with comprehensive error handling, retry policies, configuration management, and extensive documentation. Choose the SDK that best fits your technology stack and start building intelligent agents today.

For implementation help, examples, and support:
- [GitHub Repository](https://github.com/aimatrix/sdks)
- [API Documentation](/api)
- [Community Discord](https://discord.gg/aimatrix)
- [Enterprise Support](mailto:enterprise@aimatrix.com)