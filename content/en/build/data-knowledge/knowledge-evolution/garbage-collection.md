---
title: "Garbage Collection"
description: "Advanced knowledge garbage collection with reference counting, mark-and-sweep algorithms, and intelligent storage optimization"
weight: 4
---

Knowledge graphs accumulate vast amounts of data over time, requiring sophisticated garbage collection strategies to maintain performance and storage efficiency. This document covers advanced garbage collection algorithms, including reference counting, mark-and-sweep for knowledge, and intelligent storage optimization.

## Garbage Collection Framework

### Reference Tracking System

Comprehensive reference counting for knowledge entities:

```sql
-- Reference counting infrastructure
CREATE TABLE entity_references (
    reference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_entity_id UUID NOT NULL REFERENCES temporal_entities(entity_id),
    target_entity_id UUID NOT NULL REFERENCES temporal_entities(entity_id),
    reference_type TEXT NOT NULL, -- 'HARD', 'SOFT', 'WEAK', 'PHANTOM'
    reference_context TEXT, -- Context where reference occurs
    
    -- Reference strength and metadata
    weight FLOAT DEFAULT 1.0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_accessed TIMESTAMPTZ DEFAULT NOW(),
    access_count INTEGER DEFAULT 1,
    
    -- Lifecycle management
    is_active BOOLEAN DEFAULT TRUE,
    marked_for_deletion BOOLEAN DEFAULT FALSE,
    deletion_scheduled_for TIMESTAMPTZ,
    
    CONSTRAINT unique_reference UNIQUE (source_entity_id, target_entity_id, reference_type, reference_context),
    CONSTRAINT valid_reference_type CHECK (reference_type IN ('HARD', 'SOFT', 'WEAK', 'PHANTOM'))
);

-- Reference count materialized view for performance
CREATE MATERIALIZED VIEW entity_reference_counts AS
SELECT 
    target_entity_id as entity_id,
    reference_type,
    COUNT(*) as reference_count,
    SUM(weight) as total_weight,
    MAX(last_accessed) as last_referenced,
    AVG(access_count) as avg_access_count
FROM entity_references
WHERE is_active = TRUE AND NOT marked_for_deletion
GROUP BY target_entity_id, reference_type;

-- Indexes for performance
CREATE INDEX CONCURRENTLY idx_entity_refs_source ON entity_references (source_entity_id);
CREATE INDEX CONCURRENTLY idx_entity_refs_target ON entity_references (target_entity_id);
CREATE INDEX CONCURRENTLY idx_entity_refs_type ON entity_references (reference_type);
CREATE INDEX CONCURRENTLY idx_entity_refs_access ON entity_references (last_accessed);
CREATE INDEX CONCURRENTLY idx_entity_refs_scheduled ON entity_references (deletion_scheduled_for) 
    WHERE deletion_scheduled_for IS NOT NULL;

-- Reference counting functions
CREATE OR REPLACE FUNCTION get_entity_reference_count(
    entity_id UUID,
    ref_type TEXT DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    ref_count INTEGER;
BEGIN
    SELECT COALESCE(SUM(reference_count), 0)
    INTO ref_count
    FROM entity_reference_counts erc
    WHERE erc.entity_id = get_entity_reference_count.entity_id
      AND (ref_type IS NULL OR erc.reference_type = ref_type);
    
    RETURN ref_count;
END;
$$ LANGUAGE plpgsql;

-- Update reference count when references change
CREATE OR REPLACE FUNCTION update_reference_count()
RETURNS TRIGGER AS $$
BEGIN
    -- Refresh materialized view for affected entities
    IF TG_OP = 'INSERT' THEN
        REFRESH MATERIALIZED VIEW CONCURRENTLY entity_reference_counts;
        
        -- Update last accessed time for source entity
        UPDATE temporal_entities 
        SET metadata = metadata || jsonb_build_object('last_accessed', NOW())
        WHERE entity_id = NEW.source_entity_id;
        
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        REFRESH MATERIALIZED VIEW CONCURRENTLY entity_reference_counts;
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        REFRESH MATERIALIZED VIEW CONCURRENTLY entity_reference_counts;
        
        -- Update access statistics if access count changed
        IF NEW.access_count != OLD.access_count THEN
            NEW.last_accessed := NOW();
        END IF;
        
        RETURN NEW;
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER reference_count_update_trigger
    AFTER INSERT OR UPDATE OR DELETE ON entity_references
    FOR EACH ROW
    EXECUTE FUNCTION update_reference_count();
```

### Mark and Sweep Algorithm

Implement sophisticated mark-and-sweep garbage collection:

