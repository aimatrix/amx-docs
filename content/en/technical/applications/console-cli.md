---
title: "Console CLI Tools"
description: "Powerful command-line interface tools built with Kotlin and Python for developers and administrators, featuring remote daemon management, setup assistants, and CI/CD integration"
weight: 5
date: 2025-08-23
toc: true
tags: ["cli", "command-line", "kotlin", "python", "automation", "devops", "scripting"]
---

# AIMatrix Console CLI Tools

## Developer-First Command Line Interface

AIMatrix Console CLI Tools provide powerful, git-like command-line interfaces for workspace management, agent operations, and system administration. Built with both Kotlin and Python implementations, these tools offer git-like workflow for workspace management, agent orchestration, system monitoring, and seamless integration with CI/CD pipelines.

## Multi-Language Architecture

Our CLI tools are implemented in both Kotlin and Python to serve different use cases and preferences:

### 🟨 **Kotlin CLI (amx)**
High-performance, type-safe CLI with native compilation and fast startup times

### 🐍 **Python CLI (amx-py)**
Feature-rich CLI with extensive library ecosystem and rapid prototyping capabilities

## Architecture Overview

```mermaid
graph TB
    subgraph "CLI Implementations"
        KOTLIN[Kotlin CLI - amx]
        PYTHON[Python CLI - amx-py]
    end
    
    subgraph "Core Features"
        AGENT_MGR[Agent Management]
        WORKFLOW_MGR[Workflow Operations]
        SYSTEM_ADMIN[System Administration]
        CONFIG_MGR[Configuration Management]
    end
    
    subgraph "Integration Layer"
        REST_CLIENT[REST API Client]
        WS_CLIENT[WebSocket Client]
        SUPABASE[Supabase Client]
        MCP_CLIENT[MCP Client]
    end
    
    subgraph "Output & Formatting"
        JSON_OUT[JSON Output]
        TABLE_OUT[Table Format]
        YAML_OUT[YAML Output]
        INTERACTIVE[Interactive Mode]
    end
    
    subgraph "External Systems"
        AMX_DAEMON[AMX Daemon]
        SUPABASE_BE[Supabase Backend]
        MCP_SERVERS[MCP Servers]
        CI_CD[CI/CD Systems]
    end
    
    KOTLIN --> Core Features
    PYTHON --> Core Features
    
    Core Features --> Integration Layer
    Integration Layer --> External Systems
    
    Core Features --> Output & Formatting
```

## Kotlin CLI Implementation

### Core CLI Framework
```kotlin
// Main CLI application using Clikt framework
import com.github.ajalt.clikt.core.*
import com.github.ajalt.clikt.parameters.arguments.*
import com.github.ajalt.clikt.parameters.options.*
import com.github.ajalt.clikt.parameters.types.*
import kotlinx.coroutines.runBlocking
import kotlinx.serialization.json.Json
import java.io.File

class AMXCli : CliktCommand(
    name = "amx",
    help = "AIMatrix Command Line Interface"
) {
    private val config by option("--config", "-c")
        .file(mustExist = true, canBeDir = false)
        .help("Configuration file path")
    
    private val verbose by option("--verbose", "-v")
        .flag()
        .help("Enable verbose output")
    
    private val outputFormat by option("--output", "-o")
        .choice("json", "yaml", "table", "csv")
        .default("table")
        .help("Output format")
    
    private val profile by option("--profile", "-p")
        .help("Configuration profile to use")
        .default("default")
    
    override fun run() {
        // Initialize global configuration
        GlobalConfig.initialize(config, profile, verbose)
        
        // Set output formatter
        OutputFormatter.setFormat(outputFormat)
        
        if (verbose) {
            echo("AMX CLI initialized with profile: $profile", err = true)
        }
    }
}

// Agent management subcommand
class AgentCommand : CliktCommand(
    name = "agent",
    help = "Agent management operations"
) {
    override fun run() = Unit
}

class AgentListCommand : CliktCommand(
    name = "list",
    help = "List all agents"
) {
    private val status by option("--status", "-s")
        .choice("active", "inactive", "failed", "all")
        .default("all")
        .help("Filter agents by status")
    
    private val limit by option("--limit", "-l")
        .int()
        .default(50)
        .help("Maximum number of agents to display")
    
    private val watch by option("--watch", "-w")
        .flag()
        .help("Watch for real-time updates")
    
    private val json by option("--json")
        .flag()
        .help("Output as JSON")
    
    override fun run() = runBlocking {
        try {
            val agentService = ServiceLocator.getAgentService()
            
            if (watch) {
                watchAgents(agentService)
            } else {
                val agents = agentService.listAgents(status, limit)
                
                if (json) {
                    echo(Json.encodeToString(agents))
                } else {
                    displayAgentsTable(agents)
                }
            }
            
        } catch (e: Exception) {
            echo("Error listing agents: ${e.message}", err = true)
            throw ProgramResult(1)
        }
    }
    
    private suspend fun watchAgents(agentService: AgentService) {
        echo("Watching agents (Press Ctrl+C to stop)...")
        
        agentService.watchAgents { agents ->
            // Clear screen and redisplay
            print("\u001b[2J\u001b[H")
            displayAgentsTable(agents)
            echo("\nLast updated: ${java.time.LocalDateTime.now()}")
        }
    }
    
    private fun displayAgentsTable(agents: List<Agent>) {
        val table = Table.Builder()
            .addColumn("ID")
            .addColumn("Name")
            .addColumn("Status")
            .addColumn("Type")
            .addColumn("CPU %")
            .addColumn("Memory MB")
            .addColumn("Uptime")
            .build()
        
        agents.forEach { agent ->
            table.addRow(
                agent.id.take(8),
                agent.name,
                colorizeStatus(agent.status),
                agent.type,
                "%.1f".format(agent.metrics.cpuUsage),
                agent.metrics.memoryUsageMB.toString(),
                formatUptime(agent.uptime)
            )
        }
        
        echo(table.render())
        echo("\nTotal agents: ${agents.size}")
    }
    
    private fun colorizeStatus(status: String): String {
        return when (status.lowercase()) {
            "active" -> "\u001b[32m$status\u001b[0m"  // Green
            "failed" -> "\u001b[31m$status\u001b[0m"   // Red
            "inactive" -> "\u001b[33m$status\u001b[0m" // Yellow
            else -> status
        }
    }
}

class AgentCreateCommand : CliktCommand(
    name = "create",
    help = "Create a new agent"
) {
    private val name by argument("name")
        .help("Agent name")
    
    private val type by option("--type", "-t")
        .choice("analytics", "automation", "monitoring", "custom")
        .required()
        .help("Agent type")
    
    private val description by option("--description", "-d")
        .help("Agent description")
    
    private val capabilities by option("--capability")
        .multiple()
        .help("Agent capabilities (can specify multiple)")
    
    private val configFile by option("--config")
        .file(mustExist = true)
        .help("Agent configuration file")
    
    private val dryRun by option("--dry-run")
        .flag()
        .help("Show what would be created without actually creating")
    
    override fun run() = runBlocking {
        try {
            val agentConfig = if (configFile != null) {
                parseAgentConfig(configFile!!)
            } else {
                AgentConfig(
                    name = name,
                    type = type,
                    description = description ?: "",
                    capabilities = capabilities.toList()
                )
            }
            
            if (dryRun) {
                echo("Would create agent:")
                echo(Json { prettyPrint = true }.encodeToString(agentConfig))
                return@runBlocking
            }
            
            val agentService = ServiceLocator.getAgentService()
            val agent = agentService.createAgent(agentConfig)
            
            echo("Agent created successfully:")
            echo("  ID: ${agent.id}")
            echo("  Name: ${agent.name}")
            echo("  Type: ${agent.type}")
            echo("  Status: ${agent.status}")
            
        } catch (e: Exception) {
            echo("Error creating agent: ${e.message}", err = true)
            throw ProgramResult(1)
        }
    }
}

// Workflow management subcommand
class WorkflowCommand : CliktCommand(
    name = "workflow",
    help = "Workflow management operations"
) {
    override fun run() = Unit
}

class WorkflowRunCommand : CliktCommand(
    name = "run",
    help = "Execute a workflow"
) {
    private val workflowId by argument("workflow-id")
        .help("Workflow ID to execute")
    
    private val parameters by option("--param", "-p")
        .multiple()
        .help("Workflow parameters in key=value format")
    
    private val wait by option("--wait", "-w")
        .flag()
        .help("Wait for workflow completion")
    
    private val timeout by option("--timeout", "-t")
        .int()
        .default(300)
        .help("Timeout in seconds (only with --wait)")
    
    override fun run() = runBlocking {
        try {
            val workflowService = ServiceLocator.getWorkflowService()
            
            val params = parameters.associate { param ->
                val (key, value) = param.split("=", limit = 2)
                key to value
            }
            
            val execution = workflowService.executeWorkflow(
                workflowId = workflowId,
                parameters = params
            )
            
            echo("Workflow execution started:")
            echo("  Execution ID: ${execution.id}")
            echo("  Workflow: ${execution.workflowId}")
            echo("  Status: ${execution.status}")
            
            if (wait) {
                echo("Waiting for completion (timeout: ${timeout}s)...")
                val result = workflowService.waitForCompletion(
                    executionId = execution.id,
                    timeoutSeconds = timeout
                )
                
                echo("\nWorkflow completed:")
                echo("  Status: ${result.status}")
                echo("  Duration: ${result.durationSeconds}s")
                
                if (result.error != null) {
                    echo("  Error: ${result.error}", err = true)
                    throw ProgramResult(1)
                }
            }
            
        } catch (e: Exception) {
            echo("Error executing workflow: ${e.message}", err = true)
            throw ProgramResult(1)
        }
    }
}

// System administration subcommand
class SystemCommand : CliktCommand(
    name = "system",
    help = "System administration operations"
) {
    override fun run() = Unit
}

class SystemStatusCommand : CliktCommand(
    name = "status",
    help = "Show system status"
) {
    private val detailed by option("--detailed", "-d")
        .flag()
        .help("Show detailed status information")
    
    private val json by option("--json")
        .flag()
        .help("Output as JSON")
    
    override fun run() = runBlocking {
        try {
            val systemService = ServiceLocator.getSystemService()
            val status = systemService.getSystemStatus(detailed)
            
            if (json) {
                echo(Json { prettyPrint = true }.encodeToString(status))
            } else {
                displaySystemStatus(status)
            }
            
        } catch (e: Exception) {
            echo("Error getting system status: ${e.message}", err = true)
            throw ProgramResult(1)
        }
    }
    
    private fun displaySystemStatus(status: SystemStatus) {
        echo("=== AIMatrix System Status ===\n")
        
        echo("Overall Status: ${colorizeStatus(status.overallStatus)}")
        echo("Uptime: ${formatUptime(status.uptime)}")
        echo("Version: ${status.version}")
        
        echo("\n--- Resource Usage ---")
        echo("CPU: ${String.format("%.1f", status.resources.cpuUsage)}%")
        echo("Memory: ${String.format("%.1f", status.resources.memoryUsage)}%")
        echo("Disk: ${String.format("%.1f", status.resources.diskUsage)}%")
        
        echo("\n--- Services ---")
        status.services.forEach { service ->
            echo("${service.name}: ${colorizeStatus(service.status)}")
        }
        
        echo("\n--- Agents ---")
        echo("Active: ${status.agents.active}")
        echo("Inactive: ${status.agents.inactive}")
        echo("Failed: ${status.agents.failed}")
        
        if (status.alerts.isNotEmpty()) {
            echo("\n--- Active Alerts ---")
            status.alerts.forEach { alert ->
                echo("${alert.level}: ${alert.message}")
            }
        }
    }
}

// Configuration management
class ConfigCommand : CliktCommand(
    name = "config",
    help = "Configuration management"
) {
    override fun run() = Unit
}

class ConfigSetCommand : CliktCommand(
    name = "set",
    help = "Set configuration value"
) {
    private val key by argument("key").help("Configuration key")
    private val value by argument("value").help("Configuration value")
    
    private val profile by option("--profile", "-p")
        .default("default")
        .help("Configuration profile")
    
    override fun run() {
        try {
            ConfigManager.setValue(profile, key, value)
            echo("Configuration updated: $key = $value")
        } catch (e: Exception) {
            echo("Error setting configuration: ${e.message}", err = true)
            throw ProgramResult(1)
        }
    }
}

// Main function
fun main(args: Array<String>) {
    val cli = AMXCli()
    
    // Register subcommands
    cli.subcommands(
        AgentCommand().subcommands(
            AgentListCommand(),
            AgentCreateCommand(),
            AgentDeleteCommand(),
            AgentStartCommand(),
            AgentStopCommand(),
            AgentLogsCommand()
        ),
        WorkflowCommand().subcommands(
            WorkflowRunCommand(),
            WorkflowListCommand(),
            WorkflowStatusCommand(),
            WorkflowCreateCommand()
        ),
        SystemCommand().subcommands(
            SystemStatusCommand(),
            SystemHealthCommand(),
            SystemMetricsCommand(),
            SystemLogsCommand()
        ),
        ConfigCommand().subcommands(
            ConfigSetCommand(),
            ConfigGetCommand(),
            ConfigListCommand(),
            ConfigValidateCommand()
        )
    )
    
    cli.main(args)
}
```

