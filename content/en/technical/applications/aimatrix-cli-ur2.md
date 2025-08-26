---
title: "aimatrix-cli UR² Commands Reference"
description: "Complete command reference for UR² Framework integration in aimatrix-cli"
weight: 15
---

The aimatrix-cli provides comprehensive command-line access to the UR² (Unified RAG-Reasoning) Framework capabilities within the AMX Engine, enabling developers and operators to assess query difficulty, configure retrieval strategies, monitor performance, and manage the continuous learning pipeline.

## Overview

The UR² command suite in aimatrix-cli provides:
- Real-time difficulty assessment for queries
- Configuration management for UR² parameters
- Performance monitoring and metrics collection
- Curriculum training management
- Experience replay buffer operations
- Resource allocation optimization

## Installation

```bash
# Install or update aimatrix-cli with UR² support
curl -sSL https://aimatrix.com/cli/install.sh | bash

# Verify UR² commands are available
aimatrix ur2 --help

# Check version
aimatrix --version
# Output: aimatrix-cli v2.5.0 (UR² enabled)
```

## Command Structure

```bash
aimatrix ur2 <subcommand> [options] [arguments]
```

### Global Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--engine-url` | `-e` | AMX Engine endpoint URL | `localhost:8080` |
| `--output` | `-o` | Output format (json, table, yaml) | `table` |
| `--verbose` | `-v` | Enable verbose logging | `false` |
| `--config` | `-c` | Path to configuration file | `~/.aimatrix/config` |

## Core Commands

### assess - Difficulty Assessment

Assess the difficulty of a query to determine optimal processing strategy.

```bash
# Basic difficulty assessment
aimatrix ur2 assess --query "What is 2+2?"
# Output: Difficulty: SIMPLE (confidence: 0.95)

# Detailed assessment with context
aimatrix ur2 assess \
  --query "Analyze market trends and predict Q4 revenue" \
  --context '{"domain": "finance", "historical_data": true}' \
  --detailed
```

**Output Example:**
```json
{
  "difficulty": "COMPLEX",
  "confidence": 0.87,
  "factors": {
    "token_complexity": 0.72,
    "semantic_complexity": 0.91,
    "domain_specificity": 0.83
  },
  "recommended_strategy": "HYBRID_RETRIEVAL",
  "estimated_processing_time": "200ms",
  "resource_requirements": {
    "cpu": 2.0,
    "memory": "2GB",
    "gpu": false
  }
}
```

### config - Configuration Management

Manage UR² configuration parameters.

```bash
# View current configuration
aimatrix ur2 config show

# Set difficulty thresholds
aimatrix ur2 config set difficulty.threshold.simple 0.3
aimatrix ur2 config set difficulty.threshold.moderate 0.6
aimatrix ur2 config set difficulty.threshold.complex 0.85

# Configure retrieval strategies
aimatrix ur2 config set retrieval.strategy.simple NONE
aimatrix ur2 config set retrieval.strategy.moderate CACHED
aimatrix ur2 config set retrieval.strategy.complex HYBRID

# Set learning parameters
aimatrix ur2 config set learning.rate 0.001
aimatrix ur2 config set learning.batch_size 32
aimatrix ur2 config set learning.experience_buffer_size 10000

# Export configuration
aimatrix ur2 config export --file ur2-config.yaml

# Import configuration
aimatrix ur2 config import --file ur2-config.yaml
```

### metrics - Performance Monitoring

Monitor UR² performance metrics and statistics.

```bash
# View overall metrics
aimatrix ur2 metrics

# Component-specific metrics
aimatrix ur2 metrics --component difficulty-assessor
aimatrix ur2 metrics --component knowledge-manager
aimatrix ur2 metrics --component rl-orchestrator

# Time-range specific metrics
aimatrix ur2 metrics --since 1h
aimatrix ur2 metrics --since "2025-08-26 10:00:00" --until now

# Export metrics
aimatrix ur2 metrics --format json > metrics.json
aimatrix ur2 metrics --format csv > metrics.csv

# Real-time streaming metrics
aimatrix ur2 metrics --stream
```

**Output Example:**
```
╭─────────────────────────────────────────────────────────────╮
│                    UR² Performance Metrics                  │
├─────────────────────────────────────────────────────────────┤
│ Query Distribution                                          │
│   Simple:    42% (21,543 queries)                          │
│   Moderate:  31% (15,892 queries)                          │
│   Complex:   20% (10,256 queries)                          │
│   Expert:     7% (3,589 queries)                           │
├─────────────────────────────────────────────────────────────┤
│ Performance Gains                                          │
│   Response Time:     -43% (avg: 32ms → 18ms)              │
│   Accuracy:          +31% (78% → 91%)                      │
│   API Calls:         -58% (10K/hr → 4.2K/hr)              │
│   Resource Usage:    -35% (normalized)                     │
├─────────────────────────────────────────────────────────────┤
│ Learning Progress                                          │
│   Episodes:          125,430                               │
│   Avg Reward:        0.847                                 │
│   Convergence:       87%                                   │
╰─────────────────────────────────────────────────────────────╯
```