```sql
-- Garbage collection state tracking
CREATE TABLE gc_execution (
    gc_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gc_type TEXT NOT NULL, -- 'MARK_SWEEP', 'GENERATIONAL', 'INCREMENTAL'
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    status TEXT DEFAULT 'RUNNING', -- 'RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED'
    
    -- Statistics
    entities_scanned INTEGER DEFAULT 0,
    entities_marked INTEGER DEFAULT 0,
    entities_swept INTEGER DEFAULT 0,
    storage_reclaimed BIGINT DEFAULT 0,
    
    -- Configuration
    root_entities UUID[],
    max_generations INTEGER DEFAULT 3,
    aggressive_mode BOOLEAN DEFAULT FALSE,
    
    -- Error handling
    error_message TEXT,
    
    CONSTRAINT valid_status CHECK (status IN ('RUNNING', 'COMPLETED', 'FAILED', 'CANCELLED'))
);

-- Mark phase: identify reachable entities
CREATE OR REPLACE FUNCTION mark_reachable_entities(
    gc_id UUID,
    root_entities UUID[] DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    marked_count INTEGER := 0;
    current_roots UUID[];
BEGIN
    -- Use provided roots or find root entities automatically
    IF root_entities IS NULL THEN
        SELECT ARRAY(
            SELECT te.entity_id
            FROM temporal_entities te
            WHERE te.valid_to = 'infinity'
              AND NOT te.is_deleted
              AND (
                  -- Recently created entities
                  te.valid_from >= NOW() - INTERVAL '24 hours' OR
                  -- Entities with high access frequency
                  (te.metadata->>'access_frequency')::float > 0.8 OR
                  -- Entities with hard references from external systems
                  EXISTS (
                      SELECT 1 FROM entity_references er
                      WHERE er.target_entity_id = te.entity_id
                        AND er.reference_type = 'HARD'
                        AND er.reference_context = 'EXTERNAL'
                  )
              )
        ) INTO current_roots;
    ELSE
        current_roots := root_entities;
    END IF;
    
    -- Create temporary table for mark phase
    CREATE TEMP TABLE IF NOT EXISTS marked_entities (
        entity_id UUID PRIMARY KEY,
        mark_generation INTEGER DEFAULT 0,
        marked_at TIMESTAMPTZ DEFAULT NOW()
    ) ON COMMIT DROP;
    
    -- Mark root entities
    INSERT INTO marked_entities (entity_id, mark_generation)
    SELECT unnest(current_roots), 0
    ON CONFLICT (entity_id) DO NOTHING;
    
    GET DIAGNOSTICS marked_count = ROW_COUNT;
    
    -- Recursive marking using CTE
    WITH RECURSIVE reachable_entities AS (
        -- Start with marked root entities
        SELECT 
            me.entity_id,
            me.mark_generation,
            ARRAY[me.entity_id] as path
        FROM marked_entities me
        
        UNION ALL
        
        -- Follow references to mark reachable entities
        SELECT 
            er.target_entity_id,
            re.mark_generation + 1,
            re.path || er.target_entity_id
        FROM reachable_entities re
        JOIN entity_references er ON re.entity_id = er.source_entity_id
        WHERE re.mark_generation < 10 -- Limit depth to prevent infinite loops
          AND er.is_active = TRUE
          AND NOT er.marked_for_deletion
          AND er.reference_type IN ('HARD', 'SOFT') -- Only follow strong references
          AND NOT (er.target_entity_id = ANY(re.path)) -- Prevent cycles
    )
    INSERT INTO marked_entities (entity_id, mark_generation)
    SELECT DISTINCT re.entity_id, re.mark_generation
    FROM reachable_entities re
    ON CONFLICT (entity_id) DO UPDATE SET
        mark_generation = LEAST(marked_entities.mark_generation, EXCLUDED.mark_generation);
    
    -- Update statistics
    UPDATE gc_execution 
    SET entities_marked = (SELECT COUNT(*) FROM marked_entities)
    WHERE gc_execution.gc_id = mark_reachable_entities.gc_id;
    
    RETURN (SELECT COUNT(*) FROM marked_entities);
END;
$$ LANGUAGE plpgsql;

-- Sweep phase: collect unmarked entities
CREATE OR REPLACE FUNCTION sweep_unmarked_entities(
    gc_id UUID,
    dry_run BOOLEAN DEFAULT FALSE
) RETURNS TABLE (
    entity_id UUID,
    entity_type TEXT,
    size_bytes BIGINT,
    last_accessed TIMESTAMPTZ,
    action TEXT
) AS $$
DECLARE
    swept_count INTEGER := 0;
    total_size BIGINT := 0;
BEGIN
    -- Find unmarked entities eligible for collection
    RETURN QUERY
    WITH unmarked_entities AS (
        SELECT 
            te.entity_id,
            te.entity_type,
            octet_length(te.content::text) as content_size,
            (te.metadata->>'last_accessed')::timestamptz as last_accessed,
            -- Determine action based on entity characteristics
            CASE 
                WHEN get_entity_reference_count(te.entity_id, 'HARD') > 0 THEN 'KEEP_HARD_REF'
                WHEN get_entity_reference_count(te.entity_id, 'SOFT') > 0 AND 
                     (te.metadata->>'last_accessed')::timestamptz > NOW() - INTERVAL '30 days' THEN 'KEEP_RECENT_SOFT'
                WHEN te.entity_type IN ('system', 'configuration') THEN 'KEEP_SYSTEM'
                WHEN (te.metadata->>'importance_score')::float > 0.8 THEN 'KEEP_IMPORTANT'
                ELSE 'COLLECT'
            END as suggested_action
        FROM temporal_entities te
        WHERE te.valid_to = 'infinity'
          AND NOT te.is_deleted
          AND NOT EXISTS (
              SELECT 1 FROM marked_entities me
              WHERE me.entity_id = te.entity_id
          )
    )
    SELECT 
        ue.entity_id,
        ue.entity_type,
        ue.content_size,
        ue.last_accessed,
        ue.suggested_action
    FROM unmarked_entities ue;
    
    -- Execute sweep if not dry run
    IF NOT dry_run THEN
        -- Soft delete entities marked for collection
        WITH entities_to_collect AS (
            SELECT entity_id
            FROM unmarked_entities ue
            WHERE ue.suggested_action = 'COLLECT'
        )
        UPDATE temporal_entities te
        SET 
            is_deleted = TRUE,
            valid_to = NOW(),
            metadata = metadata || jsonb_build_object(
                'deleted_by_gc', gc_id,
                'deleted_reason', 'garbage_collection',
                'deleted_at', NOW()
            )
        WHERE te.entity_id IN (SELECT entity_id FROM entities_to_collect);
        
        GET DIAGNOSTICS swept_count = ROW_COUNT;
        
        -- Calculate reclaimed storage
        SELECT COALESCE(SUM(octet_length(content::text)), 0)
        INTO total_size
        FROM temporal_entities te
        WHERE te.metadata->>'deleted_by_gc' = gc_id::text;
        
        -- Update statistics
        UPDATE gc_execution
        SET 
            entities_swept = swept_count,
            storage_reclaimed = total_size
        WHERE gc_execution.gc_id = sweep_unmarked_entities.gc_id;
    END IF;
END;
$$ LANGUAGE plpgsql;
```

