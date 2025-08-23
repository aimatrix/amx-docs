---
title: "AMX Daemon"
description: "System-level background services for continuous AI agent operations, featuring auto-scaling, health monitoring, resource management, and automated recovery capabilities"
weight: 4
date: 2025-08-23
toc: true
tags: ["daemon", "background", "service", "system", "monitoring", "auto-scaling", "health-check"]
---

# AMX Daemon

## System-Level Intelligence for Continuous Operations

AMX Daemon is the backbone service that ensures continuous, reliable operation of AI agents and workflows across your infrastructure. Running as a system-level service, it provides intelligent resource management, automatic scaling, health monitoring, and recovery capabilities that keep your AI operations running smoothly 24/7.

## Core Architecture

```mermaid
graph TB
    subgraph "AMX Daemon Core"
        CONTROLLER[Daemon Controller]
        SCHEDULER[Task Scheduler]
        MONITOR[Health Monitor]
        SCALER[Auto Scaler]
    end
    
    subgraph "Service Management"
        AGENT_MGR[Agent Manager]
        WORKFLOW_MGR[Workflow Manager] 
        RESOURCE_MGR[Resource Manager]
        CONFIG_MGR[Config Manager]
    end
    
    subgraph "Monitoring & Analytics"
        METRICS[Metrics Collector]
        ALERTS[Alert Engine]
        LOGS[Log Aggregator]
        HEALTH[Health Checker]
    end
    
    subgraph "External Integrations"
        SUPABASE[Supabase Backend]
        MCP[MCP Servers]
        DOCKER[Container Runtime]
        K8S[Kubernetes API]
    end
    
    subgraph "System Services"
        CRON[Cron Jobs]
        SYSTEMD[SystemD]
        WINDOWS_SVC[Windows Service]
        LAUNCHD[macOS LaunchAgent]
    end
    
    CONTROLLER --> Service Management
    CONTROLLER --> Monitoring & Analytics
    
    Service Management --> External Integrations
    Monitoring & Analytics --> System Services
    
    External Integrations --> System Services
```

## System Daemon Architecture

### Cross-Platform Service Implementation

#### Linux SystemD Service
```ini
# /etc/systemd/system/amx-daemon.service
[Unit]
Description=AIMatrix Daemon - AI Agent Management Service
Documentation=https://docs.aimatrix.com/applications/amx-daemon/
After=network-online.target
Wants=network-online.target
Requires=postgresql.service
After=postgresql.service

[Service]
Type=notify
User=amx
Group=amx
Environment=NODE_ENV=production
Environment=AMX_CONFIG_PATH=/etc/amx/daemon.conf
Environment=AMX_LOG_PATH=/var/log/amx/daemon.log
Environment=AMX_DATA_PATH=/var/lib/amx

ExecStartPre=/usr/bin/amx-daemon --config-check
ExecStart=/usr/bin/amx-daemon --daemon --config /etc/amx/daemon.conf
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/bin/kill -TERM $MAINPID

# Restart configuration
Restart=always
RestartSec=10
TimeoutStartSec=60
TimeoutStopSec=30

# Security settings
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/amx /var/log/amx /tmp
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096
MemoryMax=4G
CPUQuota=200%

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=amx-daemon

[Install]
WantedBy=multi-user.target
```

#### Windows Service Implementation
```csharp
// Windows service implementation
using System.ServiceProcess;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace AMXDaemon.Windows
{
    public class AMXWindowsService : ServiceBase
    {
        private IHost? _host;
        private readonly ILogger<AMXWindowsService> _logger;
        
        public AMXWindowsService()
        {
            ServiceName = "AMXDaemon";
            CanStop = true;
            CanPauseAndContinue = true;
            AutoLog = true;
        }
        
        protected override void OnStart(string[] args)
        {
            try
            {
                _host = CreateHostBuilder(args).Build();
                _host.StartAsync();
                
                _logger?.LogInformation("AMX Daemon service started successfully");
            }
            catch (Exception ex)
            {
                _logger?.LogError(ex, "Failed to start AMX Daemon service");
                throw;
            }
        }
        
        protected override void OnStop()
        {
            try
            {
                _host?.StopAsync(TimeSpan.FromSeconds(30)).Wait();
                _host?.Dispose();
                
                _logger?.LogInformation("AMX Daemon service stopped");
            }
            catch (Exception ex)
            {
                _logger?.LogError(ex, "Error stopping AMX Daemon service");
            }
        }
        
        protected override void OnPause()
        {
            var daemonController = _host?.Services.GetService<IDaemonController>();
            daemonController?.Pause();
            
            _logger?.LogInformation("AMX Daemon service paused");
        }
        
        protected override void OnContinue()
        {
            var daemonController = _host?.Services.GetService<IDaemonController>();
            daemonController?.Resume();
            
            _logger?.LogInformation("AMX Daemon service resumed");
        }
        
        private static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
                .UseWindowsService(options =>
                {
                    options.ServiceName = "AMXDaemon";
                })
                .ConfigureServices((context, services) =>
                {
                    services.AddSingleton<IDaemonController, DaemonController>();
                    services.AddSingleton<IAgentManager, AgentManager>();
                    services.AddSingleton<IWorkflowManager, WorkflowManager>();
                    services.AddSingleton<IHealthMonitor, HealthMonitor>();
                    services.AddSingleton<IMetricsCollector, MetricsCollector>();
                    services.AddHostedService<AMXDaemonHostedService>();
                })
                .ConfigureLogging((context, logging) =>
                {
                    logging.AddEventLog(options =>
                    {
                        options.LogName = "AIMatrix";
                        options.SourceName = "AMXDaemon";
                    });
                });
        
        public static void Main(string[] args)
        {
            if (Environment.UserInteractive)
            {
                // Running as console application
                CreateHostBuilder(args).Build().Run();
            }
            else
            {
                // Running as Windows service
                ServiceBase.Run(new AMXWindowsService());
            }
        }
    }
    
    public class AMXDaemonHostedService : BackgroundService
    {
        private readonly IDaemonController _daemonController;
        private readonly ILogger<AMXDaemonHostedService> _logger;
        
        public AMXDaemonHostedService(
            IDaemonController daemonController,
            ILogger<AMXDaemonHostedService> logger)
        {
            _daemonController = daemonController;
            _logger = logger;
        }
        
        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            try
            {
                await _daemonController.StartAsync(stoppingToken);
                
                while (!stoppingToken.IsCancellationRequested)
                {
                    await _daemonController.ProcessTasksAsync(stoppingToken);
                    await Task.Delay(5000, stoppingToken); // 5-second intervals
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in daemon execution");
                throw;
            }
        }
        
        public override async Task StopAsync(CancellationToken cancellationToken)
        {
            _logger.LogInformation("Stopping AMX Daemon...");
            await _daemonController.StopAsync(cancellationToken);
            await base.StopAsync(cancellationToken);
        }
    }
}
```