### train - Curriculum Training Management

Manage curriculum training jobs for continuous improvement.

```bash
# Start curriculum training
aimatrix ur2 train start \
  --dataset path/to/training/data \
  --curriculum progressive \
  --stages "basic,intermediate,advanced,expert"

# Monitor training progress
aimatrix ur2 train status --job-id abc123

# List all training jobs
aimatrix ur2 train list

# Stop training job
aimatrix ur2 train stop --job-id abc123

# Export training metrics
aimatrix ur2 train export --job-id abc123 --format tensorboard
```

### replay - Experience Replay Management

Manage the experience replay buffer for reinforcement learning.

```bash
# View replay buffer statistics
aimatrix ur2 replay stats

# Show recent experiences
aimatrix ur2 replay show --limit 100

# Filter experiences by difficulty
aimatrix ur2 replay show --difficulty complex --limit 50

# Clear old experiences
aimatrix ur2 replay clear --before "2025-08-01"

# Export replay buffer
aimatrix ur2 replay export --file replay-buffer.json

# Import experiences
aimatrix ur2 replay import --file external-experiences.json
```

### optimize - Resource Optimization

Optimize resource allocation based on workload patterns.

```bash
# Analyze resource usage patterns
aimatrix ur2 optimize analyze

# Apply optimization recommendations
aimatrix ur2 optimize apply --profile balanced

# Create custom optimization profile
aimatrix ur2 optimize create-profile \
  --name "high-throughput" \
  --simple-cpu 0.25 \
  --complex-cpu 4.0 \
  --cache-size 4GB

# Test optimization profile
aimatrix ur2 optimize test --profile high-throughput --duration 5m
```

## Advanced Usage

### Batch Processing

Process multiple queries with difficulty assessment:

```bash
# Create batch file (queries.txt)
cat > queries.txt << EOF
What is 2+2?
Explain quantum computing principles
Analyze financial market trends for Q4
Design a distributed system architecture
EOF

# Process batch
aimatrix ur2 batch process --file queries.txt --output results.json
```

### Pipeline Integration

Integrate UR² commands into CI/CD pipelines:

```bash
#!/bin/bash
# ur2-pipeline.sh

# Assess deployment complexity
COMPLEXITY=$(aimatrix ur2 assess \
  --query "Deploy microservices to production" \
  --output json | jq -r '.difficulty')

# Allocate resources based on complexity
if [ "$COMPLEXITY" == "COMPLEX" ]; then
  kubectl scale deployment amx-engine --replicas=5
else
  kubectl scale deployment amx-engine --replicas=3
fi

# Monitor performance during deployment
aimatrix ur2 metrics --stream --duration 10m > deployment-metrics.log
```

### Scripting Examples

**Python Integration:**

```python
import subprocess
import json

def assess_query_difficulty(query):
    """Assess query difficulty using aimatrix-cli"""
    result = subprocess.run(
        ['aimatrix', 'ur2', 'assess', '--query', query, '--output', 'json'],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

# Example usage
difficulty = assess_query_difficulty("Complex reasoning task")
print(f"Difficulty: {difficulty['difficulty']}")
print(f"Strategy: {difficulty['recommended_strategy']}")
```

**Node.js Integration:**

```javascript
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function getUR2Metrics() {
    const { stdout } = await execPromise('aimatrix ur2 metrics --output json');
    return JSON.parse(stdout);
}

// Example usage
getUR2Metrics().then(metrics => {
    console.log('Query Distribution:', metrics.queryDistribution);
    console.log('Performance Gains:', metrics.performanceGains);
});
```

## Configuration Files

### UR² Configuration Schema

```yaml
# ~/.aimatrix/ur2.config.yaml
ur2:
  difficulty:
    thresholds:
      simple: 0.3
      moderate: 0.6
      complex: 0.85
    weights:
      token_complexity: 0.4
      semantic_complexity: 0.3
      domain_specificity: 0.3
  
  retrieval:
    strategies:
      simple: NONE
      moderate: CACHED
      complex: HYBRID
      expert: FULL
    
    cache:
      size: 4GB
      ttl: 3600
      eviction: LRU
  
  learning:
    rate: 0.001
    batch_size: 32
    experience_buffer:
      capacity: 10000
      priority_replay: true
    
    curriculum:
      stages:
        - name: basic
          duration: 1000
          threshold: 0.8
        - name: intermediate
          duration: 2000
          threshold: 0.85
        - name: advanced
          duration: 3000
          threshold: 0.9
        - name: expert
          duration: 5000
          threshold: 0.95
  
  resources:
    allocation:
      simple:
        cpu: 0.5
        memory: 512MB
        timeout: 5s
      moderate:
        cpu: 1.0
        memory: 1GB
        timeout: 15s
      complex:
        cpu: 2.0
        memory: 2GB
        timeout: 30s
      expert:
        cpu: 4.0
        memory: 4GB
        timeout: 60s
```

