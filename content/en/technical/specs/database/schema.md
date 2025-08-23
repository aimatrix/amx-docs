---
title: Database Schema Design
description: Complete database schema specifications for AIMatrix platform
weight: 1
---

# AIMatrix Database Schema Specification

## Overview

AIMatrix uses a **polyglot persistence** strategy with different database systems optimized for specific use cases. This document provides complete schema definitions, relationships, and design rationale.

## Database Systems

| System | Use Case | Data Type | Volume |
|--------|----------|-----------|--------|
| PostgreSQL | Transactional data, ACID operations | Structured | 100TB |
| MongoDB | Documents, configurations, logs | Semi-structured | 500TB |
| Redis | Caching, sessions, real-time data | Key-value | 10TB |
| Pinecone | Vector embeddings | Vectors | 1B vectors |
| Neo4j | Knowledge graphs | Graph | 10B nodes |
| ClickHouse | Analytics, time-series | Columnar | 1PB |
| S3 | Binary objects, backups | Blobs | Unlimited |

## PostgreSQL Schema

### Core Domain Model

```sql
-- =============================================
-- Users and Authentication
-- =============================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Profile
    full_name VARCHAR(255),
    avatar_url TEXT,
    timezone VARCHAR(50) DEFAULT 'UTC',
    locale VARCHAR(10) DEFAULT 'en-US',
    
    -- Status
    email_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    
    -- Indexes
    INDEX idx_users_email (email) WHERE is_deleted = FALSE,
    INDEX idx_users_username (username) WHERE is_deleted = FALSE,
    INDEX idx_users_created (created_at DESC)
);

-- Multi-factor authentication
CREATE TABLE user_mfa (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    method VARCHAR(20) NOT NULL, -- totp, sms, email, backup_codes
    secret TEXT,
    phone_number VARCHAR(20),
    backup_codes TEXT[],
    is_primary BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    UNIQUE(user_id, method),
    INDEX idx_mfa_user (user_id)
);

-- API Keys for programmatic access
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    key_prefix VARCHAR(10) NOT NULL, -- For identification
    
    -- Permissions
    scopes TEXT[] DEFAULT '{}',
    rate_limit INTEGER DEFAULT 1000, -- requests per hour
    
    -- Usage tracking
    last_used_at TIMESTAMPTZ,
    usage_count BIGINT DEFAULT 0,
    
    -- Lifecycle
    expires_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    revoked_at TIMESTAMPTZ,
    
    INDEX idx_api_keys_hash (key_hash),
    INDEX idx_api_keys_user (user_id),
    INDEX idx_api_keys_prefix (key_prefix)
);

-- =============================================
-- Organizations and Workspaces
-- =============================================

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    
    -- Billing
    billing_email VARCHAR(255),
    billing_plan VARCHAR(50) DEFAULT 'free',
    billing_status VARCHAR(50) DEFAULT 'active',
    trial_ends_at TIMESTAMPTZ,
    
    -- Limits
    max_users INTEGER DEFAULT 5,
    max_agents INTEGER DEFAULT 10,
    max_storage_gb INTEGER DEFAULT 100,
    max_api_calls_per_month BIGINT DEFAULT 100000,
    
    -- Settings
    settings JSONB DEFAULT '{}',
    features TEXT[] DEFAULT '{}',
    
    -- Metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    INDEX idx_org_slug (slug),
    INDEX idx_org_billing_status (billing_status)
);

CREATE TABLE organization_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'member', -- owner, admin, member, viewer
    
    -- Permissions
    permissions TEXT[] DEFAULT '{}',
    
    -- Metadata
    invited_by UUID REFERENCES users(id),
    invited_at TIMESTAMPTZ,
    accepted_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    UNIQUE(organization_id, user_id),
    INDEX idx_org_members_org (organization_id),
    INDEX idx_org_members_user (user_id),
    INDEX idx_org_members_role (role)
);

CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Type and purpose
    type VARCHAR(50) DEFAULT 'general', -- general, development, production
    environment VARCHAR(50) DEFAULT 'development',
    
    -- Settings
    settings JSONB DEFAULT '{}',
    secrets JSONB DEFAULT '{}', -- Encrypted
    
    -- Resource limits
    max_agents INTEGER,
    max_storage_gb INTEGER,
    max_compute_hours INTEGER,
    
    -- Metadata
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    archived_at TIMESTAMPTZ,
    
    UNIQUE(organization_id, slug),
    INDEX idx_workspace_org (organization_id),
    INDEX idx_workspace_slug (slug),
    INDEX idx_workspace_active (is_active)
);

-- =============================================
-- Agents and Capabilities
-- =============================================

CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    -- Identity
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,
    avatar_url TEXT,
    
    -- Type and category
    type VARCHAR(50) NOT NULL, -- conversational, autonomous, reactive, scheduled
    category VARCHAR(50), -- customer_service, sales, operations, analytics
    
    -- Configuration
    system_prompt TEXT,
    model_preferences JSONB DEFAULT '{}',
    tools TEXT[] DEFAULT '{}',
    capabilities TEXT[] DEFAULT '{}',
    
    -- Behavior settings
    temperature DECIMAL(3,2) DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 4096,
    response_format VARCHAR(20) DEFAULT 'text', -- text, json, markdown
    
    -- Memory configuration
    memory_type VARCHAR(50) DEFAULT 'conversation', -- none, conversation, summary, full
    memory_window_size INTEGER DEFAULT 10,
    
    -- State
    state VARCHAR(50) DEFAULT 'created', -- created, ready, running, paused, error
    last_error TEXT,
    
    -- Metrics
    total_executions BIGINT DEFAULT 0,
    total_tokens_used BIGINT DEFAULT 0,
    average_response_time_ms INTEGER,
    success_rate DECIMAL(5,2),
    
    -- Metadata
    version INTEGER DEFAULT 1,
    is_public BOOLEAN DEFAULT FALSE,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deployed_at TIMESTAMPTZ,
    
    UNIQUE(workspace_id, slug),
    INDEX idx_agent_workspace (workspace_id),
    INDEX idx_agent_type (type),
    INDEX idx_agent_state (state),
    INDEX idx_agent_public (is_public) WHERE is_public = TRUE
);

CREATE TABLE agent_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    version INTEGER NOT NULL,
    
    -- Snapshot of configuration
    config JSONB NOT NULL,
    system_prompt TEXT,
    tools TEXT[],
    
    -- Change tracking
    change_summary TEXT,
    changed_by UUID REFERENCES users(id),
    
    -- Deployment status
    is_deployed BOOLEAN DEFAULT FALSE,
    deployed_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    UNIQUE(agent_id, version),
    INDEX idx_agent_version_agent (agent_id),
    INDEX idx_agent_version_deployed (is_deployed)
);

-- =============================================
-- Agent Executions and Tasks
-- =============================================

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    -- Task definition
    name VARCHAR(255),
    type VARCHAR(50) NOT NULL, -- chat, api_call, scheduled, triggered
    priority INTEGER DEFAULT 5,
    
    -- Scheduling (for scheduled tasks)
    schedule_cron VARCHAR(100),
    scheduled_at TIMESTAMPTZ,
    
    -- Trigger configuration
    trigger_type VARCHAR(50), -- webhook, event, manual
    trigger_config JSONB DEFAULT '{}',
    
    -- Execution settings
    timeout_seconds INTEGER DEFAULT 300,
    max_retries INTEGER DEFAULT 3,
    retry_delay_seconds INTEGER DEFAULT 60,
    
    -- State
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    INDEX idx_task_workspace (workspace_id),
    INDEX idx_task_scheduled (scheduled_at) WHERE scheduled_at IS NOT NULL,
    INDEX idx_task_active (is_active)
);

CREATE TABLE agent_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    session_id UUID,
    
    -- Execution context
    user_id UUID REFERENCES users(id),
    workspace_id UUID NOT NULL REFERENCES workspaces(id),
    
    -- Input/Output
    input JSONB NOT NULL,
    output JSONB,
    
    -- Model usage
    model_used VARCHAR(100),
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    
    -- Performance
    execution_time_ms INTEGER,
    first_token_time_ms INTEGER,
    
    -- Status
    status VARCHAR(50) NOT NULL, -- pending, running, completed, failed, cancelled
    error_message TEXT,
    error_code VARCHAR(50),
    
    -- Retry information
    retry_count INTEGER DEFAULT 0,
    parent_execution_id UUID REFERENCES agent_executions(id),
    
    -- Timestamps
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    
    -- Partitioning by month
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    INDEX idx_execution_agent (agent_id),
    INDEX idx_execution_session (session_id),
    INDEX idx_execution_status (status),
    INDEX idx_execution_created (created_at DESC),
    INDEX idx_execution_workspace (workspace_id)
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE agent_executions_2025_01 
    PARTITION OF agent_executions
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

CREATE TABLE agent_executions_2025_02
    PARTITION OF agent_executions
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- =============================================
-- Conversations and Messages
-- =============================================

CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    
    -- Conversation metadata
    title VARCHAR(255),
    summary TEXT,
    tags TEXT[] DEFAULT '{}',
    
    -- Channel information
    channel VARCHAR(50) DEFAULT 'web', -- web, api, telegram, whatsapp, email
    channel_id VARCHAR(255), -- External ID for the channel
    
    -- State
    is_active BOOLEAN DEFAULT TRUE,
    is_archived BOOLEAN DEFAULT FALSE,
    
    -- Metrics
    message_count INTEGER DEFAULT 0,
    total_tokens_used INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_message_at TIMESTAMPTZ,
    archived_at TIMESTAMPTZ,
    
    INDEX idx_conversation_workspace (workspace_id),
    INDEX idx_conversation_agent (agent_id),
    INDEX idx_conversation_user (user_id),
    INDEX idx_conversation_active (is_active),
    INDEX idx_conversation_last_message (last_message_at DESC)
);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    
    -- Message content
    role VARCHAR(20) NOT NULL, -- user, assistant, system, function
    content TEXT NOT NULL,
    
    -- Attachments
    attachments JSONB DEFAULT '[]',
    
    -- For function messages
    function_name VARCHAR(100),
    function_response JSONB,
    
    -- Token usage
    tokens_used INTEGER,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    
    -- Edit history
    edited_at TIMESTAMPTZ,
    edit_history JSONB DEFAULT '[]',
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    INDEX idx_message_conversation (conversation_id),
    INDEX idx_message_created (created_at),
    INDEX idx_message_role (role)
);

-- =============================================
-- Knowledge Base and Documents
-- =============================================

CREATE TABLE knowledge_bases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    -- Identity
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- Configuration
    embedding_model VARCHAR(100) DEFAULT 'text-embedding-ada-002',
    chunk_size INTEGER DEFAULT 512,
    chunk_overlap INTEGER DEFAULT 128,
    
    -- Vector store configuration
    vector_store_type VARCHAR(50) DEFAULT 'pinecone', -- pinecone, weaviate, qdrant
    vector_store_config JSONB DEFAULT '{}',
    
    -- Statistics
    document_count INTEGER DEFAULT 0,
    total_chunks INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    storage_size_bytes BIGINT DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_indexed_at TIMESTAMPTZ,
    
    INDEX idx_kb_workspace (workspace_id)
);

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    knowledge_base_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    
    -- Source information
    source_type VARCHAR(50) NOT NULL, -- file, url, api, manual
    source_url TEXT,
    source_metadata JSONB DEFAULT '{}',
    
    -- Document metadata
    title VARCHAR(500),
    author VARCHAR(255),
    content_type VARCHAR(100),
    language VARCHAR(10) DEFAULT 'en',
    
    -- Content
    raw_content TEXT,
    processed_content TEXT,
    summary TEXT,
    
    -- Processing status
    processing_status VARCHAR(50) DEFAULT 'pending',
    processing_error TEXT,
    processed_at TIMESTAMPTZ,
    
    -- Chunking information
    chunk_count INTEGER DEFAULT 0,
    token_count INTEGER DEFAULT 0,
    
    -- Deduplication
    content_hash VARCHAR(64) NOT NULL,
    
    -- Metadata
    tags TEXT[] DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    INDEX idx_doc_kb (knowledge_base_id),
    INDEX idx_doc_status (processing_status),
    INDEX idx_doc_hash (content_hash),
    INDEX idx_doc_created (created_at DESC)
);

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    
    -- Chunk information
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    chunk_tokens INTEGER,
    
    -- Vector information
    vector_id VARCHAR(255), -- ID in vector store
    embedding_model VARCHAR(100),
    embedded_at TIMESTAMPTZ,
    
    -- Metadata for retrieval
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    UNIQUE(document_id, chunk_index),
    INDEX idx_chunk_document (document_id),
    INDEX idx_chunk_vector (vector_id)
);

-- =============================================
-- Workflows and Automations
-- =============================================

CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    -- Identity
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    
    -- Workflow definition (JSON DSL)
    definition JSONB NOT NULL,
    
    -- Trigger configuration
    triggers JSONB DEFAULT '[]',
    
    -- Schedule (if scheduled workflow)
    schedule_cron VARCHAR(100),
    schedule_timezone VARCHAR(50) DEFAULT 'UTC',
    
    -- State
    is_active BOOLEAN DEFAULT TRUE,
    is_paused BOOLEAN DEFAULT FALSE,
    
    -- Version control
    version INTEGER DEFAULT 1,
    published_version INTEGER,
    
    -- Metadata
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_run_at TIMESTAMPTZ,
    
    INDEX idx_workflow_workspace (workspace_id),
    INDEX idx_workflow_active (is_active),
    INDEX idx_workflow_category (category)
);

CREATE TABLE workflow_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    
    -- Trigger information
    triggered_by VARCHAR(50) NOT NULL, -- manual, schedule, webhook, event
    trigger_metadata JSONB DEFAULT '{}',
    
    -- Execution context
    input_data JSONB DEFAULT '{}',
    output_data JSONB,
    
    -- State and status
    status VARCHAR(50) NOT NULL, -- pending, running, completed, failed, cancelled
    current_step VARCHAR(255),
    completed_steps JSONB DEFAULT '[]',
    
    -- Error handling
    error_message TEXT,
    error_step VARCHAR(255),
    
    -- Timing
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    execution_time_ms INTEGER,
    
    INDEX idx_workflow_run_workflow (workflow_id),
    INDEX idx_workflow_run_status (status),
    INDEX idx_workflow_run_started (started_at DESC)
);

-- =============================================
-- P2P Compute Network
-- =============================================

CREATE TABLE compute_nodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id VARCHAR(255) UNIQUE NOT NULL,
    owner_id UUID NOT NULL REFERENCES users(id),
    
    -- Node capabilities
    cpu_cores INTEGER NOT NULL,
    memory_gb INTEGER NOT NULL,
    gpu_count INTEGER DEFAULT 0,
    gpu_model VARCHAR(100),
    gpu_memory_gb INTEGER,
    
    -- Network information
    ip_address INET,
    port INTEGER,
    region VARCHAR(50),
    
    -- Availability
    availability_schedule JSONB DEFAULT '{}',
    is_available BOOLEAN DEFAULT FALSE,
    
    -- Performance metrics
    benchmark_score DECIMAL(10,2),
    average_job_time_ms INTEGER,
    success_rate DECIMAL(5,2) DEFAULT 100.00,
    
    -- Reputation and earnings
    reputation_score DECIMAL(3,2) DEFAULT 5.00,
    total_jobs_completed INTEGER DEFAULT 0,
    total_jobs_failed INTEGER DEFAULT 0,
    total_credits_earned DECIMAL(12,2) DEFAULT 0,
    total_compute_hours DECIMAL(12,2) DEFAULT 0,
    
    -- Status
    status VARCHAR(50) DEFAULT 'offline',
    last_heartbeat TIMESTAMPTZ,
    
    -- Metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    INDEX idx_compute_node_owner (owner_id),
    INDEX idx_compute_node_status (status),
    INDEX idx_compute_node_available (is_available),
    INDEX idx_compute_node_heartbeat (last_heartbeat)
);

CREATE TABLE compute_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    
    -- Job specification
    job_type VARCHAR(50) NOT NULL, -- training, inference, processing, analysis
    job_name VARCHAR(255),
    description TEXT,
    
    -- Requirements
    min_cpu_cores INTEGER DEFAULT 1,
    min_memory_gb INTEGER DEFAULT 4,
    requires_gpu BOOLEAN DEFAULT FALSE,
    min_gpu_memory_gb INTEGER,
    estimated_duration_minutes INTEGER,
    
    -- Job payload
    input_data_url TEXT,
    output_data_url TEXT,
    job_config JSONB NOT NULL,
    
    -- Assignment
    assigned_node_id UUID REFERENCES compute_nodes(id),
    
    -- Scheduling
    priority INTEGER DEFAULT 5,
    deadline_at TIMESTAMPTZ,
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending',
    progress_percentage INTEGER DEFAULT 0,
    status_message TEXT,
    
    -- Results
    result JSONB,
    result_metrics JSONB,
    
    -- Credits and billing
    credits_offered DECIMAL(10,2) NOT NULL,
    credits_paid DECIMAL(10,2),
    
    -- Retry logic
    max_retries INTEGER DEFAULT 3,
    retry_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    assigned_at TIMESTAMPTZ,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    failed_at TIMESTAMPTZ,
    
    INDEX idx_compute_job_workspace (workspace_id),
    INDEX idx_compute_job_status (status),
    INDEX idx_compute_job_priority (priority DESC, created_at ASC) WHERE status = 'pending',
    INDEX idx_compute_job_node (assigned_node_id),
    INDEX idx_compute_job_deadline (deadline_at) WHERE deadline_at IS NOT NULL
);

-- =============================================
-- Billing and Usage
-- =============================================

CREATE TABLE usage_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    workspace_id UUID REFERENCES workspaces(id),
    
    -- Usage type
    resource_type VARCHAR(50) NOT NULL, -- api_calls, tokens, storage, compute
    resource_name VARCHAR(100),
    
    -- Quantity
    quantity DECIMAL(20,6) NOT NULL,
    unit VARCHAR(20) NOT NULL, -- tokens, bytes, seconds, calls
    
    -- Cost calculation
    unit_price DECIMAL(10,6),
    total_cost DECIMAL(10,2),
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- Period
    period_start TIMESTAMPTZ NOT NULL,
    period_end TIMESTAMPTZ NOT NULL,
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    INDEX idx_usage_org (organization_id),
    INDEX idx_usage_workspace (workspace_id),
    INDEX idx_usage_period (period_start, period_end),
    INDEX idx_usage_type (resource_type)
) PARTITION BY RANGE (period_start);

-- Create monthly partitions for usage
CREATE TABLE usage_records_2025_01
    PARTITION OF usage_records
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- =============================================
-- Audit and Security
-- =============================================

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Actor
    user_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    ip_address INET,
    user_agent TEXT,
    
    -- Action
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    
    -- Details
    old_values JSONB,
    new_values JSONB,
    metadata JSONB DEFAULT '{}',
    
    -- Result
    status VARCHAR(20) NOT NULL, -- success, failure
    error_message TEXT,
    
    -- Timestamp
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    INDEX idx_audit_user (user_id),
    INDEX idx_audit_org (organization_id),
    INDEX idx_audit_action (action),
    INDEX idx_audit_resource (resource_type, resource_id),
    INDEX idx_audit_created (created_at DESC)
) PARTITION BY RANGE (created_at);

-- Create monthly partitions for audit logs
CREATE TABLE audit_logs_2025_01
    PARTITION OF audit_logs
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- =============================================
-- Functions and Triggers
-- =============================================

-- Update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update trigger to all tables with updated_at
DO $$
DECLARE
    t text;
BEGIN
    FOR t IN 
        SELECT table_name 
        FROM information_schema.columns 
        WHERE column_name = 'updated_at' 
        AND table_schema = 'public'
    LOOP
        EXECUTE format('
            CREATE TRIGGER update_%I_updated_at 
            BEFORE UPDATE ON %I 
            FOR EACH ROW 
            EXECUTE FUNCTION update_updated_at()',
            t, t);
    END LOOP;
END;
$$;

-- Soft delete function
CREATE OR REPLACE FUNCTION soft_delete()
RETURNS TRIGGER AS $$
BEGIN
    NEW.is_deleted = TRUE;
    NEW.deleted_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Archive old partitions
CREATE OR REPLACE FUNCTION archive_old_partitions()
RETURNS void AS $$
DECLARE
    partition_name text;
    archive_date date;
BEGIN
    archive_date := CURRENT_DATE - INTERVAL '90 days';
    
    FOR partition_name IN
        SELECT tablename 
        FROM pg_tables 
        WHERE tablename LIKE 'agent_executions_%' 
        OR tablename LIKE 'audit_logs_%'
        OR tablename LIKE 'usage_records_%'
    LOOP
        -- Move to archive schema or cold storage
        EXECUTE format('ALTER TABLE %I SET TABLESPACE archive_storage', partition_name);
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- Indexes for Performance
-- =============================================

-- Full-text search indexes
CREATE INDEX idx_agents_search ON agents 
    USING GIN (to_tsvector('english', name || ' ' || COALESCE(description, '')));

CREATE INDEX idx_documents_search ON documents 
    USING GIN (to_tsvector('english', title || ' ' || COALESCE(processed_content, '')));

-- JSONB indexes
CREATE INDEX idx_agents_capabilities ON agents USING GIN (capabilities);
CREATE INDEX idx_agents_tools ON agents USING GIN (tools);
CREATE INDEX idx_workflows_triggers ON workflows USING GIN (triggers);

-- Partial indexes for common queries
CREATE INDEX idx_active_agents ON agents (workspace_id, state) 
    WHERE state IN ('ready', 'running');

CREATE INDEX idx_pending_jobs ON compute_jobs (priority DESC, created_at ASC) 
    WHERE status = 'pending';

CREATE INDEX idx_available_nodes ON compute_nodes (is_available, benchmark_score DESC) 
    WHERE is_available = TRUE;

-- =============================================
-- Row Level Security (RLS)
-- =============================================

-- Enable RLS on sensitive tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE workspaces ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;

-- User can only see their own data
CREATE POLICY users_isolation ON users
    USING (id = current_setting('app.current_user_id')::uuid);

-- Workspace isolation
CREATE POLICY workspace_isolation ON agents
    USING (workspace_id IN (
        SELECT w.id FROM workspaces w
        JOIN organization_members om ON om.organization_id = w.organization_id
        WHERE om.user_id = current_setting('app.current_user_id')::uuid
    ));

-- =============================================
-- Materialized Views for Analytics
-- =============================================

CREATE MATERIALIZED VIEW agent_performance_stats AS
SELECT 
    a.id,
    a.name,
    a.workspace_id,
    COUNT(DISTINCT ae.id) as total_executions,
    AVG(ae.execution_time_ms) as avg_execution_time,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY ae.execution_time_ms) as median_execution_time,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY ae.execution_time_ms) as p95_execution_time,
    SUM(ae.total_tokens) as total_tokens_used,
    AVG(ae.total_tokens) as avg_tokens_per_execution,
    COUNT(CASE WHEN ae.status = 'completed' THEN 1 END)::float / 
        NULLIF(COUNT(*), 0) * 100 as success_rate,
    MAX(ae.started_at) as last_execution_at
FROM agents a
LEFT JOIN agent_executions ae ON ae.agent_id = a.id
WHERE ae.started_at >= NOW() - INTERVAL '30 days'
GROUP BY a.id, a.name, a.workspace_id;

CREATE INDEX idx_agent_perf_stats_workspace ON agent_performance_stats (workspace_id);

-- Refresh materialized view periodically
CREATE OR REPLACE FUNCTION refresh_agent_stats()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY agent_performance_stats;
END;
$$ LANGUAGE plpgsql;

-- Schedule refresh every hour
SELECT cron.schedule('refresh-agent-stats', '0 * * * *', 'SELECT refresh_agent_stats()');
```

