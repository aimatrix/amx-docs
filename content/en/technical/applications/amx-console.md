---
title: "AMX Console"
description: "Universal user interface with conversational and graphical UI, built with Compose Multiplatform for all platforms"
weight: 1
date: 2025-08-23
toc: true
tags: ["console", "cross-platform", "conversational-ui", "gui", "desktop", "mobile", "compose-multiplatform"]
---

## The Universal Interface for Everyone

AMX Console is the user-facing application that employees, customers, and suppliers use to interact with AIMatrix. Built with Compose Multiplatform, it provides native applications for iOS, Android, Windows, macOS, and Linux. The console combines conversational UI with traditional graphical interfaces, includes the studio functionality for workspace configuration, and serves as the primary interface for all users.

## Key Features

### 🎯 Hybrid Interface
- **Conversational UI**: Natural language interactions with AI agents
- **Graphical UI**: Traditional interface for structured tasks  
- **Studio Mode**: Configure workspaces and agent behaviors
- **Seamless Switching**: Move between modes effortlessly

### 📱 True Multi-Platform with Compose Multiplatform
- **One Codebase**: Single Kotlin codebase for all platforms
- **Native Performance**: Not web wrappers - true native apps
- **Platform Integration**: Deep OS-level integration
- **Consistent Experience**: Same features across all devices

## Platform Support

| Platform | Conversational UI | Graphical UI | Studio Mode | Native Features |
|----------|------------------|--------------|-------------|-----------------|
| **iOS** | ✅ | ✅ | ✅ | Face ID, Push Notifications, Widgets |
| **Android** | ✅ | ✅ | ✅ | Material You, Biometric Auth, Widgets |
| **Windows** | ✅ | ✅ | ✅ | System Tray, Windows Hello, Notifications |
| **macOS** | ✅ | ✅ | ✅ | Touch Bar, Menu Bar, Continuity |
| **Linux** | ✅ | ✅ | ✅ | System Tray, Desktop Integration |

## Architecture

```kotlin
// Compose Multiplatform architecture
@Composable
fun AMXConsoleApp() {
    val viewModel = rememberConsoleViewModel()
    
    MaterialTheme {
        when (viewModel.currentMode) {
            ConsoleMode.CONVERSATIONAL -> ConversationalUI(viewModel)
            ConsoleMode.GRAPHICAL -> GraphicalUI(viewModel)
            ConsoleMode.STUDIO -> StudioUI(viewModel)
            ConsoleMode.HYBRID -> HybridUI(viewModel)
        }
    }
}

@Composable
fun ConversationalUI(viewModel: ConsoleViewModel) {
    Column {
        // Conversation history
        LazyColumn(
            reverseLayout = true,
            modifier = Modifier.weight(1f)
        ) {
            items(viewModel.conversations) { message ->
                MessageBubble(message)
            }
        }
        
        // Input area
        MessageInput(
            onSend = { text ->
                viewModel.sendMessage(text)
            }
        )
    }
}

@Composable
fun GraphicalUI(viewModel: ConsoleViewModel) {
    Row {
        // Navigation sidebar
        NavigationRail {
            TodosTab()
            ConversationsTab()
            AgentsTab()
            WorkflowsTab()
            SettingsTab()
        }
        
        // Main content area
        Box(modifier = Modifier.fillMaxSize()) {
            when (viewModel.selectedTab) {
                Tab.TODOS -> TodoListView(viewModel.todos)
                Tab.CONVERSATIONS -> ConversationListView(viewModel.conversations)
                Tab.AGENTS -> AgentMonitoringView(viewModel.agents)
                Tab.WORKFLOWS -> WorkflowView(viewModel.workflows)
                Tab.SETTINGS -> SettingsView(viewModel.settings)
            }
        }
    }
}
```

## Core Capabilities

### 📝 Todo Management
- View AI-generated todos
- Prioritize and organize tasks
- Track completion status
- Collaborative task assignment
- Due date management
- Recurring task support

### 💬 Conversation Hub
- All AI conversations in one place
- Multi-channel aggregation (email, chat, voice)
- Context preservation across sessions
- Search conversation history
- Export conversation logs
- Real-time translation

### 🤖 Agent Monitoring
- See AI agents responding to customers
- Monitor performance metrics
- Intervene when necessary
- Provide training feedback
- View agent decision logs
- Track success rates

### 🎨 Studio Mode (Workspace Configuration)
The studio functionality is integrated directly into AMX Console, allowing users to:

```kotlin
@Composable
fun StudioUI(viewModel: StudioViewModel) {
    Row {
        // Workspace explorer
        Column(modifier = Modifier.width(250.dp)) {
            WorkspaceExplorer(
                workspaces = viewModel.workspaces,
                onSelect = { workspace ->
                    viewModel.selectWorkspace(workspace)
                }
            )
        }
        
        // Configuration panels
        Column(modifier = Modifier.weight(1f)) {
            TabRow(selectedTabIndex = viewModel.selectedTab) {
                Tab(text = { Text("Agents") })
                Tab(text = { Text("Workflows") })
                Tab(text = { Text("Integrations") })
                Tab(text = { Text("Settings") })
            }
            
            when (viewModel.selectedTab) {
                0 -> AgentDesigner(viewModel.currentWorkspace)
                1 -> WorkflowBuilder(viewModel.currentWorkspace)
                2 -> IntegrationManager(viewModel.currentWorkspace)
                3 -> WorkspaceSettings(viewModel.currentWorkspace)
            }
        }
    }
}
```

### Agent Designer
```kotlin
@Composable
fun AgentDesigner(workspace: Workspace) {
    Column {
        // Agent properties
        TextField(
            value = workspace.agent.name,
            onValueChange = { workspace.agent.name = it },
            label = { Text("Agent Name") }
        )
        
        // Capabilities selection
        LazyColumn {
            items(AvailableCapabilities.all) { capability ->
                CheckboxListItem(
                    text = capability.name,
                    checked = workspace.agent.hasCapability(capability),
                    onCheckedChange = { checked ->
                        if (checked) {
                            workspace.agent.addCapability(capability)
                        } else {
                            workspace.agent.removeCapability(capability)
                        }
                    }
                )
            }
        }
        
        // Behavior configuration
        BehaviorEditor(workspace.agent.behavior)
    }
}
```

### Workflow Builder
```kotlin
@Composable
fun WorkflowBuilder(workspace: Workspace) {
    Box {
        // Visual workflow canvas
        Canvas(modifier = Modifier.fillMaxSize()) {
            drawWorkflowNodes(workspace.workflow.nodes)
            drawWorkflowConnections(workspace.workflow.connections)
        }
        
        // Drag and drop node palette
        NodePalette(
            onNodeDrop = { nodeType, position ->
                workspace.workflow.addNode(nodeType, position)
            }
        )
    }
}
```

## User Scenarios

### For Employees
```kotlin
// Morning routine
class EmployeeDayStart {
    fun startDay() {
        // Open AMX Console
        amxConsole.launch()
        
        // Check AI-prioritized todos
        val todos = amxConsole.getTodos()
            .sortedBy { it.priority }
            .filter { it.dueDate == today }
        
        // Review overnight AI actions
        val aiActions = amxConsole.getAIActions(
            since = yesterday.endOfDay,
            requiresReview = true
        )
        
        // Start conversational mode for quick tasks
        amxConsole.switchToConversational()
        amxConsole.say("Show me urgent customer issues")
    }
}
```

### For Customers
```kotlin
// Customer interaction
class CustomerExperience {
    fun getSupport() {
        // Open AMX Console (web or mobile)
        val console = AMXConsole.forCustomer()
        
        // Natural language support
        console.chat("I need help with my order #12345")
        
        // AI agent responds immediately
        // Shows order status, shipping info, etc.
        
        // Escalate if needed
        if (needsHuman) {
            console.requestHumanAgent()
        }
    }
}
```

### For Suppliers
```kotlin
// Supplier portal
class SupplierInterface {
    fun manageOrders() {
        val console = AMXConsole.forSupplier()
        
        // View purchase orders
        val orders = console.getPurchaseOrders()
        
        // Update inventory levels
        console.updateInventory(product, quantity)
        
        // Communicate via AI
        console.chat("When can you deliver 500 units of SKU-789?")
    }
}
```

## Installation

### Desktop Installation

#### From AIMatrix CLI
```bash
# Install AMX Console via AIMatrix CLI
aimatrix console install

# Launch AMX Console
aimatrix console launch

# Configure console settings
aimatrix console config --theme matrix --mode hybrid
```

#### Direct Download
- **Windows**: Download from Microsoft Store or `.exe` from aimatrix.com
- **macOS**: Download from Mac App Store or `.dmg` from aimatrix.com  
- **Linux**: Available via Snap, Flatpak, or AppImage