## Environment Variables

Configure aimatrix-cli UR² behavior using environment variables:

```bash
# Engine connection
export AIMATRIX_ENGINE_URL="https://engine.aimatrix.com"
export AIMATRIX_API_KEY="your-api-key"

# UR² specific settings
export AIMATRIX_UR2_ENABLED=true
export AIMATRIX_UR2_DEFAULT_TIMEOUT=30
export AIMATRIX_UR2_METRICS_INTERVAL=5

# Logging
export AIMATRIX_LOG_LEVEL=debug
export AIMATRIX_LOG_FILE=/var/log/aimatrix/ur2.log
```

## Troubleshooting

### Common Issues

**Difficulty assessment timeout:**
```bash
# Increase timeout for complex queries
aimatrix ur2 assess --query "..." --timeout 60

# Check engine connectivity
aimatrix ur2 health
```

**Configuration not applying:**
```bash
# Verify configuration
aimatrix ur2 config validate

# Force reload configuration
aimatrix ur2 config reload

# Check effective configuration
aimatrix ur2 config show --effective
```

**Metrics not collecting:**
```bash
# Check metrics collector status
aimatrix ur2 metrics --status

# Reset metrics
aimatrix ur2 metrics reset

# Enable debug logging
aimatrix ur2 metrics --verbose --debug
```

### Debug Mode

Enable comprehensive debugging for UR² operations:

```bash
# Enable debug mode
export AIMATRIX_DEBUG=true

# Run with trace logging
aimatrix ur2 assess --query "test" --trace

# Generate debug report
aimatrix ur2 debug report --output debug-report.tar.gz
```

## Performance Tips

### Optimization Strategies

1. **Batch Processing**: Process multiple queries together for better throughput
2. **Connection Pooling**: Reuse engine connections with `--persistent`
3. **Local Caching**: Enable local result caching with `--cache`
4. **Async Operations**: Use `--async` for non-blocking operations

```bash
# Optimized batch processing
aimatrix ur2 batch process \
  --file queries.txt \
  --persistent \
  --cache \
  --async \
  --parallel 4
```

### Resource Management

Monitor and optimize resource usage:

```bash
# Check resource usage
aimatrix ur2 resources status

# Set resource limits
aimatrix ur2 resources limit --cpu 2 --memory 4GB

# Auto-scale based on load
aimatrix ur2 resources autoscale --min 1 --max 10 --target-cpu 70
```

## Integration Examples

### Docker Integration

```dockerfile
FROM aimatrix/cli:latest

# Install UR² configuration
COPY ur2.config.yaml /etc/aimatrix/ur2.config.yaml

# Set environment
ENV AIMATRIX_UR2_ENABLED=true
ENV AIMATRIX_ENGINE_URL=http://amx-engine:8080

# Health check using UR²
HEALTHCHECK --interval=30s --timeout=3s \
  CMD aimatrix ur2 health || exit 1
```

### Kubernetes CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ur2-metrics-collector
spec:
  schedule: "*/5 * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: metrics-collector
            image: aimatrix/cli:latest
            command:
            - /bin/sh
            - -c
            - |
              aimatrix ur2 metrics --format json > /data/metrics-$(date +%s).json
              aimatrix ur2 replay export --file /data/replay-$(date +%s).json
          restartPolicy: OnFailure
```

## Command Reference Summary

| Command | Description | Example |
|---------|-------------|---------|
| `assess` | Assess query difficulty | `aimatrix ur2 assess --query "..."` |
| `config` | Manage configuration | `aimatrix ur2 config set key value` |
| `metrics` | View performance metrics | `aimatrix ur2 metrics --component all` |
| `train` | Manage training jobs | `aimatrix ur2 train start --dataset data/` |
| `replay` | Manage experience buffer | `aimatrix ur2 replay show --limit 100` |
| `optimize` | Resource optimization | `aimatrix ur2 optimize analyze` |
| `batch` | Batch processing | `aimatrix ur2 batch process --file q.txt` |
| `health` | Check UR² health | `aimatrix ur2 health` |
| `debug` | Debug operations | `aimatrix ur2 debug report` |

## Support

For additional help and support:

```bash
# Get help for any command
aimatrix ur2 <command> --help

# View documentation
aimatrix ur2 docs

# Report issues
aimatrix ur2 report-issue

# Join community
aimatrix community join
```

---

*The UR² Framework in aimatrix-cli brings cutting-edge AI optimization directly to your command line, enabling unprecedented control over query processing, resource allocation, and continuous learning.*