## MongoDB Schema

### Collections and Document Structures

```javascript
// =============================================
// Agent Configurations Collection
// =============================================
db.createCollection("agent_configs", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["agentId", "version", "config"],
            properties: {
                agentId: {
                    bsonType: "string",
                    description: "UUID of the agent"
                },
                version: {
                    bsonType: "int",
                    minimum: 1
                },
                config: {
                    bsonType: "object",
                    properties: {
                        prompts: {
                            bsonType: "object",
                            properties: {
                                system: { bsonType: "string" },
                                examples: {
                                    bsonType: "array",
                                    items: {
                                        bsonType: "object",
                                        properties: {
                                            input: { bsonType: "string" },
                                            output: { bsonType: "string" }
                                        }
                                    }
                                }
                            }
                        },
                        tools: {
                            bsonType: "array",
                            items: {
                                bsonType: "object",
                                required: ["name", "type"],
                                properties: {
                                    name: { bsonType: "string" },
                                    type: { bsonType: "string" },
                                    description: { bsonType: "string" },
                                    parameters: { bsonType: "object" },
                                    implementation: { bsonType: "string" }
                                }
                            }
                        },
                        modelPreferences: {
                            bsonType: "array",
                            items: {
                                bsonType: "object",
                                properties: {
                                    task: { bsonType: "string" },
                                    model: { bsonType: "string" },
                                    provider: { bsonType: "string" },
                                    fallback: { bsonType: "string" }
                                }
                            }
                        },
                        memory: {
                            bsonType: "object",
                            properties: {
                                type: {
                                    enum: ["none", "conversation", "summary", "rag"],
                                    bsonType: "string"
                                },
                                maxTokens: { bsonType: "int" },
                                summaryStrategy: { bsonType: "string" },
                                vectorStore: { bsonType: "object" }
                            }
                        }
                    }
                },
                metadata: {
                    bsonType: "object"
                },
                createdAt: {
                    bsonType: "date"
                },
                createdBy: {
                    bsonType: "string"
                }
            }
        }
    }
});

// Indexes
db.agent_configs.createIndex({ "agentId": 1, "version": -1 });
db.agent_configs.createIndex({ "createdAt": -1 });

// =============================================
// Conversation History Collection
// =============================================
db.createCollection("conversation_history", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["conversationId", "messages"],
            properties: {
                conversationId: { bsonType: "string" },
                sessionId: { bsonType: "string" },
                agentId: { bsonType: "string" },
                userId: { bsonType: "string" },
                messages: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["id", "role", "content", "timestamp"],
                        properties: {
                            id: { bsonType: "string" },
                            role: {
                                enum: ["user", "assistant", "system", "function"],
                                bsonType: "string"
                            },
                            content: { bsonType: "string" },
                            attachments: {
                                bsonType: "array",
                                items: {
                                    bsonType: "object",
                                    properties: {
                                        type: { bsonType: "string" },
                                        url: { bsonType: "string" },
                                        mimeType: { bsonType: "string" },
                                        size: { bsonType: "int" }
                                    }
                                }
                            },
                            functionCall: {
                                bsonType: "object",
                                properties: {
                                    name: { bsonType: "string" },
                                    arguments: { bsonType: "object" },
                                    result: { bsonType: "object" }
                                }
                            },
                            metadata: {
                                bsonType: "object",
                                properties: {
                                    model: { bsonType: "string" },
                                    tokensUsed: { bsonType: "int" },
                                    processingTime: { bsonType: "int" },
                                    confidence: { bsonType: "double" }
                                }
                            },
                            timestamp: { bsonType: "date" }
                        }
                    }
                },
                summary: { bsonType: "string" },
                tags: {
                    bsonType: "array",
                    items: { bsonType: "string" }
                },
                sentiment: {
                    bsonType: "object",
                    properties: {
                        overall: { bsonType: "double" },
                        trend: { bsonType: "string" }
                    }
                },
                createdAt: { bsonType: "date" },
                lastActivityAt: { bsonType: "date" }
            }
        }
    },
    timeseries: {
        timeField: "lastActivityAt",
        metaField: "metadata",
        granularity: "hours"
    }
});

// Indexes
db.conversation_history.createIndex({ "conversationId": 1 });
db.conversation_history.createIndex({ "userId": 1, "lastActivityAt": -1 });
db.conversation_history.createIndex({ "agentId": 1, "lastActivityAt": -1 });
db.conversation_history.createIndex({ "tags": 1 });
db.conversation_history.createIndex({ "messages.timestamp": -1 });

// =============================================
// Knowledge Graph Nodes
// =============================================
db.createCollection("knowledge_nodes", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["nodeId", "labels", "properties"],
            properties: {
                nodeId: { bsonType: "string" },
                labels: {
                    bsonType: "array",
                    items: { bsonType: "string" }
                },
                properties: {
                    bsonType: "object"
                },
                embeddings: {
                    bsonType: "object",
                    properties: {
                        model: { bsonType: "string" },
                        vector: {
                            bsonType: "array",
                            items: { bsonType: "double" }
                        },
                        dimension: { bsonType: "int" },
                        generatedAt: { bsonType: "date" }
                    }
                },
                relationships: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["type", "targetId"],
                        properties: {
                            type: { bsonType: "string" },
                            targetId: { bsonType: "string" },
                            properties: { bsonType: "object" },
                            weight: { bsonType: "double" }
                        }
                    }
                },
                metadata: {
                    bsonType: "object",
                    properties: {
                        source: { bsonType: "string" },
                        confidence: { bsonType: "double" },
                        lastVerified: { bsonType: "date" },
                        version: { bsonType: "int" }
                    }
                },
                createdAt: { bsonType: "date" },
                updatedAt: { bsonType: "date" }
            }
        }
    }
});

// Indexes for graph traversal
db.knowledge_nodes.createIndex({ "nodeId": 1 });
db.knowledge_nodes.createIndex({ "labels": 1 });
db.knowledge_nodes.createIndex({ "relationships.targetId": 1 });
db.knowledge_nodes.createIndex({ "relationships.type": 1 });

// Vector search index (MongoDB Atlas)
db.knowledge_nodes.createSearchIndex({
    name: "vector_search",
    type: "vectorSearch",
    definition: {
        "fields": [{
            "type": "vector",
            "path": "embeddings.vector",
            "numDimensions": 1536,
            "similarity": "cosine"
        }]
    }
});

// =============================================
// Workflow Definitions
// =============================================
db.createCollection("workflow_definitions", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["workflowId", "name", "steps"],
            properties: {
                workflowId: { bsonType: "string" },
                name: { bsonType: "string" },
                description: { bsonType: "string" },
                version: { bsonType: "int" },
                steps: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        required: ["id", "type", "config"],
                        properties: {
                            id: { bsonType: "string" },
                            name: { bsonType: "string" },
                            type: {
                                enum: ["agent", "condition", "loop", "parallel", "webhook", "wait"],
                                bsonType: "string"
                            },
                            config: { bsonType: "object" },
                            inputs: {
                                bsonType: "array",
                                items: { bsonType: "string" }
                            },
                            outputs: {
                                bsonType: "array",
                                items: { bsonType: "string" }
                            },
                            errorHandling: {
                                bsonType: "object",
                                properties: {
                                    strategy: {
                                        enum: ["retry", "skip", "fail"],
                                        bsonType: "string"
                                    },
                                    maxRetries: { bsonType: "int" },
                                    retryDelay: { bsonType: "int" }
                                }
                            }
                        }
                    }
                },
                connections: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        properties: {
                            from: { bsonType: "string" },
                            to: { bsonType: "string" },
                            condition: { bsonType: "object" }
                        }
                    }
                },
                triggers: {
                    bsonType: "array",
                    items: {
                        bsonType: "object",
                        properties: {
                            type: {
                                enum: ["schedule", "webhook", "event", "manual"],
                                bsonType: "string"
                            },
                            config: { bsonType: "object" }
                        }
                    }
                },
                variables: {
                    bsonType: "object"
                },
                createdAt: { bsonType: "date" },
                updatedAt: { bsonType: "date" }
            }
        }
    }
});

// =============================================
// Aggregation Pipelines
// =============================================

// Agent usage analytics
db.agent_executions.aggregate([
    {
        $match: {
            createdAt: {
                $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
            }
        }
    },
    {
        $group: {
            _id: {
                agentId: "$agentId",
                day: { $dateToString: { format: "%Y-%m-%d", date: "$createdAt" } }
            },
            executions: { $sum: 1 },
            totalTokens: { $sum: "$tokensUsed" },
            avgResponseTime: { $avg: "$processingTime" },
            errors: {
                $sum: {
                    $cond: [{ $eq: ["$status", "error"] }, 1, 0]
                }
            }
        }
    },
    {
        $group: {
            _id: "$_id.agentId",
            dailyStats: {
                $push: {
                    date: "$_id.day",
                    executions: "$executions",
                    tokens: "$totalTokens",
                    avgResponseTime: "$avgResponseTime",
                    errorRate: {
                        $multiply: [
                            { $divide: ["$errors", "$executions"] },
                            100
                        ]
                    }
                }
            },
            totalExecutions: { $sum: "$executions" },
            totalTokens: { $sum: "$totalTokens" }
        }
    },
    {
        $out: "agent_analytics"
    }
]);
```