#### macOS LaunchAgent Implementation
```xml
<!-- ~/Library/LaunchAgents/com.aimatrix.daemon.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.aimatrix.daemon</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/amx-daemon</string>
        <string>--daemon</string>
        <string>--config</string>
        <string>/usr/local/etc/amx/daemon.conf</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
        <key>Crashed</key>
        <true/>
    </dict>
    
    <key>ThrottleInterval</key>
    <integer>10</integer>
    
    <key>StandardOutPath</key>
    <string>/usr/local/var/log/amx/daemon.out.log</string>
    
    <key>StandardErrorPath</key>
    <string>/usr/local/var/log/amx/daemon.err.log</string>
    
    <key>WorkingDirectory</key>
    <string>/usr/local/var/lib/amx</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>NODE_ENV</key>
        <string>production</string>
        <key>AMX_CONFIG_PATH</key>
        <string>/usr/local/etc/amx/daemon.conf</string>
        <key>AMX_LOG_LEVEL</key>
        <string>info</string>
    </dict>
    
    <key>LimitLoadToSessionType</key>
    <string>Aqua</string>
    
    <key>ProcessType</key>
    <string>Background</string>
    
    <!-- Resource limits -->
    <key>SoftResourceLimits</key>
    <dict>
        <key>NumberOfFiles</key>
        <integer>4096</integer>
        <key>NumberOfProcesses</key>
        <integer>512</integer>
    </dict>
    
    <key>HardResourceLimits</key>
    <dict>
        <key>NumberOfFiles</key>
        <integer>8192</integer>
        <key>NumberOfProcesses</key>
        <integer>1024</integer>
    </dict>
</dict>
</plist>
```

## Background Updates & Monitoring

### Intelligent Task Scheduler
```go
// Go implementation for high-performance task scheduling
package scheduler

import (
    "context"
    "sync"
    "time"
    
    "github.com/robfig/cron/v3"
    "go.uber.org/zap"
)

type TaskScheduler struct {
    cron        *cron.Cron
    tasks       map[string]*ScheduledTask
    mu          sync.RWMutex
    logger      *zap.Logger
    ctx         context.Context
    cancel      context.CancelFunc
    metrics     *SchedulerMetrics
}

type ScheduledTask struct {
    ID          string
    Name        string
    Schedule    string
    Handler     TaskHandler
    Enabled     bool
    LastRun     time.Time
    NextRun     time.Time
    RunCount    int64
    ErrorCount  int64
    AvgDuration time.Duration
}

type TaskHandler func(ctx context.Context) error

type SchedulerMetrics struct {
    TasksScheduled  int64
    TasksExecuted   int64
    TasksSucceeded  int64
    TasksFailed     int64
    AvgExecTime     time.Duration
    QueueDepth      int
}

func NewTaskScheduler(logger *zap.Logger) *TaskScheduler {
    ctx, cancel := context.WithCancel(context.Background())
    
    return &TaskScheduler{
        cron:    cron.New(cron.WithSeconds()),
        tasks:   make(map[string]*ScheduledTask),
        logger:  logger,
        ctx:     ctx,
        cancel:  cancel,
        metrics: &SchedulerMetrics{},
    }
}

func (ts *TaskScheduler) Start() error {
    ts.logger.Info("Starting task scheduler")
    
    // Add default system tasks
    ts.scheduleSystemTasks()
    
    ts.cron.Start()
    
    // Start metrics collection
    go ts.collectMetrics()
    
    return nil
}

func (ts *TaskScheduler) Stop() error {
    ts.logger.Info("Stopping task scheduler")
    
    ts.cancel()
    ts.cron.Stop()
    
    return nil
}

func (ts *TaskScheduler) AddTask(task *ScheduledTask) error {
    ts.mu.Lock()
    defer ts.mu.Unlock()
    
    // Remove existing task if it exists
    if existingTask, exists := ts.tasks[task.ID]; exists {
        ts.cron.Remove(cron.EntryID(existingTask.RunCount))
    }
    
    // Wrap handler with metrics and error handling
    wrappedHandler := ts.wrapTaskHandler(task)
    
    // Schedule the task
    entryID, err := ts.cron.AddFunc(task.Schedule, func() {
        if task.Enabled {
            wrappedHandler(ts.ctx)
        }
    })
    
    if err != nil {
        return err
    }
    
    task.RunCount = int64(entryID)
    ts.tasks[task.ID] = task
    ts.metrics.TasksScheduled++
    
    ts.logger.Info("Task scheduled",
        zap.String("id", task.ID),
        zap.String("name", task.Name),
        zap.String("schedule", task.Schedule))
    
    return nil
}

func (ts *TaskScheduler) wrapTaskHandler(task *ScheduledTask) func(context.Context) {
    return func(ctx context.Context) {
        start := time.Now()
        
        ts.logger.Debug("Executing task",
            zap.String("id", task.ID),
            zap.String("name", task.Name))
        
        ts.metrics.TasksExecuted++
        
        err := task.Handler(ctx)
        duration := time.Since(start)
        
        ts.mu.Lock()
        task.LastRun = start
        task.RunCount++
        
        if err != nil {
            task.ErrorCount++
            ts.metrics.TasksFailed++
            
            ts.logger.Error("Task execution failed",
                zap.String("id", task.ID),
                zap.String("name", task.Name),
                zap.Error(err),
                zap.Duration("duration", duration))
        } else {
            ts.metrics.TasksSucceeded++
            
            ts.logger.Debug("Task executed successfully",
                zap.String("id", task.ID),
                zap.String("name", task.Name),
                zap.Duration("duration", duration))
        }
        
        // Update average duration
        if task.RunCount > 0 {
            task.AvgDuration = time.Duration(
                (int64(task.AvgDuration) * (task.RunCount - 1) + int64(duration)) / task.RunCount,
            )
        }
        
        ts.mu.Unlock()
    }
}

func (ts *TaskScheduler) scheduleSystemTasks() {
    // Health check task
    ts.AddTask(&ScheduledTask{
        ID:       "system-health-check",
        Name:     "System Health Check",
        Schedule: "0 */5 * * * *", // Every 5 minutes
        Enabled:  true,
        Handler:  ts.systemHealthCheck,
    })
    
    // Agent status sync
    ts.AddTask(&ScheduledTask{
        ID:       "agent-status-sync",
        Name:     "Agent Status Synchronization",
        Schedule: "0 */1 * * * *", // Every minute
        Enabled:  true,
        Handler:  ts.agentStatusSync,
    })
    
    // Metrics cleanup
    ts.AddTask(&ScheduledTask{
        ID:       "metrics-cleanup",
        Name:     "Metrics Cleanup",
        Schedule: "0 0 2 * * *", // Daily at 2 AM
        Enabled:  true,
        Handler:  ts.metricsCleanup,
    })
    
    // Auto-scaling evaluation
    ts.AddTask(&ScheduledTask{
        ID:       "auto-scaling",
        Name:     "Auto-scaling Evaluation",
        Schedule: "0 */2 * * * *", // Every 2 minutes
        Enabled:  true,
        Handler:  ts.autoScalingEvaluation,
    })
}

func (ts *TaskScheduler) systemHealthCheck(ctx context.Context) error {
    // Check system resources
    cpuUsage, err := getCPUUsage()
    if err != nil {
        return err
    }
    
    memoryUsage, err := getMemoryUsage()
    if err != nil {
        return err
    }
    
    diskUsage, err := getDiskUsage()
    if err != nil {
        return err
    }
    
    // Check service health
    agentHealth := ts.checkAgentHealth()
    workflowHealth := ts.checkWorkflowHealth()
    
    // Report metrics
    ts.reportHealthMetrics(HealthMetrics{
        CPU:       cpuUsage,
        Memory:    memoryUsage,
        Disk:      diskUsage,
        Agents:    agentHealth,
        Workflows: workflowHealth,
    })
    
    return nil
}

func (ts *TaskScheduler) collectMetrics() {
    ticker := time.NewTicker(30 * time.Second)
    defer ticker.Stop()
    
    for {
        select {
        case <-ticker.C:
            ts.updateMetrics()
        case <-ts.ctx.Done():
            return
        }
    }
}

func (ts *TaskScheduler) updateMetrics() {
    ts.mu.RLock()
    defer ts.mu.RUnlock()
    
    totalDuration := time.Duration(0)
    activeTasks := 0
    
    for _, task := range ts.tasks {
        if task.Enabled {
            activeTasks++
            totalDuration += task.AvgDuration
        }
    }
    
    if activeTasks > 0 {
        ts.metrics.AvgExecTime = totalDuration / time.Duration(activeTasks)
    }
    
    ts.metrics.QueueDepth = len(ts.tasks)
}
```

