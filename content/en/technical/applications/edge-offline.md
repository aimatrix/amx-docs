---
title: "Edge & Offline Components"
description: "Distributed edge computing and offline-capable components featuring SQLite local storage, PostgreSQL + Git workspace management, intelligent sync mechanisms, and advanced conflict resolution"
weight: 6
date: 2025-08-23
toc: true
tags: ["edge", "offline", "distributed", "sqlite", "postgresql", "git", "sync", "conflict-resolution"]
---

# AIMatrix Edge & Offline Components

## Distributed Intelligence at the Edge

AIMatrix Edge & Offline Components enable truly distributed AI operations, bringing intelligent processing capabilities to edge environments while maintaining seamless synchronization with cloud infrastructure. These components ensure continuous operation regardless of network connectivity, with intelligent local storage, workspace management, and conflict resolution mechanisms.

## Edge Computing Philosophy

Our edge architecture is built on four fundamental principles:

### 🌐 **Edge-First Design**
Intelligence deployed where data is generated, minimizing latency and bandwidth usage

### 🔄 **Autonomous Operation**
Full functionality without constant cloud connectivity, with intelligent local decision-making

### 🔄 **Intelligent Synchronization**
Smart sync mechanisms that handle conflicts, prioritize critical data, and optimize bandwidth

### 🏗️ **Elastic Scalability**
Seamless scaling from single edge nodes to distributed edge clusters

## Architecture Overview

```mermaid
graph TB
    subgraph "Edge Node"
        subgraph "Local Storage Layer"
            SQLITE[SQLite Database]
            FILES[File System Storage]
            GIT[Git Repository]
            PGLOCAL[PostgreSQL Local]
        end
        
        subgraph "Processing Layer"
            AI_ENGINE[Local AI Engine]
            WORKFLOW[Workflow Processor]
            AGENT_MGR[Agent Manager]
            CACHE_MGR[Cache Manager]
        end
        
        subgraph "Sync Layer"
            SYNC_ENGINE[Sync Engine]
            CONFLICT_RES[Conflict Resolver]
            QUEUE_MGR[Queue Manager]
            PRIORITY_MGR[Priority Manager]
        end
    end
    
    subgraph "Cloud Infrastructure"
        SUPABASE[Supabase Backend]
        CDN[Content Delivery]
        BACKUP[Backup Storage]
        ANALYTICS[Analytics Engine]
    end
    
    subgraph "Network Layer"
        LB[Load Balancer]
        MESH[Service Mesh]
        VPN[Secure VPN]
        WAN[WAN Optimization]
    end
    
    Local Storage Layer --> Processing Layer
    Processing Layer --> Sync Layer
    
    Sync Layer --> Network Layer
    Network Layer --> Cloud Infrastructure
    
    Cloud Infrastructure --> CDN
    CDN --> Edge Node
```

## SQLite Local Storage

### Optimized Database Schema
```sql
-- SQLite schema optimized for edge computing
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 10000;
PRAGMA temp_store = memory;
PRAGMA mmap_size = 268435456; -- 256MB

-- Core tables for edge operations
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    status TEXT DEFAULT 'inactive',
    config TEXT, -- JSON configuration
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_sync DATETIME,
    sync_status TEXT DEFAULT 'pending', -- pending, synced, conflict, error
    version INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS workflows (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    definition TEXT, -- JSON workflow definition
    status TEXT DEFAULT 'draft',
    agent_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_execution DATETIME,
    execution_count INTEGER DEFAULT 0,
    sync_status TEXT DEFAULT 'pending',
    version INTEGER DEFAULT 1,
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);

CREATE TABLE IF NOT EXISTS executions (
    id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    status TEXT DEFAULT 'queued',
    input_data TEXT, -- JSON input
    output_data TEXT, -- JSON output
    error_message TEXT,
    started_at DATETIME,
    completed_at DATETIME,
    duration_ms INTEGER,
    resource_usage TEXT, -- JSON metrics
    sync_status TEXT DEFAULT 'pending',
    FOREIGN KEY (workflow_id) REFERENCES workflows(id)
);

CREATE TABLE IF NOT EXISTS sync_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    operation TEXT NOT NULL, -- INSERT, UPDATE, DELETE
    data TEXT, -- JSON data
    priority INTEGER DEFAULT 5, -- 1-10, higher is more important
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 5,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_attempt DATETIME,
    error_message TEXT,
    status TEXT DEFAULT 'pending' -- pending, processing, completed, failed
);

CREATE TABLE IF NOT EXISTS conflict_resolution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    record_id TEXT NOT NULL,
    local_version INTEGER,
    remote_version INTEGER,
    local_data TEXT, -- JSON
    remote_data TEXT, -- JSON
    resolution_strategy TEXT, -- auto, manual, local_wins, remote_wins
    resolved_data TEXT, -- JSON
    resolved_at DATETIME,
    resolved_by TEXT, -- system, user_id
    status TEXT DEFAULT 'pending' -- pending, resolved, escalated
);

-- Performance indexes
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_sync_status ON agents(sync_status);
CREATE INDEX IF NOT EXISTS idx_workflows_agent_id ON workflows(agent_id);
CREATE INDEX IF NOT EXISTS idx_executions_workflow_id ON executions(workflow_id);
CREATE INDEX IF NOT EXISTS idx_executions_status ON executions(status);
CREATE INDEX IF NOT EXISTS idx_sync_queue_status ON sync_queue(status);
CREATE INDEX IF NOT EXISTS idx_sync_queue_priority ON sync_queue(priority DESC);
CREATE INDEX IF NOT EXISTS idx_conflict_status ON conflict_resolution(status);

-- Triggers for automatic timestamp updates
CREATE TRIGGER IF NOT EXISTS update_agents_timestamp 
    AFTER UPDATE ON agents
BEGIN
    UPDATE agents SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_workflows_timestamp 
    AFTER UPDATE ON workflows
BEGIN
    UPDATE workflows SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Automatic sync queue population
CREATE TRIGGER IF NOT EXISTS agents_sync_trigger 
    AFTER INSERT OR UPDATE ON agents
    WHEN NEW.sync_status = 'pending'
BEGIN
    INSERT INTO sync_queue (table_name, record_id, operation, data, priority)
    VALUES ('agents', NEW.id, 
           CASE WHEN OLD.id IS NULL THEN 'INSERT' ELSE 'UPDATE' END,
           json_object(
               'id', NEW.id,
               'name', NEW.name,
               'type', NEW.type,
               'status', NEW.status,
               'config', NEW.config,
               'version', NEW.version
           ),
           CASE WHEN NEW.status = 'critical' THEN 10 ELSE 5 END
    );
END;

-- Views for common queries
CREATE VIEW IF NOT EXISTS active_agents AS
SELECT * FROM agents 
WHERE status IN ('active', 'running', 'processing')
ORDER BY updated_at DESC;

CREATE VIEW IF NOT EXISTS pending_sync AS
SELECT table_name, record_id, operation, priority, created_at
FROM sync_queue 
WHERE status = 'pending'
ORDER BY priority DESC, created_at ASC;

CREATE VIEW IF NOT EXISTS conflict_summary AS
SELECT 
    table_name,
    COUNT(*) as conflict_count,
    MIN(created_at) as oldest_conflict,
    MAX(created_at) as newest_conflict
FROM conflict_resolution 
WHERE status = 'pending'
GROUP BY table_name;
```