### Service Layer Implementation
```kotlin
// Service layer for API interactions
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.plugins.logging.*
import io.ktor.client.request.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.coroutines.flow.Flow
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

@Serializable
data class Agent(
    val id: String,
    val name: String,
    val status: String,
    val type: String,
    val uptime: Long,
    val metrics: AgentMetrics
)

@Serializable
data class AgentMetrics(
    val cpuUsage: Double,
    val memoryUsageMB: Int,
    val requestCount: Long,
    val errorCount: Long
)

interface AgentService {
    suspend fun listAgents(status: String = "all", limit: Int = 50): List<Agent>
    suspend fun getAgent(id: String): Agent?
    suspend fun createAgent(config: AgentConfig): Agent
    suspend fun deleteAgent(id: String): Boolean
    suspend fun startAgent(id: String): Boolean
    suspend fun stopAgent(id: String): Boolean
    suspend fun getAgentLogs(id: String, lines: Int = 100): List<LogEntry>
    suspend fun watchAgents(callback: (List<Agent>) -> Unit)
}

class AgentServiceImpl(
    private val httpClient: HttpClient,
    private val baseUrl: String
) : AgentService {
    
    override suspend fun listAgents(status: String, limit: Int): List<Agent> {
        return try {
            httpClient.get("$baseUrl/api/agents") {
                parameter("status", if (status == "all") null else status)
                parameter("limit", limit)
            }.body()
        } catch (e: Exception) {
            throw ServiceException("Failed to list agents: ${e.message}", e)
        }
    }
    
    override suspend fun getAgent(id: String): Agent? {
        return try {
            httpClient.get("$baseUrl/api/agents/$id").body()
        } catch (e: ClientRequestException) {
            if (e.response.status.value == 404) null
            else throw ServiceException("Failed to get agent: ${e.message}", e)
        }
    }
    
    override suspend fun createAgent(config: AgentConfig): Agent {
        return try {
            httpClient.post("$baseUrl/api/agents") {
                contentType(ContentType.Application.Json)
                setBody(config)
            }.body()
        } catch (e: Exception) {
            throw ServiceException("Failed to create agent: ${e.message}", e)
        }
    }
    
    override suspend fun deleteAgent(id: String): Boolean {
        return try {
            val response = httpClient.delete("$baseUrl/api/agents/$id")
            response.status.isSuccess()
        } catch (e: Exception) {
            throw ServiceException("Failed to delete agent: ${e.message}", e)
        }
    }
    
    override suspend fun watchAgents(callback: (List<Agent>) -> Unit) {
        // WebSocket implementation for real-time updates
        val webSocketClient = WebSocketClient(baseUrl)
        webSocketClient.connect("/ws/agents") { message ->
            val agents = Json.decodeFromString<List<Agent>>(message)
            callback(agents)
        }
    }
}

// HTTP client configuration
object HttpClientFactory {
    fun create(config: ClientConfig): HttpClient {
        return HttpClient(CIO) {
            install(ContentNegotiation) {
                json(Json {
                    prettyPrint = true
                    ignoreUnknownKeys = true
                })
            }
            
            install(Logging) {
                logger = Logger.SIMPLE
                level = if (config.verbose) LogLevel.ALL else LogLevel.INFO
            }
            
            install(DefaultRequest) {
                header("User-Agent", "AMX-CLI/${BuildConfig.VERSION}")
                if (config.apiKey.isNotEmpty()) {
                    header("Authorization", "Bearer ${config.apiKey}")
                }
            }
            
            install(HttpTimeout) {
                requestTimeoutMillis = config.timeoutMs
                connectTimeoutMillis = 10_000
                socketTimeoutMillis = config.timeoutMs
            }
            
            install(HttpRequestRetry) {
                retryOnServerErrors(maxRetries = 3)
                exponentialDelay()
            }
        }
    }
}

// Service locator for dependency injection
object ServiceLocator {
    private lateinit var config: ClientConfig
    private lateinit var httpClient: HttpClient
    
    fun initialize(clientConfig: ClientConfig) {
        config = clientConfig
        httpClient = HttpClientFactory.create(config)
    }
    
    fun getAgentService(): AgentService = 
        AgentServiceImpl(httpClient, config.baseUrl)
    
    fun getWorkflowService(): WorkflowService = 
        WorkflowServiceImpl(httpClient, config.baseUrl)
    
    fun getSystemService(): SystemService = 
        SystemServiceImpl(httpClient, config.baseUrl)
}
```

## Python CLI Implementation

