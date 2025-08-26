---
title: "aimatrix-console UR² Dashboard Guide"
description: "Complete guide for UR² Framework visualization and management in aimatrix-console"
weight: 16
---

The aimatrix-console provides an intuitive web-based interface for monitoring, configuring, and optimizing the UR² (Unified RAG-Reasoning) Framework within your AMX Engine deployment. This comprehensive dashboard enables real-time visualization of query difficulty distribution, performance metrics, and learning progress.

## Overview

The UR² Dashboard in aimatrix-console offers:
- Real-time query difficulty visualization
- Performance metrics and gains tracking
- Interactive configuration management
- Learning progress monitoring
- Resource utilization analytics
- Experience replay buffer insights

## Accessing the UR² Dashboard

### Navigation

```
aimatrix-console → Intelligence → UR² Framework
```

Or direct URL:
```
https://console.aimatrix.com/intelligence/ur2
```

### Required Permissions

| Permission | Description | Required For |
|------------|-------------|--------------|
| `ur2:read` | View metrics and status | All users |
| `ur2:config` | Modify configuration | Administrators |
| `ur2:train` | Manage training jobs | ML Engineers |
| `ur2:debug` | Access debug tools | DevOps |

## Dashboard Components

### Main Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                        UR² Framework Dashboard                   │
├─────────────────┬──────────────────┬──────────────────┬─────────┤
│ Query           │ Performance      │ Resource         │ Learning│
│ Distribution    │ Metrics          │ Utilization     │ Progress│
│ [Pie Chart]     │ [Line Graph]     │ [Gauge Charts]  │ [Curve] │
├─────────────────┴──────────────────┴──────────────────┴─────────┤
│                     Retrieval Strategy Heatmap                   │
│                        [Interactive Heatmap]                     │
├───────────────────────────────────────────────────────────────────┤
│ Recent Queries │ Configuration │ Training Jobs │ Alerts          │
│ [Table View]   │ [Settings]    │ [Job List]    │ [Alert Panel]  │
└───────────────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Query Distribution Analysis

The Query Distribution panel provides real-time visualization of incoming queries categorized by difficulty level.

**Interactive Elements:**
- **Pie Chart**: Shows percentage distribution across difficulty levels
- **Time Series**: Historical trends over selected time range
- **Drill-down**: Click any segment to see detailed query samples

**Metrics Displayed:**
```javascript
{
  simple: {
    count: 21543,
    percentage: 42,
    avgLatency: "10ms",
    trend: "+5%"
  },
  moderate: {
    count: 15892,
    percentage: 31,
    avgLatency: "45ms",
    trend: "-2%"
  },
  complex: {
    count: 10256,
    percentage: 20,
    avgLatency: "180ms",
    trend: "+8%"
  },
  expert: {
    count: 3589,
    percentage: 7,
    avgLatency: "420ms",
    trend: "+12%"
  }
}
```

### 2. Performance Metrics Visualization

Track key performance indicators showing the impact of UR² optimization.

**Real-time Metrics:**
- **Response Time Reduction**: Animated gauge showing improvement
- **Accuracy Enhancement**: Comparative bar chart (before/after)
- **API Call Reduction**: Cost savings calculator
- **Throughput Increase**: Requests per second graph

**Dashboard Widget Example:**
```typescript
<PerformanceWidget
  title="Response Time Improvement"
  baseline={50} // ms
  current={18} // ms
  improvement={64} // percentage
  sparkline={last24Hours}
  alert={threshold > 100}
/>
```

### 3. Resource Utilization Monitor

Visual representation of resource allocation across difficulty levels.

**Components:**
- **CPU Usage**: Stacked area chart by difficulty level
- **Memory Allocation**: Real-time memory distribution
- **GPU Utilization**: GPU usage for complex queries
- **Network I/O**: Bandwidth consumption patterns

**Interactive Controls:**
- Adjust resource limits per difficulty level
- Set auto-scaling thresholds
- Configure alert boundaries

### 4. Learning Progress Tracker

Monitor the continuous improvement of the UR² system through reinforcement learning.

**Visualization Elements:**
- **Learning Curve**: Reward progression over episodes
- **Convergence Indicator**: Progress toward optimal performance
- **Experience Buffer**: Replay buffer utilization
- **Training Metrics**: Loss, accuracy, and validation scores