### Generational Garbage Collection

Implement generational GC for better performance:

```typescript
interface GenerationalGCConfig {
  youngGenerationThreshold: number; // hours
  middleGenerationThreshold: number; // days  
  oldGenerationThreshold: number; // months
  youngGCFrequency: number; // minutes
  fullGCFrequency: number; // hours
  aggressiveMode: boolean;
}

interface Generation {
  name: 'YOUNG' | 'MIDDLE' | 'OLD';
  ageThreshold: number;
  size: number;
  lastGC: Date;
  gcCount: number;
}

class GenerationalGarbageCollector {
  private config: GenerationalGCConfig;
  private currentGCId?: string;
  private isRunning = false;

  constructor(config: GenerationalGCConfig) {
    this.config = config;
  }

  async runGenerationalGC(forceFullGC = false): Promise<GenerationalGCResult> {
    if (this.isRunning) {
      throw new Error('Garbage collection already in progress');
    }

    this.isRunning = true;
    this.currentGCId = crypto.randomUUID();

    try {
      const generations = await this.analyzeGenerations();
      const gcStrategy = this.determineGCStrategy(generations, forceFullGC);
      
      let result: GenerationalGCResult;
      
      switch (gcStrategy.type) {
        case 'YOUNG_ONLY':
          result = await this.runYoungGenGC();
          break;
        case 'YOUNG_AND_MIDDLE':
          result = await this.runYoungAndMiddleGC();
          break;
        case 'FULL_GC':
          result = await this.runFullGC();
          break;
        default:
          result = { type: 'NO_OP', reason: 'No collection needed' };
      }

      await this.updateGenerationStatistics(result);
      return result;

    } finally {
      this.isRunning = false;
      this.currentGCId = undefined;
    }
  }

  private async analyzeGenerations(): Promise<Generation[]> {
    const { data: generationData } = await supabase.rpc('analyze_entity_generations');
    
    return [
      {
        name: 'YOUNG',
        ageThreshold: this.config.youngGenerationThreshold,
        size: generationData?.young_count || 0,
        lastGC: new Date(generationData?.young_last_gc || 0),
        gcCount: generationData?.young_gc_count || 0
      },
      {
        name: 'MIDDLE', 
        ageThreshold: this.config.middleGenerationThreshold,
        size: generationData?.middle_count || 0,
        lastGC: new Date(generationData?.middle_last_gc || 0),
        gcCount: generationData?.middle_gc_count || 0
      },
      {
        name: 'OLD',
        ageThreshold: this.config.oldGenerationThreshold,
        size: generationData?.old_count || 0,
        lastGC: new Date(generationData?.old_last_gc || 0),
        gcCount: generationData?.old_gc_count || 0
      }
    ];
  }

  private determineGCStrategy(generations: Generation[], forceFullGC: boolean): GCStrategy {
    if (forceFullGC) {
      return { type: 'FULL_GC', reason: 'Force full GC requested' };
    }

    const youngGen = generations.find(g => g.name === 'YOUNG')!;
    const middleGen = generations.find(g => g.name === 'MIDDLE')!;
    const oldGen = generations.find(g => g.name === 'OLD')!;

    // Check if young generation GC is needed
    const youngGCDue = Date.now() - youngGen.lastGC.getTime() > this.config.youngGCFrequency * 60 * 1000;
    const youngGenFull = youngGen.size > 10000; // Threshold for young generation

    if (youngGenFull || youngGCDue) {
      // Check if middle generation also needs collection
      const middleGCDue = Date.now() - middleGen.lastGC.getTime() > this.config.fullGCFrequency * 60 * 60 * 1000;
      const middleGenFull = middleGen.size > 50000;

      if (middleGenFull || middleGCDue) {
        // Check if full GC is needed
        const oldGenFull = oldGen.size > 100000;
        if (oldGenFull || this.config.aggressiveMode) {
          return { type: 'FULL_GC', reason: 'All generations need collection' };
        }
        return { type: 'YOUNG_AND_MIDDLE', reason: 'Young and middle generations need collection' };
      }
      return { type: 'YOUNG_ONLY', reason: 'Young generation needs collection' };
    }

    return { type: 'NO_OP', reason: 'No collection needed' };
  }

  private async runYoungGenGC(): Promise<GenerationalGCResult> {
    const startTime = Date.now();
    
    // Mark and sweep young generation only
    const { data: youngEntities } = await supabase.rpc('get_young_generation_entities', {
      age_threshold_hours: this.config.youngGenerationThreshold
    });

    const markedCount = await supabase.rpc('mark_reachable_entities', {
      gc_id: this.currentGCId,
      root_entities: youngEntities?.map(e => e.entity_id)
    });

    const { data: sweptEntities } = await supabase.rpc('sweep_unmarked_entities', {
      gc_id: this.currentGCId,
      dry_run: false
    });

    return {
      type: 'YOUNG_ONLY',
      gcId: this.currentGCId!,
      duration: Date.now() - startTime,
      entitiesScanned: youngEntities?.length || 0,
      entitiesMarked: markedCount,
      entitiesSwept: sweptEntities?.length || 0,
      storageReclaimed: sweptEntities?.reduce((sum, e) => sum + e.size_bytes, 0) || 0,
      generations: ['YOUNG']
    };
  }

  private async runFullGC(): Promise<GenerationalGCResult> {
    const startTime = Date.now();
    
    // Full mark and sweep across all generations
    const markedCount = await supabase.rpc('mark_reachable_entities', {
      gc_id: this.currentGCId,
      root_entities: null // Let function determine roots
    });

    const { data: sweptEntities } = await supabase.rpc('sweep_unmarked_entities', {
      gc_id: this.currentGCId,
      dry_run: false
    });

    // Additional full GC optimizations
    await this.defragmentStorage();
    await this.optimizeIndexes();
    await this.compactEmbeddings();

    return {
      type: 'FULL_GC',
      gcId: this.currentGCId!,
      duration: Date.now() - startTime,
      entitiesScanned: await this.getTotalEntityCount(),
      entitiesMarked: markedCount,
      entitiesSwept: sweptEntities?.length || 0,
      storageReclaimed: sweptEntities?.reduce((sum, e) => sum + e.size_bytes, 0) || 0,
      generations: ['YOUNG', 'MIDDLE', 'OLD'],
      additionalOptimizations: [
        'storage_defragmentation',
        'index_optimization', 
        'embedding_compaction'
      ]
    };
  }

  private async defragmentStorage(): Promise<void> {
    // Defragment temporal_entities table
    await supabase.rpc('defragment_temporal_entities');
    
    // Compact embeddings table
    await supabase.rpc('compact_embeddings_storage');
    
    // Rebuild indexes if needed
    await supabase.rpc('rebuild_fragmented_indexes');
  }

  private async optimizeIndexes(): Promise<void> {
    // Analyze and optimize frequently used indexes
    await supabase.rpc('analyze_index_usage');
    await supabase.rpc('reindex_if_beneficial');
  }

  private async compactEmbeddings(): Promise<void> {
    // Remove duplicate embeddings and optimize storage
    await supabase.rpc('deduplicate_embeddings');
    await supabase.rpc('compress_embedding_storage');
  }
}
```

