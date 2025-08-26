---
title: "Open Source Tools We Love: The Stack Powering AIMatrix"
description: "The open source tools that saved us months of development time building AIMatrix. From vector databases to testing frameworks, here's our honest take on what works and what doesn't."
date: 2025-07-10
author: "David Park"
authorTitle: "Platform Engineering Lead"
readTime: "7 min read"
categories: ["Engineering", "Open Source", "Tools"]
tags: ["Open Source", "Tools", "Infrastructure", "Engineering"]
image: "/images/blog/open-source-stack.jpg"
featured: false
---

Building AIMatrix wouldn't have been possible without the incredible open source ecosystem. These tools saved us literally months of development time and helped us focus on what makes our platform unique.

Here's our honest take on the open source tools we rely on daily, including what works great, what's frustrating, and how we contribute back.

## Vector Database: Qdrant

**Why we chose it:** When we were evaluating vector databases (Pinecone, Weaviate, Chroma), Qdrant struck the best balance of performance, features, and operational simplicity.

```rust
// Our Qdrant setup for agent memory storage
use qdrant_client::{
    prelude::*,
    qdrant::{vectors_config::Config, CreateCollection, VectorParams, VectorsConfig},
};

async fn setup_agent_memory_collection() -> Result<(), Box<dyn std::error::Error>> {
    let client = QdrantClient::from_url("http://localhost:6334").build()?;
    
    client.create_collection(&CreateCollection {
        collection_name: "agent_memories".to_string(),
        vectors_config: Some(VectorsConfig {
            config: Some(Config::Params(VectorParams {
                size: 1536, // OpenAI ada-002 embedding size
                distance: Distance::Cosine.into(),
                ..Default::default()
            })),
        }),
        ..Default::default()
    }).await?;
    
    Ok(())
}
```

**What we love:**
- **Performance:** Handles our 10M+ vector searches per day without breaking a sweat
- **Filtering:** Complex metadata filtering works exactly as expected
- **API design:** RESTful API is intuitive, gRPC option for performance
- **Operational simplicity:** Single binary, reasonable resource usage
- **Clustering:** Built-in distributed mode for high availability

**What's annoying:**
- **Memory usage:** Can be memory-hungry with large collections
- **Documentation:** Some advanced features lack detailed examples
- **Migration tools:** Moving from other vector DBs requires custom tooling

**Our contribution:**
We've contributed performance benchmarks and documentation improvements, particularly around metadata filtering patterns.

## Testing: Testcontainers

**Why it's essential:** Testing AI systems requires realistic data stores, message queues, and external services. Testcontainers lets us spin up real infrastructure for tests.

```kotlin
class AgentIntegrationTest {
    companion object {
        @Container
        val postgres = PostgreSQLContainer("postgres:15")
            .withDatabaseName("test_agents")
            .withUsername("test")
            .withPassword("test")
        
        @Container
        val redis = GenericContainer("redis:7-alpine")
            .withExposedPorts(6379)
        
        @Container
        val qdrant = GenericContainer("qdrant/qdrant:v1.7.0")
            .withExposedPorts(6334)
    }
    
    @Test
    fun `agent should persist conversation state correctly`() = runTest {
        // Test with real database, no mocking needed
        val agent = createTestAgent(
            dbUrl = postgres.jdbcUrl,
            redisUrl = "redis://localhost:${redis.firstMappedPort}",
            qdrantUrl = "http://localhost:${qdrant.firstMappedPort}"
        )
        
        val conversation = agent.startConversation("user123")
        agent.processMessage(conversation.id, "Hello")
        
        // Verify state is actually persisted
        val retrieved = agent.getConversation(conversation.id)
        assertThat(retrieved.messages).hasSize(1)
    }
}
```

**What we love:**
- **Real environment testing:** No more "works in tests, fails in prod" surprises
- **Easy setup:** Container management is completely handled
- **Multiple languages:** Works with our Kotlin, Python, and Node.js services
- **CI/CD friendly:** Plays well with GitHub Actions and other CI systems