### SQLite Performance Optimization
```python
# Python SQLite optimization and connection management
import sqlite3
import json
import threading
import time
from contextlib import contextmanager
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import logging

class SQLiteManager:
    def __init__(self, db_path: Path, pool_size: int = 5):
        self.db_path = db_path
        self.pool_size = pool_size
        self._connection_pool = []
        self._pool_lock = threading.Lock()
        self._local = threading.local()
        
        # Create database and tables
        self._initialize_database()
        
        # Start background optimization
        self._start_optimization_thread()
    
    def _initialize_database(self):
        """Initialize database with optimized settings"""
        with self._get_connection() as conn:
            # Apply performance optimizations
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA synchronous = NORMAL") 
            conn.execute("PRAGMA cache_size = 10000")
            conn.execute("PRAGMA temp_store = MEMORY")
            conn.execute("PRAGMA mmap_size = 268435456")  # 256MB
            conn.execute("PRAGMA page_size = 4096")
            conn.execute("PRAGMA auto_vacuum = INCREMENTAL")
            
            # Enable foreign keys
            conn.execute("PRAGMA foreign_keys = ON")
            
            # Load schema from file or create tables
            self._create_tables(conn)
    
    @contextmanager
    def _get_connection(self):
        """Get connection from pool or create new one"""
        conn = None
        try:
            with self._pool_lock:
                if self._connection_pool:
                    conn = self._connection_pool.pop()
                else:
                    conn = sqlite3.connect(
                        str(self.db_path),
                        timeout=30.0,
                        check_same_thread=False
                    )
                    conn.row_factory = sqlite3.Row
            
            yield conn
            
        finally:
            if conn:
                with self._pool_lock:
                    if len(self._connection_pool) < self.pool_size:
                        self._connection_pool.append(conn)
                    else:
                        conn.close()
    
    def insert_agent(self, agent_data: Dict[str, Any]) -> str:
        """Insert new agent with automatic sync queue entry"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT INTO agents (id, name, type, status, config, version)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    agent_data['id'],
                    agent_data['name'],
                    agent_data['type'],
                    agent_data.get('status', 'inactive'),
                    json.dumps(agent_data.get('config', {})),
                    agent_data.get('version', 1)
                ))
                
                conn.commit()
                return agent_data['id']
                
            except sqlite3.IntegrityError as e:
                conn.rollback()
                raise Exception(f"Agent with ID {agent_data['id']} already exists")
    
    def update_agent(self, agent_id: str, updates: Dict[str, Any]) -> bool:
        """Update agent with version control and conflict detection"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                # Get current version
                cursor.execute("SELECT version FROM agents WHERE id = ?", (agent_id,))
                result = cursor.fetchone()
                
                if not result:
                    return False
                
                current_version = result['version']
                expected_version = updates.get('expected_version', current_version)
                
                if current_version != expected_version:
                    # Version conflict detected
                    self._create_conflict_record(
                        conn, 'agents', agent_id, 
                        expected_version, current_version,
                        updates
                    )
                    return False
                
                # Build update query
                set_clauses = []
                values = []
                
                for key, value in updates.items():
                    if key in ['id', 'expected_version']:
                        continue
                    
                    if key == 'config' and isinstance(value, dict):
                        value = json.dumps(value)
                    
                    set_clauses.append(f"{key} = ?")
                    values.append(value)
                
                set_clauses.append("version = version + 1")
                set_clauses.append("sync_status = 'pending'")
                
                values.append(agent_id)
                
                cursor.execute(f"""
                    UPDATE agents 
                    SET {', '.join(set_clauses)}
                    WHERE id = ?
                """, values)
                
                conn.commit()
                return cursor.rowcount > 0
                
            except Exception as e:
                conn.rollback()
                raise
    
    def get_agents(self, 
                  status: Optional[str] = None, 
                  limit: Optional[int] = None,
                  offset: int = 0) -> List[Dict[str, Any]]:
        """Get agents with filtering and pagination"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM agents"
            params = []
            
            if status:
                query += " WHERE status = ?"
                params.append(status)
            
            query += " ORDER BY updated_at DESC"
            
            if limit:
                query += " LIMIT ? OFFSET ?"
                params.extend([limit, offset])
            
            cursor.execute(query, params)
            
            agents = []
            for row in cursor.fetchall():
                agent = dict(row)
                if agent['config']:
                    agent['config'] = json.loads(agent['config'])
                agents.append(agent)
            
            return agents
    
    def get_sync_queue(self, status: str = 'pending', limit: int = 100) -> List[Dict[str, Any]]:
        """Get items from sync queue ordered by priority"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM sync_queue 
                WHERE status = ?
                ORDER BY priority DESC, created_at ASC
                LIMIT ?
            """, (status, limit))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_sync_completed(self, sync_id: int) -> bool:
        """Mark sync queue item as completed"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE sync_queue 
                SET status = 'completed', last_attempt = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (sync_id,))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def mark_sync_failed(self, sync_id: int, error_message: str) -> bool:
        """Mark sync queue item as failed and increment attempts"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE sync_queue 
                SET attempts = attempts + 1,
                    last_attempt = CURRENT_TIMESTAMP,
                    error_message = ?,
                    status = CASE 
                        WHEN attempts + 1 >= max_attempts THEN 'failed'
                        ELSE 'pending'
                    END
                WHERE id = ?
            """, (error_message, sync_id))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def _create_conflict_record(self, conn, table_name: str, record_id: str,
                              local_version: int, remote_version: int, 
                              local_data: Dict[str, Any]):
        """Create conflict resolution record"""
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conflict_resolution 
            (table_name, record_id, local_version, remote_version, local_data, status)
            VALUES (?, ?, ?, ?, ?, 'pending')
        """, (table_name, record_id, local_version, remote_version, json.dumps(local_data)))
    
    def get_conflicts(self, status: str = 'pending') -> List[Dict[str, Any]]:
        """Get unresolved conflicts"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM conflict_resolution 
                WHERE status = ?
                ORDER BY created_at ASC
            """, (status,))
            
            conflicts = []
            for row in cursor.fetchall():
                conflict = dict(row)
                if conflict['local_data']:
                    conflict['local_data'] = json.loads(conflict['local_data'])
                if conflict['remote_data']:
                    conflict['remote_data'] = json.loads(conflict['remote_data'])
                if conflict['resolved_data']:
                    conflict['resolved_data'] = json.loads(conflict['resolved_data'])
                conflicts.append(conflict)
            
            return conflicts
    
    def resolve_conflict(self, conflict_id: int, resolution_data: Dict[str, Any],
                        strategy: str = 'manual') -> bool:
        """Resolve a conflict with specified resolution"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    UPDATE conflict_resolution 
                    SET resolved_data = ?,
                        resolution_strategy = ?,
                        resolved_at = CURRENT_TIMESTAMP,
                        status = 'resolved'
                    WHERE id = ?
                """, (json.dumps(resolution_data), strategy, conflict_id))
                
                conn.commit()
                return cursor.rowcount > 0
                
            except Exception as e:
                conn.rollback()
                raise
    
    def _start_optimization_thread(self):
        """Start background optimization thread"""
        def optimization_worker():
            while True:
                try:
                    self._run_maintenance()
                    time.sleep(300)  # Run every 5 minutes
                except Exception as e:
                    logging.error(f"SQLite optimization error: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=optimization_worker, daemon=True)
        thread.start()
    
    def _run_maintenance(self):
        """Run database maintenance operations"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Analyze query performance
            cursor.execute("ANALYZE")
            
            # Clean up old completed sync queue entries
            cursor.execute("""
                DELETE FROM sync_queue 
                WHERE status = 'completed' 
                AND created_at < datetime('now', '-7 days')
            """)
            
            # Clean up old resolved conflicts
            cursor.execute("""
                DELETE FROM conflict_resolution 
                WHERE status = 'resolved' 
                AND resolved_at < datetime('now', '-30 days')
            """)
            
            # Incremental vacuum
            cursor.execute("PRAGMA incremental_vacuum(1000)")
            
            conn.commit()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics and health information"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Table counts
            cursor.execute("SELECT COUNT(*) FROM agents")
            stats['total_agents'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM workflows")
            stats['total_workflows'] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM executions")
            stats['total_executions'] = cursor.fetchone()[0]
            
            # Sync queue statistics
            cursor.execute("SELECT status, COUNT(*) FROM sync_queue GROUP BY status")
            stats['sync_queue'] = dict(cursor.fetchall())
            
            # Conflict statistics
            cursor.execute("SELECT status, COUNT(*) FROM conflict_resolution GROUP BY status")
            stats['conflicts'] = dict(cursor.fetchall())
            
            # Database size information
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            stats['database_size_mb'] = (page_count * page_size) / (1024 * 1024)
            
            return stats
```

## File System Persistence