### CLI Framework with Click
```python
# Python CLI implementation using Click framework
import click
import asyncio
import json
import yaml
import sys
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path
import aiohttp
import asyncclick as aclick
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.live import Live
import websockets

console = Console()

class ClickAliasedGroup(click.Group):
    """Custom group that supports command aliases"""
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        
        # Try to find command by prefix
        matches = [cmd for cmd in self.list_commands(ctx) 
                  if cmd.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

@click.group(cls=ClickAliasedGroup)
@click.option('--config', '-c', 
              type=click.Path(exists=True),
              help='Configuration file path')
@click.option('--profile', '-p', 
              default='default',
              help='Configuration profile to use')
@click.option('--verbose', '-v', 
              is_flag=True,
              help='Enable verbose output')
@click.option('--output', '-o',
              type=click.Choice(['json', 'yaml', 'table', 'csv']),
              default='table',
              help='Output format')
@click.pass_context
def cli(ctx, config, profile, verbose, output):
    """AIMatrix Python CLI - Comprehensive agent and workflow management"""
    ctx.ensure_object(dict)
    
    # Initialize global configuration
    ctx.obj['config'] = load_config(config, profile)
    ctx.obj['verbose'] = verbose
    ctx.obj['output_format'] = output
    
    if verbose:
        console.print(f"[blue]AMX CLI initialized with profile: {profile}[/]",
                     file=sys.stderr)

# Agent management commands
@cli.group()
def agent():
    """Agent management operations"""
    pass

@agent.command('list')
@click.option('--status', '-s',
              type=click.Choice(['active', 'inactive', 'failed', 'all']),
              default='all',
              help='Filter agents by status')
@click.option('--limit', '-l', 
              type=int, 
              default=50,
              help='Maximum number of agents to display')
@click.option('--watch', '-w', 
              is_flag=True,
              help='Watch for real-time updates')
@click.option('--json', 'output_json',
              is_flag=True,
              help='Output as JSON')
@click.pass_context
@aclick.async_command
async def list_agents(ctx, status, limit, watch, output_json):
    """List all agents"""
    try:
        agent_service = AgentService(ctx.obj['config'])
        
        if watch:
            await watch_agents(agent_service, status, limit)
        else:
            agents = await agent_service.list_agents(status, limit)
            
            if output_json or ctx.obj['output_format'] == 'json':
                console.print_json(json.dumps([agent.to_dict() for agent in agents]))
            else:
                display_agents_table(agents)
                
    except Exception as e:
        console.print(f"[red]Error listing agents: {str(e)}[/]", file=sys.stderr)
        sys.exit(1)

async def watch_agents(agent_service: 'AgentService', status: str, limit: int):
    """Watch agents with real-time updates"""
    console.print("Watching agents (Press Ctrl+C to stop)...")
    
    try:
        async def update_display():
            while True:
                agents = await agent_service.list_agents(status, limit)
                
                # Clear screen
                console.clear()
                display_agents_table(agents)
                console.print(f"\n[dim]Last updated: {datetime.now().strftime('%H:%M:%S')}[/]")
                
                await asyncio.sleep(5)  # Update every 5 seconds
        
        await update_display()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped watching[/]")

def display_agents_table(agents: List['Agent']):
    """Display agents in a formatted table"""
    table = Table(title="AIMatrix Agents")
    
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="white")
    table.add_column("Status", justify="center")
    table.add_column("Type", style="magenta")
    table.add_column("CPU %", justify="right", style="yellow")
    table.add_column("Memory MB", justify="right", style="blue")
    table.add_column("Uptime", justify="right", style="green")
    
    for agent in agents:
        status_color = {
            'active': '[green]active[/]',
            'inactive': '[yellow]inactive[/]',
            'failed': '[red]failed[/]'
        }.get(agent.status.lower(), agent.status)
        
        table.add_row(
            agent.id[:8],
            agent.name,
            status_color,
            agent.type,
            f"{agent.metrics.cpu_usage:.1f}",
            str(agent.metrics.memory_usage_mb),
            format_uptime(agent.uptime)
        )
    
    console.print(table)
    console.print(f"\nTotal agents: {len(agents)}")

@agent.command('create')
@click.argument('name')
@click.option('--type', '-t',
              type=click.Choice(['analytics', 'automation', 'monitoring', 'custom']),
              required=True,
              help='Agent type')
@click.option('--description', '-d',
              help='Agent description')
@click.option('--capability',
              multiple=True,
              help='Agent capabilities (can specify multiple)')
@click.option('--config-file',
              type=click.File('r'),
              help='Agent configuration file')
@click.option('--dry-run',
              is_flag=True,
              help='Show what would be created without actually creating')
@click.pass_context
@aclick.async_command
async def create_agent(ctx, name, type, description, capability, config_file, dry_run):
    """Create a new agent"""
    try:
        if config_file:
            config_data = json.load(config_file)
            agent_config = AgentConfig.from_dict(config_data)
        else:
            agent_config = AgentConfig(
                name=name,
                type=type,
                description=description or "",
                capabilities=list(capability)
            )
        
        if dry_run:
            console.print("[yellow]Would create agent:[/]")
            console.print_json(agent_config.to_dict())
            return
        
        agent_service = AgentService(ctx.obj['config'])
        agent = await agent_service.create_agent(agent_config)
        
        console.print("[green]Agent created successfully:[/]")
        console.print(f"  ID: {agent.id}")
        console.print(f"  Name: {agent.name}")
        console.print(f"  Type: {agent.type}")
        console.print(f"  Status: {agent.status}")
        
    except Exception as e:
        console.print(f"[red]Error creating agent: {str(e)}[/]", file=sys.stderr)
        sys.exit(1)

# Workflow management commands
@cli.group()
def workflow():
    """Workflow management operations"""
    pass

@workflow.command('run')
@click.argument('workflow_id')
@click.option('--param', '-p',
              multiple=True,
              help='Workflow parameters in key=value format')
@click.option('--wait', '-w',
              is_flag=True,
              help='Wait for workflow completion')
@click.option('--timeout', '-t',
              type=int,
              default=300,
              help='Timeout in seconds (only with --wait)')
@click.pass_context
@aclick.async_command
async def run_workflow(ctx, workflow_id, param, wait, timeout):
    """Execute a workflow"""
    try:
        # Parse parameters
        parameters = {}
        for p in param:
            if '=' not in p:
                raise click.BadParameter(f"Parameter must be in key=value format: {p}")
            key, value = p.split('=', 1)
            parameters[key] = value
        
        workflow_service = WorkflowService(ctx.obj['config'])
        
        execution = await workflow_service.execute_workflow(
            workflow_id=workflow_id,
            parameters=parameters
        )
        
        console.print("[green]Workflow execution started:[/]")
        console.print(f"  Execution ID: {execution.id}")
        console.print(f"  Workflow: {execution.workflow_id}")
        console.print(f"  Status: {execution.status}")
        
        if wait:
            with Progress() as progress:
                task = progress.add_task("Waiting for completion...", total=timeout)
                
                result = await workflow_service.wait_for_completion(
                    execution_id=execution.id,
                    timeout_seconds=timeout,
                    progress_callback=lambda remaining: progress.update(task, completed=timeout-remaining)
                )
                
                progress.update(task, completed=timeout)
            
            console.print(f"\n[green]Workflow completed:[/]")
            console.print(f"  Status: {result.status}")
            console.print(f"  Duration: {result.duration_seconds}s")
            
            if result.error:
                console.print(f"  [red]Error: {result.error}[/]")
                sys.exit(1)
                
    except Exception as e:
        console.print(f"[red]Error executing workflow: {str(e)}[/]", file=sys.stderr)
        sys.exit(1)

# System administration commands
@cli.group()
def system():
    """System administration operations"""
    pass

@system.command('status')
@click.option('--detailed', '-d',
              is_flag=True,
              help='Show detailed status information')
@click.option('--json', 'output_json',
              is_flag=True,
              help='Output as JSON')
@click.pass_context
@aclick.async_command
async def system_status(ctx, detailed, output_json):
    """Show system status"""
    try:
        system_service = SystemService(ctx.obj['config'])
        status = await system_service.get_system_status(detailed)
        
        if output_json or ctx.obj['output_format'] == 'json':
            console.print_json(status.to_dict())
        else:
            display_system_status(status)
            
    except Exception as e:
        console.print(f"[red]Error getting system status: {str(e)}[/]", file=sys.stderr)
        sys.exit(1)

def display_system_status(status: 'SystemStatus'):
    """Display system status in a formatted view"""
    console.print("[bold blue]═══ AIMatrix System Status ═══[/]\n")
    
    # Overall status
    status_color = {
        'healthy': '[green]',
        'degraded': '[yellow]',
        'unhealthy': '[red]',
        'critical': '[red bold]'
    }.get(status.overall_status.lower(), '[white]')
    
    console.print(f"Overall Status: {status_color}{status.overall_status}[/]")
    console.print(f"Uptime: {format_uptime(status.uptime)}")
    console.print(f"Version: {status.version}")
    
    # Resource usage
    console.print("\n[bold]─── Resource Usage ───[/]")
    console.print(f"CPU: {status.resources.cpu_usage:.1f}%")
    console.print(f"Memory: {status.resources.memory_usage:.1f}%")
    console.print(f"Disk: {status.resources.disk_usage:.1f}%")
    
    # Services
    console.print("\n[bold]─── Services ───[/]")
    for service in status.services:
        service_color = {
            'running': '[green]',
            'stopped': '[red]',
            'degraded': '[yellow]'
        }.get(service.status.lower(), '[white]')
        
        console.print(f"{service.name}: {service_color}{service.status}[/]")
    
    # Agents
    console.print("\n[bold]─── Agents ───[/]")
    console.print(f"Active: [green]{status.agents.active}[/]")
    console.print(f"Inactive: [yellow]{status.agents.inactive}[/]")
    console.print(f"Failed: [red]{status.agents.failed}[/]")
    
    # Alerts
    if status.alerts:
        console.print("\n[bold red]─── Active Alerts ───[/]")
        for alert in status.alerts:
            alert_color = {
                'info': '[blue]',
                'warning': '[yellow]',
                'error': '[red]',
                'critical': '[red bold]'
            }.get(alert.level.lower(), '[white]')
            
            console.print(f"{alert_color}{alert.level}: {alert.message}[/]")

# Configuration management commands
@cli.group()
def config():
    """Configuration management"""
    pass

@config.command('set')
@click.argument('key')
@click.argument('value')
@click.option('--profile', '-p',
              default='default',
              help='Configuration profile')
@click.pass_context
def config_set(ctx, key, value, profile):
    """Set configuration value"""
    try:
        config_manager = ConfigManager()
        config_manager.set_value(profile, key, value)
        console.print(f"[green]Configuration updated: {key} = {value}[/]")
    except Exception as e:
        console.print(f"[red]Error setting configuration: {str(e)}[/]", file=sys.stderr)
        sys.exit(1)

@config.command('get')
@click.argument('key')
@click.option('--profile', '-p',
              default='default',
              help='Configuration profile')
@click.pass_context
def config_get(ctx, key, profile):
    """Get configuration value"""
    try:
        config_manager = ConfigManager()
        value = config_manager.get_value(profile, key)
        
        if value is None:
            console.print(f"[yellow]Configuration key not found: {key}[/]")
            sys.exit(1)
        else:
            console.print(value)
    except Exception as e:
        console.print(f"[red]Error getting configuration: {str(e)}[/]", file=sys.stderr)
        sys.exit(1)

# Setup assistant command
@cli.command('setup')
@click.option('--interactive', '-i',
              is_flag=True,
              default=True,
              help='Interactive setup mode')
@click.option('--config-file',
              type=click.Path(),
              help='Write configuration to file')
@aclick.async_command
async def setup(interactive, config_file):
    """Setup assistant for AMX CLI configuration"""
    console.print("[bold blue]Welcome to AMX CLI Setup Assistant[/]\n")
    
    config = {}
    
    if interactive:
        # Interactive configuration
        config['supabase_url'] = click.prompt("Supabase URL")
        config['supabase_key'] = click.prompt("Supabase API Key", hide_input=True)
        config['daemon_url'] = click.prompt("AMX Daemon URL", default="http://localhost:8080")
        
        # Optional configurations
        if click.confirm("Configure advanced settings?", default=False):
            config['timeout'] = click.prompt("Request timeout (seconds)", type=int, default=30)
            config['retries'] = click.prompt("Max retries", type=int, default=3)
            config['output_format'] = click.prompt(
                "Default output format",
                type=click.Choice(['json', 'yaml', 'table', 'csv']),
                default='table'
            )
    
    # Test configuration
    console.print("\n[yellow]Testing configuration...[/]")
    
    try:
        # Test Supabase connection
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{config['supabase_url']}/rest/v1/",
                headers={"apikey": config['supabase_key']}
            ) as response:
                if response.status == 200:
                    console.print("[green]✓ Supabase connection successful[/]")
                else:
                    console.print(f"[red]✗ Supabase connection failed: HTTP {response.status}[/]")
        
        # Test daemon connection
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{config['daemon_url']}/health") as response:
                if response.status == 200:
                    console.print("[green]✓ Daemon connection successful[/]")
                else:
                    console.print(f"[yellow]⚠ Daemon connection failed: HTTP {response.status}[/]")
        
    except Exception as e:
        console.print(f"[red]✗ Connection test failed: {str(e)}[/]")
    
    # Save configuration
    if config_file:
        config_path = Path(config_file)
    else:
        config_dir = Path.home() / '.amx'
        config_dir.mkdir(exist_ok=True)
        config_path = config_dir / 'config.yaml'
    
    with open(config_path, 'w') as f:
        yaml.dump({'default': config}, f, default_flow_style=False)
    
    console.print(f"\n[green]Configuration saved to: {config_path}[/]")
    console.print("\nYou can now use the AMX CLI. Try:")
    console.print("  [cyan]amx agent list[/]")
    console.print("  [cyan]amx system status[/]")

if __name__ == '__main__':
    cli()
```

