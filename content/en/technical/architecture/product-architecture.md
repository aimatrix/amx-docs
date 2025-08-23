---
title: Product Architecture
weight: 2
---

# AIMatrix Product Architecture

Complete technical architecture of the four-product AIMatrix ecosystem.

## Product Overview

AIMatrix consists of four integrated products, each built with specific technologies for optimal performance:

1. **AIMatrix CLI** - Kotlin + Clikt
2. **AMX Console** - Compose Multiplatform  
3. **AMX Engine** - Ktor
4. **AMX Hub** - Spring Cloud Gateway + Angular

## AIMatrix CLI

### Purpose
Free command-line tool for developers and power users to manage AIMatrix environments.

### Technology Stack
- **Language**: Kotlin
- **CLI Framework**: Clikt (Command Line Interface for Kotlin)
- **Build Tool**: Gradle
- **Distribution**: Native executables via GraalVM

### Architecture
```
aimatrix-cli/
├── src/main/kotlin/
│   ├── commands/
│   │   ├── InitCommand.kt
│   │   ├── EngineCommand.kt
│   │   ├── ConsoleCommand.kt
│   │   └── HubCommand.kt
│   ├── services/
│   │   ├── EngineManager.kt
│   │   ├── AuthService.kt
│   │   └── ConfigService.kt
│   └── Application.kt
├── build.gradle.kts
└── native-image/
```

### Key Features
- Environment initialization and setup
- Engine lifecycle management
- Desktop app launcher for AMX Console
- User authentication and account management
- Workspace synchronization with AMX Hub

### Commands Structure
```kotlin
class AimatrixCli : CliktCommand() {
    override fun run() = Unit
}

class InitCommand : CliktCommand(name = "init") {
    override fun run() {
        // Initialize AIMatrix workspace
    }
}

class EngineCommand : CliktCommand(name = "engine") {
    override fun run() = Unit
}

class StartEngine : CliktCommand(name = "start") {
    override fun run() {
        // Start AMX Engine daemon
    }
}
```

---

## AMX Console

### Purpose
Universal user interface for all stakeholders (employees, customers, suppliers) with both conversational and graphical UI.

### Technology Stack
- **Framework**: Compose Multiplatform
- **Language**: Kotlin
- **Platforms**: iOS, Android, Desktop (Windows, macOS, Linux)
- **Architecture**: MVVM with Coroutines and Flow

### Project Structure
```
amx-console/
├── shared/
│   ├── src/commonMain/kotlin/
│   │   ├── ui/
│   │   │   ├── conversations/
│   │   │   ├── todos/
│   │   │   └── agents/
│   │   ├── viewmodels/
│   │   ├── repositories/
│   │   └── models/
│   └── src/commonTest/
├── androidApp/
├── iosApp/
├── desktopApp/
└── build.gradle.kts
```

### UI Components
```kotlin
@Composable
fun ConversationalUI() {
    Column {
        ConversationList()
        MessageInput()
        AgentResponseView()
    }
}

@Composable
fun TodoListUI() {
    LazyColumn {
        items(todos) { todo ->
            TodoItem(todo)
        }
    }
}

@Composable
fun AgentMonitoringUI() {
    // Real-time agent activity monitoring
}
```

### Platform-Specific Features
- **Mobile**: Push notifications, camera integration, location services
- **Desktop**: System tray, keyboard shortcuts, file system access
- **All Platforms**: Offline mode, data sync, real-time updates

---

## AMX Engine

### Purpose
The core simulation and agent orchestration engine that runs digital twins, manages agents, and handles integrations.

### Technology Stack
- **Framework**: Ktor (Kotlin async web framework)
- **Simulation**: Kalasim (discrete event simulation)
- **Database**: PostgreSQL with Supabase
- **Message Queue**: Kafka/RabbitMQ
- **Container**: Docker/Kubernetes

### Architecture
```
amx-engine/
├── src/main/kotlin/
│   ├── core/
│   │   ├── DigitalTwinFactory.kt
│   │   ├── AgentOrchestrator.kt
│   │   └── SimulationEngine.kt
│   ├── servers/
│   │   ├── mcp/
│   │   │   ├── MCPServer.kt
│   │   │   └── ProtocolTranslator.kt
│   │   └── a2a/
│   │       ├── A2AServer.kt
│   │       └── AgentCommunication.kt
│   ├── integrations/
│   │   ├── ERPConnector.kt
│   │   ├── CRMConnector.kt
│   │   └── WebhookHandler.kt
│   └── Application.kt
├── docker/
│   └── Dockerfile
└── kubernetes/
    └── deployment.yaml
```

### Core Components

#### Digital Twin Factory
```kotlin
class DigitalTwinFactory {
    fun createBusinessTwin(config: TwinConfig): DigitalTwin {
        return DigitalTwin(
            processes = modelBusinessProcesses(config),
            agents = createAgents(config),
            simulation = KalasimEngine()
        )
    }
    
    fun runSimulation(twin: DigitalTwin, scenario: Scenario) {
        // Run predictive simulations
    }
}
```

#### MCP Server Implementation
```kotlin
class MCPServer {
    fun translateProtocol(source: System, target: System, data: Any) {
        // Universal protocol translation
    }
    
    fun syncData(systems: List<System>) {
        // Real-time data synchronization
    }
}
```