### Intelligent File Management
```rust
// Rust implementation for high-performance file system operations
use std::path::{Path, PathBuf};
use std::collections::HashMap;
use std::fs::{self, File, OpenOptions};
use std::io::{self, Read, Write, BufReader, BufWriter};
use std::time::{SystemTime, UNIX_EPOCH};
use tokio::fs as tokio_fs;
use serde::{Serialize, Deserialize};
use blake3;
use lz4_flex;
use walkdir::WalkDir;

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct FileMetadata {
    pub path: PathBuf,
    pub size: u64,
    pub modified: u64,
    pub hash: String,
    pub compressed: bool,
    pub encrypted: bool,
    pub sync_status: SyncStatus,
    pub priority: u8,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
pub enum SyncStatus {
    Synced,
    Pending,
    Conflict,
    Error(String),
}

pub struct FileSystemManager {
    root_path: PathBuf,
    metadata_cache: HashMap<PathBuf, FileMetadata>,
    compression_enabled: bool,
    encryption_enabled: bool,
    max_file_size: u64,
}

impl FileSystemManager {
    pub fn new(root_path: PathBuf) -> io::Result<Self> {
        if !root_path.exists() {
            fs::create_dir_all(&root_path)?;
        }
        
        let mut manager = Self {
            root_path,
            metadata_cache: HashMap::new(),
            compression_enabled: true,
            encryption_enabled: false,
            max_file_size: 100 * 1024 * 1024, // 100MB
        };
        
        manager.load_metadata_cache()?;
        Ok(manager)
    }
    
    pub async fn store_file(&mut self, 
                           relative_path: &Path, 
                           data: &[u8], 
                           priority: u8) -> io::Result<FileMetadata> {
        
        let full_path = self.root_path.join(relative_path);
        
        // Create parent directories
        if let Some(parent) = full_path.parent() {
            tokio_fs::create_dir_all(parent).await?;
        }
        
        // Check file size limits
        if data.len() as u64 > self.max_file_size {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                format!("File too large: {} bytes", data.len())
            ));
        }
        
        // Calculate hash
        let hash = blake3::hash(data).to_string();
        
        // Prepare data for storage
        let storage_data = if self.compression_enabled && data.len() > 1024 {
            // Compress data
            let compressed = lz4_flex::compress_prepend_size(data);
            if compressed.len() < data.len() {
                (compressed, true)
            } else {
                (data.to_vec(), false)
            }
        } else {
            (data.to_vec(), false)
        };
        
        // Write to file
        tokio_fs::write(&full_path, &storage_data.0).await?;
        
        // Create metadata
        let metadata = FileMetadata {
            path: relative_path.to_path_buf(),
            size: data.len() as u64,
            modified: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs(),
            hash,
            compressed: storage_data.1,
            encrypted: false, // TODO: implement encryption
            sync_status: SyncStatus::Pending,
            priority,
        };
        
        // Update cache
        self.metadata_cache.insert(relative_path.to_path_buf(), metadata.clone());
        self.save_metadata_cache()?;
        
        Ok(metadata)
    }
    
    pub async fn load_file(&self, relative_path: &Path) -> io::Result<Vec<u8>> {
        let full_path = self.root_path.join(relative_path);
        
        if !full_path.exists() {
            return Err(io::Error::new(
                io::ErrorKind::NotFound,
                "File not found"
            ));
        }
        
        let data = tokio_fs::read(&full_path).await?;
        
        // Check if file is compressed
        if let Some(metadata) = self.metadata_cache.get(relative_path) {
            if metadata.compressed {
                // Decompress data
                match lz4_flex::decompress_size_prepended(&data) {
                    Ok(decompressed) => return Ok(decompressed),
                    Err(e) => {
                        eprintln!("Decompression failed: {}", e);
                        // Fall through to return raw data
                    }
                }
            }
        }
        
        Ok(data)
    }
    
    pub fn get_pending_sync_files(&self, max_count: usize) -> Vec<FileMetadata> {
        let mut pending_files: Vec<_> = self.metadata_cache
            .values()
            .filter(|meta| matches!(meta.sync_status, SyncStatus::Pending))
            .cloned()
            .collect();
        
        // Sort by priority (highest first), then by modification time
        pending_files.sort_by(|a, b| {
            b.priority.cmp(&a.priority)
                .then(b.modified.cmp(&a.modified))
        });
        
        pending_files.into_iter().take(max_count).collect()
    }
    
    pub fn mark_synced(&mut self, relative_path: &Path) -> io::Result<()> {
        if let Some(metadata) = self.metadata_cache.get_mut(relative_path) {
            metadata.sync_status = SyncStatus::Synced;
            self.save_metadata_cache()?;
        }
        Ok(())
    }
    
    pub fn mark_conflict(&mut self, relative_path: &Path, error: String) -> io::Result<()> {
        if let Some(metadata) = self.metadata_cache.get_mut(relative_path) {
            metadata.sync_status = SyncStatus::Conflict;
            self.save_metadata_cache()?;
        }
        Ok(())
    }
    
    pub async fn cleanup_old_files(&mut self, max_age_days: u64) -> io::Result<u64> {
        let cutoff_time = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs() - (max_age_days * 24 * 3600);
        
        let mut cleaned_size = 0u64;
        let mut to_remove = Vec::new();
        
        for (path, metadata) in &self.metadata_cache {
            if metadata.modified < cutoff_time && 
               matches!(metadata.sync_status, SyncStatus::Synced) {
                
                let full_path = self.root_path.join(path);
                
                if full_path.exists() {
                    let file_size = tokio_fs::metadata(&full_path).await?.len();
                    tokio_fs::remove_file(&full_path).await?;
                    cleaned_size += file_size;
                    to_remove.push(path.clone());
                }
            }
        }
        
        // Remove from cache
        for path in to_remove {
            self.metadata_cache.remove(&path);
        }
        
        self.save_metadata_cache()?;
        Ok(cleaned_size)
    }
    
    pub fn get_storage_statistics(&self) -> io::Result<StorageStatistics> {
        let mut stats = StorageStatistics::default();
        
        // Walk through all files in root directory
        for entry in WalkDir::new(&self.root_path) {
            let entry = entry?;
            
            if entry.file_type().is_file() {
                let metadata = entry.metadata()?;
                stats.total_files += 1;
                stats.total_size += metadata.len();
                
                if let Some(relative_path) = entry.path().strip_prefix(&self.root_path).ok() {
                    if let Some(file_meta) = self.metadata_cache.get(relative_path) {
                        match file_meta.sync_status {
                            SyncStatus::Synced => stats.synced_files += 1,
                            SyncStatus::Pending => stats.pending_files += 1,
                            SyncStatus::Conflict => stats.conflict_files += 1,
                            SyncStatus::Error(_) => stats.error_files += 1,
                        }
                        
                        if file_meta.compressed {
                            stats.compressed_files += 1;
                        }
                    }
                }
            }
        }
        
        Ok(stats)
    }
    
    fn load_metadata_cache(&mut self) -> io::Result<()> {
        let cache_path = self.root_path.join(".metadata_cache.json");
        
        if cache_path.exists() {
            let data = fs::read_to_string(&cache_path)?;
            
            match serde_json::from_str::<HashMap<PathBuf, FileMetadata>>(&data) {
                Ok(cache) => {
                    self.metadata_cache = cache;
                }
                Err(e) => {
                    eprintln!("Failed to load metadata cache: {}", e);
                    // Continue with empty cache
                }
            }
        }
        
        Ok(())
    }
    
    fn save_metadata_cache(&self) -> io::Result<()> {
        let cache_path = self.root_path.join(".metadata_cache.json");
        let data = serde_json::to_string_pretty(&self.metadata_cache)?;
        fs::write(&cache_path, data)?;
        Ok(())
    }
}

#[derive(Default, Debug)]
pub struct StorageStatistics {
    pub total_files: u64,
    pub total_size: u64,
    pub synced_files: u64,
    pub pending_files: u64,
    pub conflict_files: u64,
    pub error_files: u64,
    pub compressed_files: u64,
}

// Async file operations with retry logic
pub struct AsyncFileOperations;

impl AsyncFileOperations {
    pub async fn copy_with_retry(src: &Path, dst: &Path, max_retries: u32) -> io::Result<()> {
        let mut attempts = 0;
        
        loop {
            match tokio_fs::copy(src, dst).await {
                Ok(_) => return Ok(()),
                Err(e) => {
                    attempts += 1;
                    
                    if attempts >= max_retries {
                        return Err(e);
                    }
                    
                    // Exponential backoff
                    let delay = std::time::Duration::from_millis(100 * (1 << attempts));
                    tokio::time::sleep(delay).await;
                }
            }
        }
    }
    
    pub async fn atomic_write(path: &Path, data: &[u8]) -> io::Result<()> {
        let temp_path = path.with_extension("tmp");
        
        // Write to temporary file first
        tokio_fs::write(&temp_path, data).await?;
        
        // Atomically rename to target
        tokio_fs::rename(&temp_path, path).await?;
        
        Ok(())
    }
    
    pub async fn safe_delete(path: &Path) -> io::Result<()> {
        if path.exists() {
            // Move to trash directory first
            let trash_dir = path.parent().unwrap().join(".trash");
            tokio_fs::create_dir_all(&trash_dir).await?;
            
            let timestamp = SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs();
            
            let trash_path = trash_dir.join(format!("{}_{}", 
                path.file_name().unwrap().to_string_lossy(), 
                timestamp));
            
            tokio_fs::rename(path, &trash_path).await?;
        }
        
        Ok(())
    }
}
```