### Service Layer Implementation (Python)
```python
# Python service layer for API interactions
import aiohttp
import asyncio
import json
import websockets
from typing import List, Dict, Optional, Any, Callable
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta

@dataclass
class Agent:
    id: str
    name: str
    status: str
    type: str
    uptime: int
    metrics: 'AgentMetrics'
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AgentMetrics:
    cpu_usage: float
    memory_usage_mb: int
    request_count: int
    error_count: int

@dataclass
class AgentConfig:
    name: str
    type: str
    description: str
    capabilities: List[str]
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentConfig':
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class ServiceException(Exception):
    """Base exception for service errors"""
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error

class AgentService:
    def __init__(self, config: Dict[str, Any]):
        self.base_url = config.get('daemon_url', 'http://localhost:8080')
        self.timeout = config.get('timeout', 30)
        self.headers = {
            'User-Agent': f'AMX-CLI-Python/{get_version()}',
            'Content-Type': 'application/json'
        }
        
        if 'api_key' in config:
            self.headers['Authorization'] = f"Bearer {config['api_key']}"
    
    async def list_agents(self, status: str = 'all', limit: int = 50) -> List[Agent]:
        """List all agents"""
        try:
            params = {'limit': limit}
            if status != 'all':
                params['status'] = status
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.get(
                    f"{self.base_url}/api/agents",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return [
                            Agent(
                                id=agent['id'],
                                name=agent['name'],
                                status=agent['status'],
                                type=agent['type'],
                                uptime=agent['uptime'],
                                metrics=AgentMetrics(**agent['metrics'])
                            )
                            for agent in data.get('agents', [])
                        ]
                    else:
                        raise ServiceException(f"Failed to list agents: HTTP {response.status}")
        
        except aiohttp.ClientError as e:
            raise ServiceException(f"Network error: {str(e)}", e)
        except Exception as e:
            raise ServiceException(f"Unexpected error: {str(e)}", e)
    
    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get specific agent details"""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.get(
                    f"{self.base_url}/api/agents/{agent_id}",
                    headers=self.headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return Agent(
                            id=data['id'],
                            name=data['name'],
                            status=data['status'],
                            type=data['type'],
                            uptime=data['uptime'],
                            metrics=AgentMetrics(**data['metrics'])
                        )
                    elif response.status == 404:
                        return None
                    else:
                        raise ServiceException(f"Failed to get agent: HTTP {response.status}")
        
        except aiohttp.ClientError as e:
            raise ServiceException(f"Network error: {str(e)}", e)
        except Exception as e:
            raise ServiceException(f"Unexpected error: {str(e)}", e)
    
    async def create_agent(self, config: AgentConfig) -> Agent:
        """Create a new agent"""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.base_url}/api/agents",
                    headers=self.headers,
                    json=config.to_dict()
                ) as response:
                    if response.status == 201:
                        data = await response.json()
                        return Agent(
                            id=data['id'],
                            name=data['name'],
                            status=data['status'],
                            type=data['type'],
                            uptime=data.get('uptime', 0),
                            metrics=AgentMetrics(**data.get('metrics', {
                                'cpu_usage': 0.0,
                                'memory_usage_mb': 0,
                                'request_count': 0,
                                'error_count': 0
                            }))
                        )
                    else:
                        error_data = await response.json()
                        raise ServiceException(f"Failed to create agent: {error_data.get('message', 'Unknown error')}")
        
        except aiohttp.ClientError as e:
            raise ServiceException(f"Network error: {str(e)}", e)
        except Exception as e:
            raise ServiceException(f"Unexpected error: {str(e)}", e)
    
    async def watch_agents(self, callback: Callable[[List[Agent]], None]):
        """Watch agents for real-time updates"""
        ws_url = self.base_url.replace('http://', 'ws://').replace('https://', 'wss://')
        
        try:
            async with websockets.connect(f"{ws_url}/ws/agents") as websocket:
                async for message in websocket:
                    try:
                        data = json.loads(message)
                        agents = [
                            Agent(
                                id=agent['id'],
                                name=agent['name'],
                                status=agent['status'],
                                type=agent['type'],
                                uptime=agent['uptime'],
                                metrics=AgentMetrics(**agent['metrics'])
                            )
                            for agent in data.get('agents', [])
                        ]
                        callback(agents)
                    except json.JSONDecodeError:
                        continue
                        
        except Exception as e:
            raise ServiceException(f"WebSocket error: {str(e)}", e)

class WorkflowService:
    def __init__(self, config: Dict[str, Any]):
        self.base_url = config.get('daemon_url', 'http://localhost:8080')
        self.timeout = config.get('timeout', 30)
        self.headers = {
            'User-Agent': f'AMX-CLI-Python/{get_version()}',
            'Content-Type': 'application/json'
        }
        
        if 'api_key' in config:
            self.headers['Authorization'] = f"Bearer {config['api_key']}"
    
    async def execute_workflow(self, workflow_id: str, parameters: Dict[str, Any]) -> 'WorkflowExecution':
        """Execute a workflow"""
        try:
            payload = {
                'workflow_id': workflow_id,
                'parameters': parameters
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout)) as session:
                async with session.post(
                    f"{self.base_url}/api/workflows/execute",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 201:
                        data = await response.json()
                        return WorkflowExecution(
                            id=data['id'],
                            workflow_id=data['workflow_id'],
                            status=data['status'],
                            created_at=datetime.fromisoformat(data['created_at'])
                        )
                    else:
                        error_data = await response.json()
                        raise ServiceException(f"Failed to execute workflow: {error_data.get('message', 'Unknown error')}")
        
        except aiohttp.ClientError as e:
            raise ServiceException(f"Network error: {str(e)}", e)
        except Exception as e:
            raise ServiceException(f"Unexpected error: {str(e)}", e)
    
    async def wait_for_completion(
        self, 
        execution_id: str, 
        timeout_seconds: int = 300,
        progress_callback: Optional[Callable[[int], None]] = None
    ) -> 'WorkflowResult':
        """Wait for workflow completion with optional progress callback"""
        start_time = datetime.now()
        
        while (datetime.now() - start_time).total_seconds() < timeout_seconds:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.base_url}/api/workflows/executions/{execution_id}",
                        headers=self.headers
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            if data['status'] in ['completed', 'failed', 'cancelled']:
                                return WorkflowResult(
                                    id=data['id'],
                                    status=data['status'],
                                    duration_seconds=data.get('duration_seconds', 0),
                                    error=data.get('error'),
                                    result=data.get('result')
                                )
                            
                            # Update progress
                            if progress_callback:
                                elapsed = (datetime.now() - start_time).total_seconds()
                                remaining = max(0, timeout_seconds - elapsed)
                                progress_callback(int(remaining))
                            
                            await asyncio.sleep(5)  # Poll every 5 seconds
                        else:
                            raise ServiceException(f"Failed to get execution status: HTTP {response.status}")
            
            except Exception as e:
                if progress_callback:
                    elapsed = (datetime.now() - start_time).total_seconds()
                    remaining = max(0, timeout_seconds - elapsed)
                    progress_callback(int(remaining))
                
                await asyncio.sleep(5)
        
        raise ServiceException(f"Workflow execution timed out after {timeout_seconds} seconds")

@dataclass
class WorkflowExecution:
    id: str
    workflow_id: str
    status: str
    created_at: datetime

@dataclass
class WorkflowResult:
    id: str
    status: str
    duration_seconds: int
    error: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

# Utility functions
def format_uptime(seconds: int) -> str:
    """Format uptime in human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m {seconds % 60}s"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{days}d {hours}h"

def load_config(config_file: Optional[str], profile: str) -> Dict[str, Any]:
    """Load configuration from file or environment"""
    import os
    import yaml
    from pathlib import Path
    
    # Default configuration
    config = {
        'daemon_url': os.getenv('AMX_DAEMON_URL', 'http://localhost:8080'),
        'supabase_url': os.getenv('SUPABASE_URL', ''),
        'supabase_key': os.getenv('SUPABASE_ANON_KEY', ''),
        'timeout': int(os.getenv('AMX_TIMEOUT', '30')),
        'output_format': 'table'
    }
    
    # Load from config file
    if config_file:
        config_path = Path(config_file)
    else:
        config_path = Path.home() / '.amx' / 'config.yaml'
    
    if config_path.exists():
        with open(config_path) as f:
            file_config = yaml.safe_load(f)
            if profile in file_config:
                config.update(file_config[profile])
    
    return config

def get_version() -> str:
    """Get CLI version"""
    return "2.0.0"
```