### 5. Retrieval Strategy Heatmap

Interactive heatmap showing retrieval strategy effectiveness across different query types and domains.

**Features:**
- Color-coded efficiency scores
- Click to modify strategy for specific combinations
- A/B testing comparison view
- Historical performance overlay

## Configuration Interface

### Difficulty Thresholds Configuration

```typescript
interface DifficultyConfig {
  simple: Slider(0.0 - 1.0, step: 0.01)
  moderate: Slider(0.0 - 1.0, step: 0.01)
  complex: Slider(0.0 - 1.0, step: 0.01)
  weights: {
    tokenComplexity: Slider(0.0 - 1.0, step: 0.05)
    semanticComplexity: Slider(0.0 - 1.0, step: 0.05)
    domainSpecificity: Slider(0.0 - 1.0, step: 0.05)
  }
}
```

**Visual Configuration Panel:**
```
┌─────────────────────────────────────────────┐
│        Difficulty Threshold Settings         │
├─────────────────────────────────────────────┤
│ Simple:   [====------] 0.30                 │
│ Moderate: [===========-] 0.60               │
│ Complex:  [================-] 0.85          │
├─────────────────────────────────────────────┤
│ Token Complexity:    [========] 0.40        │
│ Semantic Complexity: [======] 0.30          │
│ Domain Specificity:  [======] 0.30          │
├─────────────────────────────────────────────┤
│ [Apply] [Reset] [Save Profile] [Load]       │
└─────────────────────────────────────────────┘
```

### Retrieval Strategy Manager

Configure retrieval strategies for each difficulty level with visual feedback.

```
┌─────────────────────────────────────────────┐
│       Retrieval Strategy Configuration       │
├─────────────────────────────────────────────┤
│ Simple:                                      │
│   ○ None  ● Cache Only  ○ Full             │
│                                              │
│ Moderate:                                    │
│   ○ None  ○ Cache Only  ● Selective        │
│                                              │
│ Complex:                                     │
│   ○ None  ○ Cache Only  ○ Selective ● Hybrid│
│                                              │
│ Expert:                                      │
│   ○ None  ○ Cache Only  ○ Selective ● Full │
├─────────────────────────────────────────────┤
│ Cache Size: [===========] 4GB               │
│ TTL: [====] 3600s                           │
│ [Update Configuration]                       │
└─────────────────────────────────────────────┘
```

### Learning Parameters

Fine-tune reinforcement learning parameters with real-time preview.

```typescript
interface LearningConfig {
  learningRate: NumberInput(0.0001 - 0.1, log_scale)
  batchSize: Select([16, 32, 64, 128, 256])
  experienceBuffer: {
    capacity: NumberInput(1000 - 100000)
    priorityReplay: Toggle(enabled/disabled)
    replayRatio: Slider(0.1 - 1.0)
  }
  curriculum: {
    enabled: Toggle
    stages: DynamicList<Stage>
    progressionThreshold: Percentage
  }
}
```

## Real-time Monitoring

### Live Query Stream

Monitor queries as they're processed with difficulty assessment.

```
┌─────────────────────────────────────────────────────────┐
│                    Live Query Stream                     │
├──────┬────────┬───────────────────────┬────────┬────────┤
│ Time │ Diff.  │ Query Preview         │ Latency│ Status │
├──────┼────────┼───────────────────────┼────────┼────────┤
│ 10:45│ SIMPLE │ "What is 2+2?"        │ 8ms    │ ✓      │
│ 10:45│ COMPLEX│ "Analyze Q4 trends..."│ 187ms  │ ✓      │
│ 10:44│ MODERATE│"Explain quantum..."  │ 42ms   │ ✓      │
│ 10:44│ EXPERT │ "Design distributed..."│ 523ms  │ ⚠      │
└──────┴────────┴───────────────────────┴────────┴────────┘
```

### Performance Alerts

Configure and view alerts for UR² performance metrics.

```typescript
interface AlertConfiguration {
  metric: 'latency' | 'accuracy' | 'apiCalls' | 'resources'
  condition: 'above' | 'below' | 'equals'
  threshold: number
  duration: '1m' | '5m' | '15m' | '1h'
  severity: 'info' | 'warning' | 'critical'
  notification: {
    email: boolean
    slack: boolean
    webhook: string
  }
}
```