### Resource Management System
```rust
// Rust implementation for efficient resource management
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};
use tokio::time::interval;

#[derive(Debug, Clone)]
pub struct ResourceMetrics {
    pub cpu_usage: f64,
    pub memory_usage: f64,
    pub disk_usage: f64,
    pub network_io: NetworkIO,
    pub process_count: u32,
    pub thread_count: u32,
    pub open_files: u32,
}

#[derive(Debug, Clone)]
pub struct NetworkIO {
    pub bytes_sent: u64,
    pub bytes_received: u64,
    pub packets_sent: u64,
    pub packets_received: u64,
}

#[derive(Debug, Clone)]
pub struct ResourceLimits {
    pub max_cpu_percent: f64,
    pub max_memory_mb: u64,
    pub max_disk_percent: f64,
    pub max_processes: u32,
    pub max_threads: u32,
    pub max_open_files: u32,
}

pub struct ResourceManager {
    limits: ResourceLimits,
    metrics_history: Arc<Mutex<Vec<(Instant, ResourceMetrics)>>>,
    alerts: Arc<Mutex<Vec<ResourceAlert>>>,
    processes: Arc<Mutex<HashMap<String, ProcessInfo>>>,
}

#[derive(Debug, Clone)]
pub struct ResourceAlert {
    pub level: AlertLevel,
    pub message: String,
    pub timestamp: Instant,
    pub resolved: bool,
}

#[derive(Debug, Clone, PartialEq)]
pub enum AlertLevel {
    Info,
    Warning,
    Critical,
}

#[derive(Debug, Clone)]
pub struct ProcessInfo {
    pub pid: u32,
    pub name: String,
    pub cpu_usage: f64,
    pub memory_usage: u64,
    pub start_time: Instant,
    pub command: String,
}

impl ResourceManager {
    pub fn new(limits: ResourceLimits) -> Self {
        Self {
            limits,
            metrics_history: Arc::new(Mutex::new(Vec::new())),
            alerts: Arc::new(Mutex::new(Vec::new())),
            processes: Arc::new(Mutex::new(HashMap::new())),
        }
    }
    
    pub async fn start_monitoring(&self) {
        let mut interval = interval(Duration::from_secs(30));
        
        loop {
            interval.tick().await;
            
            if let Ok(metrics) = self.collect_metrics().await {
                self.analyze_metrics(&metrics).await;
                self.store_metrics(metrics).await;
                self.cleanup_old_metrics().await;
            }
        }
    }
    
    async fn collect_metrics(&self) -> Result<ResourceMetrics, Box<dyn std::error::Error>> {
        let cpu_usage = self.get_cpu_usage().await?;
        let memory_usage = self.get_memory_usage().await?;
        let disk_usage = self.get_disk_usage().await?;
        let network_io = self.get_network_io().await?;
        let (process_count, thread_count) = self.get_process_stats().await?;
        let open_files = self.get_open_files_count().await?;
        
        Ok(ResourceMetrics {
            cpu_usage,
            memory_usage,
            disk_usage,
            network_io,
            process_count,
            thread_count,
            open_files,
        })
    }
    
    async fn analyze_metrics(&self, metrics: &ResourceMetrics) {
        let mut alerts = self.alerts.lock().unwrap();
        
        // CPU usage check
        if metrics.cpu_usage > self.limits.max_cpu_percent {
            let alert = ResourceAlert {
                level: if metrics.cpu_usage > 90.0 {
                    AlertLevel::Critical
                } else {
                    AlertLevel::Warning
                },
                message: format!("High CPU usage: {:.1}%", metrics.cpu_usage),
                timestamp: Instant::now(),
                resolved: false,
            };
            alerts.push(alert);
        }
        
        // Memory usage check
        let memory_usage_mb = metrics.memory_usage * 1024.0; // Convert GB to MB
        if memory_usage_mb > self.limits.max_memory_mb as f64 {
            let alert = ResourceAlert {
                level: if memory_usage_mb > (self.limits.max_memory_mb as f64 * 0.95) {
                    AlertLevel::Critical
                } else {
                    AlertLevel::Warning
                },
                message: format!("High memory usage: {:.0} MB", memory_usage_mb),
                timestamp: Instant::now(),
                resolved: false,
            };
            alerts.push(alert);
        }
        
        // Disk usage check
        if metrics.disk_usage > self.limits.max_disk_percent {
            let alert = ResourceAlert {
                level: if metrics.disk_usage > 95.0 {
                    AlertLevel::Critical
                } else {
                    AlertLevel::Warning
                },
                message: format!("High disk usage: {:.1}%", metrics.disk_usage),
                timestamp: Instant::now(),
                resolved: false,
            };
            alerts.push(alert);
        }
        
        // Process count check
        if metrics.process_count > self.limits.max_processes {
            let alert = ResourceAlert {
                level: AlertLevel::Warning,
                message: format!("High process count: {}", metrics.process_count),
                timestamp: Instant::now(),
                resolved: false,
            };
            alerts.push(alert);
        }
        
        // Clean up old alerts
        alerts.retain(|alert| {
            alert.timestamp.elapsed() < Duration::from_hours(24)
        });
    }
    
    async fn store_metrics(&self, metrics: ResourceMetrics) {
        let mut history = self.metrics_history.lock().unwrap();
        history.push((Instant::now(), metrics));
    }
    
    async fn cleanup_old_metrics(&self) {
        let mut history = self.metrics_history.lock().unwrap();
        let cutoff = Instant::now() - Duration::from_secs(3600 * 24); // 24 hours
        
        history.retain(|(timestamp, _)| *timestamp > cutoff);
    }
    
    async fn get_cpu_usage(&self) -> Result<f64, Box<dyn std::error::Error>> {
        // Platform-specific CPU usage implementation
        #[cfg(target_os = "linux")]
        {
            use std::fs;
            let stat = fs::read_to_string("/proc/stat")?;
            // Parse /proc/stat and calculate CPU usage
            Ok(self.parse_linux_cpu_usage(&stat))
        }
        
        #[cfg(target_os = "windows")]
        {
            // Windows performance counter implementation
            Ok(self.get_windows_cpu_usage().await?)
        }
        
        #[cfg(target_os = "macos")]
        {
            // macOS system call implementation
            Ok(self.get_macos_cpu_usage().await?)
        }
    }
    
    async fn get_memory_usage(&self) -> Result<f64, Box<dyn std::error::Error>> {
        #[cfg(target_os = "linux")]
        {
            use std::fs;
            let meminfo = fs::read_to_string("/proc/meminfo")?;
            Ok(self.parse_linux_memory_usage(&meminfo))
        }
        
        #[cfg(not(target_os = "linux"))]
        {
            // Cross-platform fallback using sysinfo
            use sysinfo::{System, SystemExt};
            let mut system = System::new_all();
            system.refresh_memory();
            
            let used = system.used_memory() as f64;
            let total = system.total_memory() as f64;
            
            Ok((used / total) * 100.0)
        }
    }
    
    pub async fn enforce_limits(&self) -> Result<(), Box<dyn std::error::Error>> {
        let metrics = self.collect_metrics().await?;
        
        // CPU throttling
        if metrics.cpu_usage > self.limits.max_cpu_percent {
            self.throttle_cpu_intensive_processes().await?;
        }
        
        // Memory cleanup
        if metrics.memory_usage > (self.limits.max_memory_mb as f64 / 1024.0) {
            self.cleanup_memory().await?;
        }
        
        // Process limit enforcement
        if metrics.process_count > self.limits.max_processes {
            self.terminate_excess_processes().await?;
        }
        
        Ok(())
    }
    
    async fn throttle_cpu_intensive_processes(&self) -> Result<(), Box<dyn std::error::Error>> {
        let processes = self.processes.lock().unwrap();
        
        for (_, process) in processes.iter() {
            if process.cpu_usage > 50.0 {
                // Lower process priority
                self.set_process_priority(process.pid, -5).await?;
            }
        }
        
        Ok(())
    }
    
    async fn cleanup_memory(&self) -> Result<(), Box<dyn std::error::Error>> {
        // Force garbage collection in managed processes
        self.trigger_garbage_collection().await?;
        
        // Clear system caches
        self.clear_system_caches().await?;
        
        Ok(())
    }
    
    pub fn get_resource_recommendations(&self) -> Vec<String> {
        let mut recommendations = Vec::new();
        
        if let Ok(metrics) = tokio::runtime::Runtime::new()
            .unwrap()
            .block_on(self.collect_metrics()) 
        {
            if metrics.cpu_usage > 80.0 {
                recommendations.push(
                    "Consider adding more CPU cores or reducing agent workload".to_string()
                );
            }
            
            if metrics.memory_usage > 80.0 {
                recommendations.push(
                    "Consider adding more RAM or optimizing memory usage".to_string()
                );
            }
            
            if metrics.disk_usage > 85.0 {
                recommendations.push(
                    "Consider adding more storage or cleaning up old data".to_string()
                );
            }
            
            if metrics.process_count > (self.limits.max_processes as f64 * 0.8) as u32 {
                recommendations.push(
                    "Consider consolidating processes or increasing process limits".to_string()
                );
            }
        }
        
        recommendations
    }
}
```