## Lazy Deletion Strategies

### Soft Delete with Grace Periods

Implement intelligent soft deletion:

```sql
-- Soft deletion framework
CREATE TABLE deletion_queue (
    deletion_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_id UUID NOT NULL REFERENCES temporal_entities(entity_id),
    deletion_reason TEXT NOT NULL,
    requested_at TIMESTAMPTZ DEFAULT NOW(),
    requested_by UUID REFERENCES auth.users(id),
    
    -- Grace period configuration
    grace_period INTERVAL DEFAULT '30 days',
    hard_delete_at TIMESTAMPTZ GENERATED ALWAYS AS (requested_at + grace_period) STORED,
    
    -- Status tracking
    status TEXT DEFAULT 'PENDING', -- 'PENDING', 'RESTORED', 'CONFIRMED', 'EXECUTED'
    confirmed_at TIMESTAMPTZ,
    confirmed_by UUID REFERENCES auth.users(id),
    executed_at TIMESTAMPTZ,
    
    -- Undo information
    restore_data JSONB,
    restoration_count INTEGER DEFAULT 0,
    
    CONSTRAINT valid_deletion_status CHECK (status IN ('PENDING', 'RESTORED', 'CONFIRMED', 'EXECUTED'))
);

-- Intelligent grace period calculation
CREATE OR REPLACE FUNCTION calculate_grace_period(
    entity_id UUID,
    deletion_reason TEXT,
    base_period INTERVAL DEFAULT '30 days'
) RETURNS INTERVAL AS $$
DECLARE
    entity_importance FLOAT;
    reference_count INTEGER;
    last_access TIMESTAMPTZ;
    calculated_period INTERVAL;
BEGIN
    -- Get entity metadata
    SELECT 
        (metadata->>'importance_score')::float,
        (metadata->>'last_accessed')::timestamptz
    INTO entity_importance, last_access
    FROM temporal_entities
    WHERE temporal_entities.entity_id = calculate_grace_period.entity_id;
    
    -- Get reference count
    SELECT get_entity_reference_count(entity_id) INTO reference_count;
    
    -- Calculate base period multiplier
    calculated_period := base_period;
    
    -- Extend grace period for important entities
    IF entity_importance > 0.8 THEN
        calculated_period := calculated_period * 2;
    ELSIF entity_importance > 0.5 THEN
        calculated_period := calculated_period * 1.5;
    END IF;
    
    -- Extend for heavily referenced entities
    IF reference_count > 10 THEN
        calculated_period := calculated_period * (1 + (reference_count / 100.0));
    END IF;
    
    -- Reduce for recently unused entities
    IF last_access < NOW() - INTERVAL '6 months' THEN
        calculated_period := calculated_period * 0.5;
    ELSIF last_access < NOW() - INTERVAL '3 months' THEN
        calculated_period := calculated_period * 0.75;
    END IF;
    
    -- Special handling for system entities
    IF deletion_reason = 'user_request' AND entity_importance > 0.9 THEN
        calculated_period := calculated_period * 3; -- Extra protection
    END IF;
    
    -- Minimum and maximum bounds
    calculated_period := GREATEST(calculated_period, INTERVAL '7 days');
    calculated_period := LEAST(calculated_period, INTERVAL '365 days');
    
    RETURN calculated_period;
END;
$$ LANGUAGE plpgsql;

-- Soft delete with grace period
CREATE OR REPLACE FUNCTION soft_delete_entity(
    entity_id UUID,
    deletion_reason TEXT,
    requested_by UUID,
    custom_grace_period INTERVAL DEFAULT NULL
) RETURNS UUID AS $$
DECLARE
    deletion_id UUID;
    grace_period INTERVAL;
    restore_data JSONB;
BEGIN
    -- Calculate appropriate grace period
    IF custom_grace_period IS NOT NULL THEN
        grace_period := custom_grace_period;
    ELSE
        grace_period := calculate_grace_period(entity_id, deletion_reason);
    END IF;
    
    -- Prepare restore data
    SELECT jsonb_build_object(
        'entity_data', row_to_json(te),
        'references', (
            SELECT jsonb_agg(row_to_json(er))
            FROM entity_references er
            WHERE er.source_entity_id = entity_id OR er.target_entity_id = entity_id
        ),
        'metadata', jsonb_build_object(
            'deletion_initiated_at', NOW(),
            'original_status', 'active'
        )
    ) INTO restore_data
    FROM temporal_entities te
    WHERE te.entity_id = soft_delete_entity.entity_id;
    
    -- Queue for deletion
    INSERT INTO deletion_queue (
        entity_id,
        deletion_reason,
        requested_by,
        grace_period,
        restore_data
    ) VALUES (
        entity_id,
        deletion_reason,
        requested_by,
        grace_period,
        restore_data
    ) RETURNING deletion_id INTO deletion_id;
    
    -- Mark entity as soft deleted
    UPDATE temporal_entities
    SET 
        is_deleted = TRUE,
        valid_to = NOW(),
        metadata = metadata || jsonb_build_object(
            'soft_deleted', TRUE,
            'deletion_id', deletion_id,
            'deletion_reason', deletion_reason,
            'grace_period_ends', NOW() + grace_period
        )
    WHERE temporal_entities.entity_id = soft_delete_entity.entity_id;
    
    -- Mark references for potential cleanup
    UPDATE entity_references
    SET 
        marked_for_deletion = TRUE,
        deletion_scheduled_for = NOW() + grace_period
    WHERE source_entity_id = entity_id OR target_entity_id = entity_id;
    
    RETURN deletion_id;
END;
$$ LANGUAGE plpgsql;

-- Restore soft deleted entity
CREATE OR REPLACE FUNCTION restore_soft_deleted_entity(
    deletion_id UUID,
    restored_by UUID,
    restore_reason TEXT DEFAULT 'user_request'
) RETURNS BOOLEAN AS $$
DECLARE
    queue_record RECORD;
    restore_data JSONB;
BEGIN
    -- Get deletion queue record
    SELECT * INTO queue_record
    FROM deletion_queue dq
    WHERE dq.deletion_id = restore_soft_deleted_entity.deletion_id
      AND dq.status = 'PENDING'
      AND dq.hard_delete_at > NOW(); -- Still within grace period
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Deletion record not found or grace period expired';
    END IF;
    
    restore_data := queue_record.restore_data;
    
    -- Restore entity
    UPDATE temporal_entities
    SET 
        is_deleted = FALSE,
        valid_to = 'infinity',
        metadata = (restore_data->'entity_data'->>'metadata')::jsonb || jsonb_build_object(
            'restored_at', NOW(),
            'restored_by', restored_by,
            'restore_reason', restore_reason,
            'restoration_count', COALESCE((metadata->>'restoration_count')::integer, 0) + 1
        )
    WHERE entity_id = queue_record.entity_id;
    
    -- Restore references
    UPDATE entity_references
    SET 
        marked_for_deletion = FALSE,
        deletion_scheduled_for = NULL
    WHERE source_entity_id = queue_record.entity_id 
       OR target_entity_id = queue_record.entity_id;
    
    -- Update deletion queue
    UPDATE deletion_queue
    SET 
        status = 'RESTORED',
        restoration_count = restoration_count + 1
    WHERE deletion_queue.deletion_id = restore_soft_deleted_entity.deletion_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

## Storage Optimization

### Intelligent Archiving

Archive old data to cheaper storage:

```typescript
interface ArchivalPolicy {
  name: string;
  criteria: ArchivalCriteria;
  destination: ArchivalDestination;
  retention: RetentionPolicy;
  compression: CompressionConfig;
}

