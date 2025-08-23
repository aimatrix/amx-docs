---
title: "Mobile Applications"
description: "Native mobile applications built with Kotlin Compose Multiplatform, featuring offline-first architecture, biometric authentication, and seamless AI agent interaction for iOS and Android"
weight: 2
date: 2025-08-23
toc: true
tags: ["mobile", "ios", "android", "kotlin", "compose", "offline-first", "biometric", "native"]
---

# AIMatrix Mobile Applications

## Native Mobile Excellence for AI-First Organizations

AIMatrix Mobile Applications bring the full power of AI agent management and interaction to iOS and Android devices through native applications built with Kotlin Compose Multiplatform (CMP). Designed with an offline-first architecture, these applications ensure productivity and agent connectivity regardless of network conditions while leveraging platform-specific capabilities for optimal user experience.

## Mobile-First Philosophy

Our mobile applications are built on four core principles:

### 🏗️ **Offline-First Architecture**
Every feature works without internet connectivity, with intelligent synchronization when available.

### ⚡ **Native Performance**  
Platform-specific optimizations while maintaining cross-platform code sharing.

### 🔒 **Mobile Security**
Biometric authentication, secure enclaves, and encrypted local storage.

### 🎯 **Context-Aware Intelligence**
Location services, sensors, and mobile-specific AI capabilities.

## Architecture Overview

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[Compose Multiplatform UI]
        NAV[Navigation]
        THEME[Theming System]
    end
    
    subgraph "Business Logic Layer"
        VM[ViewModels]
        UC[Use Cases]
        REPO[Repositories]
    end
    
    subgraph "Data Layer"
        LOCAL[Local Storage]
        REMOTE[Remote APIs]
        CACHE[Cache Manager]
        SYNC[Sync Engine]
    end
    
    subgraph "Platform Layer"
        IOS[iOS Native]
        ANDROID[Android Native]
        SHARED[Shared Code]
    end
    
    subgraph "External Services"
        SUPABASE[Supabase Backend]
        MCP[MCP Servers]
        PUSH[Push Notifications]
        BIOMETRIC[Biometric Services]
    end
    
    UI --> VM
    NAV --> VM
    THEME --> UI
    
    VM --> UC
    UC --> REPO
    
    REPO --> LOCAL
    REPO --> REMOTE
    REPO --> CACHE
    
    CACHE --> SYNC
    SYNC --> External Services
    
    Platform Layer --> Business Logic Layer
    External Services --> Data Layer
```

## Kotlin Compose Multiplatform Framework

### Shared Business Logic
```kotlin
// Shared domain model across platforms
@Serializable
data class AIAgent(
    val id: String,
    val name: String,
    val type: AgentType,
    val status: AgentStatus,
    val capabilities: List<String>,
    val lastActivity: Instant,
    val metrics: AgentMetrics,
    val configuration: Map<String, String>
) {
    val isActive: Boolean get() = status == AgentStatus.ACTIVE
    val healthStatus: HealthStatus get() = calculateHealth()
    
    private fun calculateHealth(): HealthStatus {
        return when {
            metrics.errorRate > 0.1 -> HealthStatus.CRITICAL
            metrics.responseTime > 5000 -> HealthStatus.WARNING
            metrics.cpuUsage > 80 -> HealthStatus.WARNING
            else -> HealthStatus.HEALTHY
        }
    }
}