## Neo4j Graph Schema

### Node and Relationship Definitions

```cypher
// =============================================
// Node Definitions
// =============================================

// User Node
CREATE CONSTRAINT user_id_unique ON (u:User) ASSERT u.id IS UNIQUE;
CREATE INDEX user_email FOR (u:User) ON (u.email);

// Agent Node
CREATE CONSTRAINT agent_id_unique ON (a:Agent) ASSERT a.id IS UNIQUE;
CREATE INDEX agent_name FOR (a:Agent) ON (a.name);
CREATE INDEX agent_type FOR (a:Agent) ON (a.type);

// Document Node
CREATE CONSTRAINT doc_id_unique ON (d:Document) ASSERT d.id IS UNIQUE;
CREATE INDEX doc_title FOR (d:Document) ON (d.title);

// Concept Node (Knowledge Graph)
CREATE CONSTRAINT concept_id_unique ON (c:Concept) ASSERT c.id IS UNIQUE;
CREATE INDEX concept_name FOR (c:Concept) ON (c.name);

// Entity Node
CREATE CONSTRAINT entity_id_unique ON (e:Entity) ASSERT e.id IS UNIQUE;
CREATE INDEX entity_name FOR (e:Entity) ON (e.name);
CREATE INDEX entity_type FOR (e:Entity) ON (e.type);

// Topic Node
CREATE CONSTRAINT topic_id_unique ON (t:Topic) ASSERT t.id IS UNIQUE;
CREATE INDEX topic_name FOR (t:Topic) ON (t.name);

// =============================================
// Relationship Definitions
// =============================================

// User relationships
(:User)-[:OWNS]->(:Agent)
(:User)-[:CREATED]->(:Document)
(:User)-[:MEMBER_OF]->(:Organization)
(:User)-[:HAS_CONVERSATION]->(:Conversation)

// Agent relationships
(:Agent)-[:USES]->(:Model)
(:Agent)-[:HAS_CAPABILITY]->(:Capability)
(:Agent)-[:PROCESSES]->(:Document)
(:Agent)-[:RESPONDS_TO]->(:User)
(:Agent)-[:DEPENDS_ON]->(:Agent)

// Document relationships
(:Document)-[:CONTAINS]->(:Concept)
(:Document)-[:MENTIONS]->(:Entity)
(:Document)-[:RELATES_TO]->(:Topic)
(:Document)-[:REFERENCES]->(:Document)
(:Document)-[:CONTRADICTS]->(:Document)

// Knowledge relationships
(:Concept)-[:IS_A]->(:Concept)
(:Concept)-[:PART_OF]->(:Concept)
(:Concept)-[:RELATED_TO {weight: 0.8}]->(:Concept)
(:Entity)-[:LOCATED_IN]->(:Location)
(:Entity)-[:WORKS_FOR]->(:Organization)

// =============================================
// Graph Algorithms
// =============================================

// PageRank for important concepts
CALL gds.pageRank.stream('knowledge-graph')
YIELD nodeId, score
MATCH (n) WHERE id(n) = nodeId
SET n.importance = score;

// Community detection for topic clustering
CALL gds.louvain.stream('knowledge-graph')
YIELD nodeId, communityId
MATCH (n) WHERE id(n) = nodeId
SET n.community = communityId;

// Similarity for document recommendations
CALL gds.nodeSimilarity.stream('document-graph')
YIELD node1, node2, similarity
WHERE similarity > 0.8
MATCH (d1:Document), (d2:Document)
WHERE id(d1) = node1 AND id(d2) = node2
CREATE (d1)-[:SIMILAR_TO {score: similarity}]->(d2);

// =============================================
// Complex Queries
// =============================================

// Find knowledge paths between concepts
MATCH path = shortestPath(
    (c1:Concept {name: $concept1})-[*..5]-(c2:Concept {name: $concept2})
)
RETURN path;

// Get agent collaboration network
MATCH (a1:Agent)-[:DEPENDS_ON*1..3]-(a2:Agent)
WHERE a1.workspace_id = $workspaceId
RETURN a1, a2, count(*) as collaborations
ORDER BY collaborations DESC;

// Knowledge graph expansion
MATCH (d:Document {id: $documentId})
OPTIONAL MATCH (d)-[:CONTAINS]->(c:Concept)
OPTIONAL MATCH (c)-[:RELATED_TO*1..2]-(related:Concept)
OPTIONAL MATCH (d)-[:MENTIONS]->(e:Entity)
RETURN d, collect(DISTINCT c) as concepts, 
       collect(DISTINCT related) as relatedConcepts,
       collect(DISTINCT e) as entities;
```

---

*This schema specification is version controlled and requires approval for changes.*