## Auto-Scaling Capabilities

### Horizontal Pod Autoscaling (Kubernetes)
```yaml
# Kubernetes HPA configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: amx-daemon-hpa
  namespace: aimatrix
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: amx-daemon
  
  minReplicas: 2
  maxReplicas: 10
  
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  
  - type: Pods
    pods:
      metric:
        name: agent_queue_depth
      target:
        type: AverageValue
        averageValue: "10"
  
  - type: External
    external:
      metric:
        name: supabase_connection_count
      target:
        type: Value
        value: "100"

  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
      - type: Pods
        value: 2
        periodSeconds: 60
      selectPolicy: Min
    
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
      - type: Pods
        value: 4
        periodSeconds: 60
      selectPolicy: Max

---
# Vertical Pod Autoscaler
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: amx-daemon-vpa
  namespace: aimatrix
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: amx-daemon
  
  updatePolicy:
    updateMode: "Auto"
  
  resourcePolicy:
    containerPolicies:
    - containerName: amx-daemon
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2
        memory: 4Gi
      controlledResources: ["cpu", "memory"]
```

### Custom Auto-Scaling Logic
```typescript
// Custom auto-scaling implementation
interface ScalingMetrics {
  cpuUtilization: number
  memoryUtilization: number
  queueDepth: number
  responseTime: number
  errorRate: number
  concurrentAgents: number
}

interface ScalingPolicy {
  name: string
  triggers: ScalingTrigger[]
  actions: ScalingAction[]
  cooldownPeriod: number
  enabled: boolean
}

interface ScalingTrigger {
  metric: keyof ScalingMetrics
  operator: 'gt' | 'lt' | 'gte' | 'lte'
  threshold: number
  duration: number
}

interface ScalingAction {
  type: 'scale_up' | 'scale_down' | 'throttle' | 'notify'
  parameters: Record<string, any>
}

class AutoScaler {
  private policies: ScalingPolicy[] = []
  private metrics: ScalingMetrics[] = []
  private lastScalingAction: number = 0
  
  constructor(
    private metricsCollector: MetricsCollector,
    private resourceManager: ResourceManager,
    private notificationService: NotificationService
  ) {
    this.setupDefaultPolicies()
  }
  
  private setupDefaultPolicies() {
    // High CPU utilization policy
    this.policies.push({
      name: 'high_cpu_scale_up',
      triggers: [
        {
          metric: 'cpuUtilization',
          operator: 'gt',
          threshold: 80,
          duration: 300000 // 5 minutes
        }
      ],
      actions: [
        {
          type: 'scale_up',
          parameters: {
            increment: 2,
            maxInstances: 10
          }
        }
      ],
      cooldownPeriod: 600000, // 10 minutes
      enabled: true
    })
    
    // High queue depth policy
    this.policies.push({
      name: 'high_queue_scale_up',
      triggers: [
        {
          metric: 'queueDepth',
          operator: 'gt',
          threshold: 50,
          duration: 120000 // 2 minutes
        }
      ],
      actions: [
        {
          type: 'scale_up',
          parameters: {
            increment: 3,
            maxInstances: 15
          }
        }
      ],
      cooldownPeriod: 300000, // 5 minutes
      enabled: true
    })
    
    // Low utilization scale down
    this.policies.push({
      name: 'low_utilization_scale_down',
      triggers: [
        {
          metric: 'cpuUtilization',
          operator: 'lt',
          threshold: 30,
          duration: 900000 // 15 minutes
        },
        {
          metric: 'queueDepth',
          operator: 'lt',
          threshold: 5,
          duration: 900000 // 15 minutes
        }
      ],
      actions: [
        {
          type: 'scale_down',
          parameters: {
            decrement: 1,
            minInstances: 2
          }
        }
      ],
      cooldownPeriod: 1800000, // 30 minutes
      enabled: true
    })
    
    // High error rate throttling
    this.policies.push({
      name: 'high_error_rate_throttle',
      triggers: [
        {
          metric: 'errorRate',
          operator: 'gt',
          threshold: 10,
          duration: 180000 // 3 minutes
        }
      ],
      actions: [
        {
          type: 'throttle',
          parameters: {
            throttlePercentage: 50
          }
        },
        {
          type: 'notify',
          parameters: {
            level: 'critical',
            message: 'High error rate detected, throttling enabled'
          }
        }
      ],
      cooldownPeriod: 600000, // 10 minutes
      enabled: true
    })
  }
  
  async evaluateScaling(): Promise<void> {
    // Collect current metrics
    const currentMetrics = await this.metricsCollector.getCurrentMetrics()
    this.metrics.push(currentMetrics)
    
    // Keep only recent metrics (last hour)
    const oneHourAgo = Date.now() - 3600000
    this.metrics = this.metrics.filter(m => m.timestamp > oneHourAgo)
    
    // Evaluate each policy
    for (const policy of this.policies) {
      if (!policy.enabled) continue
      
      const shouldTrigger = await this.evaluatePolicy(policy, currentMetrics)
      
      if (shouldTrigger) {
        await this.executeActions(policy.actions)
        this.lastScalingAction = Date.now()
      }
    }
  }
  
  private async evaluatePolicy(
    policy: ScalingPolicy, 
    currentMetrics: ScalingMetrics
  ): Promise<boolean> {
    // Check cooldown period
    const timeSinceLastAction = Date.now() - this.lastScalingAction
    if (timeSinceLastAction < policy.cooldownPeriod) {
      return false
    }
    
    // All triggers must be satisfied
    for (const trigger of policy.triggers) {
      const metricValue = currentMetrics[trigger.metric]
      
      // Check if trigger condition is met for required duration
      const validMetrics = this.metrics.filter(m => {
        const age = Date.now() - m.timestamp
        if (age > trigger.duration) return false
        
        return this.evaluateCondition(
          m[trigger.metric],
          trigger.operator,
          trigger.threshold
        )
      })
      
      // Need consistent trigger for full duration
      const requiredSamples = Math.ceil(trigger.duration / 30000) // 30s sampling
      if (validMetrics.length < requiredSamples) {
        return false
      }
    }
    
    return true
  }
  
  private evaluateCondition(
    value: number,
    operator: string,
    threshold: number
  ): boolean {
    switch (operator) {
      case 'gt': return value > threshold
      case 'lt': return value < threshold
      case 'gte': return value >= threshold
      case 'lte': return value <= threshold
      default: return false
    }
  }
  
  private async executeActions(actions: ScalingAction[]): Promise<void> {
    for (const action of actions) {
      try {
        await this.executeAction(action)
      } catch (error) {
        console.error(`Failed to execute scaling action: ${action.type}`, error)
      }
    }
  }
  
  private async executeAction(action: ScalingAction): Promise<void> {
    switch (action.type) {
      case 'scale_up':
        await this.scaleUp(
          action.parameters.increment,
          action.parameters.maxInstances
        )
        break
        
      case 'scale_down':
        await this.scaleDown(
          action.parameters.decrement,
          action.parameters.minInstances
        )
        break
        
      case 'throttle':
        await this.enableThrottling(action.parameters.throttlePercentage)
        break
        
      case 'notify':
        await this.notificationService.send({
          level: action.parameters.level,
          message: action.parameters.message,
          timestamp: new Date()
        })
        break
    }
  }
  
  private async scaleUp(increment: number, maxInstances: number): Promise<void> {
    const currentInstances = await this.resourceManager.getCurrentInstanceCount()
    const newInstanceCount = Math.min(
      currentInstances + increment,
      maxInstances
    )
    
    if (newInstanceCount > currentInstances) {
      await this.resourceManager.setInstanceCount(newInstanceCount)
      
      console.log(
        `Scaled up from ${currentInstances} to ${newInstanceCount} instances`
      )
    }
  }
  
  private async scaleDown(decrement: number, minInstances: number): Promise<void> {
    const currentInstances = await this.resourceManager.getCurrentInstanceCount()
    const newInstanceCount = Math.max(
      currentInstances - decrement,
      minInstances
    )
    
    if (newInstanceCount < currentInstances) {
      await this.resourceManager.setInstanceCount(newInstanceCount)
      
      console.log(
        `Scaled down from ${currentInstances} to ${newInstanceCount} instances`
      )
    }
  }
  
  private async enableThrottling(percentage: number): Promise<void> {
    await this.resourceManager.setThrottleLevel(percentage)
    console.log(`Enabled throttling at ${percentage}%`)
  }
}
```