## Remote Daemon Management

### Daemon Control Commands
```bash
#!/bin/bash
# Remote daemon management script

# Daemon management functions
manage_remote_daemon() {
    local action=$1
    local daemon_host=$2
    local daemon_port=${3:-8080}
    
    case $action in
        "start")
            curl -X POST "http://$daemon_host:$daemon_port/api/daemon/start" \
                -H "Authorization: Bearer $AMX_API_TOKEN" \
                -H "Content-Type: application/json"
            ;;
        "stop")
            curl -X POST "http://$daemon_host:$daemon_port/api/daemon/stop" \
                -H "Authorization: Bearer $AMX_API_TOKEN" \
                -H "Content-Type: application/json"
            ;;
        "restart")
            curl -X POST "http://$daemon_host:$daemon_port/api/daemon/restart" \
                -H "Authorization: Bearer $AMX_API_TOKEN" \
                -H "Content-Type: application/json"
            ;;
        "status")
            curl -s "http://$daemon_host:$daemon_port/api/daemon/status" \
                -H "Authorization: Bearer $AMX_API_TOKEN" | jq '.'
            ;;
        *)
            echo "Unknown action: $action"
            echo "Usage: manage_remote_daemon {start|stop|restart|status} <host> [port]"
            return 1
            ;;
    esac
}

# Cluster management
manage_daemon_cluster() {
    local action=$1
    local cluster_config=$2
    
    if [[ ! -f "$cluster_config" ]]; then
        echo "Cluster configuration file not found: $cluster_config"
        return 1
    fi
    
    # Read daemon endpoints from config
    local daemons=($(yq eval '.daemons[].endpoint' "$cluster_config"))
    
    echo "Managing ${#daemons[@]} daemons..."
    
    for daemon in "${daemons[@]}"; do
        echo "Processing daemon: $daemon"
        
        # Extract host and port
        local host=$(echo "$daemon" | cut -d: -f1)
        local port=$(echo "$daemon" | cut -d: -f2)
        
        manage_remote_daemon "$action" "$host" "$port"
        
        if [[ $? -eq 0 ]]; then
            echo "✓ $daemon: $action completed successfully"
        else
            echo "✗ $daemon: $action failed"
        fi
        
        sleep 2  # Brief pause between operations
    done
}

# Health check across cluster
check_cluster_health() {
    local cluster_config=$1
    local daemons=($(yq eval '.daemons[].endpoint' "$cluster_config"))
    local healthy_count=0
    local total_count=${#daemons[@]}
    
    echo "Checking health of $total_count daemons..."
    
    for daemon in "${daemons[@]}"; do
        local host=$(echo "$daemon" | cut -d: -f1)
        local port=$(echo "$daemon" | cut -d: -f2)
        
        local health_response=$(curl -s -w "%{http_code}" \
            "http://$host:$port/health" \
            -H "Authorization: Bearer $AMX_API_TOKEN" \
            -o /tmp/health_response.json)
        
        if [[ "$health_response" == "200" ]]; then
            local status=$(jq -r '.overall_status' /tmp/health_response.json 2>/dev/null)
            echo "✓ $daemon: $status"
            ((healthy_count++))
        else
            echo "✗ $daemon: unreachable (HTTP $health_response)"
        fi
    done
    
    echo ""
    echo "Cluster Health Summary:"
    echo "  Healthy: $healthy_count/$total_count"
    echo "  Health: $(( healthy_count * 100 / total_count ))%"
    
    if [[ $healthy_count -eq $total_count ]]; then
        echo "  Status: All daemons healthy"
        return 0
    elif [[ $healthy_count -gt $(( total_count / 2 )) ]]; then
        echo "  Status: Majority healthy"
        return 0
    else
        echo "  Status: Cluster unhealthy"
        return 1
    fi
}
```