interface ArchivalCriteria {
  ageThreshold: number; // days
  accessFrequency: number; // access per month threshold
  importanceScore: number; // minimum importance to keep active
  referenceThreshold: number; // minimum references to keep active
  customFilters: string[]; // SQL where conditions
}

class StorageOptimizer {
  async optimizeStorage(policies: ArchivalPolicy[]): Promise<OptimizationResult> {
    const results: PolicyResult[] = [];
    let totalSavings = 0;
    
    for (const policy of policies) {
      const policyResult = await this.applyArchivalPolicy(policy);
      results.push(policyResult);
      totalSavings += policyResult.spaceSaved;
    }
    
    // Additional optimizations
    const compressionResult = await this.compressActiveData();
    const deduplicationResult = await this.deduplicateData();
    const indexOptimization = await this.optimizeIndexes();
    
    return {
      totalSpaceSaved: totalSavings + compressionResult.spaceSaved + deduplicationResult.spaceSaved,
      policyResults: results,
      compressionResult,
      deduplicationResult,
      indexOptimization
    };
  }

  private async applyArchivalPolicy(policy: ArchivalPolicy): Promise<PolicyResult> {
    // Find entities matching archival criteria
    const candidates = await this.findArchivalCandidates(policy.criteria);
    
    let archivedCount = 0;
    let spaceSaved = 0;
    
    for (const candidate of candidates) {
      try {
        // Create archive entry
        const archiveResult = await this.archiveEntity(candidate, policy);
        
        if (archiveResult.success) {
          archivedCount++;
          spaceSaved += archiveResult.spaceSaved;
          
          // Update entity to reference archive
          await this.convertToArchiveReference(candidate.entityId, archiveResult.archiveId);
        }
      } catch (error) {
        console.warn(`Failed to archive entity ${candidate.entityId}:`, error);
      }
    }
    
    return {
      policyName: policy.name,
      candidatesFound: candidates.length,
      entitiesArchived: archivedCount,
      spaceSaved
    };
  }