## Health Checks & Recovery

### Comprehensive Health Monitoring
```python
# Python implementation for health monitoring
import asyncio
import aiohttp
import psutil
import time
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"

@dataclass
class HealthCheck:
    name: str
    status: HealthStatus
    message: str
    details: Dict[str, Any]
    timestamp: float
    duration_ms: int

@dataclass
class SystemHealth:
    overall_status: HealthStatus
    checks: List[HealthCheck]
    system_metrics: Dict[str, float]
    uptime: float
    version: str

class HealthMonitor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.checks = {}
        self.health_history = []
        self.max_history = config.get('max_history', 1000)
        self.check_interval = config.get('check_interval', 30)
        
    async def start(self):
        """Start the health monitoring loop"""
        await asyncio.create_task(self.monitoring_loop())
    
    async def monitoring_loop(self):
        """Main monitoring loop"""
        while True:
            try:
                health = await self.perform_health_checks()
                self.store_health_result(health)
                
                # Trigger recovery if needed
                if health.overall_status in [HealthStatus.UNHEALTHY, HealthStatus.CRITICAL]:
                    await self.trigger_recovery(health)
                
                await asyncio.sleep(self.check_interval)
                
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self.check_interval)
    
    async def perform_health_checks(self) -> SystemHealth:
        """Perform all configured health checks"""
        checks = []
        start_time = time.time()
        
        # System resource checks
        checks.append(await self.check_cpu_usage())
        checks.append(await self.check_memory_usage())
        checks.append(await self.check_disk_usage())
        checks.append(await self.check_network_connectivity())
        
        # Application-specific checks
        checks.append(await self.check_supabase_connection())
        checks.append(await self.check_agent_processes())
        checks.append(await self.check_workflow_queue())
        checks.append(await self.check_database_connection())
        
        # External service checks
        checks.append(await self.check_mcp_servers())
        checks.append(await self.check_container_runtime())
        
        # Determine overall status
        overall_status = self.calculate_overall_status(checks)
        
        # Collect system metrics
        system_metrics = await self.collect_system_metrics()
        
        return SystemHealth(
            overall_status=overall_status,
            checks=checks,
            system_metrics=system_metrics,
            uptime=time.time() - start_time,
            version=self.config.get('version', '1.0.0')
        )
    
    async def check_cpu_usage(self) -> HealthCheck:
        """Check CPU usage"""
        start_time = time.time()
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            duration_ms = int((time.time() - start_time) * 1000)
            
            if cpu_percent > 90:
                status = HealthStatus.CRITICAL
                message = f"Critical CPU usage: {cpu_percent}%"
            elif cpu_percent > 80:
                status = HealthStatus.UNHEALTHY
                message = f"High CPU usage: {cpu_percent}%"
            elif cpu_percent > 70:
                status = HealthStatus.DEGRADED
                message = f"Elevated CPU usage: {cpu_percent}%"
            else:
                status = HealthStatus.HEALTHY
                message = f"CPU usage normal: {cpu_percent}%"
            
            return HealthCheck(
                name="cpu_usage",
                status=status,
                message=message,
                details={"cpu_percent": cpu_percent},
                timestamp=time.time(),
                duration_ms=duration_ms
            )
            
        except Exception as e:
            return HealthCheck(
                name="cpu_usage",
                status=HealthStatus.UNHEALTHY,
                message=f"Failed to check CPU usage: {str(e)}",
                details={},
                timestamp=time.time(),
                duration_ms=int((time.time() - start_time) * 1000)
            )
    
    async def check_memory_usage(self) -> HealthCheck:
        """Check memory usage"""
        start_time = time.time()
        
        try:
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            available_gb = memory.available / (1024**3)
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            if memory_percent > 95:
                status = HealthStatus.CRITICAL
                message = f"Critical memory usage: {memory_percent}%"
            elif memory_percent > 85:
                status = HealthStatus.UNHEALTHY
                message = f"High memory usage: {memory_percent}%"
            elif memory_percent > 75:
                status = HealthStatus.DEGRADED
                message = f"Elevated memory usage: {memory_percent}%"
            else:
                status = HealthStatus.HEALTHY
                message = f"Memory usage normal: {memory_percent}%"
            
            return HealthCheck(
                name="memory_usage",
                status=status,
                message=message,
                details={
                    "memory_percent": memory_percent,
                    "available_gb": available_gb,
                    "total_gb": memory.total / (1024**3)
                },
                timestamp=time.time(),
                duration_ms=duration_ms
            )
            
        except Exception as e:
            return HealthCheck(
                name="memory_usage",
                status=HealthStatus.UNHEALTHY,
                message=f"Failed to check memory usage: {str(e)}",
                details={},
                timestamp=time.time(),
                duration_ms=int((time.time() - start_time) * 1000)
            )
    
    async def check_supabase_connection(self) -> HealthCheck:
        """Check Supabase database connection"""
        start_time = time.time()
        
        try:
            supabase_url = self.config.get('supabase_url')
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{supabase_url}/rest/v1/",
                    headers={"apikey": self.config.get('supabase_key')},
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    duration_ms = int((time.time() - start_time) * 1000)
                    
                    if response.status == 200:
                        return HealthCheck(
                            name="supabase_connection",
                            status=HealthStatus.HEALTHY,
                            message="Supabase connection healthy",
                            details={"response_time_ms": duration_ms},
                            timestamp=time.time(),
                            duration_ms=duration_ms
                        )
                    else:
                        return HealthCheck(
                            name="supabase_connection",
                            status=HealthStatus.UNHEALTHY,
                            message=f"Supabase connection failed: HTTP {response.status}",
                            details={"status_code": response.status},
                            timestamp=time.time(),
                            duration_ms=duration_ms
                        )
                        
        except asyncio.TimeoutError:
            return HealthCheck(
                name="supabase_connection",
                status=HealthStatus.UNHEALTHY,
                message="Supabase connection timeout",
                details={"timeout_seconds": 10},
                timestamp=time.time(),
                duration_ms=int((time.time() - start_time) * 1000)
            )
        except Exception as e:
            return HealthCheck(
                name="supabase_connection",
                status=HealthStatus.UNHEALTHY,
                message=f"Supabase connection error: {str(e)}",
                details={},
                timestamp=time.time(),
                duration_ms=int((time.time() - start_time) * 1000)
            )
    
    async def check_agent_processes(self) -> HealthCheck:
        """Check AI agent processes"""
        start_time = time.time()
        
        try:
            # Count agent processes
            agent_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if 'amx-agent' in ' '.join(proc.info['cmdline'] or []):
                    agent_processes.append(proc.info)
            
            duration_ms = int((time.time() - start_time) * 1000)
            agent_count = len(agent_processes)
            expected_min = self.config.get('min_agents', 1)
            expected_max = self.config.get('max_agents', 10)
            
            if agent_count == 0:
                status = HealthStatus.CRITICAL
                message = "No agent processes running"
            elif agent_count < expected_min:
                status = HealthStatus.UNHEALTHY
                message = f"Too few agents running: {agent_count} < {expected_min}"
            elif agent_count > expected_max:
                status = HealthStatus.DEGRADED
                message = f"Too many agents running: {agent_count} > {expected_max}"
            else:
                status = HealthStatus.HEALTHY
                message = f"Agent count normal: {agent_count}"
            
            return HealthCheck(
                name="agent_processes",
                status=status,
                message=message,
                details={
                    "agent_count": agent_count,
                    "expected_min": expected_min,
                    "expected_max": expected_max,
                    "processes": agent_processes
                },
                timestamp=time.time(),
                duration_ms=duration_ms
            )
            
        except Exception as e:
            return HealthCheck(
                name="agent_processes",
                status=HealthStatus.UNHEALTHY,
                message=f"Failed to check agent processes: {str(e)}",
                details={},
                timestamp=time.time(),
                duration_ms=int((time.time() - start_time) * 1000)
            )
    
    def calculate_overall_status(self, checks: List[HealthCheck]) -> HealthStatus:
        """Calculate overall system health status"""
        if not checks:
            return HealthStatus.UNHEALTHY
        
        critical_count = sum(1 for check in checks if check.status == HealthStatus.CRITICAL)
        unhealthy_count = sum(1 for check in checks if check.status == HealthStatus.UNHEALTHY)
        degraded_count = sum(1 for check in checks if check.status == HealthStatus.DEGRADED)
        
        # Any critical check makes the system critical
        if critical_count > 0:
            return HealthStatus.CRITICAL
        
        # Multiple unhealthy checks make the system critical
        if unhealthy_count >= 3:
            return HealthStatus.CRITICAL
        
        # Any unhealthy check makes the system unhealthy
        if unhealthy_count > 0:
            return HealthStatus.UNHEALTHY
        
        # Multiple degraded checks make the system unhealthy
        if degraded_count >= 3:
            return HealthStatus.UNHEALTHY
        
        # Any degraded check makes the system degraded
        if degraded_count > 0:
            return HealthStatus.DEGRADED
        
        return HealthStatus.HEALTHY
    
    async def trigger_recovery(self, health: SystemHealth):
        """Trigger automatic recovery actions"""
        for check in health.checks:
            if check.status in [HealthStatus.UNHEALTHY, HealthStatus.CRITICAL]:
                await self.handle_unhealthy_check(check)
    
    async def handle_unhealthy_check(self, check: HealthCheck):
        """Handle specific unhealthy checks"""
        if check.name == "agent_processes" and "No agent processes" in check.message:
            await self.restart_agent_services()
        
        elif check.name == "memory_usage" and check.status == HealthStatus.CRITICAL:
            await self.trigger_memory_cleanup()
        
        elif check.name == "supabase_connection":
            await self.restart_network_services()
    
    async def restart_agent_services(self):
        """Restart agent services"""
        print("Triggering agent service restart...")
        # Implementation depends on deployment method
    
    async def trigger_memory_cleanup(self):
        """Trigger memory cleanup procedures"""
        print("Triggering memory cleanup...")
        # Force garbage collection, clear caches, etc.
    
    def store_health_result(self, health: SystemHealth):
        """Store health check results"""
        self.health_history.append(health)
        
        # Maintain history size
        if len(self.health_history) > self.max_history:
            self.health_history.pop(0)
    
    def get_health_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get health summary for the last N hours"""
        cutoff_time = time.time() - (hours * 3600)
        recent_health = [h for h in self.health_history if h.checks[0].timestamp > cutoff_time]
        
        if not recent_health:
            return {"error": "No health data available"}
        
        # Calculate availability
        total_checks = len(recent_health)
        healthy_checks = sum(1 for h in recent_health if h.overall_status == HealthStatus.HEALTHY)
        availability = (healthy_checks / total_checks) * 100
        
        # Calculate average response times
        avg_response_times = {}
        for check_name in ["supabase_connection", "agent_processes"]:
            response_times = []
            for health in recent_health:
                for check in health.checks:
                    if check.name == check_name and check.status == HealthStatus.HEALTHY:
                        response_times.append(check.duration_ms)
            
            if response_times:
                avg_response_times[check_name] = sum(response_times) / len(response_times)
        
        return {
            "availability_percentage": availability,
            "total_checks": total_checks,
            "healthy_checks": healthy_checks,
            "average_response_times": avg_response_times,
            "current_status": recent_health[-1].overall_status.value if recent_health else "unknown"
        }
```

