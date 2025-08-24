---
title: Product Architecture
weight: 2
---

# AIMatrix Product Architecture

Complete technical architecture of the four-product AIMatrix ecosystem.

## Product Overview

AIMatrix consists of four integrated products that work together around the concept of AMX Workspaces:

1. **AIMatrix CLI** - Git-like workspace management tool (Kotlin + Clikt)
2. **AMX Console** - Universal workspace UI (Compose Multiplatform)  
3. **AMX Engine** - Workspace processing engine (Ktor + Kalasim)
4. **AMX Hub** - Workspace hosting platform (Spring Cloud Gateway + Angular)

## AIMatrix CLI

### Purpose
Git-like command-line tool for managing AMX Workspaces (like `git` manages repositories).

### Technology Stack
- **Language**: Kotlin
- **CLI Framework**: Clikt (Command Line Interface for Kotlin)
- **Build Tool**: Gradle
- **Distribution**: Native executables via GraalVM

### Workspace Structure Created by CLI
```
my-workspace/
├── .aimatrix/           # Workspace metadata (like .git/)
├── knowledge/
│   ├── capsules/        # Knowledge capsule files
│   ├── volumes/         # Knowledge volume files
│   └── libraries/       # Knowledge library files
├── agents/              # Agent configuration files
├── workflows/           # Workflow definition files
├── integrations/        # Integration configurations
└── models/              # Custom model files
```

### Key Features (Git-like Operations)
- Workspace initialization (`aimatrix init`)
- Clone workspaces (`aimatrix clone`)
- Stage changes (`aimatrix add`)
- Commit changes (`aimatrix commit`)
- Push to AMX Hub (`aimatrix push`)
- Pull from AMX Hub (`aimatrix pull`)
- Check status (`aimatrix status`)
- View differences (`aimatrix diff`)

### Git-like Commands Structure
```kotlin
class AimatrixCli : CliktCommand() {
    override fun run() = Unit
}

class InitCommand : CliktCommand(name = "init") {
    override fun run() {
        // Initialize new AMX workspace (like git init)
        createWorkspaceStructure()
    }
}

class CloneCommand : CliktCommand(name = "clone") {
    override fun run() {
        // Clone workspace from AMX Hub (like git clone)
    }
}

class CommitCommand : CliktCommand(name = "commit") {
    override fun run() {
        // Commit workspace changes (like git commit)
    }
}

class PushCommand : CliktCommand(name = "push") {
    override fun run() {
        // Push to AMX Hub (like git push)
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
The processing engine that reads workspace files and executes simulations, agents, and integrations locally or in the cloud.

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
GitHub-like platform for hosting AMX Workspaces (not storing knowledge directly - knowledge is stored as files within workspaces).

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

#### Workspace Hosting (Like GitHub)
```kotlin
@Service
class WorkspaceService {
    fun createWorkspace(owner: User, name: String): Workspace
    fun forkWorkspace(original: Workspace, owner: User): Workspace
    fun cloneWorkspace(workspace: Workspace): CloneInfo
    fun pushWorkspace(workspace: Workspace, changes: Changes)
    fun pullWorkspace(workspace: Workspace): Changes
    fun versionControl(workspace: Workspace): Version
    fun collaborate(workspace: Workspace, users: List<User>)
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
1. **CLI → Workspace Files**: Create, modify workspace structure and files
2. **CLI → Hub**: Push/pull workspace changes (like git push/pull)
3. **Engine → Workspace Files**: Read knowledge, agents, workflows from files
4. **Console → Engine**: User interactions, monitoring, control
5. **Hub**: Hosts workspaces for collaboration and version control

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