  private async findArchivalCandidates(criteria: ArchivalCriteria): Promise<ArchivalCandidate[]> {
    const { data: candidates } = await supabase.rpc('find_archival_candidates', {
      age_threshold_days: criteria.ageThreshold,
      access_frequency_threshold: criteria.accessFrequency,
      importance_threshold: criteria.importanceScore,
      reference_threshold: criteria.referenceThreshold,
      custom_filters: criteria.customFilters
    });
    
    return (candidates || []).map(c => ({
      entityId: c.entity_id,
      size: c.content_size,
      lastAccessed: new Date(c.last_accessed),
      accessCount: c.access_count,
      importanceScore: c.importance_score,
      referenceCount: c.reference_count
    }));
  }

  private async archiveEntity(
    candidate: ArchivalCandidate,
    policy: ArchivalPolicy
  ): Promise<ArchiveResult> {
    // Get full entity data
    const { data: entityData } = await supabase
      .from('temporal_entities')
      .select('*')
      .eq('entity_id', candidate.entityId)
      .single();
    
    if (!entityData) {
      throw new Error('Entity not found');
    }
    
    // Compress data if configured
    let compressedData = entityData.content;
    let compressionRatio = 1;
    
    if (policy.compression.enabled) {
      const compressed = await this.compressContent(entityData.content, policy.compression);
      compressedData = compressed.data;
      compressionRatio = compressed.ratio;
    }
    
    // Store in archive destination
    const archiveId = await this.storeInArchive(
      candidate.entityId,
      {
        ...entityData,
        content: compressedData,
        metadata: {
          ...entityData.metadata,
          archived_at: new Date(),
          archival_policy: policy.name,
          compression_ratio: compressionRatio,
          original_size: JSON.stringify(entityData.content).length
        }
      },
      policy.destination
    );
    
    return {
      success: true,
      archiveId,
      spaceSaved: JSON.stringify(entityData.content).length * (1 - 1/compressionRatio),
      compressionRatio
    };
  }