## Configuration & Management

### Daemon Configuration
```yaml
# /etc/amx/daemon.conf
# AIMatrix Daemon Configuration

daemon:
  # Basic daemon settings
  name: "amx-daemon"
  version: "2.0.0"
  description: "AIMatrix Agent Management Daemon"
  
  # Process settings
  user: "amx"
  group: "amx"
  pid_file: "/var/run/amx/daemon.pid"
  working_directory: "/var/lib/amx"
  
  # Logging configuration
  logging:
    level: "info"  # debug, info, warn, error, fatal
    output: "file"  # console, file, syslog, json
    file_path: "/var/log/amx/daemon.log"
    max_size: "100MB"
    max_files: 10
    compress: true
    
  # Service management
  services:
    enabled:
      - "agent_manager"
      - "workflow_manager"
      - "health_monitor"
      - "metrics_collector"
      - "auto_scaler"
    
    disabled:
      - "debug_service"
  
  # Resource limits
  resources:
    max_cpu_percent: 80.0
    max_memory_mb: 2048
    max_disk_percent: 85.0
    max_processes: 100
    max_threads: 500
    max_open_files: 4096
    
  # Auto-scaling configuration
  auto_scaling:
    enabled: true
    min_instances: 2
    max_instances: 10
    scale_up_threshold: 80.0
    scale_down_threshold: 30.0
    scale_up_cooldown: 300  # seconds
    scale_down_cooldown: 900  # seconds
    
  # Health monitoring
  health:
    check_interval: 30  # seconds
    timeout: 10  # seconds
    unhealthy_threshold: 3
    recovery_enabled: true
    
    checks:
      - name: "cpu_usage"
        enabled: true
        thresholds:
          warning: 70.0
          critical: 90.0
      
      - name: "memory_usage"
        enabled: true
        thresholds:
          warning: 75.0
          critical: 95.0
      
      - name: "disk_usage"
        enabled: true
        thresholds:
          warning: 80.0
          critical: 95.0
      
      - name: "supabase_connection"
        enabled: true
        timeout: 10
        retries: 3
        
      - name: "agent_processes"
        enabled: true
        min_count: 1
        max_count: 50

# Supabase connection
supabase:
  url: "${SUPABASE_URL}"
  anon_key: "${SUPABASE_ANON_KEY}"
  service_role_key: "${SUPABASE_SERVICE_ROLE_KEY}"
  
  connection:
    timeout: 30
    retries: 3
    retry_delay: 5
    
  realtime:
    enabled: true
    heartbeat_interval: 30
    reconnect_interval: 5

# MCP servers configuration
mcp_servers:
  discovery:
    enabled: true
    interval: 300  # 5 minutes
    
  servers:
    - name: "salesforce"
      url: "https://mcp-sf.aimatrix.com"
      enabled: true
      health_check: "/health"
      
    - name: "erp_connector"
      url: "https://mcp-erp.aimatrix.com"
      enabled: true
      health_check: "/health"

# Agent management
agents:
  # Default agent settings
  defaults:
    cpu_limit: "1"
    memory_limit: "512Mi"
    timeout: 300
    max_retries: 3
    
  # Agent lifecycle
  lifecycle:
    startup_timeout: 60
    shutdown_timeout: 30
    health_check_interval: 60
    
  # Resource allocation
  scheduling:
    strategy: "least_loaded"  # round_robin, least_loaded, cpu_based
    max_agents_per_node: 10
    resource_reservation: 0.1  # Reserve 10% of resources

# Workflow management
workflows:
  # Queue settings
  queue:
    max_size: 1000
    timeout: 3600  # 1 hour
    retry_attempts: 3
    retry_delay: 60
    
  # Execution settings
  execution:
    parallel_limit: 20
    timeout: 1800  # 30 minutes
    cleanup_interval: 3600  # 1 hour

# Metrics and monitoring
metrics:
  collection:
    enabled: true
    interval: 30  # seconds
    retention: 7  # days
    
  exporters:
    - type: "prometheus"
      enabled: true
      port: 9090
      endpoint: "/metrics"
      
    - type: "supabase"
      enabled: true
      table: "daemon_metrics"
      batch_size: 100
      
  alerts:
    enabled: true
    providers:
      - type: "email"
        enabled: false
        smtp_server: "smtp.company.com"
        recipients: ["admin@company.com"]
        
      - type: "webhook"
        enabled: true
        url: "https://hooks.slack.com/services/xxx"

# Security settings
security:
  # TLS configuration
  tls:
    enabled: true
    cert_file: "/etc/amx/certs/daemon.crt"
    key_file: "/etc/amx/certs/daemon.key"
    ca_file: "/etc/amx/certs/ca.crt"
    
  # Authentication
  auth:
    enabled: true
    method: "jwt"  # jwt, api_key, mutual_tls
    token_expiry: 3600  # 1 hour
    
  # API access
  api:
    enabled: true
    bind_address: "127.0.0.1"
    port: 8080
    cors_enabled: false
    rate_limiting:
      enabled: true
      requests_per_minute: 60

# Development settings (only in dev mode)
development:
  debug: false
  profiling: false
  hot_reload: false
  test_mode: false
```