### Mobile Installation
- **iOS**: Download from Apple App Store
- **Android**: Download from Google Play Store

### Configuration
```yaml
# ~/.amx/console.yaml
console:
  # Interface settings
  interface:
    default_mode: "hybrid"
    theme: "matrix"
    language: "en"
    
  # Connection to AMX Engine
  engine:
    url: "http://localhost:8080"
    auto_connect: true
    
  # Studio settings
  studio:
    auto_save: true
    workspace_dir: "~/.amx/workspaces"
    
  # Sync with AMX Hub
  hub:
    url: "https://hub.aimatrix.com"
    sync_interval: 300  # seconds
```

## Development with Compose Multiplatform

### Project Structure
```
amx-console/
├── shared/
│   ├── src/commonMain/kotlin/
│   │   ├── ui/
│   │   │   ├── conversational/
│   │   │   ├── graphical/
│   │   │   └── studio/
│   │   ├── viewmodels/
│   │   ├── data/
│   │   └── navigation/
│   └── src/commonTest/
├── androidApp/
│   └── src/main/
├── iosApp/
│   └── iosApp/
├── desktopApp/
│   └── src/jvmMain/
└── build.gradle.kts
```

### Shared UI Components
```kotlin
// Common UI components across all platforms
@Composable
expect fun PlatformSpecificButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
)

// iOS implementation
@Composable
actual fun PlatformSpecificButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier
) {
    // iOS-specific styling
    Button(
        onClick = onClick,
        modifier = modifier,
        colors = ButtonDefaults.buttonColors(
            containerColor = Color(0xFF007AFF)  // iOS blue
        )
    ) {
        Text(text)
    }
}

// Android implementation  
@Composable
actual fun PlatformSpecificButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier
) {
    // Material You dynamic colors
    Button(
        onClick = onClick,
        modifier = modifier,
        colors = ButtonDefaults.buttonColors(
            containerColor = MaterialTheme.colorScheme.primary
        )
    ) {
        Text(text)
    }
}
```

### Platform-Specific Features

#### iOS-Specific
```swift
// iOS-specific integrations
class IOSIntegration {
    func configureFaceID() {
        // Face ID authentication
    }
    
    func setupWidgets() {
        // iOS widgets for todos
    }
    
    func enableSiri() {
        // Siri shortcuts for AMX Console
    }
}
```

#### Android-Specific
```kotlin
// Android-specific features
class AndroidIntegration {
    fun setupMaterialYou() {
        // Dynamic color theming
    }
    
    fun createWidgets() {
        // Android home screen widgets
    }
    
    fun integrateAssistant() {
        // Google Assistant actions
    }
}
```

## Integration with Other Products

### With AIMatrix CLI
```bash
# CLI launches Console
aimatrix console

# CLI configures Console
aimatrix console config --engine-url "http://localhost:8080"

# CLI updates Console
aimatrix console update
```

### With AMX Engine
```kotlin
// Console connects to Engine
class EngineConnection {
    private val engine = AMXEngineClient("http://localhost:8080")
    
    suspend fun connect() {
        engine.connect()
        
        // Subscribe to real-time updates
        engine.subscribe { event ->
            when (event) {
                is AgentEvent -> updateAgentStatus(event)
                is WorkflowEvent -> updateWorkflow(event)
                is SystemEvent -> handleSystemEvent(event)
            }
        }
    }
}
```

### With AMX Hub
```kotlin
// Sync workspaces with Hub
class HubSync {
    private val hub = AMXHubClient("https://hub.aimatrix.com")
    
    suspend fun syncWorkspace(workspace: Workspace) {
        // Upload workspace to Hub
        hub.uploadWorkspace(workspace)
        
        // Download shared workspaces
        val sharedWorkspaces = hub.getSharedWorkspaces()
        
        // Apply updates
        mergeWorkspaces(sharedWorkspaces)
    }
}
```

## Best Practices

### Performance Optimization
- Use lazy loading for large data sets
- Implement virtual scrolling for lists
- Cache frequently accessed data
- Optimize image loading with Coil

### User Experience
- Provide offline functionality
- Show loading states clearly
- Implement pull-to-refresh
- Support keyboard shortcuts on desktop

### Security
- Encrypt local storage
- Use biometric authentication
- Implement session timeout
- Secure communication with Engine

---

*AMX Console - The universal interface for AIMatrix, bringing conversational AI and workspace configuration to every platform*