// Shared business logic
class AgentRepository(
    private val localDataSource: AgentLocalDataSource,
    private val remoteDataSource: AgentRemoteDataSource,
    private val syncManager: SyncManager
) {
    suspend fun getAgents(forceRefresh: Boolean = false): Flow<List<AIAgent>> {
        return if (forceRefresh) {
            // Try remote first, fallback to local
            flow {
                try {
                    val remoteAgents = remoteDataSource.getAgents()
                    localDataSource.insertAgents(remoteAgents)
                    emit(remoteAgents)
                } catch (e: Exception) {
                    emit(localDataSource.getAgents())
                }
            }
        } else {
            // Local first, sync in background
            localDataSource.getAgentsFlow().onStart {
                syncManager.scheduleSync()
            }
        }
    }
    
    suspend fun createAgent(agent: AIAgent): Result<AIAgent> {
        return try {
            // Store locally first
            val localAgent = agent.copy(
                id = UUID.randomUUID().toString(),
                status = AgentStatus.PENDING_SYNC
            )
            
            localDataSource.insertAgent(localAgent)
            
            // Queue for remote sync
            syncManager.queueForSync(localAgent.id)
            
            Result.success(localAgent)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

### Cross-Platform UI Components
```kotlin
// Compose Multiplatform UI components
@Composable
fun AgentListScreen(
    viewModel: AgentListViewModel = koinViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    
    Column {
        // Platform-adaptive top bar
        PlatformTopAppBar(
            title = "AI Agents",
            actions = {
                IconButton(onClick = { viewModel.refreshAgents() }) {
                    Icon(Icons.Default.Refresh, contentDescription = "Refresh")
                }
            }
        )
        
        when (val state = uiState) {
            is AgentListUiState.Loading -> {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    PlatformProgressIndicator()
                }
            }
            
            is AgentListUiState.Success -> {
                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    items(
                        items = state.agents,
                        key = { it.id }
                    ) { agent ->
                        AgentCard(
                            agent = agent,
                            onClick = { viewModel.selectAgent(agent.id) },
                            onStatusToggle = { viewModel.toggleAgentStatus(agent.id) }
                        )
                    }
                }
            }
            
            is AgentListUiState.Error -> {
                ErrorView(
                    error = state.error,
                    onRetry = { viewModel.refreshAgents() }
                )
            }
        }
        
        // Platform-specific floating action button
        PlatformFloatingActionButton(
            onClick = { viewModel.createAgent() },
            modifier = Modifier.align(Alignment.End)
        ) {
            Icon(Icons.Default.Add, contentDescription = "Add Agent")
        }
    }
}

@Composable
fun AgentCard(
    agent: AIAgent,
    onClick: () -> Unit,
    onStatusToggle: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onClick() },
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = agent.name,
                    style = MaterialTheme.typography.headlineSmall
                )
                
                AgentStatusIndicator(
                    status = agent.status,
                    health = agent.healthStatus
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            Text(
                text = "Type: ${agent.type.displayName}",
                style = MaterialTheme.typography.bodyMedium
            )
            
            Text(
                text = "Last Activity: ${agent.lastActivity.toRelativeString()}",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(12.dp))
            
            // Performance metrics
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                MetricChip(
                    label = "CPU",
                    value = "${agent.metrics.cpuUsage}%",
                    color = getCpuColor(agent.metrics.cpuUsage)
                )
                
                MetricChip(
                    label = "Response",
                    value = "${agent.metrics.responseTime}ms",
                    color = getResponseTimeColor(agent.metrics.responseTime)
                )
                
                MetricChip(
                    label = "Success",
                    value = "${(agent.metrics.successRate * 100).toInt()}%",
                    color = getSuccessRateColor(agent.metrics.successRate)
                )
            }
        }
    }
}
```

## Platform-Specific Implementations

### iOS Native Features
```swift
// iOS-specific implementations using expect/actual
import Foundation
import LocalAuthentication
import UIKit
import UserNotifications

// Biometric authentication
actual class BiometricAuthenticator {
    actual suspend fun authenticate(reason: String): AuthResult {
        return withCheckedContinuation { continuation in
            let context = LAContext()
            var error: NSError?
            
            guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, 
                                           error: &error) else {
                continuation.resume(returning: AuthResult.NotAvailable)
                return
            }
            
            context.evaluatePolicy(.deviceOwnerAuthenticationWithBiometrics,
                                  localizedReason: reason) { success, error in
                DispatchQueue.main.async {
                    if success {
                        continuation.resume(returning: AuthResult.Success)
                    } else {
                        continuation.resume(returning: AuthResult.Failed(error?.localizedDescription))
                    }
                }
            }
        }
    }
}

// iOS-specific secure storage
actual class SecureStorage {
    actual suspend fun store(key: String, value: String): Boolean {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: value.data(using: .utf8)!,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        ]
        
        // Delete existing item
        SecItemDelete(query as CFDictionary)
        
        // Add new item
        let status = SecItemAdd(query as CFDictionary, nil)
        return status == errSecSuccess
    }
    
    actual suspend fun retrieve(key: String): String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]
        
        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)
        
        guard status == errSecSuccess,
              let data = result as? Data,
              let value = String(data: data, encoding: .utf8) else {
            return nil
        }
        
        return value
    }
}

// iOS push notifications
actual class PushNotificationManager {
    actual suspend fun requestPermission(): Boolean {
        return withCheckedContinuation { continuation in
            UNUserNotificationCenter.current()
                .requestAuthorization(options: [.alert, .badge, .sound]) { granted, _ in
                    continuation.resume(returning: granted)
                }
        }
    }
    
    actual suspend fun registerForRemoteNotifications() {
        await MainActor.run {
            UIApplication.shared.registerForRemoteNotifications()
        }
    }
    
    actual fun handleNotificationPayload(payload: Map<String, Any>) {
        // Handle FCM payload
        if let agentId = payload["agent_id"] as? String,
           let action = payload["action"] as? String {
            // Navigate to agent detail or handle action
            NotificationCenter.default.post(
                name: .agentNotificationReceived,
                object: nil,
                userInfo: ["agentId": agentId, "action": action]
            )
        }
    }
}
```

### Android Native Features
```kotlin
// Android-specific implementations
actual class BiometricAuthenticator(private val context: Context) {
    actual suspend fun authenticate(reason: String): AuthResult {
        return suspendCoroutine { continuation ->
            val biometricPrompt = BiometricPrompt(
                context as FragmentActivity,
                ContextCompat.getMainExecutor(context),
                object : BiometricPrompt.AuthenticationCallback() {
                    override fun onAuthenticationSucceeded(
                        result: BiometricPrompt.AuthenticationResult
                    ) {
                        continuation.resume(AuthResult.Success)
                    }
                    
                    override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                        continuation.resume(AuthResult.Failed(errString.toString()))
                    }
                    
                    override fun onAuthenticationFailed() {
                        continuation.resume(AuthResult.Failed("Authentication failed"))
                    }
                }
            )
            
            val promptInfo = BiometricPrompt.PromptInfo.Builder()
                .setTitle("Biometric Authentication")
                .setSubtitle(reason)
                .setNegativeButtonText("Cancel")
                .setAllowedAuthenticators(
                    BiometricManager.Authenticators.BIOMETRIC_STRONG or
                    BiometricManager.Authenticators.DEVICE_CREDENTIAL
                )
                .build()
            
            biometricPrompt.authenticate(promptInfo)
        }
    }
}

// Android secure storage using EncryptedSharedPreferences
actual class SecureStorage(private val context: Context) {
    private val sharedPreferences by lazy {
        EncryptedSharedPreferences.create(
            "amx_secure_prefs",
            MasterKey.Builder(context)
                .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
                .build(),
            context,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }
    
    actual suspend fun store(key: String, value: String): Boolean {
        return try {
            sharedPreferences.edit()
                .putString(key, value)
                .apply()
            true
        } catch (e: Exception) {
            false
        }
    }
    
    actual suspend fun retrieve(key: String): String? {
        return sharedPreferences.getString(key, null)
    }
}

// Android push notifications using Firebase
actual class PushNotificationManager(private val context: Context) {
    actual suspend fun requestPermission(): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            ActivityCompat.checkSelfPermission(
                context,
                Manifest.permission.POST_NOTIFICATIONS
            ) == PackageManager.PERMISSION_GRANTED
        } else {
            true // Permissions granted by default on older versions
        }
    }
    
    actual suspend fun registerForRemoteNotifications() {
        FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
            if (!task.isSuccessful) {
                Log.w("FCM", "Fetching FCM registration token failed", task.exception)
                return@addOnCompleteListener
            }
            
            val token = task.result
            Log.d("FCM", "FCM Registration Token: $token")
            
            // Send token to server
            GlobalScope.launch {
                try {
                    supabaseClient.from("device_tokens").insert(
                        mapOf(
                            "token" to token,
                            "platform" to "android",
                            "user_id" to getCurrentUserId()
                        )
                    )
                } catch (e: Exception) {
                    Log.e("FCM", "Failed to register token", e)
                }
            }
        }
    }
}
```

## Offline-First Architecture

### Local Storage Implementation
```kotlin
// SQLite database using Room/SQLDelight
@Database(
    entities = [
        AgentEntity::class,
        WorkflowEntity::class,
        SyncQueueEntity::class,
        CacheEntity::class
    ],
    version = 1,
    exportSchema = false
)
@TypeConverters(Converters::class)
abstract class AMXDatabase : RoomDatabase() {
    abstract fun agentDao(): AgentDao
    abstract fun workflowDao(): WorkflowDao
    abstract fun syncDao(): SyncDao
    abstract fun cacheDao(): CacheDao
    
    companion object {
        @Volatile
        private var INSTANCE: AMXDatabase? = null
        
        fun getDatabase(context: Context): AMXDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AMXDatabase::class.java,
                    "amx_database"
                )
                .addMigrations(MIGRATION_1_2)
                .fallbackToDestructiveMigration()
                .build()
                
                INSTANCE = instance
                instance
            }
        }
    }
}

@Dao
interface AgentDao {
    @Query("SELECT * FROM agents ORDER BY last_activity DESC")
    fun getAllAgentsFlow(): Flow<List<AgentEntity>>
    
    @Query("SELECT * FROM agents WHERE id = :id")
    suspend fun getAgentById(id: String): AgentEntity?
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAgent(agent: AgentEntity)
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAgents(agents: List<AgentEntity>)
    
    @Update
    suspend fun updateAgent(agent: AgentEntity)
    
    @Delete
    suspend fun deleteAgent(agent: AgentEntity)
    
    @Query("DELETE FROM agents WHERE id = :id")
    suspend fun deleteAgentById(id: String)
    
    @Query("SELECT * FROM agents WHERE sync_status = :status")
    suspend fun getAgentsWithSyncStatus(status: SyncStatus): List<AgentEntity>
}
```

### Intelligent Sync Engine
```kotlin
// Background sync implementation
class SyncManager(
    private val database: AMXDatabase,
    private val remoteDataSource: RemoteDataSource,
    private val conflictResolver: ConflictResolver,
    private val notificationManager: NotificationManager
) {
    private val syncQueue = Channel<SyncOperation>(Channel.UNLIMITED)
    private val _syncStatus = MutableStateFlow(SyncStatus.IDLE)
    val syncStatus: StateFlow<SyncStatus> = _syncStatus.asStateFlow()
    
    init {
        // Start sync worker
        GlobalScope.launch {
            processSyncQueue()
        }
        
        // Schedule periodic sync
        schedulePeriodicSync()
    }
    
    suspend fun queueForSync(entityId: String, operation: SyncOperation.Type) {
        val syncOp = SyncOperation(
            id = UUID.randomUUID().toString(),
            entityId = entityId,
            type = operation,
            timestamp = Clock.System.now(),
            attempts = 0
        )
        
        database.syncDao().insertSyncOperation(syncOp.toEntity())
        syncQueue.send(syncOp)
    }
    
    private suspend fun processSyncQueue() {
        while (true) {
            try {
                val operation = syncQueue.receive()
                processSyncOperation(operation)
            } catch (e: Exception) {
                Log.e("SyncManager", "Error processing sync operation", e)
            }
        }
    }
    
    private suspend fun processSyncOperation(operation: SyncOperation) {
        _syncStatus.value = SyncStatus.SYNCING
        
        try {
            when (operation.type) {
                SyncOperation.Type.CREATE -> syncCreateOperation(operation)
                SyncOperation.Type.UPDATE -> syncUpdateOperation(operation)
                SyncOperation.Type.DELETE -> syncDeleteOperation(operation)
            }
            
            // Mark as completed
            database.syncDao().deleteSyncOperation(operation.id)
            
        } catch (e: NetworkException) {
            // Network error - retry later
            val updatedOp = operation.copy(
                attempts = operation.attempts + 1,
                lastAttempt = Clock.System.now()
            )
            
            if (updatedOp.attempts < MAX_RETRY_ATTEMPTS) {
                database.syncDao().updateSyncOperation(updatedOp.toEntity())
                // Exponential backoff
                delay(calculateBackoff(updatedOp.attempts))
                syncQueue.send(updatedOp)
            } else {
                // Max retries exceeded
                handleSyncFailure(operation, e)
            }
            
        } catch (e: ConflictException) {
            // Data conflict - needs resolution
            val resolution = conflictResolver.resolve(e.localData, e.remoteData)
            applySyncResolution(operation, resolution)
            
        } finally {
            _syncStatus.value = SyncStatus.IDLE
        }
    }
    
    private suspend fun syncCreateOperation(operation: SyncOperation) {
        val localEntity = database.agentDao().getAgentById(operation.entityId)
            ?: throw SyncException("Local entity not found: ${operation.entityId}")
        
        try {
            val remoteEntity = remoteDataSource.createAgent(localEntity.toDomain())
            
            // Update local entity with server data
            val updatedEntity = localEntity.copy(
                id = remoteEntity.id, // Server-generated ID
                syncStatus = SyncStatus.SYNCED,
                lastSync = Clock.System.now()
            )
            
            database.agentDao().updateAgent(updatedEntity)
            
        } catch (e: Exception) {
            when (e) {
                is NetworkException -> throw e // Will be retried
                is ValidationException -> {
                    // Mark as failed - won't retry
                    val failedEntity = localEntity.copy(
                        syncStatus = SyncStatus.FAILED,
                        syncError = e.message
                    )
                    database.agentDao().updateAgent(failedEntity)
                }
            }
        }
    }
}
```

## Push Notifications & Background Sync

### Firebase Cloud Messaging Integration
```kotlin
// Firebase Cloud Messaging service
class AMXFirebaseMessagingService : FirebaseMessagingService() {
    override fun onMessageReceived(remoteMessage: RemoteMessage) {
        super.onMessageReceived(remoteMessage)
        
        Log.d("FCM", "From: ${remoteMessage.from}")
        
        // Handle data payload
        if (remoteMessage.data.isNotEmpty()) {
            Log.d("FCM", "Message data payload: ${remoteMessage.data}")
            handleDataMessage(remoteMessage.data)
        }
        
        // Handle notification payload
        remoteMessage.notification?.let {
            Log.d("FCM", "Message Notification Body: ${it.body}")
            showNotification(it.title ?: "AMX", it.body ?: "")
        }
    }
    
    override fun onNewToken(token: String) {
        Log.d("FCM", "Refreshed token: $token")
        sendTokenToServer(token)
    }
    
    private fun handleDataMessage(data: Map<String, String>) {
        when (data["type"]) {
            "agent_status_change" -> {
                val agentId = data["agent_id"] ?: return
                val status = data["status"] ?: return
                
                // Update local database
                GlobalScope.launch {
                    try {
                        val database = AMXDatabase.getDatabase(applicationContext)
                        val agent = database.agentDao().getAgentById(agentId)
                        
                        agent?.let {
                            val updatedAgent = it.copy(
                                status = AgentStatus.valueOf(status),
                                lastSync = Clock.System.now()
                            )
                            database.agentDao().updateAgent(updatedAgent)
                        }
                    } catch (e: Exception) {
                        Log.e("FCM", "Error updating agent status", e)
                    }
                }
                
                // Show notification if app is in background
                if (!isAppInForeground()) {
                    showNotification(
                        "Agent Status Update",
                        "Agent ${data["agent_name"]} is now $status"
                    )
                }
            }
            
            "workflow_completion" -> {
                val workflowId = data["workflow_id"] ?: return
                val success = data["success"]?.toBoolean() ?: false
                
                // Trigger sync for workflow data
                val syncManager = get<SyncManager>()
                GlobalScope.launch {
                    syncManager.queueForSync(workflowId, SyncOperation.Type.UPDATE)
                }
                
                showNotification(
                    "Workflow Complete",
                    if (success) "Workflow completed successfully" else "Workflow failed"
                )
            }
            
            "sync_request" -> {
                // Server requesting full sync
                val syncManager = get<SyncManager>()
                GlobalScope.launch {
                    syncManager.performFullSync()
                }
            }
        }
    }
    
    private fun showNotification(title: String, body: String) {
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        }
        
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_ONE_SHOT or PendingIntent.FLAG_IMMUTABLE
        )
        
        val notificationBuilder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_amx_logo)
            .setContentTitle(title)
            .setContentText(body)
            .setAutoCancel(true)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(pendingIntent)
        
        val notificationManager = NotificationManagerCompat.from(this)
        notificationManager.notify(0, notificationBuilder.build())
    }
    
    private fun sendTokenToServer(token: String) {
        GlobalScope.launch {
            try {
                val supabase = get<SupabaseClient>()
                val userId = get<UserSession>().currentUserId
                
                supabase.from("device_tokens")
                    .upsert(
                        mapOf(
                            "user_id" to userId,
                            "token" to token,
                            "platform" to "android",
                            "last_updated" to Clock.System.now().toString()
                        )
                    )
            } catch (e: Exception) {
                Log.e("FCM", "Failed to send token to server", e)
            }
        }
    }
}
```

### Background Sync Worker
```kotlin
// Android WorkManager for background sync
class SyncWorker(
    context: Context,
    params: WorkerParameters
) : CoroutineWorker(context, params) {
    
    override suspend fun doWork(): Result {
        return try {
            val syncManager = get<SyncManager>()
            val networkManager = get<NetworkManager>()
            
            // Check network connectivity
            if (!networkManager.isConnected()) {
                return Result.retry()
            }
            
            // Perform incremental sync
            val syncResult = syncManager.performIncrementalSync()
            
            when (syncResult) {
                is SyncResult.Success -> {
                    Log.i("SyncWorker", "Sync completed successfully")
                    Result.success()
                }
                
                is SyncResult.PartialFailure -> {
                    Log.w("SyncWorker", "Sync partially failed: ${syncResult.errors}")
                    Result.success() // Don't retry for partial failures
                }
                
                is SyncResult.Failure -> {
                    Log.e("SyncWorker", "Sync failed: ${syncResult.error}")
                    Result.retry()
                }
            }
            
        } catch (e: Exception) {
            Log.e("SyncWorker", "Sync worker failed", e)
            Result.failure()
        }
    }
    
    companion object {
        private const val SYNC_WORK_NAME = "amx_background_sync"
        
        fun schedulePeriodicSync(context: Context) {
            val constraints = Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .setRequiresBatteryNotLow(true)
                .build()
            
            val syncRequest = PeriodicWorkRequestBuilder<SyncWorker>(
                repeatInterval = 15,
                repeatIntervalTimeUnit = TimeUnit.MINUTES
            )
                .setConstraints(constraints)
                .setBackoffCriteria(
                    BackoffPolicy.EXPONENTIAL,
                    PeriodicWorkRequest.MIN_BACKOFF_MILLIS,
                    TimeUnit.MILLISECONDS
                )
                .build()
            
            WorkManager.getInstance(context)
                .enqueueUniquePeriodicWork(
                    SYNC_WORK_NAME,
                    ExistingPeriodicWorkPolicy.KEEP,
                    syncRequest
                )
        }
    }
}
```

## Biometric Authentication & Security

### Multi-Platform Biometric Implementation
```kotlin
// Shared biometric authentication interface
expect class BiometricAuthenticator {
    suspend fun authenticate(reason: String): AuthResult
    suspend fun isAvailable(): Boolean
    suspend fun getSupportedMethods(): List<BiometricMethod>
}

sealed class AuthResult {
    object Success : AuthResult()
    object NotAvailable : AuthResult()
    object UserCancel : AuthResult()
    data class Failed(val error: String?) : AuthResult()
}

enum class BiometricMethod {
    FINGERPRINT,
    FACE,
    VOICE,
    IRIS,
    DEVICE_CREDENTIAL
}

// Biometric authentication flow
class BiometricAuthViewModel(
    private val biometricAuth: BiometricAuthenticator,
    private val userSession: UserSession
) : ViewModel() {
    
    private val _authState = MutableStateFlow(AuthState.IDLE)
    val authState: StateFlow<AuthState> = _authState.asStateFlow()
    
    suspend fun authenticateUser(reason: String = "Authenticate to access AIMatrix") {
        _authState.value = AuthState.AUTHENTICATING
        
        try {
            if (!biometricAuth.isAvailable()) {
                _authState.value = AuthState.NOT_AVAILABLE
                return
            }
            
            val result = biometricAuth.authenticate(reason)
            
            when (result) {
                is AuthResult.Success -> {
                    userSession.markAuthenticated()
                    _authState.value = AuthState.AUTHENTICATED
                }
                
                is AuthResult.NotAvailable -> {
                    _authState.value = AuthState.NOT_AVAILABLE
                }
                
                is AuthResult.UserCancel -> {
                    _authState.value = AuthState.CANCELLED
                }
                
                is AuthResult.Failed -> {
                    _authState.value = AuthState.ERROR(result.error ?: "Authentication failed")
                }
            }
            
        } catch (e: Exception) {
            _authState.value = AuthState.ERROR(e.message ?: "Unknown error")
        }
    }
    
    fun resetAuthState() {
        _authState.value = AuthState.IDLE
    }
}

enum class AuthState {
    IDLE,
    AUTHENTICATING,
    AUTHENTICATED,
    NOT_AVAILABLE,
    CANCELLED,
    ERROR(val message: String)
}
```

### Secure Local Storage
```kotlin
// Encrypted local storage for sensitive data
class SecureDataStore(
    private val secureStorage: SecureStorage,
    private val encryptionManager: EncryptionManager
) {
    suspend fun storeSecurely(key: String, value: String): Boolean {
        return try {
            val encryptedValue = encryptionManager.encrypt(value)
            secureStorage.store(key, encryptedValue)
        } catch (e: Exception) {
            Log.e("SecureDataStore", "Failed to store securely", e)
            false
        }
    }
    
    suspend fun retrieveSecurely(key: String): String? {
        return try {
            val encryptedValue = secureStorage.retrieve(key) ?: return null
            encryptionManager.decrypt(encryptedValue)
        } catch (e: Exception) {
            Log.e("SecureDataStore", "Failed to retrieve securely", e)
            null
        }
    }
    
    suspend fun storeUserCredentials(credentials: UserCredentials) {
        storeSecurely("access_token", credentials.accessToken)
        storeSecurely("refresh_token", credentials.refreshToken)
        storeSecurely("user_id", credentials.userId)
    }
    
    suspend fun getUserCredentials(): UserCredentials? {
        val accessToken = retrieveSecurely("access_token") ?: return null
        val refreshToken = retrieveSecurely("refresh_token") ?: return null
        val userId = retrieveSecurely("user_id") ?: return null
        
        return UserCredentials(
            accessToken = accessToken,
            refreshToken = refreshToken,
            userId = userId
        )
    }
    
    suspend fun clearUserCredentials() {
        secureStorage.delete("access_token")
        secureStorage.delete("refresh_token")
        secureStorage.delete("user_id")
    }
}

// Certificate pinning for network security
class NetworkSecurityManager {
    private val certificatePinner = CertificatePinner.Builder()
        .add("*.supabase.co", "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=")
        .add("api.aimatrix.com", "sha256/BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=")
        .build()
    
    fun createSecureHttpClient(): OkHttpClient {
        return OkHttpClient.Builder()
            .certificatePinner(certificatePinner)
            .connectionSpecs(listOf(ConnectionSpec.MODERN_TLS))
            .addNetworkInterceptor(HttpLoggingInterceptor().apply {
                level = if (BuildConfig.DEBUG) {
                    HttpLoggingInterceptor.Level.BODY
                } else {
                    HttpLoggingInterceptor.Level.NONE
                }
            })
            .addInterceptor { chain ->
                val originalRequest = chain.request()
                val authenticatedRequest = originalRequest.newBuilder()
                    .addHeader("Authorization", "Bearer ${getAccessToken()}")
                    .addHeader("User-Agent", "AIMatrix-Mobile/${BuildConfig.VERSION_NAME}")
                    .build()
                
                chain.proceed(authenticatedRequest)
            }
            .build()
    }
}
```

## Real-Time Features & WebSocket Integration

### Supabase Realtime Client
```kotlin
// Realtime subscription management
class RealtimeManager(
    private val supabaseClient: SupabaseClient
) {
    private val subscriptions = mutableMapOf<String, RealtimeChannel>()
    private val _connectionState = MutableStateFlow(ConnectionState.DISCONNECTED)
    val connectionState: StateFlow<ConnectionState> = _connectionState.asStateFlow()
    
    suspend fun subscribeToAgentUpdates(
        userId: String,
        onUpdate: (AgentUpdate) -> Unit
    ): String {
        val subscriptionId = "agent_updates_$userId"
        
        val channel = supabaseClient.realtime.createChannel("agent_updates") {
            // Subscribe to agent table changes for user
            onPostgresChanges(
                event = "UPDATE",
                schema = "public",
                table = "agents",
                filter = "user_id=eq.$userId"
            ) { payload ->
                try {
                    val update = AgentUpdate.fromJson(payload.new)
                    onUpdate(update)
                } catch (e: Exception) {
                    Log.e("RealtimeManager", "Error parsing agent update", e)
                }
            }
            
            // Subscribe to workflow completions
            onPostgresChanges(
                event = "INSERT",
                schema = "public",
                table = "workflow_executions",
                filter = "user_id=eq.$userId"
            ) { payload ->
                try {
                    val execution = WorkflowExecution.fromJson(payload.new)
                    onUpdate(AgentUpdate.WorkflowCompleted(execution))
                } catch (e: Exception) {
                    Log.e("RealtimeManager", "Error parsing workflow completion", e)
                }
            }
        }
        
        // Track connection state
        channel.onJoin { _connectionState.value = ConnectionState.CONNECTED }
        channel.onLeave { _connectionState.value = ConnectionState.DISCONNECTED }
        channel.onError { error ->
            Log.e("RealtimeManager", "Realtime error: $error")
            _connectionState.value = ConnectionState.ERROR
        }
        
        // Subscribe and store reference
        channel.subscribe()
        subscriptions[subscriptionId] = channel
        
        return subscriptionId
    }
    
    suspend fun subscribeToPresence(
        channelName: String,
        userInfo: Map<String, Any>,
        onPresenceUpdate: (List<PresenceState>) -> Unit
    ): String {
        val subscriptionId = "presence_$channelName"
        
        val channel = supabaseClient.realtime.createChannel(channelName) {
            onPresenceSync {
                onPresenceUpdate(it.values.toList())
            }
            
            onPresenceJoin { key, currentPresence, newPresence ->
                Log.d("RealtimeManager", "User $key joined")
                onPresenceUpdate(currentPresence.values.toList())
            }
            
            onPresenceLeave { key, currentPresence, leftPresence ->
                Log.d("RealtimeManager", "User $key left")
                onPresenceUpdate(currentPresence.values.toList())
            }
        }
        
        channel.subscribe()
        
        // Track user presence
        channel.track(userInfo)
        
        subscriptions[subscriptionId] = channel
        return subscriptionId
    }
    
    fun unsubscribe(subscriptionId: String) {
        subscriptions[subscriptionId]?.let { channel ->
            channel.unsubscribe()
            subscriptions.remove(subscriptionId)
        }
    }
    
    fun unsubscribeAll() {
        subscriptions.values.forEach { channel ->
            channel.unsubscribe()
        }
        subscriptions.clear()
    }
}

enum class ConnectionState {
    CONNECTED,
    DISCONNECTED,
    ERROR,
    RECONNECTING
}
```

### Real-Time UI Updates
```kotlin
// Compose UI with real-time updates
@Composable
fun AgentDashboardScreen(
    viewModel: AgentDashboardViewModel = koinViewModel()
) {
    val agents by viewModel.agents.collectAsState()
    val connectionState by viewModel.connectionState.collectAsState()
    
    LaunchedEffect(Unit) {
        viewModel.startRealtimeUpdates()
    }
    
    DisposableEffect(Unit) {
        onDispose {
            viewModel.stopRealtimeUpdates()
        }
    }
    
    Column {
        // Connection status indicator
        ConnectionStatusBar(
            state = connectionState,
            onRetry = { viewModel.reconnect() }
        )
        
        // Agent grid with real-time updates
        LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            contentPadding = PaddingValues(16.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(
                items = agents,
                key = { it.id }
            ) { agent ->
                AgentCard(
                    agent = agent,
                    modifier = Modifier.animateItemPlacement()
                ) {
                    viewModel.navigateToAgent(agent.id)
                }
            }
        }
    }
}

@Composable
fun ConnectionStatusBar(
    state: ConnectionState,
    onRetry: () -> Unit
) {
    AnimatedVisibility(
        visible = state != ConnectionState.CONNECTED,
        enter = slideInVertically(),
        exit = slideOutVertically()
    ) {
        Surface(
            color = when (state) {
                ConnectionState.DISCONNECTED -> MaterialTheme.colorScheme.error
                ConnectionState.ERROR -> MaterialTheme.colorScheme.error
                ConnectionState.RECONNECTING -> MaterialTheme.colorScheme.primary
                else -> Color.Transparent
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Row(
                modifier = Modifier
                    .padding(horizontal = 16.dp, vertical = 8.dp)
                    .fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    when (state) {
                        ConnectionState.RECONNECTING -> {
                            CircularProgressIndicator(
                                modifier = Modifier.size(16.dp),
                                strokeWidth = 2.dp,
                                color = MaterialTheme.colorScheme.onPrimary
                            )
                        }
                        else -> {
                            Icon(
                                imageVector = Icons.Default.WifiOff,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp),
                                tint = MaterialTheme.colorScheme.onError
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.width(8.dp))
                    
                    Text(
                        text = when (state) {
                            ConnectionState.DISCONNECTED -> "Offline"
                            ConnectionState.ERROR -> "Connection Error"
                            ConnectionState.RECONNECTING -> "Reconnecting..."
                            else -> ""
                        },
                        style = MaterialTheme.typography.bodySmall,
                        color = when (state) {
                            ConnectionState.RECONNECTING -> MaterialTheme.colorScheme.onPrimary
                            else -> MaterialTheme.colorScheme.onError
                        }
                    )
                }
                
                if (state == ConnectionState.ERROR || state == ConnectionState.DISCONNECTED) {
                    TextButton(
                        onClick = onRetry
                    ) {
                        Text(
                            "Retry",
                            color = MaterialTheme.colorScheme.onError
                        )
                    }
                }
            }
        }
    }
}
```

## Performance Optimization

### Memory Management & Caching
```kotlin
// Intelligent memory management
class MemoryManager {
    private val memoryCache = LruCache<String, Any>(calculateCacheSize())
    private val diskCache = DiskLruCache.create(getCacheDir(), 1, 1, DISK_CACHE_SIZE)
    
    private fun calculateCacheSize(): Int {
        val runtime = Runtime.getRuntime()
        val maxMemory = runtime.maxMemory()
        
        // Use 1/8th of available memory for cache
        return (maxMemory / 8).toInt()
    }
    
    suspend fun getCached(key: String): Any? {
        // Try memory cache first
        memoryCache.get(key)?.let { return it }
        
        // Then try disk cache
        return withContext(Dispatchers.IO) {
            try {
                diskCache.get(key)?.let { snapshot ->
                    val data = snapshot.getInputStream(0).use { input ->
                        ObjectInputStream(input).readObject()
                    }
                    
                    // Put back in memory cache
                    memoryCache.put(key, data)
                    data
                }
            } catch (e: Exception) {
                Log.e("MemoryManager", "Error reading from disk cache", e)
                null
            }
        }
    }
    
    suspend fun putCached(key: String, value: Any) {
        // Store in memory cache
        memoryCache.put(key, value)
        
        // Store in disk cache
        withContext(Dispatchers.IO) {
            try {
                diskCache.edit(key)?.let { editor ->
                    editor.newOutputStream(0).use { output ->
                        ObjectOutputStream(output).writeObject(value)
                    }
                    editor.commit()
                }
            } catch (e: Exception) {
                Log.e("MemoryManager", "Error writing to disk cache", e)
            }
        }
    }
    
    fun clearMemoryCache() {
        memoryCache.evictAll()
    }
    
    suspend fun clearDiskCache() {
        withContext(Dispatchers.IO) {
            try {
                diskCache.delete()
            } catch (e: Exception) {
                Log.e("MemoryManager", "Error clearing disk cache", e)
            }
        }
    }
    
    companion object {
        private const val DISK_CACHE_SIZE = 50 * 1024 * 1024L // 50MB
    }
}
```

### Image Loading & Processing
```kotlin
// Optimized image loading with Coil
@Composable
fun AgentAvatar(
    agent: AIAgent,
    size: Dp = 40.dp,
    modifier: Modifier = Modifier
) {
    AsyncImage(
        model = ImageRequest.Builder(LocalContext.current)
            .data(agent.avatarUrl)
            .placeholder(R.drawable.placeholder_avatar)
            .error(R.drawable.default_avatar)
            .memoryCachePolicy(CachePolicy.ENABLED)
            .diskCachePolicy(CachePolicy.ENABLED)
            .transformations(
                CircleCropTransformation(),
                RoundedCornersTransformation(8.dp.toPx())
            )
            .build(),
        contentDescription = "${agent.name} avatar",
        modifier = modifier.size(size),
        contentScale = ContentScale.Crop
    )
}

// Custom image transformations for performance
class CircleCropTransformation : Transformation {
    override val cacheKey: String = "circle_crop"
    
    override suspend fun transform(input: Bitmap, size: Size): Bitmap {
        return withContext(Dispatchers.Default) {
            val minSize = minOf(input.width, input.height)
            val radius = minSize / 2f
            val centerX = input.width / 2f
            val centerY = input.height / 2f
            
            val output = Bitmap.createBitmap(minSize, minSize, Bitmap.Config.ARGB_8888)
            val canvas = Canvas(output)
            val paint = Paint().apply {
                isAntiAlias = true
                shader = BitmapShader(input, Shader.TileMode.CLAMP, Shader.TileMode.CLAMP)
            }
            
            canvas.drawCircle(radius, radius, radius, paint)
            output
        }
    }
}
```

## Testing Strategy

### Unit Testing
```kotlin
// Unit tests for business logic
@RunWith(MockitoJUnitRunner::class)
class AgentRepositoryTest {
    
    @Mock
    private lateinit var localDataSource: AgentLocalDataSource
    
    @Mock  
    private lateinit var remoteDataSource: AgentRemoteDataSource
    
    @Mock
    private lateinit var syncManager: SyncManager
    
    private lateinit var repository: AgentRepository
    
    @Before
    fun setup() {
        repository = AgentRepository(localDataSource, remoteDataSource, syncManager)
    }
    
    @Test
    fun `getAgents returns local data when offline`() = runTest {
        // Given
        val localAgents = listOf(
            createTestAgent(id = "1", name = "Agent 1"),
            createTestAgent(id = "2", name = "Agent 2")
        )
        
        `when`(localDataSource.getAgentsFlow()).thenReturn(flowOf(localAgents))
        `when`(remoteDataSource.getAgents()).thenThrow(NetworkException("No internet"))
        
        // When
        val result = repository.getAgents().first()
        
        // Then
        assertEquals(2, result.size)
        assertEquals("Agent 1", result[0].name)
        assertEquals("Agent 2", result[1].name)
    }
    
    @Test
    fun `createAgent stores locally and queues for sync`() = runTest {
        // Given
        val newAgent = createTestAgent(name = "New Agent")
        
        // When
        val result = repository.createAgent(newAgent)
        
        // Then
        assertTrue(result.isSuccess)
        verify(localDataSource).insertAgent(any())
        verify(syncManager).queueForSync(any(), eq(SyncOperation.Type.CREATE))
    }
    
    private fun createTestAgent(
        id: String = UUID.randomUUID().toString(),
        name: String = "Test Agent",
        status: AgentStatus = AgentStatus.ACTIVE
    ) = AIAgent(
        id = id,
        name = name,
        type = AgentType.ANALYTICS,
        status = status,
        capabilities = listOf("data_processing"),
        lastActivity = Clock.System.now(),
        metrics = AgentMetrics(
            cpuUsage = 25.0,
            memoryUsage = 512,
            responseTime = 150,
            successRate = 0.95,
            errorRate = 0.05
        ),
        configuration = emptyMap()
    )
}
```

### UI Testing with Compose
```kotlin
// Compose UI tests
@RunWith(AndroidJUnit4::class)
class AgentListScreenTest {
    
    @get:Rule
    val composeTestRule = createComposeRule()
    
    @Mock
    private lateinit var viewModel: AgentListViewModel
    
    @Before
    fun setup() {
        MockitoAnnotations.openMocks(this)
    }
    
    @Test
    fun agentListScreen_displaysAgents() {
        // Given
        val testAgents = listOf(
            createTestAgent(id = "1", name = "Data Processor"),
            createTestAgent(id = "2", name = "Report Generator")
        )
        
        `when`(viewModel.uiState).thenReturn(
            flowOf(AgentListUiState.Success(testAgents)).asLiveData().asFlow()
        )
        
        // When
        composeTestRule.setContent {
            AgentListScreen(viewModel = viewModel)
        }
        
        // Then
        composeTestRule.onNodeWithText("Data Processor").assertIsDisplayed()
        composeTestRule.onNodeWithText("Report Generator").assertIsDisplayed()
    }
    
    @Test
    fun agentListScreen_showsLoadingState() {
        // Given
        `when`(viewModel.uiState).thenReturn(
            flowOf(AgentListUiState.Loading).asLiveData().asFlow()
        )
        
        // When
        composeTestRule.setContent {
            AgentListScreen(viewModel = viewModel)
        }
        
        // Then
        composeTestRule.onNode(hasTestTag("progress_indicator")).assertIsDisplayed()
    }
    
    @Test
    fun agentCard_clickTriggersSelection() {
        // Given
        val testAgent = createTestAgent(id = "1", name = "Test Agent")
        
        // When
        composeTestRule.setContent {
            AgentCard(
                agent = testAgent,
                onClick = { viewModel.selectAgent(testAgent.id) },
                onStatusToggle = { }
            )
        }
        
        composeTestRule.onNodeWithText("Test Agent").performClick()
        
        // Then
        verify(viewModel).selectAgent("1")
    }
}
```

### Integration Testing
```kotlin
// Integration tests with real database
@RunWith(AndroidJUnit4::class)
class AgentDatabaseTest {
    
    private lateinit var database: AMXDatabase
    private lateinit var agentDao: AgentDao
    
    @Before
    fun createDb() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        database = Room.inMemoryDatabaseBuilder(context, AMXDatabase::class.java)
            .allowMainThreadQueries()
            .build()
        agentDao = database.agentDao()
    }
    
    @After
    fun closeDb() {
        database.close()
    }
    
    @Test
    fun insertAndRetrieveAgent() = runTest {
        // Given
        val agent = AgentEntity(
            id = "test-id",
            name = "Test Agent",
            type = "analytics",
            status = "active",
            capabilities = listOf("data_processing"),
            lastActivity = Clock.System.now(),
            createdAt = Clock.System.now(),
            updatedAt = Clock.System.now(),
            syncStatus = SyncStatus.SYNCED
        )
        
        // When
        agentDao.insertAgent(agent)
        val retrievedAgent = agentDao.getAgentById("test-id")
        
        // Then
        assertNotNull(retrievedAgent)
        assertEquals("Test Agent", retrievedAgent?.name)
        assertEquals("analytics", retrievedAgent?.type)
    }
    
    @Test
    fun agentFlowUpdatesWhenDataChanges() = runTest {
        // Given
        val initialAgent = createTestAgentEntity(id = "1", name = "Initial Name")
        agentDao.insertAgent(initialAgent)
        
        val agentsFlow = agentDao.getAllAgentsFlow()
        val testCollector = TestCollector(agentsFlow)
        
        // When - update agent
        val updatedAgent = initialAgent.copy(name = "Updated Name")
        agentDao.updateAgent(updatedAgent)
        
        // Then
        val emissions = testCollector.getEmissions()
        assertEquals(2, emissions.size)
        assertEquals("Initial Name", emissions[0][0].name)
        assertEquals("Updated Name", emissions[1][0].name)
    }
}
```

## App Store Deployment

### iOS App Store Configuration
```swift
// iOS-specific App Store configuration
// Info.plist configuration
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>AIMatrix</string>
    
    <key>CFBundleDisplayName</key>
    <string>AIMatrix</string>
    
    <key>CFBundleIdentifier</key>
    <string>com.aimatrix.mobile</string>
    
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    
    <key>LSRequiresIPhoneOS</key>
    <true/>
    
    <key>UIRequiredDeviceCapabilities</key>
    <array>
        <string>armv7</string>
    </array>
    
    <key>NSFaceIDUsageDescription</key>
    <string>Use Face ID to securely access your AI agents</string>
    
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>Location access enables context-aware AI agent recommendations</string>
    
    <key>NSCameraUsageDescription</key>
    <string>Camera access allows AI agents to process visual data</string>
    
    <key>NSMicrophoneUsageDescription</key>
    <string>Microphone access enables voice interaction with AI agents</string>
    
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <false/>
        <key>NSExceptionDomains</key>
        <dict>
            <key>supabase.co</key>
            <dict>
                <key>NSExceptionRequiresForwardSecrecy</key>
                <false/>
                <key>NSIncludesSubdomains</key>
                <true/>
            </dict>
        </dict>
    </dict>
</dict>
</plist>
```

### Android Play Store Configuration
```xml
<!-- Android manifest configuration -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.aimatrix.mobile">
    
    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.USE_FINGERPRINT" />
    <uses-permission android:name="android.permission.USE_BIOMETRIC" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.RECORD_AUDIO" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    
    <!-- Hardware features -->
    <uses-feature android:name="android.hardware.fingerprint" android:required="false" />
    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.location.gps" android:required="false" />
    
    <application
        android:name=".AMXApplication"
        android:allowBackup="false"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.AIMatrix">
        
        <!-- Main Activity -->
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.AIMatrix.NoActionBar">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
        <!-- Firebase Messaging Service -->
        <service
            android:name=".AMXFirebaseMessagingService"
            android:exported="false">
            <intent-filter>
                <action android:name="com.google.firebase.MESSAGING_EVENT" />
            </intent-filter>
        </service>
        
        <!-- Background Sync Service -->
        <service
            android:name=".SyncService"
            android:permission="android.permission.BIND_JOB_SERVICE"
            android:exported="false" />
        
        <!-- Boot Receiver -->
        <receiver
            android:name=".BootReceiver"
            android:enabled="true"
            android:exported="true">
            <intent-filter android:priority="1000">
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />
                <action android:name="android.intent.action.PACKAGE_REPLACED" />
                <data android:scheme="package" />
            </intent-filter>
        </receiver>
        
    </application>
    
</manifest>
```

### Build Configuration
```kotlin
// Build configuration for both platforms
// build.gradle.kts (Android)
android {
    compileSdk = 34
    
    defaultConfig {
        applicationId = "com.aimatrix.mobile"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
        
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }
    
    buildTypes {
        debug {
            isDebuggable = true
            applicationIdSuffix = ".debug"
            versionNameSuffix = "-debug"
            buildConfigField("String", "SUPABASE_URL", "\"https://dev-project.supabase.co\"")
            buildConfigField("String", "SUPABASE_ANON_KEY", "\"dev-anon-key\"")
        }
        
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
            buildConfigField("String", "SUPABASE_URL", "\"https://prod-project.supabase.co\"")
            buildConfigField("String", "SUPABASE_ANON_KEY", "\"prod-anon-key\"")
            
            signingConfig = signingConfigs.getByName("release")
        }
    }
    
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    
    buildFeatures {
        compose = true
        buildConfig = true
    }
    
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.4"
    }
    
    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }
}
```

## Best Practices & Guidelines

### Development Best Practices

1. **Architecture Patterns**
   - Use MVVM with Compose for UI layer
   - Implement Repository pattern for data access
   - Apply Dependency Injection with Koin
   - Follow Clean Architecture principles

2. **Performance Optimization**
   - Implement lazy loading for large lists
   - Use efficient image loading with Coil
   - Cache frequently accessed data locally
   - Minimize network requests with intelligent sync

3. **Security Guidelines**
   - Store sensitive data in secure storage only
   - Implement certificate pinning for network calls
   - Use biometric authentication where available
   - Encrypt all local databases

4. **Testing Strategy**
   - Unit test business logic thoroughly
   - Use Compose testing for UI validation
   - Implement integration tests for critical flows
   - Test offline scenarios extensively

### User Experience Guidelines

1. **Offline-First Design**
   - All core features work without internet
   - Clear indication of sync status
   - Intelligent conflict resolution
   - Queue actions for later sync

2. **Platform Consistency**
   - Follow Material Design on Android
   - Respect iOS Human Interface Guidelines
   - Use platform-appropriate navigation patterns
   - Implement native gestures and interactions

3. **Performance Standards**
   - App startup under 2 seconds
   - Smooth 60fps animations
   - Memory usage under 150MB baseline
   - Background battery usage under 2% per hour

---

> [!TIP]
> **Getting Started**: Download the AIMatrix mobile app from the [App Store](https://apps.apple.com/app/aimatrix) or [Google Play](https://play.google.com/store/apps/details?id=com.aimatrix.mobile) to experience AI agent management on mobile devices.

> [!NOTE]
> **Offline Capabilities**: The mobile app maintains full functionality without internet connectivity, automatically syncing when connection is restored. Perfect for field work and unstable network environments.

---

*AIMatrix Mobile Applications - AI agent management in your pocket*