### Load Balancing & Failover
```python
# Load balancing for CLI operations
import asyncio
import aiohttp
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time

class DaemonStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded" 
    UNHEALTHY = "unhealthy"
    UNREACHABLE = "unreachable"

@dataclass
class DaemonEndpoint:
    host: str
    port: int
    status: DaemonStatus = DaemonStatus.HEALTHY
    last_check: float = 0
    response_time: float = 0
    error_count: int = 0
    weight: int = 1  # For weighted load balancing

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

class LoadBalancer:
    def __init__(self, endpoints: List[DaemonEndpoint], strategy: str = "round_robin"):
        self.endpoints = endpoints
        self.strategy = strategy
        self.current_index = 0
        self.health_check_interval = 30  # seconds
        self.max_errors = 3
        
        # Start health checking
        asyncio.create_task(self.health_check_loop())
    
    async def health_check_loop(self):
        """Continuous health checking of all endpoints"""
        while True:
            await self.check_all_endpoints_health()
            await asyncio.sleep(self.health_check_interval)
    
    async def check_all_endpoints_health(self):
        """Check health of all endpoints"""
        tasks = [self.check_endpoint_health(endpoint) for endpoint in self.endpoints]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def check_endpoint_health(self, endpoint: DaemonEndpoint):
        """Check health of a single endpoint"""
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                async with session.get(f"{endpoint.url}/health") as response:
                    endpoint.response_time = time.time() - start_time
                    endpoint.last_check = time.time()
                    
                    if response.status == 200:
                        data = await response.json()
                        overall_status = data.get('overall_status', 'unknown').lower()
                        
                        if overall_status == 'healthy':
                            endpoint.status = DaemonStatus.HEALTHY
                            endpoint.error_count = 0
                        elif overall_status in ['degraded']:
                            endpoint.status = DaemonStatus.DEGRADED
                        else:
                            endpoint.status = DaemonStatus.UNHEALTHY
                    else:
                        endpoint.error_count += 1
                        endpoint.status = DaemonStatus.UNHEALTHY
                        
        except Exception as e:
            endpoint.error_count += 1
            endpoint.response_time = time.time() - start_time
            endpoint.last_check = time.time()
            
            if endpoint.error_count >= self.max_errors:
                endpoint.status = DaemonStatus.UNREACHABLE
            else:
                endpoint.status = DaemonStatus.UNHEALTHY
    
    def get_next_endpoint(self) -> Optional[DaemonEndpoint]:
        """Get next endpoint based on load balancing strategy"""
        healthy_endpoints = [
            ep for ep in self.endpoints 
            if ep.status in [DaemonStatus.HEALTHY, DaemonStatus.DEGRADED]
        ]
        
        if not healthy_endpoints:
            return None
        
        if self.strategy == "round_robin":
            endpoint = healthy_endpoints[self.current_index % len(healthy_endpoints)]
            self.current_index = (self.current_index + 1) % len(healthy_endpoints)
            return endpoint
            
        elif self.strategy == "least_connections":
            # For CLI, we can use response time as proxy for load
            return min(healthy_endpoints, key=lambda ep: ep.response_time)
            
        elif self.strategy == "weighted_random":
            total_weight = sum(ep.weight for ep in healthy_endpoints)
            if total_weight == 0:
                return random.choice(healthy_endpoints)
            
            rand_weight = random.uniform(0, total_weight)
            current_weight = 0
            
            for endpoint in healthy_endpoints:
                current_weight += endpoint.weight
                if rand_weight <= current_weight:
                    return endpoint
                    
        elif self.strategy == "fastest":
            return min(healthy_endpoints, key=lambda ep: ep.response_time)
            
        else:  # fallback to random
            return random.choice(healthy_endpoints)
    
    async def execute_request(self, method: str, path: str, **kwargs) -> aiohttp.ClientResponse:
        """Execute request with failover"""
        max_attempts = min(3, len(self.endpoints))
        last_exception = None
        
        for attempt in range(max_attempts):
            endpoint = self.get_next_endpoint()
            
            if not endpoint:
                raise Exception("No healthy endpoints available")
            
            try:
                url = f"{endpoint.url}{path}"
                
                async with aiohttp.ClientSession() as session:
                    async with session.request(method, url, **kwargs) as response:
                        # Reset error count on successful request
                        endpoint.error_count = 0
                        return response
                        
            except Exception as e:
                last_exception = e
                endpoint.error_count += 1
                
                if endpoint.error_count >= self.max_errors:
                    endpoint.status = DaemonStatus.UNREACHABLE
                
                # Brief pause before retry
                if attempt < max_attempts - 1:
                    await asyncio.sleep(0.5)
        
        raise last_exception or Exception("All endpoints failed")

# Enhanced CLI client with load balancing
class LoadBalancedCLIClient:
    def __init__(self, config: Dict[str, Any]):
        # Parse daemon endpoints from config
        daemon_urls = config.get('daemon_urls', ['http://localhost:8080'])
        
        self.endpoints = []
        for url in daemon_urls:
            if '://' in url:
                parts = url.split('://')[1].split(':')
                host = parts[0]
                port = int(parts[1]) if len(parts) > 1 else 8080
            else:
                host, port = url.split(':') if ':' in url else (url, 8080)
                port = int(port)
            
            self.endpoints.append(DaemonEndpoint(host=host, port=port))
        
        self.load_balancer = LoadBalancer(
            endpoints=self.endpoints,
            strategy=config.get('load_balancing_strategy', 'round_robin')
        )
        
        self.timeout = config.get('timeout', 30)
        self.headers = {
            'User-Agent': f'AMX-CLI-Python/{get_version()}',
            'Content-Type': 'application/json'
        }
        
        if 'api_key' in config:
            self.headers['Authorization'] = f"Bearer {config['api_key']}"
    
    async def list_agents(self, status: str = 'all', limit: int = 50) -> List[Dict[str, Any]]:
        """List agents with load balancing and failover"""
        params = {'limit': limit}
        if status != 'all':
            params['status'] = status
        
        try:
            async with self.load_balancer.execute_request(
                'GET', 
                '/api/agents',
                headers=self.headers,
                params=params,
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('agents', [])
                else:
                    raise Exception(f"API error: HTTP {response.status}")
                    
        except Exception as e:
            raise Exception(f"Failed to list agents: {str(e)}")
    
    async def get_cluster_status(self) -> Dict[str, Any]:
        """Get status of all endpoints in the cluster"""
        cluster_status = {
            'total_endpoints': len(self.endpoints),
            'healthy_endpoints': 0,
            'degraded_endpoints': 0,
            'unhealthy_endpoints': 0,
            'unreachable_endpoints': 0,
            'endpoints': []
        }
        
        for endpoint in self.endpoints:
            status_counts = {
                DaemonStatus.HEALTHY: 'healthy_endpoints',
                DaemonStatus.DEGRADED: 'degraded_endpoints', 
                DaemonStatus.UNHEALTHY: 'unhealthy_endpoints',
                DaemonStatus.UNREACHABLE: 'unreachable_endpoints'
            }
            
            cluster_status[status_counts[endpoint.status]] += 1
            
            cluster_status['endpoints'].append({
                'url': endpoint.url,
                'status': endpoint.status.value,
                'response_time': endpoint.response_time,
                'error_count': endpoint.error_count,
                'last_check': endpoint.last_check
            })
        
        cluster_status['overall_health'] = (
            cluster_status['healthy_endpoints'] / cluster_status['total_endpoints']
        ) * 100
        
        return cluster_status
```

## Setup Assistant & Configuration

### Interactive Setup Wizard
```kotlin
// Kotlin setup assistant
import com.github.ajalt.clikt.core.*
import com.github.ajalt.clikt.parameters.options.*
import kotlinx.coroutines.runBlocking
import java.io.File
import java.net.URL

class SetupCommand : CliktCommand(
    name = "setup",
    help = "Interactive setup assistant for AMX CLI"
) {
    private val configFile by option("--config", "-c")
        .help("Configuration file path")
    
    private val profile by option("--profile", "-p")
        .default("default")
        .help("Configuration profile name")
    
    override fun run() = runBlocking {
        echo("Welcome to AMX CLI Setup Assistant", color = true)
        echo("===================================\n")
        
        val wizard = SetupWizard()
        val config = wizard.runInteractiveSetup()
        
        // Save configuration
        val configPath = configFile?.let { File(it) } ?: getDefaultConfigPath()
        saveConfiguration(configPath, profile, config)
        
        echo("\n✓ Configuration saved successfully!", color = true)
        echo("Configuration saved to: ${configPath.absolutePath}")
        echo("\nYou can now use the AMX CLI. Try:")
        echo("  amx agent list")
        echo("  amx system status")
    }
    
    private fun getDefaultConfigPath(): File {
        val homeDir = System.getProperty("user.home")
        val configDir = File(homeDir, ".amx")
        if (!configDir.exists()) {
            configDir.mkdirs()
        }
        return File(configDir, "config.yaml")
    }
}

class SetupWizard {
    suspend fun runInteractiveSetup(): Configuration {
        val config = Configuration()
        
        // Basic configuration
        echo("=== Basic Configuration ===")
        config.supabaseUrl = promptForUrl("Supabase URL")
        config.supabaseKey = promptForSecret("Supabase API Key")
        config.daemonUrl = promptForUrl("AMX Daemon URL", "http://localhost:8080")
        
        // Advanced configuration (optional)
        if (confirm("Configure advanced settings?", default = false)) {
            echo("\n=== Advanced Configuration ===")
            config.timeout = prompt("Request timeout (seconds)", default = "30")?.toIntOrNull() ?: 30
            config.maxRetries = prompt("Maximum retries", default = "3")?.toIntOrNull() ?: 3
            config.outputFormat = promptChoice(
                "Default output format",
                choices = listOf("table", "json", "yaml", "csv"),
                default = "table"
            )
            
            if (confirm("Configure load balancing?", default = false)) {
                config.daemonUrls = promptForMultipleUrls("Additional daemon URLs (comma-separated)")
                config.loadBalancingStrategy = promptChoice(
                    "Load balancing strategy",
                    choices = listOf("round_robin", "least_connections", "fastest"),
                    default = "round_robin"
                )
            }
        }
        
        // Test configuration
        echo("\n=== Testing Configuration ===")
        testConfiguration(config)
        
        return config
    }
    
    private fun promptForUrl(prompt: String, default: String? = null): String {
        while (true) {
            val input = prompt(prompt, default = default)
            if (input != null && isValidUrl(input)) {
                return input
            }
            echo("Please enter a valid URL (e.g., https://example.com)")
        }
    }
    
    private fun promptForSecret(prompt: String): String {
        return System.console()?.readPassword("$prompt: ")?.let { String(it) }
            ?: prompt(prompt, hideInput = true) ?: ""
    }
    
    private fun promptForMultipleUrls(prompt: String): List<String> {
        val input = prompt(prompt) ?: ""
        return input.split(",")
            .map { it.trim() }
            .filter { it.isNotEmpty() && isValidUrl(it) }
    }
    
    private fun promptChoice(prompt: String, choices: List<String>, default: String): String {
        echo("$prompt:")
        choices.forEachIndexed { index, choice ->
            val marker = if (choice == default) " (default)" else ""
            echo("  ${index + 1}. $choice$marker")
        }
        
        while (true) {
            val input = prompt("Select [1-${choices.size}]", default = choices.indexOf(default).plus(1).toString())
            val index = input?.toIntOrNull()?.minus(1)
            
            if (index != null && index in choices.indices) {
                return choices[index]
            }
            
            echo("Please select a valid option (1-${choices.size})")
        }
    }
    
    private fun isValidUrl(url: String): Boolean {
        return try {
            URL(url)
            true
        } catch (e: Exception) {
            false
        }
    }
    
    private suspend fun testConfiguration(config: Configuration) {
        echo("Testing Supabase connection...")
        val supabaseTest = testSupabaseConnection(config.supabaseUrl, config.supabaseKey)
        echo(if (supabaseTest) "✓ Supabase connection successful" else "✗ Supabase connection failed")
        
        echo("Testing daemon connection...")
        val daemonTest = testDaemonConnection(config.daemonUrl)
        echo(if (daemonTest) "✓ Daemon connection successful" else "⚠ Daemon connection failed (daemon may not be running)")
        
        if (config.daemonUrls.isNotEmpty()) {
            echo("Testing additional daemon endpoints...")
            config.daemonUrls.forEach { url ->
                val test = testDaemonConnection(url)
                echo("  ${if (test) "✓" else "✗"} $url")
            }
        }
    }
}

data class Configuration(
    var supabaseUrl: String = "",
    var supabaseKey: String = "",
    var daemonUrl: String = "http://localhost:8080",
    var daemonUrls: List<String> = emptyList(),
    var timeout: Int = 30,
    var maxRetries: Int = 3,
    var outputFormat: String = "table",
    var loadBalancingStrategy: String = "round_robin"
)
```