**Alert Panel Example:**
```
┌─────────────────────────────────────────────────────┐
│                  Active Alerts                       │
├─────────────────────────────────────────────────────┤
│ ⚠ HIGH LATENCY: Complex queries > 500ms for 5min   │
│ ⚠ LOW CACHE HIT: Rate dropped below 60%            │
│ ℹ LEARNING MILESTONE: 100k episodes completed       │
└─────────────────────────────────────────────────────┘
```

## Training Management

### Curriculum Training Control

Manage and monitor curriculum training jobs from the console.

```
┌──────────────────────────────────────────────────────┐
│              Curriculum Training Manager             │
├──────────────────────────────────────────────────────┤
│ Current Stage: INTERMEDIATE (2/4)                    │
│ Progress: [============------] 67%                   │
│ Episodes: 45,230 / 100,000                          │
│ Avg Reward: 0.724                                   │
│ Time Remaining: ~2h 15m                             │
├──────────────────────────────────────────────────────┤
│ [Pause] [Resume] [Stop] [Adjust Parameters]         │
└──────────────────────────────────────────────────────┘
```

### Training History

View and compare historical training runs.

```typescript
interface TrainingRun {
  id: string
  startTime: Date
  endTime: Date
  stages: Stage[]
  finalMetrics: {
    accuracy: number
    avgReward: number
    convergence: number
  }
  config: TrainingConfig
  artifacts: {
    model: string
    logs: string
    metrics: string
  }
}
```

## Analytics & Reports

### Performance Reports

Generate comprehensive reports on UR² performance.

**Report Types:**
- Daily Performance Summary
- Weekly Optimization Report
- Monthly ROI Analysis
- Custom Date Range Report

**Export Formats:**
- PDF with charts and graphs
- Excel with raw data
- JSON for API integration
- PowerBI/Tableau compatible

### Cost Analysis

Visualize cost savings from UR² optimization.

```
┌────────────────────────────────────────────────────┐
│                 Cost Savings Analysis              │
├────────────────────────────────────────────────────┤
│ API Calls Saved:     58% (10K → 4.2K/hour)        │
│ Compute Reduced:     35% ($2,400 → $1,560/month)  │
│ Response Time Saved: 43% (2.1M ms/day saved)      │
│ Total Monthly Savings: $3,840                      │
├────────────────────────────────────────────────────┤
│ [📊 View Detailed Breakdown] [📥 Export Report]    │
└────────────────────────────────────────────────────┘
```

## Advanced Features

### A/B Testing Interface

Compare different UR² configurations side by side.

```typescript
interface ABTest {
  name: string
  configA: UR2Config
  configB: UR2Config
  trafficSplit: Percentage
  metrics: ComparisonMetrics
  duration: Duration
  winner: 'A' | 'B' | 'undecided'
}
```

### Debug Console

Advanced debugging interface for UR² operations.

```javascript
// Debug console commands
ur2.debug.traceQuery("complex query text")
ur2.debug.explainDifficulty("query")
ur2.debug.simulateLoad(1000, "COMPLEX")
ur2.debug.dumpExperienceBuffer()
ur2.debug.forceGarbageCollection()
```

### Integration Testing

Test UR² integration with other AIMatrix components.

```
┌──────────────────────────────────────────────────┐
│           Integration Test Suite                  │
├──────────────────────────────────────────────────┤
│ ✓ Agent Runtime Environment    Connected         │
│ ✓ Twin Runtime Environment     Connected         │
│ ✓ Knowledge Capsules           Available         │
│ ✓ Message Queue               Active             │
│ ⚠ Vector Database             Slow Response      │
├──────────────────────────────────────────────────┤
│ [Run Full Test] [Test Component] [View Logs]     │
└──────────────────────────────────────────────────┘
```

## Mobile Responsive View

The UR² Dashboard is fully responsive for mobile monitoring.

### Mobile Layout
```
┌─────────────────┐
│   UR² Status    │
├─────────────────┤
│ Queries: 51,280 │
│ Simple:    42%  │
│ Complex:   20%  │
├─────────────────┤
│ Performance     │
│ Speed:    +43%  │
│ Accuracy: +31%  │
├─────────────────┤
│ [Full Dashboard]│
└─────────────────┘
```

## Keyboard Shortcuts

Enhance productivity with keyboard shortcuts:

| Shortcut | Action |
|----------|--------|
| `Ctrl+D` | Open UR² Dashboard |
| `Ctrl+M` | Toggle metrics view |
| `Ctrl+R` | Refresh data |
| `Ctrl+E` | Export current view |
| `Ctrl+S` | Save configuration |
| `Ctrl+T` | Open training manager |
| `F1` | Show help |
| `Esc` | Close dialog/panel |

## API Integration

### WebSocket Real-time Updates

```javascript
// Connect to UR² real-time stream
const ws = new WebSocket('wss://console.aimatrix.com/api/ur2/stream');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    switch(data.type) {
        case 'metrics':
            updateMetricsDisplay(data.payload);
            break;
        case 'difficulty':
            updateDifficultyChart(data.payload);
            break;
        case 'alert':
            showAlert(data.payload);
            break;
    }
};

// Subscribe to specific events
ws.send(JSON.stringify({
    action: 'subscribe',
    events: ['metrics', 'difficulty', 'alerts']
}));
```

### REST API Endpoints

```javascript
// Get current UR² status
fetch('/api/ur2/status')
    .then(res => res.json())
    .then(data => console.log(data));

// Update configuration
fetch('/api/ur2/config', {
    method: 'PUT',
    body: JSON.stringify({
        difficulty: {
            thresholds: {
                simple: 0.35,
                moderate: 0.65
            }
        }
    })
});

// Export metrics
fetch('/api/ur2/metrics/export?format=csv&range=7d')
    .then(res => res.blob())
    .then(blob => downloadFile(blob, 'ur2-metrics.csv'));
```

## Customization

### Custom Dashboards

Create personalized UR² dashboards:

```typescript
interface CustomDashboard {
    name: string
    layout: GridLayout
    widgets: Widget[]
    refreshInterval: seconds
    theme: 'light' | 'dark' | 'auto'
}

// Example custom dashboard
const executiveDashboard: CustomDashboard = {
    name: "Executive Overview",
    layout: { columns: 3, rows: 2 },
    widgets: [
        { type: 'cost-savings', position: [0, 0], size: [2, 1] },
        { type: 'performance-kpi', position: [2, 0], size: [1, 1] },
        { type: 'query-volume', position: [0, 1], size: [3, 1] }
    ],
    refreshInterval: 60,
    theme: 'auto'
};
```

### Widget Library

Available widgets for custom dashboards:

- Query Distribution Pie Chart
- Performance Line Graph
- Resource Gauges
- Learning Progress Curve
- Retrieval Heatmap
- Cost Savings Calculator
- Alert Feed
- Training Status
- Experience Buffer Monitor
- Latency Histogram

## Troubleshooting

### Common Issues

**Dashboard not loading:**
- Check browser console for errors
- Verify WebSocket connection
- Clear browser cache
- Check user permissions

**Metrics not updating:**
- Verify AMX Engine connection
- Check UR² module status
- Review network connectivity
- Inspect browser developer tools

**Configuration changes not applying:**
- Ensure proper permissions
- Check for validation errors
- Verify engine synchronization
- Review audit logs

## Best Practices

### Dashboard Usage

1. **Set up custom alerts** for critical metrics
2. **Create role-specific dashboards** for different teams
3. **Export reports regularly** for historical analysis
4. **Monitor learning progress** during initial deployment
5. **Use A/B testing** before major configuration changes

### Performance Optimization

1. **Adjust refresh intervals** based on needs
2. **Use data aggregation** for large time ranges
3. **Enable browser caching** for static resources
4. **Limit concurrent WebSocket connections**
5. **Archive old metrics** to reduce load

## Support & Documentation

### Getting Help

- **In-app Help**: Click the `?` icon in any panel
- **Documentation**: Access full docs at `/docs/ur2`
- **Video Tutorials**: Available in the learning center
- **Support Chat**: Click the chat bubble for live help

### Additional Resources

- [UR² Framework Concepts](/get-started/concepts/unified-rag-reasoning)
- [AMX Engine Architecture](/technical/architecture/ur2-integration-spec)
- [CLI Command Reference](/technical/applications/aimatrix-cli-ur2)
- [API Documentation](/technical/api/ur2-endpoints)

---

*The UR² Dashboard in aimatrix-console provides comprehensive visualization and control over the most advanced AI optimization framework, enabling teams to monitor, configure, and optimize their intelligent systems with unprecedented insight and control.*