**What's challenging:**
- **Startup time:** Tests can be slower, especially with multiple containers
- **Resource usage:** CI/CD systems need more memory and CPU
- **Flaky networks:** Occasional container networking issues in CI
- **Debugging:** When tests fail, container logs can be hard to access

## Message Queue: Apache Pulsar

**Why we picked it over Kafka:** Multi-tenancy, geo-replication, and built-in schema registry made Pulsar the better choice for our agent communication needs.

```java
// Agent message routing with Pulsar
public class AgentMessageRouter {
    private final PulsarClient client;
    private final Producer<AgentMessage> producer;
    private final Consumer<AgentMessage> consumer;
    
    public AgentMessageRouter(String pulsarUrl) throws PulsarClientException {
        this.client = PulsarClient.builder()
            .serviceUrl(pulsarUrl)
            .build();
            
        this.producer = client.newProducer(Schema.JSON(AgentMessage.class))
            .topic("persistent://aimatrix/agents/messages")
            .sendTimeout(1, TimeUnit.SECONDS)
            .create();
            
        this.consumer = client.newConsumer(Schema.JSON(AgentMessage.class))
            .topic("persistent://aimatrix/agents/messages")
            .subscriptionName("agent-processor")
            .subscriptionType(SubscriptionType.Key_Shared)
            .subscribe();
    }
    
    public void routeMessage(String agentId, AgentMessage message) {
        producer.sendAsync(message)
            .thenAccept(msgId -> log.info("Message sent: {}", msgId))
            .exceptionally(ex -> {
                log.error("Failed to send message", ex);
                return null;
            });
    }
}
```

**What works well:**
- **Multi-tenancy:** Perfect for isolating customer data
- **Schema evolution:** Built-in schema registry saves tons of migration headaches
- **Geo-replication:** Automatic data replication across regions
- **Flexible subscriptions:** Key_Shared subscriptions are perfect for agent load balancing

**Pain points:**
- **Operational complexity:** More complex than simpler message queues
- **Learning curve:** Concepts like tenants, namespaces, and subscriptions take time
- **Tooling:** Fewer third-party tools compared to Kafka ecosystem
- **Memory usage:** Can be resource-intensive

## Observability: OpenTelemetry + Jaeger

**Why this combo:** We needed distributed tracing across our polyglot services (Kotlin, Python, Node.js). OpenTelemetry's vendor-neutral approach was perfect.

```kotlin
// Tracing agent interactions
class TracedAgent(private val agent: Agent) : Agent by agent {
    private val tracer = OpenTelemetry.getGlobalTracer("aimatrix-agent")
    
    override suspend fun processMessage(message: String): AgentResponse {
        return tracer.spanBuilder("agent.processMessage")
            .setAttribute("agent.id", agent.id)
            .setAttribute("message.length", message.length)
            .use { span ->
                try {
                    val response = agent.processMessage(message)
                    span.setAttribute("response.success", true)
                    response
                } catch (ex: Exception) {
                    span.recordException(ex)
                    span.setStatus(StatusCode.ERROR, ex.message)
                    throw ex
                }
            }
    }
}
```

**The good:**
- **Vendor neutral:** Not locked into any specific observability platform
- **Language support:** SDKs work consistently across our tech stack
- **Rich context:** Distributed traces show exactly how requests flow through agents
- **Community:** Strong ecosystem and active development

**The frustrating:**
- **Configuration complexity:** Getting all the exporters and samplers right is tricky
- **Performance overhead:** Tracing everything can impact performance
- **Storage costs:** Trace data volumes can get expensive quickly
- **Query complexity:** Finding specific traces in Jaeger can be challenging

## Configuration: Typesafe Config (Lightbend Config)

**Why we still use it:** Despite being Java-focused, it's the most robust configuration library we've found for complex, hierarchical configs.