  private async storeInArchive(
    entityId: string,
    data: any,
    destination: ArchivalDestination
  ): Promise<string> {
    const archiveId = crypto.randomUUID();
    
    switch (destination.type) {
      case 'S3_GLACIER':
        await this.storeInS3Glacier(archiveId, data, destination.config);
        break;
      case 'POSTGRESQL_ARCHIVE':
        await this.storeInPostgreSQLArchive(archiveId, data, destination.config);
        break;
      case 'FILE_SYSTEM':
        await this.storeInFileSystem(archiveId, data, destination.config);
        break;
      default:
        throw new Error(`Unknown archive destination: ${destination.type}`);
    }
    
    // Create archive metadata entry
    await supabase.from('entity_archives').insert({
      archive_id: archiveId,
      entity_id: entityId,
      destination_type: destination.type,
      destination_config: destination.config,
      archived_at: new Date(),
      size_bytes: JSON.stringify(data).length
    });
    
    return archiveId;
  }

  private async compressActiveData(): Promise<CompressionResult> {
    // Compress large content fields
    const { data: largeEntities } = await supabase.rpc('find_compressible_entities', {
      min_size_bytes: 10 * 1024 // 10KB threshold
    });
    
    let totalSavings = 0;
    let compressedCount = 0;
    
    for (const entity of largeEntities || []) {
      const originalSize = JSON.stringify(entity.content).length;
      const compressed = await this.compressContent(entity.content, {
        algorithm: 'gzip',
        level: 6
      });
      
      if (compressed.ratio > 1.2) { // Only compress if >20% savings
        await supabase
          .from('temporal_entities')
          .update({
            content: compressed.data,
            metadata: {
              ...entity.metadata,
              compressed: true,
              compression_ratio: compressed.ratio,
              original_size: originalSize
            }
          })
          .eq('entity_id', entity.entity_id);
        
        totalSavings += originalSize * (1 - 1/compressed.ratio);
        compressedCount++;
      }
    }
    
    return {
      entitiesCompressed: compressedCount,
      spaceSaved: totalSavings,
      averageCompressionRatio: totalSavings / compressedCount || 0
    };
  }

  private async deduplicateData(): Promise<DeduplicationResult> {
    // Find duplicate content using content hashes
    const { data: duplicates } = await supabase.rpc('find_duplicate_content');
    
    let deduplicatedCount = 0;
    let spaceSaved = 0;
    
    for (const duplicateGroup of duplicates || []) {
      // Keep the most important/recent entity, deduplicate others
      const entities = duplicateGroup.entities.sort((a, b) => 
        (b.importance_score || 0) - (a.importance_score || 0) ||
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
      
      const primaryEntity = entities[0];
      const duplicateEntities = entities.slice(1);
      
      for (const duplicate of duplicateEntities) {
        // Replace content with reference to primary
        await supabase
          .from('temporal_entities')
          .update({
            content: { 
              $ref: primaryEntity.entity_id,
              $type: 'content_reference'
            },
            metadata: {
              ...duplicate.metadata,
              deduplicated: true,
              references_content_from: primaryEntity.entity_id,
              original_size: JSON.stringify(duplicate.content).length
            }
          })
          .eq('entity_id', duplicate.entity_id);
        
        spaceSaved += JSON.stringify(duplicate.content).length;
        deduplicatedCount++;
      }
    }
    
    return {
      entitiesDeuplicated: deduplicatedCount,
      spaceSaved,
      duplicateGroups: duplicates?.length || 0
    };
  }
}
```

### Automated Storage Monitoring

Continuous storage optimization:

```sql
-- Storage monitoring and alerting
CREATE TABLE storage_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recorded_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Size metrics
    total_entities INTEGER,
    active_entities INTEGER,
    deleted_entities INTEGER,
    archived_entities INTEGER,
    
    -- Storage metrics
    total_storage_bytes BIGINT,
    active_storage_bytes BIGINT,
    compressed_storage_bytes BIGINT,
    archive_storage_bytes BIGINT,
    
    -- Reference metrics
    total_references INTEGER,
    active_references INTEGER,
    orphaned_references INTEGER,
    
    -- Performance metrics
    avg_query_time FLOAT,
    index_efficiency FLOAT,
    
    -- Growth metrics
    entities_created_24h INTEGER,
    entities_deleted_24h INTEGER,
    storage_growth_24h BIGINT
);