### Management CLI
```bash
#!/bin/bash
# AMX Daemon management script

set -e

DAEMON_NAME="amx-daemon"
CONFIG_FILE="/etc/amx/daemon.conf"
PID_FILE="/var/run/amx/daemon.pid"
LOG_FILE="/var/log/amx/daemon.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if daemon is running
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# Start the daemon
start_daemon() {
    log_info "Starting AMX Daemon..."
    
    if is_running; then
        log_warning "AMX Daemon is already running"
        return 0
    fi
    
    # Validate configuration
    if ! amx-daemon --config-check --config "$CONFIG_FILE"; then
        log_error "Configuration validation failed"
        return 1
    fi
    
    # Create necessary directories
    mkdir -p "$(dirname "$PID_FILE")"
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # Start daemon
    if command -v systemctl >/dev/null 2>&1; then
        systemctl start amx-daemon
    else
        amx-daemon --daemon --config "$CONFIG_FILE"
    fi
    
    # Wait for startup
    for i in {1..10}; do
        if is_running; then
            log_success "AMX Daemon started successfully"
            return 0
        fi
        sleep 1
    done
    
    log_error "Failed to start AMX Daemon"
    return 1
}

# Stop the daemon
stop_daemon() {
    log_info "Stopping AMX Daemon..."
    
    if ! is_running; then
        log_warning "AMX Daemon is not running"
        return 0
    fi
    
    if command -v systemctl >/dev/null 2>&1; then
        systemctl stop amx-daemon
    else
        PID=$(cat "$PID_FILE")
        kill -TERM "$PID"
        
        # Wait for graceful shutdown
        for i in {1..30}; do
            if ! kill -0 "$PID" 2>/dev/null; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if kill -0 "$PID" 2>/dev/null; then
            log_warning "Graceful shutdown failed, forcing termination"
            kill -KILL "$PID"
        fi
        
        rm -f "$PID_FILE"
    fi
    
    log_success "AMX Daemon stopped"
}

# Restart the daemon
restart_daemon() {
    stop_daemon
    sleep 2
    start_daemon
}

# Show daemon status
show_status() {
    if is_running; then
        PID=$(cat "$PID_FILE")
        UPTIME=$(ps -o etime= -p "$PID" | tr -d ' ')
        MEMORY=$(ps -o rss= -p "$PID" | tr -d ' ')
        CPU=$(ps -o pcpu= -p "$PID" | tr -d ' ')
        
        log_success "AMX Daemon is running"
        echo "  PID: $PID"
        echo "  Uptime: $UPTIME"
        echo "  Memory: ${MEMORY}KB"
        echo "  CPU: ${CPU}%"
        
        # Show health status
        echo ""
        echo "Health Status:"
        curl -s "http://localhost:8080/health" | jq '.' 2>/dev/null || echo "  Health endpoint not available"
        
    else
        log_error "AMX Daemon is not running"
        return 1
    fi
}

# Show logs
show_logs() {
    local lines=${1:-50}
    
    if [ -f "$LOG_FILE" ]; then
        tail -n "$lines" "$LOG_FILE"
    else
        log_error "Log file not found: $LOG_FILE"
    fi
}

# Follow logs
follow_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        log_error "Log file not found: $LOG_FILE"
    fi
}

# Validate configuration
validate_config() {
    log_info "Validating configuration..."
    
    if amx-daemon --config-check --config "$CONFIG_FILE"; then
        log_success "Configuration is valid"
    else
        log_error "Configuration validation failed"
        return 1
    fi
}

# Show configuration
show_config() {
    if [ -f "$CONFIG_FILE" ]; then
        cat "$CONFIG_FILE"
    else
        log_error "Configuration file not found: $CONFIG_FILE"
    fi
}

# Reload configuration
reload_config() {
    log_info "Reloading configuration..."
    
    if ! is_running; then
        log_error "AMX Daemon is not running"
        return 1
    fi
    
    # Validate new configuration first
    if ! validate_config; then
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    kill -HUP "$PID"
    
    log_success "Configuration reloaded"
}

# Show help
show_help() {
    echo "AMX Daemon Management Script"
    echo ""
    echo "Usage: $0 {start|stop|restart|status|logs|config|reload|help}"
    echo ""
    echo "Commands:"
    echo "  start      Start the daemon"
    echo "  stop       Stop the daemon"
    echo "  restart    Restart the daemon"
    echo "  status     Show daemon status and health"
    echo "  logs       Show recent log entries"
    echo "  tail       Follow log output"
    echo "  config     Show current configuration"
    echo "  validate   Validate configuration file"
    echo "  reload     Reload configuration (without restart)"
    echo "  help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start              # Start the daemon"
    echo "  $0 logs 100           # Show last 100 log entries"
    echo "  $0 status             # Check daemon status and health"
}

# Main command processing
case "${1:-help}" in
    start)
        start_daemon
        ;;
    stop)
        stop_daemon
        ;;
    restart)
        restart_daemon
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs "${2:-50}"
        ;;
    tail)
        follow_logs
        ;;
    config)
        show_config
        ;;
    validate)
        validate_config
        ;;
    reload)
        reload_config
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
```