```hocon
# Our agent configuration in HOCON format
aimatrix {
  agents {
    default {
      timeout = 30s
      max-retries = 3
      memory {
        type = "vector"
        vector-db {
          url = "http://localhost:6334"
          collection = "agent_memories"
        }
      }
    }
    
    conversation-agent = ${aimatrix.agents.default} {
      model = "gpt-4"
      max-context-length = 8000
      memory {
        retention-days = 30
      }
    }
    
    reasoning-agent = ${aimatrix.agents.default} {
      model = "claude-3"
      timeout = 60s  # Reasoning takes longer
      memory {
        retention-days = 90  # Keep reasoning chains longer
      }
    }
  }
}
```

**Why it's great:**
- **Hierarchical configs:** Inheritance and overrides work intuitively
- **Environment handling:** Easy environment-specific configurations
- **Type safety:** Compile-time validation of config structure
- **HOCON format:** More readable than JSON or YAML for complex configs

**Downsides:**
- **Java ecosystem only:** No native support for other languages
- **Learning curve:** HOCON syntax isn't widely known
- **Runtime errors:** Some validation happens at runtime, not compile time

## API Framework: Ktor

**Why we chose it:** Lightweight, Kotlin-native, and perfect for building APIs that integrate with our agent systems.

```kotlin
fun Application.configureRouting() {
    routing {
        route("/api/v1/agents") {
            post("/{agentId}/chat") {
                val agentId = call.parameters["agentId"] ?: return@post call.respond(HttpStatusCode.BadRequest)
                val request = call.receive<ChatRequest>()
                
                val span = tracer.spanBuilder("api.chat").startSpan()
                try {
                    val agent = agentRegistry.getAgent(agentId)
                        ?: return@post call.respond(HttpStatusCode.NotFound)
                    
                    val response = agent.processMessage(request.message)
                    call.respond(HttpStatusCode.OK, response)
                } catch (ex: Exception) {
                    span.recordException(ex)
                    call.respond(HttpStatusCode.InternalServerError, ErrorResponse(ex.message))
                } finally {
                    span.end()
                }
            }
        }
    }
}
```

**What rocks:**
- **Kotlin-first:** Feels natural with our agent code
- **Coroutine support:** Async handling without callback hell
- **Modular:** Use only what you need, no bloat
- **Testing:** Built-in testing support is excellent

**Rough edges:**
- **Ecosystem:** Smaller community compared to Spring Boot
- **Documentation:** Some advanced features need better examples
- **Deployment:** Requires more setup compared to Spring Boot
- **Learning curve:** If your team knows Spring, there's adjustment time

## How We Give Back

**Our contributions to the ecosystem:**

1. **Documentation improvements:** We've added examples for Qdrant metadata filtering and Kalasim custom distributions
2. **Bug reports and fixes:** Fixed memory leaks in Testcontainers and performance issues in Ktor
3. **Benchmark data:** Shared performance comparisons for various vector databases
4. **Example projects:** Open-sourced simplified versions of our agent architectures

**Our open source releases:**
- `aimatrix-agent-sdk`: Simplified SDK for building AI agents (coming soon)
- `simulation-testing-utils`: Testcontainers extensions for simulation testing
- `otel-agent-instrumentation`: OpenTelemetry instrumentation for AI agent systems

## The Hidden Costs

Open source isn't free:

- **Learning time:** Each tool has a learning curve
- **Integration work:** Making everything work together takes effort
- **Operational overhead:** Managing updates, security patches, compatibility
- **Support burden:** When things break, you're the support team

But the benefits far outweigh the costs. These tools let a small team build sophisticated AI infrastructure that would have taken much longer to develop from scratch.

## What's Next

We're evaluating:
- **DuckDB** for analytics workloads (love the simplicity)
- **Grafana Mimir** for metrics (Prometheus is struggling with our scale)
- **Apache Arrow** for data processing between services
- **Temporal** for workflow orchestration (might replace our custom orchestration)

The open source ecosystem for AI infrastructure is evolving rapidly. Tools that didn't exist two years ago are now essential parts of our stack.

Building on open source means we can focus on what makes AIMatrix unique - the agent orchestration and reasoning capabilities - while leveraging the community's work on infrastructure, observability, and data management.

That's a pretty good deal.