## PostgreSQL + Git Workspace Management

### Git-Based Version Control
```go
// Go implementation for Git workspace management
package workspace

import (
    "fmt"
    "os"
    "path/filepath"
    "time"
    "database/sql"
    "encoding/json"
    
    "github.com/go-git/go-git/v5"
    "github.com/go-git/go-git/v5/plumbing/object"
    "github.com/go-git/go-git/v5/storage/filesystem"
    "github.com/go-git/go-billy/v5/osfs"
    _ "github.com/lib/pq"
)

type WorkspaceManager struct {
    rootPath    string
    repository  *git.Repository
    database    *sql.DB
    config      WorkspaceConfig
}

type WorkspaceConfig struct {
    RemoteURL      string `json:"remote_url"`
    Branch         string `json:"branch"`
    AutoCommit     bool   `json:"auto_commit"`
    CommitInterval int    `json:"commit_interval"` // minutes
    SyncInterval   int    `json:"sync_interval"`   // minutes
    ConflictStrategy string `json:"conflict_strategy"` // auto, manual, local, remote
}

type WorkspaceItem struct {
    ID          string    `json:"id"`
    Path        string    `json:"path"`
    Type        string    `json:"type"` // agent, workflow, config
    Content     string    `json:"content"`
    Version     int       `json:"version"`
    ModifiedAt  time.Time `json:"modified_at"`
    ModifiedBy  string    `json:"modified_by"`
    SyncStatus  string    `json:"sync_status"`
    ConflictID  *string   `json:"conflict_id,omitempty"`
}

func NewWorkspaceManager(rootPath string, config WorkspaceConfig) (*WorkspaceManager, error) {
    // Initialize or open Git repository
    repo, err := initializeRepository(rootPath, config.RemoteURL)
    if err != nil {
        return nil, fmt.Errorf("failed to initialize repository: %v", err)
    }
    
    // Connect to local PostgreSQL database
    db, err := sql.Open("postgres", "host=localhost dbname=amx_workspace sslmode=disable")
    if err != nil {
        return nil, fmt.Errorf("failed to connect to database: %v", err)
    }
    
    wm := &WorkspaceManager{
        rootPath:   rootPath,
        repository: repo,
        database:   db,
        config:     config,
    }
    
    // Initialize database schema
    if err := wm.initializeDatabase(); err != nil {
        return nil, fmt.Errorf("failed to initialize database: %v", err)
    }
    
    // Start background sync if enabled
    if config.AutoCommit {
        go wm.startAutoCommit()
    }
    
    return wm, nil
}

func initializeRepository(rootPath, remoteURL string) (*git.Repository, error) {
    gitPath := filepath.Join(rootPath, ".git")
    
    // Check if repository already exists
    if _, err := os.Stat(gitPath); err == nil {
        // Open existing repository
        fs := osfs.New(rootPath)
        storage := filesystem.NewStorage(fs, nil)
        return git.Open(storage, fs)
    }
    
    // Create new repository
    if err := os.MkdirAll(rootPath, 0755); err != nil {
        return nil, err
    }
    
    fs := osfs.New(rootPath)
    storage := filesystem.NewStorage(fs, nil)
    
    repo, err := git.Init(storage, fs)
    if err != nil {
        return nil, err
    }
    
    // Add remote if specified
    if remoteURL != "" {
        _, err = repo.CreateRemote(&config.RemoteConfig{
            Name: "origin",
            URLs: []string{remoteURL},
        })
        if err != nil {
            return nil, err
        }
    }
    
    return repo, nil
}

func (wm *WorkspaceManager) initializeDatabase() error {
    schema := `
    CREATE TABLE IF NOT EXISTS workspace_items (
        id VARCHAR(255) PRIMARY KEY,
        path VARCHAR(500) NOT NULL,
        type VARCHAR(50) NOT NULL,
        content TEXT,
        version INTEGER DEFAULT 1,
        modified_at TIMESTAMP DEFAULT NOW(),
        modified_by VARCHAR(255),
        sync_status VARCHAR(50) DEFAULT 'pending',
        conflict_id VARCHAR(255)
    );
    
    CREATE TABLE IF NOT EXISTS workspace_conflicts (
        id VARCHAR(255) PRIMARY KEY,
        item_id VARCHAR(255) REFERENCES workspace_items(id),
        local_content TEXT,
        remote_content TEXT,
        base_content TEXT,
        resolved_content TEXT,
        resolution_strategy VARCHAR(50),
        resolved_at TIMESTAMP,
        resolved_by VARCHAR(255),
        status VARCHAR(50) DEFAULT 'pending'
    );
    
    CREATE TABLE IF NOT EXISTS workspace_sync_log (
        id SERIAL PRIMARY KEY,
        operation VARCHAR(50) NOT NULL,
        item_id VARCHAR(255),
        commit_hash VARCHAR(255),
        status VARCHAR(50),
        error_message TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    
    CREATE INDEX IF NOT EXISTS idx_workspace_items_type ON workspace_items(type);
    CREATE INDEX IF NOT EXISTS idx_workspace_items_sync_status ON workspace_items(sync_status);
    CREATE INDEX IF NOT EXISTS idx_workspace_conflicts_status ON workspace_conflicts(status);
    `
    
    _, err := wm.database.Exec(schema)
    return err
}

func (wm *WorkspaceManager) CreateItem(item WorkspaceItem) error {
    // Write file to filesystem
    fullPath := filepath.Join(wm.rootPath, item.Path)
    
    // Create directory if it doesn't exist
    if err := os.MkdirAll(filepath.Dir(fullPath), 0755); err != nil {
        return err
    }
    
    // Write content to file
    if err := os.WriteFile(fullPath, []byte(item.Content), 0644); err != nil {
        return err
    }
    
    // Insert into database
    _, err := wm.database.Exec(`
        INSERT INTO workspace_items (id, path, type, content, modified_by, sync_status)
        VALUES ($1, $2, $3, $4, $5, 'pending')
    `, item.ID, item.Path, item.Type, item.Content, item.ModifiedBy)
    
    if err != nil {
        // Cleanup file on database error
        os.Remove(fullPath)
        return err
    }
    
    return nil
}

func (wm *WorkspaceManager) UpdateItem(itemID string, content string, modifiedBy string) error {
    // Get current item
    var item WorkspaceItem
    err := wm.database.QueryRow(`
        SELECT id, path, type, content, version FROM workspace_items WHERE id = $1
    `, itemID).Scan(&item.ID, &item.Path, &item.Type, &item.Content, &item.Version)
    
    if err != nil {
        return err
    }
    
    // Update file
    fullPath := filepath.Join(wm.rootPath, item.Path)
    if err := os.WriteFile(fullPath, []byte(content), 0644); err != nil {
        return err
    }
    
    // Update database
    _, err = wm.database.Exec(`
        UPDATE workspace_items 
        SET content = $1, version = version + 1, modified_at = NOW(), 
            modified_by = $2, sync_status = 'pending'
        WHERE id = $3
    `, content, modifiedBy, itemID)
    
    return err
}

func (wm *WorkspaceManager) CommitChanges(message string, author string) (string, error) {
    workTree, err := wm.repository.Worktree()
    if err != nil {
        return "", err
    }
    
    // Add all changes
    _, err = workTree.Add(".")
    if err != nil {
        return "", err
    }
    
    // Create commit
    commit, err := workTree.Commit(message, &git.CommitOptions{
        Author: &object.Signature{
            Name:  author,
            Email: fmt.Sprintf("%s@aimatrix.local", author),
            When:  time.Now(),
        },
    })
    
    if err != nil {
        return "", err
    }
    
    commitHash := commit.String()
    
    // Update sync status for all pending items
    _, err = wm.database.Exec(`
        UPDATE workspace_items 
        SET sync_status = 'committed'
        WHERE sync_status = 'pending'
    `)
    
    // Log the commit
    wm.logSyncOperation("commit", "", commitHash, "success", "")
    
    return commitHash, err
}

func (wm *WorkspaceManager) SyncWithRemote() error {
    workTree, err := wm.repository.Worktree()
    if err != nil {
        return err
    }
    
    // Fetch from remote
    err = wm.repository.Fetch(&git.FetchOptions{
        RemoteName: "origin",
    })
    if err != nil && err != git.NoErrAlreadyUpToDate {
        return err
    }
    
    // Get remote branch reference
    remoteBranch := fmt.Sprintf("refs/remotes/origin/%s", wm.config.Branch)
    remoteRef, err := wm.repository.Reference(remoteBranch, true)
    if err != nil {
        return err
    }
    
    // Check for conflicts
    conflicts, err := wm.detectConflicts(remoteRef.Hash())
    if err != nil {
        return err
    }
    
    if len(conflicts) > 0 {
        return wm.handleConflicts(conflicts)
    }
    
    // Merge remote changes
    err = workTree.Merge(remoteRef.Hash(), &git.MergeOptions{})
    if err != nil {
        return err
    }
    
    // Push local changes
    err = wm.repository.Push(&git.PushOptions{
        RemoteName: "origin",
    })
    
    if err != nil && err != git.NoErrAlreadyUpToDate {
        return err
    }
    
    // Update sync status
    _, err = wm.database.Exec(`
        UPDATE workspace_items 
        SET sync_status = 'synced'
        WHERE sync_status = 'committed'
    `)
    
    return err
}

func (wm *WorkspaceManager) detectConflicts(remoteHash plumbing.Hash) ([]string, error) {
    // This is a simplified conflict detection
    // In practice, you'd compare trees and detect actual conflicts
    
    conflicts := []string{}
    
    // Get list of modified files since last sync
    rows, err := wm.database.Query(`
        SELECT path FROM workspace_items 
        WHERE sync_status IN ('pending', 'committed')
    `)
    if err != nil {
        return nil, err
    }
    defer rows.Close()
    
    for rows.Next() {
        var path string
        if err := rows.Scan(&path); err != nil {
            continue
        }
        
        // Check if file was also modified remotely
        // This would involve comparing with remote tree
        // For now, we'll simulate potential conflicts
        conflicts = append(conflicts, path)
    }
    
    return conflicts, nil
}

func (wm *WorkspaceManager) handleConflicts(conflictPaths []string) error {
    for _, path := range conflictPaths {
        // Create conflict record
        conflictID := generateID()
        
        // Get local content
        localContent, err := os.ReadFile(filepath.Join(wm.rootPath, path))
        if err != nil {
            continue
        }
        
        // For this example, we'll use the configured strategy
        switch wm.config.ConflictStrategy {
        case "local":
            // Keep local version - mark as resolved
            wm.resolveConflict(conflictID, string(localContent), "local_wins")
        case "remote":
            // This would fetch remote content and use it
            // Implementation depends on Git internals
            continue
        case "manual":
            // Create conflict record for manual resolution
            _, err = wm.database.Exec(`
                INSERT INTO workspace_conflicts 
                (id, item_id, local_content, status)
                SELECT $1, id, $2, 'pending'
                FROM workspace_items WHERE path = $3
            `, conflictID, string(localContent), path)
            
            if err != nil {
                return err
            }
        }
    }
    
    return nil
}

func (wm *WorkspaceManager) resolveConflict(conflictID, resolvedContent, strategy string) error {
    _, err := wm.database.Exec(`
        UPDATE workspace_conflicts 
        SET resolved_content = $1, resolution_strategy = $2, 
            resolved_at = NOW(), status = 'resolved'
        WHERE id = $3
    `, resolvedContent, strategy, conflictID)
    
    return err
}

func (wm *WorkspaceManager) startAutoCommit() {
    ticker := time.NewTicker(time.Duration(wm.config.CommitInterval) * time.Minute)
    defer ticker.Stop()
    
    for range ticker.C {
        // Check if there are pending changes
        var pendingCount int
        err := wm.database.QueryRow(`
            SELECT COUNT(*) FROM workspace_items WHERE sync_status = 'pending'
        `).Scan(&pendingCount)
        
        if err != nil || pendingCount == 0 {
            continue
        }
        
        // Auto-commit changes
        message := fmt.Sprintf("Auto-commit: %d items at %s", 
                              pendingCount, time.Now().Format(time.RFC3339))
        
        commitHash, err := wm.CommitChanges(message, "system")
        if err != nil {
            wm.logSyncOperation("auto_commit", "", "", "error", err.Error())
        } else {
            wm.logSyncOperation("auto_commit", "", commitHash, "success", "")
            
            // Also sync with remote if configured
            if wm.config.SyncInterval > 0 {
                go func() {
                    time.Sleep(1 * time.Minute) // Brief delay before sync
                    if err := wm.SyncWithRemote(); err != nil {
                        wm.logSyncOperation("auto_sync", "", "", "error", err.Error())
                    }
                }()
            }
        }
    }
}

func (wm *WorkspaceManager) logSyncOperation(operation, itemID, commitHash, status, errorMessage string) {
    _, err := wm.database.Exec(`
        INSERT INTO workspace_sync_log 
        (operation, item_id, commit_hash, status, error_message)
        VALUES ($1, $2, $3, $4, $5)
    `, operation, itemID, commitHash, status, errorMessage)
    
    if err != nil {
        fmt.Printf("Failed to log sync operation: %v\n", err)
    }
}

func generateID() string {
    return fmt.Sprintf("%d", time.Now().UnixNano())
}
```

## Intelligent Sync Mechanisms

### Conflict Resolution System
```typescript
// TypeScript conflict resolution engine
interface ConflictData {
  id: string
  entityType: 'agent' | 'workflow' | 'config'
  entityId: string
  localVersion: number
  remoteVersion: number
  localData: any
  remoteData: any
  baseData?: any  // Three-way merge support
  conflictFields: string[]
  priority: number
  createdAt: Date
  resolvedAt?: Date
  resolutionStrategy?: ResolutionStrategy
}

interface ResolutionStrategy {
  type: 'auto' | 'manual' | 'local_wins' | 'remote_wins' | 'merge' | 'custom'
  rules?: ResolutionRule[]
  customHandler?: string
}

interface ResolutionRule {
  field: string
  condition: string
  action: 'local' | 'remote' | 'newest' | 'custom'
  weight?: number
}

class ConflictResolver {
  private strategies: Map<string, ResolutionStrategy> = new Map()
  private customHandlers: Map<string, ConflictHandler> = new Map()
  
  constructor() {
    this.setupDefaultStrategies()
  }
  
  private setupDefaultStrategies() {
    // Agent configuration conflicts
    this.strategies.set('agent', {
      type: 'auto',
      rules: [
        {
          field: 'name',
          condition: 'always',
          action: 'newest'
        },
        {
          field: 'status',
          condition: 'local_active',
          action: 'local',
          weight: 10
        },
        {
          field: 'config.*',
          condition: 'non_destructive',
          action: 'merge'
        }
      ]
    })
    
    // Workflow conflicts - prefer local for active workflows
    this.strategies.set('workflow', {
      type: 'auto',
      rules: [
        {
          field: 'status',
          condition: 'local_running',
          action: 'local',
          weight: 10
        },
        {
          field: 'definition',
          condition: 'syntax_valid',
          action: 'newest'
        }
      ]
    })
    
    // Configuration conflicts - prefer explicit over defaults
    this.strategies.set('config', {
      type: 'auto',
      rules: [
        {
          field: '*',
          condition: 'explicit_value',
          action: 'newest'
        }
      ]
    })
  }
  
  async resolveConflict(conflict: ConflictData): Promise<ResolvedConflict> {
    const strategy = this.strategies.get(conflict.entityType) || 
                    { type: 'manual' as const }
    
    switch (strategy.type) {
      case 'auto':
        return await this.autoResolve(conflict, strategy)
      
      case 'local_wins':
        return {
          id: conflict.id,
          resolvedData: conflict.localData,
          strategy: 'local_wins',
          confidence: 1.0,
          requiresApproval: false
        }
      
      case 'remote_wins':
        return {
          id: conflict.id,
          resolvedData: conflict.remoteData,
          strategy: 'remote_wins',
          confidence: 1.0,
          requiresApproval: false
        }
      
      case 'merge':
        return await this.threeWayMerge(conflict)
      
      case 'custom':
        if (strategy.customHandler && 
            this.customHandlers.has(strategy.customHandler)) {
          const handler = this.customHandlers.get(strategy.customHandler)!
          return await handler.resolve(conflict)
        }
        // Fall through to manual
      
      case 'manual':
      default:
        return {
          id: conflict.id,
          resolvedData: null,
          strategy: 'manual',
          confidence: 0,
          requiresApproval: true,
          suggestedResolutions: await this.generateSuggestions(conflict)
        }
    }
  }
  
  private async autoResolve(conflict: ConflictData, 
                           strategy: ResolutionStrategy): Promise<ResolvedConflict> {
    const resolvedData: any = {}
    let totalWeight = 0
    let appliedWeight = 0
    let confidence = 0
    
    // Apply rules field by field
    for (const field of conflict.conflictFields) {
      const applicableRules = strategy.rules?.filter(rule => 
        this.fieldMatches(field, rule.field)
      ) || []
      
      if (applicableRules.length === 0) {
        // No specific rule, use default strategy
        resolvedData[field] = await this.applyDefaultResolution(
          field, conflict.localData[field], conflict.remoteData[field]
        )
        continue
      }
      
      // Find best matching rule
      let bestRule: ResolutionRule | null = null
      let bestScore = 0
      
      for (const rule of applicableRules) {
        const score = await this.evaluateRule(rule, field, conflict)
        if (score > bestScore) {
          bestScore = score
          bestRule = rule
        }
      }
      
      if (bestRule) {
        resolvedData[field] = await this.applyRule(bestRule, field, conflict)
        appliedWeight += bestRule.weight || 1
      }
      
      totalWeight += 1
    }
    
    confidence = totalWeight > 0 ? appliedWeight / totalWeight : 0
    
    // Merge non-conflicting fields
    const allFields = new Set([
      ...Object.keys(conflict.localData),
      ...Object.keys(conflict.remoteData)
    ])
    
    for (const field of allFields) {
      if (!conflict.conflictFields.includes(field)) {
        // Use newest version for non-conflicting fields
        if (conflict.localVersion > conflict.remoteVersion) {
          resolvedData[field] = conflict.localData[field]
        } else {
          resolvedData[field] = conflict.remoteData[field]
        }
      }
    }
    
    return {
      id: conflict.id,
      resolvedData,
      strategy: 'auto',
      confidence,
      requiresApproval: confidence < 0.8,
      appliedRules: strategy.rules?.map(r => r.field) || []
    }
  }
  
  private async threeWayMerge(conflict: ConflictData): Promise<ResolvedConflict> {
    if (!conflict.baseData) {
      // Fallback to two-way merge
      return await this.twoWayMerge(conflict)
    }
    
    const resolvedData = { ...conflict.baseData }
    const mergeResults: MergeResult[] = []
    
    // Three-way merge algorithm
    for (const field of conflict.conflictFields) {
      const baseValue = conflict.baseData[field]
      const localValue = conflict.localData[field]
      const remoteValue = conflict.remoteData[field]
      
      // Analyze changes
      const localChanged = !this.deepEqual(baseValue, localValue)
      const remoteChanged = !this.deepEqual(baseValue, remoteValue)
      
      if (!localChanged && !remoteChanged) {
        // No changes
        resolvedData[field] = baseValue
        mergeResults.push({ field, action: 'unchanged', confidence: 1.0 })
      } else if (localChanged && !remoteChanged) {
        // Only local changed
        resolvedData[field] = localValue
        mergeResults.push({ field, action: 'local', confidence: 1.0 })
      } else if (!localChanged && remoteChanged) {
        // Only remote changed  
        resolvedData[field] = remoteValue
        mergeResults.push({ field, action: 'remote', confidence: 1.0 })
      } else {
        // Both changed - need conflict resolution
        const mergeResult = await this.mergeValues(
          field, baseValue, localValue, remoteValue
        )
        resolvedData[field] = mergeResult.value
        mergeResults.push(mergeResult)
      }
    }
    
    const confidence = mergeResults.reduce((acc, result) => 
      acc + result.confidence, 0) / mergeResults.length
    
    return {
      id: conflict.id,
      resolvedData,
      strategy: 'three_way_merge',
      confidence,
      requiresApproval: confidence < 0.9,
      mergeResults
    }
  }
  
  private async mergeValues(field: string, base: any, local: any, remote: any): 
    Promise<MergeResult> {
    
    // Handle different data types
    if (Array.isArray(base) && Array.isArray(local) && Array.isArray(remote)) {
      return await this.mergeArrays(field, base, local, remote)
    }
    
    if (this.isObject(base) && this.isObject(local) && this.isObject(remote)) {
      return await this.mergeObjects(field, base, local, remote)
    }
    
    // Primitive values - use semantic merge if possible
    if (typeof base === 'string' && typeof local === 'string' && typeof remote === 'string') {
      return await this.mergeStrings(field, base, local, remote)
    }
    
    // Default: use most recent or local preference
    return {
      field,
      action: 'local', // Prefer local changes
      value: local,
      confidence: 0.5,
      requiresReview: true
    }
  }
  
  private async mergeArrays(field: string, base: any[], local: any[], remote: any[]): 
    Promise<MergeResult> {
    
    const merged = [...base]
    
    // Find additions and removals
    const localAdded = local.filter(item => !base.includes(item))
    const remoteAdded = remote.filter(item => !base.includes(item))
    const localRemoved = base.filter(item => !local.includes(item))
    const remoteRemoved = base.filter(item => !remote.includes(item))
    
    // Add new items from both sides
    merged.push(...localAdded, ...remoteAdded)
    
    // Handle removals (only if both sides agree)
    const commonRemovals = localRemoved.filter(item => remoteRemoved.includes(item))
    const finalMerged = merged.filter(item => !commonRemovals.includes(item))
    
    return {
      field,
      action: 'merged',
      value: [...new Set(finalMerged)], // Remove duplicates
      confidence: 0.8,
      requiresReview: localRemoved.length > 0 || remoteRemoved.length > 0
    }
  }
  
  private async generateSuggestions(conflict: ConflictData): Promise<ResolutionSuggestion[]> {
    const suggestions: ResolutionSuggestion[] = []
    
    // Suggest keeping local version
    suggestions.push({
      id: 'keep_local',
      title: 'Keep Local Version',
      description: 'Use the local version of the data',
      data: conflict.localData,
      confidence: 0.6,
      pros: ['Preserves local changes', 'No data loss'],
      cons: ['Ignores remote updates']
    })
    
    // Suggest keeping remote version
    suggestions.push({
      id: 'keep_remote',
      title: 'Keep Remote Version',
      description: 'Use the remote version of the data',
      data: conflict.remoteData,
      confidence: 0.6,
      pros: ['Gets latest remote updates', 'Maintains consistency'],
      cons: ['May lose local changes']
    })
    
    // Suggest field-by-field merge
    if (conflict.conflictFields.length > 1) {
      const mergedData = { ...conflict.localData }
      
      for (const field of conflict.conflictFields) {
        if (await this.isRemoteValueBetter(field, conflict)) {
          mergedData[field] = conflict.remoteData[field]
        }
      }
      
      suggestions.push({
        id: 'smart_merge',
        title: 'Smart Merge',
        description: 'Intelligent field-by-field merge',
        data: mergedData,
        confidence: 0.8,
        pros: ['Preserves best values', 'Minimizes data loss'],
        cons: ['May be complex to review']
      })
    }
    
    return suggestions
  }
  
  registerCustomHandler(name: string, handler: ConflictHandler) {
    this.customHandlers.set(name, handler)
  }
  
  private fieldMatches(field: string, pattern: string): boolean {
    if (pattern === '*') return true
    if (pattern.endsWith('*')) {
      return field.startsWith(pattern.slice(0, -1))
    }
    return field === pattern
  }
  
  private deepEqual(a: any, b: any): boolean {
    return JSON.stringify(a) === JSON.stringify(b)
  }
  
  private isObject(value: any): boolean {
    return value !== null && typeof value === 'object' && !Array.isArray(value)
  }
}

interface ResolvedConflict {
  id: string
  resolvedData: any
  strategy: string
  confidence: number
  requiresApproval: boolean
  appliedRules?: string[]
  mergeResults?: MergeResult[]
  suggestedResolutions?: ResolutionSuggestion[]
}

interface MergeResult {
  field: string
  action: string
  value?: any
  confidence: number
  requiresReview?: boolean
}

interface ResolutionSuggestion {
  id: string
  title: string
  description: string
  data: any
  confidence: number
  pros: string[]
  cons: string[]
}

interface ConflictHandler {
  resolve(conflict: ConflictData): Promise<ResolvedConflict>
}
```

## Sync Strategies & Bandwidth Optimization

### Intelligent Sync Engine
```python
# Python sync engine with bandwidth optimization
import asyncio
import json
import time
import hashlib
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import aiohttp
import aiodns
import zlib

class SyncPriority(Enum):
    CRITICAL = 10    # System failures, security issues
    HIGH = 8        # Active agents, running workflows  
    NORMAL = 5      # Regular updates, config changes
    LOW = 3         # Logs, metrics, historical data
    BACKGROUND = 1  # Cleanup, optimization

@dataclass
class SyncItem:
    id: str
    entity_type: str
    entity_id: str
    operation: str  # create, update, delete
    data: Dict[str, Any]
    priority: SyncPriority
    size_bytes: int
    created_at: datetime
    last_attempt: Optional[datetime] = None
    attempts: int = 0
    max_attempts: int = 5
    dependencies: List[str] = field(default_factory=list)
    checksum: Optional[str] = None
    compressed: bool = False

@dataclass 
class BandwidthLimits:
    max_bps: int = 1_000_000  # 1 Mbps default
    burst_bps: int = 5_000_000  # 5 Mbps burst
    critical_bps: int = 500_000  # Reserved for critical
    daily_quota: int = 10_000_000_000  # 10 GB per day
    
@dataclass
class NetworkConditions:
    latency_ms: float
    bandwidth_bps: int
    packet_loss: float
    jitter_ms: float
    is_metered: bool = False
    is_roaming: bool = False

class IntelligentSyncEngine:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sync_queue: List[SyncItem] = []
        self.bandwidth_limits = BandwidthLimits(**config.get('bandwidth', {}))
        self.network_conditions = NetworkConditions(
            latency_ms=100,
            bandwidth_bps=1_000_000,
            packet_loss=0.01,
            jitter_ms=10
        )
        
        self.bytes_sent_today = 0
        self.bytes_received_today = 0
        self.last_reset_date = datetime.now().date()
        
        self.sync_stats = {
            'items_synced': 0,
            'bytes_transferred': 0,
            'conflicts_resolved': 0,
            'sync_errors': 0,
            'average_latency': 0
        }
        
        # Adaptive sync parameters
        self.batch_size = 10
        self.sync_interval = 30  # seconds
        self.compression_threshold = 1024  # bytes
        
        # Start background tasks
        asyncio.create_task(self.sync_loop())
        asyncio.create_task(self.network_monitor_loop())
    
    async def add_sync_item(self, item: SyncItem):
        """Add item to sync queue with priority ordering"""
        # Calculate checksum for deduplication
        data_str = json.dumps(item.data, sort_keys=True)
        item.checksum = hashlib.sha256(data_str.encode()).hexdigest()
        
        # Check for duplicates
        existing_item = next(
            (i for i in self.sync_queue 
             if i.entity_type == item.entity_type and 
                i.entity_id == item.entity_id and
                i.checksum == item.checksum),
            None
        )
        
        if existing_item:
            # Update priority if higher
            if item.priority.value > existing_item.priority.value:
                existing_item.priority = item.priority
            return
        
        # Compress data if beneficial
        if item.size_bytes > self.compression_threshold:
            compressed_data = zlib.compress(data_str.encode())
            if len(compressed_data) < item.size_bytes * 0.9:  # At least 10% savings
                item.data = {'_compressed': True, '_data': compressed_data.hex()}
                item.size_bytes = len(compressed_data)
                item.compressed = True
        
        # Insert in priority order
        inserted = False
        for i, existing in enumerate(self.sync_queue):
            if item.priority.value > existing.priority.value:
                self.sync_queue.insert(i, item)
                inserted = True
                break
        
        if not inserted:
            self.sync_queue.append(item)
    
    async def sync_loop(self):
        """Main synchronization loop with adaptive behavior"""
        while True:
            try:
                await self.adaptive_sync_cycle()
                
                # Adaptive interval based on queue size and network conditions
                base_interval = self.sync_interval
                
                if len(self.sync_queue) > 100:
                    # Increase frequency when queue is large
                    interval = max(base_interval * 0.5, 5)
                elif len(self.sync_queue) == 0:
                    # Reduce frequency when queue is empty
                    interval = base_interval * 2
                else:
                    interval = base_interval
                
                # Adjust for network conditions
                if self.network_conditions.latency_ms > 500:
                    interval *= 1.5  # Slower sync on high latency
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                print(f"Sync loop error: {e}")
                await asyncio.sleep(self.sync_interval)
    
    async def adaptive_sync_cycle(self):
        """Perform one sync cycle with adaptive batching"""
        if not self.sync_queue:
            return
        
        # Reset daily quota if needed
        today = datetime.now().date()
        if today > self.last_reset_date:
            self.bytes_sent_today = 0
            self.bytes_received_today = 0
            self.last_reset_date = today
        
        # Check daily quota
        if self.bytes_sent_today >= self.bandwidth_limits.daily_quota:
            print("Daily bandwidth quota exceeded, skipping sync")
            return
        
        # Adaptive batch sizing
        available_bandwidth = min(
            self.network_conditions.bandwidth_bps,
            self.bandwidth_limits.max_bps
        )
        
        # Reserve bandwidth for critical items
        if self.has_critical_items():
            available_bandwidth -= self.bandwidth_limits.critical_bps
        
        # Calculate optimal batch size
        batch_size = self.calculate_optimal_batch_size(available_bandwidth)
        
        # Get items to sync
        batch = self.get_sync_batch(batch_size)
        
        if not batch:
            return
        
        # Group by dependencies
        dependency_groups = self.group_by_dependencies(batch)
        
        # Process each dependency group
        for group in dependency_groups:
            await self.sync_batch(group)
    
    def calculate_optimal_batch_size(self, available_bandwidth: int) -> int:
        """Calculate optimal batch size based on network conditions"""
        # Base calculation on bandwidth and latency
        latency_factor = max(0.1, 1.0 - (self.network_conditions.latency_ms / 1000))
        loss_factor = max(0.1, 1.0 - self.network_conditions.packet_loss)
        
        # Estimate time per item
        average_item_size = self.estimate_average_item_size()
        time_per_item = (average_item_size * 8) / available_bandwidth  # seconds
        
        # Account for protocol overhead and retransmissions
        overhead_factor = 1.3 + (self.network_conditions.packet_loss * 2)
        adjusted_time = time_per_item * overhead_factor / (latency_factor * loss_factor)
        
        # Target batch completion time: 30 seconds
        target_batch_time = 30
        optimal_batch_size = max(1, int(target_batch_time / adjusted_time))
        
        # Clamp to reasonable bounds
        return min(max(optimal_batch_size, 1), 50)
    
    def get_sync_batch(self, batch_size: int) -> List[SyncItem]:
        """Get next batch of items to sync with priority ordering"""
        batch = []
        remaining_bandwidth = self.bandwidth_limits.max_bps
        
        # Always include critical items first
        critical_items = [item for item in self.sync_queue 
                         if item.priority == SyncPriority.CRITICAL]
        
        for item in critical_items[:batch_size]:
            batch.append(item)
            remaining_bandwidth -= item.size_bytes * 8  # Convert to bits
        
        # Fill remaining batch with high-priority items
        if len(batch) < batch_size:
            remaining_size = batch_size - len(batch)
            non_critical = [item for item in self.sync_queue 
                           if item.priority != SyncPriority.CRITICAL]
            
            for item in non_critical[:remaining_size]:
                if item.size_bytes * 8 <= remaining_bandwidth:
                    batch.append(item)
                    remaining_bandwidth -= item.size_bytes * 8
        
        return batch
    
    async def sync_batch(self, batch: List[SyncItem]):
        """Synchronize a batch of items"""
        if not batch:
            return
        
        start_time = time.time()
        successful_syncs = 0
        failed_syncs = 0
        
        # Create HTTP session with optimizations
        connector = aiohttp.TCPConnector(
            limit=10,
            limit_per_host=5,
            keepalive_timeout=30,
            enable_cleanup_closed=True
        )
        
        timeout = aiohttp.ClientTimeout(
            total=300,  # 5 minutes total
            connect=30,  # 30 seconds to connect
            sock_read=60  # 60 seconds to read
        )
        
        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'User-Agent': 'AMX-Edge-Sync/1.0',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive'
            }
        ) as session:
            
            # Process batch concurrently
            tasks = []
            for item in batch:
                task = asyncio.create_task(self.sync_item(session, item))
                tasks.append(task)
            
            # Wait for all tasks with timeout
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for item, result in zip(batch, results):
                    if isinstance(result, Exception):
                        failed_syncs += 1
                        item.attempts += 1
                        item.last_attempt = datetime.now()
                        print(f"Sync failed for {item.id}: {result}")
                        
                        # Move to end of queue if retries remaining
                        if item.attempts < item.max_attempts:
                            self.sync_queue.append(item)
                        else:
                            self.sync_stats['sync_errors'] += 1
                    else:
                        successful_syncs += 1
                        self.sync_stats['items_synced'] += 1
                        self.sync_stats['bytes_transferred'] += item.size_bytes
                    
                    # Remove from queue
                    if item in self.sync_queue:
                        self.sync_queue.remove(item)
                        
            except asyncio.TimeoutError:
                print("Batch sync timeout")
                # Return items to queue for retry
                for item in batch:
                    if item not in self.sync_queue:
                        item.attempts += 1
                        if item.attempts < item.max_attempts:
                            self.sync_queue.append(item)
        
        # Update statistics
        sync_duration = time.time() - start_time
        if successful_syncs > 0:
            avg_latency = sync_duration / successful_syncs
            self.sync_stats['average_latency'] = (
                self.sync_stats['average_latency'] * 0.9 + avg_latency * 0.1
            )
        
        print(f"Batch sync completed: {successful_syncs} success, {failed_syncs} failed")
    
    async def sync_item(self, session: aiohttp.ClientSession, item: SyncItem) -> bool:
        """Synchronize a single item"""
        url = f"{self.config['sync_endpoint']}/{item.entity_type}/{item.entity_id}"
        
        # Prepare request data
        request_data = {
            'operation': item.operation,
            'data': item.data,
            'version': item.data.get('version', 1),
            'checksum': item.checksum
        }
        
        # Add metadata
        headers = {
            'Content-Type': 'application/json',
            'X-Sync-Priority': str(item.priority.value),
            'X-Sync-Item-ID': item.id
        }
        
        if item.compressed:
            headers['X-Content-Compressed'] = 'true'
        
        try:
            if item.operation == 'delete':
                async with session.delete(url, headers=headers) as response:
                    await self.handle_sync_response(item, response)
            else:
                async with session.post(url, json=request_data, headers=headers) as response:
                    await self.handle_sync_response(item, response)
            
            return True
            
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Sync error: {str(e)}")
    
    async def handle_sync_response(self, item: SyncItem, response: aiohttp.ClientResponse):
        """Handle synchronization response"""
        self.bytes_sent_today += len(await response.read())
        
        if response.status == 200:
            # Successful sync
            return
            
        elif response.status == 409:
            # Conflict detected
            response_data = await response.json()
            await self.handle_sync_conflict(item, response_data)
            
        elif response.status == 429:
            # Rate limited
            retry_after = response.headers.get('Retry-After', '60')
            raise Exception(f"Rate limited, retry after {retry_after} seconds")
            
        elif 400 <= response.status < 500:
            # Client error - don't retry
            error_data = await response.json()
            raise Exception(f"Client error {response.status}: {error_data.get('message', 'Unknown error')}")
            
        elif response.status >= 500:
            # Server error - retry
            raise Exception(f"Server error {response.status}")
    
    async def handle_sync_conflict(self, item: SyncItem, conflict_data: Dict[str, Any]):
        """Handle synchronization conflict"""
        print(f"Conflict detected for {item.entity_type}:{item.entity_id}")
        
        # Create conflict resolution request
        from .conflict_resolution import ConflictResolver
        
        resolver = ConflictResolver()
        conflict = {
            'id': f"sync_conflict_{item.id}",
            'entityType': item.entity_type,
            'entityId': item.entity_id,
            'localVersion': item.data.get('version', 1),
            'remoteVersion': conflict_data.get('version', 1),
            'localData': item.data,
            'remoteData': conflict_data.get('data', {}),
            'conflictFields': conflict_data.get('conflicted_fields', []),
            'priority': item.priority.value,
            'createdAt': datetime.now()
        }
        
        # Attempt automatic resolution
        resolution = await resolver.resolveConflict(conflict)
        
        if not resolution['requiresApproval']:
            # Auto-resolved, update item data
            item.data = resolution['resolvedData']
            # Re-add to queue for sync
            await self.add_sync_item(item)
        else:
            # Requires manual resolution
            self.sync_stats['conflicts_resolved'] += 1
            print(f"Manual conflict resolution required for {item.entity_id}")
    
    async def network_monitor_loop(self):
        """Monitor network conditions and adapt sync behavior"""
        while True:
            try:
                await self.measure_network_conditions()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Network monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def measure_network_conditions(self):
        """Measure current network conditions"""
        try:
            # Simple latency test
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.config['sync_endpoint']}/health",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    latency = (time.time() - start_time) * 1000
                    
                    self.network_conditions.latency_ms = (
                        self.network_conditions.latency_ms * 0.8 + latency * 0.2
                    )
            
            # Update sync parameters based on conditions
            if self.network_conditions.latency_ms > 1000:
                # High latency - reduce batch size, increase interval
                self.batch_size = max(self.batch_size // 2, 1)
                self.sync_interval = min(self.sync_interval * 1.5, 300)
            elif self.network_conditions.latency_ms < 100:
                # Low latency - can increase batch size
                self.batch_size = min(self.batch_size + 1, 20)
                self.sync_interval = max(self.sync_interval * 0.9, 10)
            
        except Exception as e:
            # Network unreachable
            self.network_conditions.latency_ms = 5000  # Assume very high latency
            self.batch_size = 1
            self.sync_interval = 300  # 5 minutes
    
    def has_critical_items(self) -> bool:
        """Check if queue contains critical priority items"""
        return any(item.priority == SyncPriority.CRITICAL for item in self.sync_queue)
    
    def estimate_average_item_size(self) -> int:
        """Estimate average item size for batch calculations"""
        if not self.sync_queue:
            return 1024  # Default 1KB
        
        total_size = sum(item.size_bytes for item in self.sync_queue[:10])
        count = min(len(self.sync_queue), 10)
        
        return max(total_size // count, 100)  # At least 100 bytes
    
    def group_by_dependencies(self, items: List[SyncItem]) -> List[List[SyncItem]]:
        """Group items by their dependencies for ordered processing"""
        groups = []
        processed = set()
        
        def process_item(item: SyncItem, current_group: List[SyncItem]):
            if item.id in processed:
                return
            
            # Check if dependencies are satisfied
            deps_satisfied = all(dep_id in processed for dep_id in item.dependencies)
            
            if deps_satisfied:
                current_group.append(item)
                processed.add(item.id)
        
        # Process items in waves until all are processed
        remaining_items = items[:]
        
        while remaining_items:
            current_group = []
            
            for item in remaining_items[:]:
                process_item(item, current_group)
                if item in current_group:
                    remaining_items.remove(item)
            
            if current_group:
                groups.append(current_group)
            else:
                # Break circular dependencies by processing remaining items
                if remaining_items:
                    groups.append(remaining_items[:1])
                    processed.add(remaining_items[0].id)
                    remaining_items = remaining_items[1:]
        
        return groups
    
    def get_sync_statistics(self) -> Dict[str, Any]:
        """Get comprehensive sync statistics"""
        return {
            **self.sync_stats,
            'queue_size': len(self.sync_queue),
            'bytes_sent_today': self.bytes_sent_today,
            'bytes_received_today': self.bytes_received_today,
            'network_latency_ms': self.network_conditions.latency_ms,
            'current_batch_size': self.batch_size,
            'sync_interval_seconds': self.sync_interval,
            'critical_items_pending': len([
                item for item in self.sync_queue 
                if item.priority == SyncPriority.CRITICAL
            ])
        }
```

---

> [!TIP]
> **Edge Deployment**: Deploy edge components using lightweight containers or directly on edge hardware. Use the provided SQLite schema and sync configurations for quick setup.

> [!NOTE]
> **Offline Capability**: Edge components maintain full functionality without internet connectivity for up to 30 days, with intelligent local decision-making and conflict-free eventual consistency when connectivity resumes.

---

*AIMatrix Edge & Offline Components - Distributed intelligence that never stops*