## Scripting Capabilities & CI/CD Integration

### Shell Integration
```bash
#!/bin/bash
# AMX CLI shell integration and completions

# Bash completion for AMX CLI
_amx_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Main commands
    case "${COMP_CWORD}" in
        1)
            opts="agent workflow system config setup help"
            COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
            return 0
            ;;
        2)
            case "${prev}" in
                agent)
                    opts="list create delete start stop restart logs status"
                    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                    return 0
                    ;;
                workflow)
                    opts="list run create delete status logs"
                    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                    return 0
                    ;;
                system)
                    opts="status health metrics logs restart"
                    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                    return 0
                    ;;
                config)
                    opts="get set list validate edit"
                    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                    return 0
                    ;;
            esac
            ;;
        *)
            # Dynamic completion for agent/workflow IDs
            case "${COMP_WORDS[1]}" in
                agent)
                    if [[ "${COMP_WORDS[2]}" =~ ^(delete|start|stop|restart|logs|status)$ ]]; then
                        # Complete with agent IDs
                        local agent_ids=$(amx agent list --output json 2>/dev/null | jq -r '.[].id // empty' 2>/dev/null)
                        COMPREPLY=( $(compgen -W "${agent_ids}" -- ${cur}) )
                    fi
                    ;;
                workflow)
                    if [[ "${COMP_WORDS[2]}" == "run" ]]; then
                        # Complete with workflow IDs
                        local workflow_ids=$(amx workflow list --output json 2>/dev/null | jq -r '.[].id // empty' 2>/dev/null)
                        COMPREPLY=( $(compgen -W "${workflow_ids}" -- ${cur}) )
                    fi
                    ;;
            esac
            ;;
    esac
}

# Register completion
complete -F _amx_completion amx

# Convenient aliases
alias amx-agents='amx agent list'
alias amx-status='amx system status'
alias amx-logs='amx system logs --follow'
alias amx-health='amx system health'

# Environment setup function
setup_amx_env() {
    local profile=${1:-default}
    
    echo "Setting up AMX environment (profile: $profile)..."
    
    # Load configuration
    if [[ -f "$HOME/.amx/config.yaml" ]]; then
        export AMX_PROFILE="$profile"
        export AMX_CONFIG_PATH="$HOME/.amx/config.yaml"
        
        # Extract key config values for convenience
        export AMX_DAEMON_URL=$(yq eval ".${profile}.daemon_url // \"http://localhost:8080\"" "$AMX_CONFIG_PATH")
        export AMX_OUTPUT_FORMAT=$(yq eval ".${profile}.output_format // \"table\"" "$AMX_CONFIG_PATH")
        
        echo "✓ AMX environment configured"
        echo "  Profile: $AMX_PROFILE"
        echo "  Daemon: $AMX_DAEMON_URL" 
        echo "  Output: $AMX_OUTPUT_FORMAT"
    else
        echo "⚠ AMX configuration not found. Run 'amx setup' to configure."
    fi
}

# Quick status check function
amx_quick_status() {
    echo "=== AMX Quick Status ==="
    
    # System status
    echo "System:"
    amx system status --output json 2>/dev/null | jq -r '
        "  Overall: " + .overall_status + 
        " | CPU: " + (.resources.cpu_usage | tostring) + "%" +
        " | Memory: " + (.resources.memory_usage | tostring) + "%"
    ' 2>/dev/null || echo "  Status: unavailable"
    
    # Agent summary
    echo "Agents:"
    amx agent list --output json 2>/dev/null | jq -r '
        group_by(.status) | 
        map({status: .[0].status, count: length}) | 
        map("  " + .status + ": " + (.count | tostring)) | 
        join("\n")
    ' 2>/dev/null || echo "  Agents: unavailable"
    
    echo "=================="
}

# Watch function for monitoring
amx_watch() {
    local interval=${1:-5}
    
    echo "Watching AMX status (interval: ${interval}s, Press Ctrl+C to stop)"
    
    while true; do
        clear
        echo "$(date)"
        echo ""
        amx_quick_status
        sleep "$interval"
    done
}
```

### CI/CD Pipeline Integration
```yaml
# GitHub Actions workflow for AMX CLI integration
name: AMX Agent Deployment
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy-agents:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup AMX CLI
      run: |
        # Download and install AMX CLI
        curl -L "https://github.com/aimatrix/amx-cli/releases/latest/download/amx-linux-amd64.tar.gz" | tar xz
        sudo mv amx /usr/local/bin/
        amx --version
    
    - name: Configure AMX CLI
      run: |
        mkdir -p ~/.amx
        cat > ~/.amx/config.yaml << EOF
        production:
          daemon_url: "${{ secrets.AMX_DAEMON_URL }}"
          supabase_url: "${{ secrets.SUPABASE_URL }}"
          supabase_key: "${{ secrets.SUPABASE_KEY }}"
          api_key: "${{ secrets.AMX_API_KEY }}"
          timeout: 60
          output_format: "json"
        EOF
    
    - name: Validate Configuration
      run: |
        amx config validate --profile production
        amx system status --profile production
    
    - name: Deploy Agents
      run: |
        # Deploy agents from configuration
        for agent_config in agents/*.yaml; do
          echo "Deploying agent: $agent_config"
          
          agent_name=$(basename "$agent_config" .yaml)
          
          # Check if agent exists
          if amx agent list --profile production --output json | jq -e ".[] | select(.name == \"$agent_name\")" > /dev/null; then
            echo "Agent $agent_name exists, updating..."
            agent_id=$(amx agent list --profile production --output json | jq -r ".[] | select(.name == \"$agent_name\") | .id")
            amx agent update "$agent_id" --config "$agent_config" --profile production
          else
            echo "Creating new agent: $agent_name"
            amx agent create --config "$agent_config" --profile production
          fi
        done
    
    - name: Run Health Checks
      run: |
        echo "Running post-deployment health checks..."
        
        # Wait for agents to stabilize
        sleep 30
        
        # Check system health
        health_status=$(amx system health --profile production --output json | jq -r '.overall_status')
        
        if [[ "$health_status" != "healthy" ]]; then
          echo "❌ System health check failed: $health_status"
          
          # Get detailed status
          amx system status --detailed --profile production
          
          # Get recent logs
          amx system logs --lines 50 --level error --profile production
          
          exit 1
        fi
        
        echo "✅ Health check passed: $health_status"
    
    - name: Run Smoke Tests
      run: |
        echo "Running smoke tests..."
        
        # Test agent functionality
        for test_file in tests/smoke/*.sh; do
          echo "Running test: $test_file"
          bash "$test_file" --profile production
        done
    
    - name: Notify Deployment
      if: always()
      run: |
        status="${{ job.status }}"
        
        if [[ "$status" == "success" ]]; then
          message="✅ AMX agent deployment successful"
          color="good"
        else
          message="❌ AMX agent deployment failed"
          color="danger"
        fi
        
        # Send notification to Slack
        curl -X POST -H 'Content-type: application/json' \
          --data "{\"text\":\"$message\",\"color\":\"$color\"}" \
          "${{ secrets.SLACK_WEBHOOK_URL }}"

# Jenkins pipeline script
pipeline {
    agent any
    
    environment {
        AMX_PROFILE = 'production'
        AMX_CONFIG_PATH = credentials('amx-config-file')
    }
    
    stages {
        stage('Setup') {
            steps {
                script {
                    // Install AMX CLI if not available
                    sh '''
                        if ! command -v amx &> /dev/null; then
                            echo "Installing AMX CLI..."
                            curl -L "https://github.com/aimatrix/amx-cli/releases/latest/download/amx-linux-amd64.tar.gz" | tar xz
                            sudo mv amx /usr/local/bin/
                        fi
                        
                        amx --version
                    '''
                }
            }
        }
        
        stage('Validate') {
            steps {
                sh '''
                    amx config validate --profile ${AMX_PROFILE}
                    amx system status --profile ${AMX_PROFILE}
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    def agentConfigs = sh(
                        script: "find agents/ -name '*.yaml' -type f",
                        returnStdout: true
                    ).trim().split('\n')
                    
                    agentConfigs.each { config ->
                        sh """
                            echo "Deploying agent configuration: ${config}"
                            amx agent deploy --config "${config}" --profile ${AMX_PROFILE} --wait
                        """
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                sh '''
                    # Run integration tests
                    for test in tests/integration/*.sh; do
                        echo "Running test: $test"
                        bash "$test" --profile ${AMX_PROFILE}
                    done
                '''
            }
        }
    }
    
    post {
        always {
            script {
                // Collect logs and metrics
                sh '''
                    mkdir -p artifacts
                    amx system logs --lines 100 --profile ${AMX_PROFILE} > artifacts/system-logs.txt
                    amx agent list --output json --profile ${AMX_PROFILE} > artifacts/agents.json
                    amx system metrics --profile ${AMX_PROFILE} > artifacts/metrics.json
                '''
                
                archiveArtifacts artifacts: 'artifacts/*', allowEmptyArchive: true
            }
        }
        
        failure {
            script {
                // Send failure notification
                sh '''
                    curl -X POST -H "Content-Type: application/json" \
                        -d '{"text":"❌ AMX deployment failed in Jenkins pipeline"}' \
                        ${SLACK_WEBHOOK_URL}
                '''
            }
        }
        
        success {
            script {
                // Send success notification
                sh '''
                    curl -X POST -H "Content-Type: application/json" \
                        -d '{"text":"✅ AMX deployment successful in Jenkins pipeline"}' \
                        ${SLACK_WEBHOOK_URL}
                '''
            }
        }
    }
}
```