## API Endpoints

### REST API for Daemon Management
```yaml
# OpenAPI specification for AMX Daemon API
openapi: 3.0.0
info:
  title: AMX Daemon Management API
  description: REST API for managing AMX Daemon services
  version: 2.0.0
  contact:
    name: AIMatrix Support
    url: https://docs.aimatrix.com/support
    email: support@aimatrix.com

servers:
  - url: http://localhost:8080
    description: Local daemon instance
  - url: https://daemon.aimatrix.com
    description: Remote daemon instance

paths:
  /health:
    get:
      summary: Get system health status
      tags: [Health]
      responses:
        200:
          description: System health information
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthResponse'
        503:
          description: System is unhealthy
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthResponse'

  /health/checks/{checkName}:
    get:
      summary: Get specific health check details
      tags: [Health]
      parameters:
        - name: checkName
          in: path
          required: true
          schema:
            type: string
      responses:
        200:
          description: Health check details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HealthCheck'

  /metrics:
    get:
      summary: Get system metrics
      tags: [Metrics]
      parameters:
        - name: format
          in: query
          schema:
            type: string
            enum: [json, prometheus]
            default: json
      responses:
        200:
          description: System metrics
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MetricsResponse'
            text/plain:
              schema:
                type: string

  /agents:
    get:
      summary: List all managed agents
      tags: [Agents]
      parameters:
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive, failed]
        - name: limit
          in: query
          schema:
            type: integer
            default: 50
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
      responses:
        200:
          description: List of agents
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AgentListResponse'

  /agents/{agentId}:
    get:
      summary: Get agent details
      tags: [Agents]
      parameters:
        - name: agentId
          in: path
          required: true
          schema:
            type: string
      responses:
        200:
          description: Agent details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Agent'
        404:
          description: Agent not found

    post:
      summary: Control agent (start, stop, restart)
      tags: [Agents]
      parameters:
        - name: agentId
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AgentControlRequest'
      responses:
        200:
          description: Action completed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ActionResponse'

  /config:
    get:
      summary: Get current configuration
      tags: [Configuration]
      responses:
        200:
          description: Current configuration
          content:
            application/json:
              schema:
                type: object

    post:
      summary: Update configuration
      tags: [Configuration]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
      responses:
        200:
          description: Configuration updated successfully
        400:
          description: Invalid configuration

  /config/validate:
    post:
      summary: Validate configuration
      tags: [Configuration]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
      responses:
        200:
          description: Configuration is valid
        400:
          description: Configuration validation failed

  /logs:
    get:
      summary: Get daemon logs
      tags: [Logs]
      parameters:
        - name: level
          in: query
          schema:
            type: string
            enum: [debug, info, warn, error, fatal]
        - name: limit
          in: query
          schema:
            type: integer
            default: 100
        - name: since
          in: query
          schema:
            type: string
            format: date-time
      responses:
        200:
          description: Log entries
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LogsResponse'

components:
  schemas:
    HealthResponse:
      type: object
      properties:
        overall_status:
          type: string
          enum: [healthy, degraded, unhealthy, critical]
        checks:
          type: array
          items:
            $ref: '#/components/schemas/HealthCheck'
        system_metrics:
          type: object
          additionalProperties:
            type: number
        uptime:
          type: number
        version:
          type: string

    HealthCheck:
      type: object
      properties:
        name:
          type: string
        status:
          type: string
          enum: [healthy, degraded, unhealthy, critical]
        message:
          type: string
        details:
          type: object
        timestamp:
          type: number
        duration_ms:
          type: integer

    MetricsResponse:
      type: object
      properties:
        timestamp:
          type: number
        cpu_usage:
          type: number
        memory_usage:
          type: number
        disk_usage:
          type: number
        active_agents:
          type: integer
        queue_depth:
          type: integer
        response_time:
          type: number

    Agent:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        status:
          type: string
          enum: [active, inactive, failed]
        type:
          type: string
        cpu_usage:
          type: number
        memory_usage:
          type: number
        uptime:
          type: number
        last_activity:
          type: string
          format: date-time

    AgentListResponse:
      type: object
      properties:
        agents:
          type: array
          items:
            $ref: '#/components/schemas/Agent'
        total:
          type: integer
        offset:
          type: integer
        limit:
          type: integer

    AgentControlRequest:
      type: object
      properties:
        action:
          type: string
          enum: [start, stop, restart, kill]
      required:
        - action

    ActionResponse:
      type: object
      properties:
        success:
          type: boolean
        message:
          type: string
        timestamp:
          type: string
          format: date-time

    LogsResponse:
      type: object
      properties:
        logs:
          type: array
          items:
            type: object
            properties:
              timestamp:
                type: string
                format: date-time
              level:
                type: string
              message:
                type: string
              details:
                type: object
        total:
          type: integer
```

---

> [!TIP]
> **Installation**: Install AMX Daemon using your system's package manager (`systemctl enable amx-daemon` on Linux, `brew services start amx-daemon` on macOS, or use the Windows Service installer).

> [!NOTE]
> **High Availability**: For production deployments, run multiple daemon instances with load balancing and shared state storage for seamless failover and zero-downtime operations.

---

*AMX Daemon - Intelligent system services for continuous AI operations*