#### Agent-to-Agent Communication
```kotlin
class A2AServer {
    fun handleAgentMessage(from: Agent, to: Agent, message: Message) {
        // Inter-agent communication protocol
    }
    
    fun coordinateAgents(agents: List<Agent>, task: Task) {
        // Multi-agent coordination
    }
}
```

### Deployment Modes
- **Daemon Mode**: Background service on local machines
- **Server Mode**: Dedicated server deployment
- **Cloud Mode**: Kubernetes cluster deployment
- **Edge Mode**: IoT and edge computing scenarios

---

## AMX Hub

### Purpose
GitHub-like collaboration platform for hosting workspaces, managing webhooks, and orchestrating cloud engines.

### Technology Stack
- **Backend**: Spring Cloud Gateway (Reactive Kotlin)
- **Frontend**: Angular (TypeScript)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: RabbitMQ
- **Storage**: S3-compatible object storage

### Backend Architecture
```
amx-hub-backend/
├── src/main/kotlin/
│   ├── gateway/
│   │   ├── RouteConfiguration.kt
│   │   ├── AuthFilter.kt
│   │   └── RateLimiter.kt
│   ├── services/
│   │   ├── WorkspaceService.kt
│   │   ├── WebhookService.kt
│   │   ├── EngineOrchestrator.kt
│   │   └── SubscriptionService.kt
│   ├── repositories/
│   └── Application.kt
└── build.gradle.kts
```

### Frontend Architecture
```
amx-hub-frontend/
├── src/
│   ├── app/
│   │   ├── workspaces/
│   │   ├── webhooks/
│   │   ├── engines/
│   │   └── billing/
│   ├── services/
│   ├── models/
│   └── environments/
├── angular.json
└── package.json
```

### Key Features

#### Workspace Management
```kotlin
@Service
class WorkspaceService {
    fun createWorkspace(owner: User, config: WorkspaceConfig): Workspace
    fun versionControl(workspace: Workspace): Version
    fun collaborate(workspace: Workspace, users: List<User>)
    fun backup(workspace: Workspace): BackupResult
}
```

#### Webhook Reservoir
```kotlin
@RestController
class WebhookController {
    @PostMapping("/webhooks/{integration}")
    fun handleWebhook(
        @PathVariable integration: String,
        @RequestBody payload: String
    ): Mono<ResponseEntity<Any>> {
        // Process webhooks from Telegram, WhatsApp, etc.
    }
}
```

#### Engine Orchestration
```kotlin
@Service
class EngineOrchestrator {
    fun spinUpEngine(workspace: Workspace): Engine {
        // Like GitHub Actions - spin up engine on demand
    }
    
    fun scaleEngines(load: LoadMetrics) {
        // Auto-scaling based on load
    }
}
```

### API Gateway Configuration
```kotlin
@Configuration
class GatewayConfig {
    @Bean
    fun routes(builder: RouteLocatorBuilder): RouteLocator {
        return builder.routes()
            .route("workspace-route") { r ->
                r.path("/api/workspaces/**")
                    .filters { f ->
                        f.requestRateLimiter { c ->
                            c.setRateLimiter(redisRateLimiter())
                        }
                    }
                    .uri("lb://workspace-service")
            }
            .build()
    }
}
```

---

## Integration Architecture

### Product Communication Flow
```
┌──────────────┐
│ AIMatrix CLI │
└──────┬───────┘
       │ Manages
       ▼
┌──────────────┐     Connects      ┌──────────────┐
│  AMX Engine  │◄──────────────────►│ AMX Console  │
└──────┬───────┘                    └──────────────┘
       │ Syncs
       ▼
┌──────────────┐
│   AMX Hub    │
└──────────────┘
```

### Data Flow
1. **CLI → Engine**: Lifecycle management, configuration
2. **Console → Engine**: User interactions, queries, commands
3. **Engine → Hub**: Workspace sync, backup, cloud burst
4. **Hub → Engine**: Orchestration, scaling, deployment

### Authentication Flow
- All products use JWT tokens
- AMX Hub acts as identity provider
- Single sign-on across all products
- OAuth2 support for enterprise SSO

---

## Technology Decisions Rationale

### Why Kotlin Everywhere (Except Angular)?
- **Code Sharing**: Maximum code reuse across products
- **Type Safety**: Compile-time safety for enterprise reliability
- **Coroutines**: Superior async programming model
- **Multiplatform**: Single codebase for multiple platforms

### Why Angular for Hub Frontend?
- **Enterprise Features**: Robust framework for complex UIs
- **TypeScript**: Type safety in frontend
- **Material Design**: Professional UI components
- **Community**: Large ecosystem and support

### Why Specific Frameworks?
- **Clikt**: Best Kotlin CLI framework
- **Compose Multiplatform**: True native performance
- **Ktor**: Lightweight, async, perfect for engines
- **Spring Cloud Gateway**: Enterprise-grade API management
- **Kalasim**: Powerful discrete event simulation

---

## Development Guidelines

### Code Organization
- Domain-driven design principles
- Clean architecture with clear boundaries
- Repository pattern for data access
- Dependency injection throughout

### Testing Strategy
- Unit tests for business logic
- Integration tests for APIs
- UI tests for critical workflows
- Performance tests for engines

### Deployment Pipeline
- GitHub Actions for CI/CD
- Docker containers for all services
- Kubernetes for orchestration
- Terraform for infrastructure

---

*Technical documentation for AIMatrix four-product ecosystem*