### Automation Scripts
```python
# Python automation script for batch operations
#!/usr/bin/env python3
import asyncio
import argparse
import json
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any
import aiofiles

from amx_cli import AMXClient, AgentConfig

async def batch_agent_deployment(config_dir: Path, profile: str = "default"):
    """Deploy multiple agents from configuration directory"""
    client = AMXClient(profile=profile)
    
    # Find all agent configuration files
    config_files = list(config_dir.glob("*.yaml")) + list(config_dir.glob("*.yml"))
    
    if not config_files:
        print(f"No configuration files found in {config_dir}")
        return
    
    print(f"Found {len(config_files)} agent configurations")
    
    deployed_agents = []
    failed_deployments = []
    
    for config_file in config_files:
        try:
            print(f"Deploying agent from: {config_file}")
            
            # Load configuration
            async with aiofiles.open(config_file, 'r') as f:
                config_data = yaml.safe_load(await f.read())
            
            agent_config = AgentConfig.from_dict(config_data)
            
            # Check if agent already exists
            existing_agents = await client.list_agents()
            existing_agent = next((a for a in existing_agents if a.name == agent_config.name), None)
            
            if existing_agent:
                print(f"  Agent '{agent_config.name}' already exists, updating...")
                agent = await client.update_agent(existing_agent.id, agent_config)
            else:
                print(f"  Creating new agent: '{agent_config.name}'")
                agent = await client.create_agent(agent_config)
            
            deployed_agents.append({
                'name': agent.name,
                'id': agent.id,
                'status': 'deployed',
                'config_file': str(config_file)
            })
            
            print(f"  ✓ Agent '{agent.name}' deployed successfully (ID: {agent.id})")
            
        except Exception as e:
            error_msg = str(e)
            failed_deployments.append({
                'config_file': str(config_file),
                'error': error_msg
            })
            print(f"  ✗ Failed to deploy agent from {config_file}: {error_msg}")
    
    # Summary
    print("\n=== Deployment Summary ===")
    print(f"Successfully deployed: {len(deployed_agents)}")
    print(f"Failed deployments: {len(failed_deployments)}")
    
    if deployed_agents:
        print("\nDeployed agents:")
        for agent in deployed_agents:
            print(f"  - {agent['name']} (ID: {agent['id']})")
    
    if failed_deployments:
        print("\nFailed deployments:")
        for failure in failed_deployments:
            print(f"  - {failure['config_file']}: {failure['error']}")
    
    return len(failed_deployments) == 0

async def health_check_monitoring(profile: str = "default", duration_minutes: int = 60):
    """Monitor system health for specified duration"""
    client = AMXClient(profile=profile)
    
    print(f"Starting health monitoring for {duration_minutes} minutes...")
    
    check_interval = 30  # seconds
    checks_per_minute = 60 // check_interval
    total_checks = duration_minutes * checks_per_minute
    
    health_history = []
    
    for check_num in range(total_checks):
        try:
            status = await client.get_system_status(detailed=True)
            
            health_record = {
                'timestamp': datetime.now().isoformat(),
                'overall_status': status.overall_status,
                'cpu_usage': status.resources.cpu_usage,
                'memory_usage': status.resources.memory_usage,
                'active_agents': status.agents.active,
                'failed_agents': status.agents.failed
            }
            
            health_history.append(health_record)
            
            # Display current status
            progress = (check_num + 1) / total_checks * 100
            print(f"[{progress:5.1f}%] Status: {status.overall_status} | "
                  f"CPU: {status.resources.cpu_usage:.1f}% | "
                  f"Memory: {status.resources.memory_usage:.1f}% | "
                  f"Agents: {status.agents.active} active, {status.agents.failed} failed")
            
            # Alert on critical status
            if status.overall_status in ['unhealthy', 'critical']:
                print(f"⚠️  ALERT: System status is {status.overall_status}")
                
                # Get detailed information
                if status.alerts:
                    print("Active alerts:")
                    for alert in status.alerts:
                        print(f"  - {alert.level}: {alert.message}")
            
            await asyncio.sleep(check_interval)
            
        except Exception as e:
            print(f"❌ Health check failed: {str(e)}")
            
            health_record = {
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
            health_history.append(health_record)
    
    # Generate summary report
    print("\n=== Health Monitoring Summary ===")
    
    successful_checks = [h for h in health_history if 'error' not in h]
    failed_checks = [h for h in health_history if 'error' in h]
    
    print(f"Total checks: {len(health_history)}")
    print(f"Successful: {len(successful_checks)} ({len(successful_checks)/len(health_history)*100:.1f}%)")
    print(f"Failed: {len(failed_checks)} ({len(failed_checks)/len(health_history)*100:.1f}%)")
    
    if successful_checks:
        status_counts = {}
        for check in successful_checks:
            status = check['overall_status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("\nStatus distribution:")
        for status, count in status_counts.items():
            print(f"  {status}: {count} ({count/len(successful_checks)*100:.1f}%)")
        
        # Resource usage statistics
        cpu_values = [c['cpu_usage'] for c in successful_checks]
        memory_values = [c['memory_usage'] for c in successful_checks]
        
        print(f"\nResource usage:")
        print(f"  CPU: avg={sum(cpu_values)/len(cpu_values):.1f}%, max={max(cpu_values):.1f}%")
        print(f"  Memory: avg={sum(memory_values)/len(memory_values):.1f}%, max={max(memory_values):.1f}%")
    
    # Save detailed report
    report_file = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(health_history, f, indent=2)
    
    print(f"\nDetailed report saved to: {report_file}")

async def main():
    parser = argparse.ArgumentParser(description="AMX CLI Automation Scripts")
    parser.add_argument("--profile", "-p", default="default", help="Configuration profile")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Batch deployment command
    deploy_parser = subparsers.add_parser("deploy", help="Batch agent deployment")
    deploy_parser.add_argument("config_dir", type=Path, help="Directory containing agent configurations")
    
    # Health monitoring command
    health_parser = subparsers.add_parser("monitor", help="Health monitoring")
    health_parser.add_argument("--duration", "-d", type=int, default=60, help="Monitoring duration in minutes")
    
    args = parser.parse_args()
    
    if args.command == "deploy":
        success = await batch_agent_deployment(args.config_dir, args.profile)
        sys.exit(0 if success else 1)
    
    elif args.command == "monitor":
        await health_check_monitoring(args.profile, args.duration)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
```

---

> [!TIP]
> **Installation**: Install AMX CLI tools using package managers (`brew install amx-cli` on macOS, `pip install amx-cli` for Python) or download pre-built binaries from our releases page.

> [!NOTE]
> **Shell Integration**: Source the provided shell functions in your `.bashrc` or `.zshrc` for enhanced command completion, aliases, and environment management features.

---

*AIMatrix Console CLI Tools - Command-line power for AI-first operations*