-- Automated storage analysis
CREATE OR REPLACE FUNCTION analyze_storage_health() RETURNS JSONB AS $$
DECLARE
    current_metrics RECORD;
    health_score FLOAT := 1.0;
    issues JSONB := '[]'::jsonb;
    recommendations JSONB := '[]'::jsonb;
BEGIN
    -- Collect current metrics
    SELECT 
        COUNT(*) as total_entities,
        COUNT(*) FILTER (WHERE NOT is_deleted AND valid_to = 'infinity') as active_entities,
        COUNT(*) FILTER (WHERE is_deleted) as deleted_entities,
        COUNT(*) FILTER (WHERE metadata ? 'archived') as archived_entities,
        SUM(octet_length(content::text)) as total_storage,
        SUM(octet_length(content::text)) FILTER (WHERE NOT is_deleted) as active_storage,
        SUM(octet_length(content::text)) FILTER (WHERE metadata ? 'compressed') as compressed_storage
    INTO current_metrics
    FROM temporal_entities;
    
    -- Check for issues and calculate health score
    
    -- Issue 1: High deleted entity ratio
    IF current_metrics.deleted_entities::float / current_metrics.total_entities > 0.3 THEN
        health_score := health_score - 0.2;
        issues := issues || jsonb_build_array(jsonb_build_object(
            'type', 'HIGH_DELETED_RATIO',
            'severity', 'MEDIUM',
            'description', 'More than 30% of entities are deleted',
            'value', current_metrics.deleted_entities::float / current_metrics.total_entities
        ));
        recommendations := recommendations || jsonb_build_array(jsonb_build_object(
            'action', 'RUN_GARBAGE_COLLECTION',
            'priority', 'MEDIUM',
            'description', 'Run garbage collection to clean up deleted entities'
        ));
    END IF;
    
    -- Issue 2: Low compression ratio
    IF current_metrics.compressed_storage::float / current_metrics.active_storage < 0.1 THEN
        health_score := health_score - 0.15;
        issues := issues || jsonb_build_array(jsonb_build_object(
            'type', 'LOW_COMPRESSION',
            'severity', 'LOW',
            'description', 'Less than 10% of storage is compressed',
            'value', current_metrics.compressed_storage::float / current_metrics.active_storage
        ));
        recommendations := recommendations || jsonb_build_array(jsonb_build_object(
            'action', 'ENABLE_COMPRESSION',
            'priority', 'LOW',
            'description', 'Enable compression for large entities'
        ));
    END IF;
    
    -- Issue 3: Rapid growth
    DECLARE
        growth_rate FLOAT;
    BEGIN
        SELECT storage_growth_24h::float / (total_storage_bytes - storage_growth_24h)
        INTO growth_rate
        FROM storage_metrics
        ORDER BY recorded_at DESC
        LIMIT 1;
        
        IF growth_rate > 0.1 THEN -- More than 10% growth per day
            health_score := health_score - 0.25;
            issues := issues || jsonb_build_array(jsonb_build_object(
                'type', 'RAPID_GROWTH',
                'severity', 'HIGH',
                'description', 'Storage growing more than 10% per day',
                'value', growth_rate
            ));
            recommendations := recommendations || jsonb_build_array(jsonb_build_object(
                'action', 'IMPLEMENT_ARCHIVAL',
                'priority', 'HIGH',
                'description', 'Implement archival policies to control growth'
            ));
        END IF;
    END;
    
    -- Record metrics
    INSERT INTO storage_metrics (
        total_entities,
        active_entities,
        deleted_entities,
        archived_entities,
        total_storage_bytes,
        active_storage_bytes,
        compressed_storage_bytes
    ) VALUES (
        current_metrics.total_entities,
        current_metrics.active_entities,
        current_metrics.deleted_entities,
        current_metrics.archived_entities,
        current_metrics.total_storage,
        current_metrics.active_storage,
        current_metrics.compressed_storage
    );
    
    RETURN jsonb_build_object(
        'health_score', health_score,
        'issues', issues,
        'recommendations', recommendations,
        'metrics', row_to_json(current_metrics)
    );
END;
$$ LANGUAGE plpgsql;

-- Schedule automated monitoring
SELECT cron.schedule('storage-health-check', '0 */6 * * *', 'SELECT analyze_storage_health();');
SELECT cron.schedule('daily-gc', '0 2 * * *', 'SELECT run_generational_gc();');
SELECT cron.schedule('weekly-optimization', '0 3 * * 0', 'SELECT optimize_storage();');
```

This comprehensive garbage collection system provides:

1. **Advanced reference counting** with different reference types and weights
2. **Sophisticated mark-and-sweep** algorithms for thorough cleanup
3. **Generational garbage collection** for improved performance
4. **Intelligent soft deletion** with grace periods and restoration capability
5. **Storage optimization** through compression, deduplication, and archiving
6. **Automated monitoring** with health checks and proactive maintenance

The system ensures optimal knowledge graph performance while maintaining data integrity and providing recovery mechanisms for accidentally deleted information.