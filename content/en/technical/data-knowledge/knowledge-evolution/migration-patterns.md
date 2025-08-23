---
title: "Migration Patterns"
description: "Advanced migration strategies for knowledge graph evolution with forward compatibility and schema transformation pipelines"
weight: 3
---

# Migration Patterns

As knowledge graphs evolve, maintaining data integrity while enabling schema evolution requires sophisticated migration patterns. This document covers forward migration strategies, backward compatibility, and advanced data transformation pipelines for seamless knowledge evolution.

## Migration Framework Architecture

### Migration System Design

```sql
-- Migration tracking and management
CREATE TABLE knowledge_migrations (
    migration_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    migration_name TEXT UNIQUE NOT NULL,
    version TEXT NOT NULL,
    description TEXT,
    migration_type TEXT DEFAULT 'SCHEMA', -- 'SCHEMA', 'DATA', 'HYBRID'
    
    -- Migration status
    status TEXT DEFAULT 'PENDING', -- 'PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'ROLLED_BACK'
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    
    -- Migration content
    forward_script TEXT NOT NULL,
    rollback_script TEXT,
    validation_script TEXT,
    
    -- Dependencies and ordering
    depends_on UUID[] DEFAULT '{}',
    priority INTEGER DEFAULT 100,
    
    -- Execution context
    executed_by UUID REFERENCES auth.users(id),
    execution_log JSONB DEFAULT '[]'::jsonb,
    
    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT valid_status CHECK (status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'ROLLED_BACK'))
);

-- Migration execution state
CREATE TABLE migration_execution_state (
    execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    migration_id UUID REFERENCES knowledge_migrations(migration_id),
    entity_id UUID REFERENCES temporal_entities(entity_id),
    
    -- Execution tracking
    step_number INTEGER NOT NULL,
    step_name TEXT NOT NULL,
    step_status TEXT DEFAULT 'PENDING',
    
    -- Data tracking
    old_value JSONB,
    new_value JSONB,
    transformation_applied TEXT,
    
    -- Timing
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    
    -- Error handling
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    CONSTRAINT valid_step_status CHECK (step_status IN ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED', 'SKIPPED'))
);

-- Schema versioning
CREATE TABLE schema_versions (
    version_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version_number TEXT UNIQUE NOT NULL,
    schema_definition JSONB NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES auth.users(id),
    
    -- Compatibility information
    backward_compatible_with TEXT[],
    forward_compatible_with TEXT[],
    breaking_changes JSONB DEFAULT '[]'::jsonb,
    
    -- Schema metadata
    description TEXT,
    changelog TEXT,
    
    CONSTRAINT single_active_schema EXCLUDE (is_active WITH =) WHERE (is_active = TRUE)
);
```

### Migration Engine Implementation

Advanced migration execution engine:

```typescript
interface MigrationDefinition {
  name: string;
  version: string;
  description: string;
  type: 'SCHEMA' | 'DATA' | 'HYBRID';
  dependsOn: string[];
  forward: MigrationStep[];
  rollback: MigrationStep[];
  validation: ValidationRule[];
  metadata?: Record<string, any>;
}

interface MigrationStep {
  name: string;
  type: 'SQL' | 'FUNCTION' | 'TRANSFORM' | 'VALIDATE';
  script?: string;
  function?: string;
  parameters?: Record<string, any>;
  condition?: string;
  batchSize?: number;
  timeout?: number;
}

class MigrationEngine {
  private executionQueue: Map<string, MigrationExecution> = new Map();
  private rollbackStack: MigrationExecution[] = [];

  async executeMigration(
    migrationName: string,
    options: MigrationOptions = {}
  ): Promise<MigrationResult> {
    const migration = await this.loadMigration(migrationName);
    const executionId = crypto.randomUUID();
    
    try {
      // Validate prerequisites
      await this.validatePrerequisites(migration);
      
      // Create execution context
      const execution = await this.createExecutionContext(migration, executionId, options);
      this.executionQueue.set(executionId, execution);
      
      // Execute migration steps
      const result = await this.executeSteps(execution);
      
      // Post-migration validation
      await this.validateMigrationResult(execution, result);
      
      // Update migration status
      await this.updateMigrationStatus(migration.name, 'COMPLETED');
      
      return {
        executionId,
        success: true,
        result,
        affectedEntities: execution.affectedEntities,
        duration: Date.now() - execution.startTime
      };
      
    } catch (error) {
      await this.handleMigrationError(migrationName, executionId, error);
      throw error;
    } finally {
      this.executionQueue.delete(executionId);
    }
  }

  private async executeSteps(execution: MigrationExecution): Promise<any> {
    const results = [];
    
    for (let i = 0; i < execution.migration.forward.length; i++) {
      const step = execution.migration.forward[i];
      const stepResult = await this.executeStep(execution, step, i);
      results.push(stepResult);
      
      // Check for cancellation or pause requests
      if (execution.status === 'CANCELLING') {
        throw new Error('Migration cancelled by user');
      }
      
      if (execution.status === 'PAUSED') {
        await this.pauseMigration(execution);
      }
    }
    
    return results;
  }

  private async executeStep(
    execution: MigrationExecution,
    step: MigrationStep,
    stepIndex: number
  ): Promise<StepResult> {
    const stepExecution = {
      executionId: execution.id,
      migrationId: execution.migration.id,
      stepNumber: stepIndex,
      stepName: step.name,
      startedAt: new Date()
    };

    try {
      await this.updateStepStatus(stepExecution, 'RUNNING');
      
      let result: any;
      
      switch (step.type) {
        case 'SQL':
          result = await this.executeSqlStep(step, execution);
          break;
        case 'FUNCTION':
          result = await this.executeFunctionStep(step, execution);
          break;
        case 'TRANSFORM':
          result = await this.executeTransformStep(step, execution);
          break;
        case 'VALIDATE':
          result = await this.executeValidationStep(step, execution);
          break;
        default:
          throw new Error(`Unknown step type: ${step.type}`);
      }
      
      await this.updateStepStatus(stepExecution, 'COMPLETED');
      
      return {
        stepName: step.name,
        success: true,
        result,
        duration: Date.now() - stepExecution.startedAt.getTime()
      };
      
    } catch (error) {
      await this.updateStepStatus(stepExecution, 'FAILED', error.message);
      
      // Handle step failure based on migration configuration
      if (execution.options.continueOnError) {
        console.warn(`Step ${step.name} failed but continuing:`, error);
        return { stepName: step.name, success: false, error: error.message };
      } else {
        throw error;
      }
    }
  }
}
```

## Schema Evolution Strategies

### Backward Compatible Migrations

Implement zero-downtime schema changes:

```sql
-- Backward compatible schema evolution
CREATE OR REPLACE FUNCTION add_field_backward_compatible(
    entity_type TEXT,
    field_name TEXT,
    field_schema JSONB,
    default_value JSONB DEFAULT NULL
) RETURNS VOID AS $$
DECLARE
    current_schema JSONB;
    new_schema JSONB;
    migration_id UUID;
BEGIN
    -- Get current schema version
    SELECT schema_definition INTO current_schema
    FROM schema_versions
    WHERE is_active = TRUE;
    
    -- Create new schema with additional field
    new_schema := jsonb_deep_merge(
        current_schema,
        jsonb_build_object(
            'entities',
            jsonb_build_object(
                entity_type,
                jsonb_build_object(
                    'fields',
                    jsonb_build_object(field_name, field_schema)
                )
            )
        )
    );
    
    -- Create migration
    INSERT INTO knowledge_migrations (
        migration_name,
        version,
        description,
        migration_type,
        forward_script,
        rollback_script
    ) VALUES (
        'add_field_' || entity_type || '_' || field_name,
        (SELECT version_number FROM schema_versions WHERE is_active = TRUE) || '_patch',
        'Add field ' || field_name || ' to ' || entity_type,
        'SCHEMA',
        format('ALTER TABLE %I ADD COLUMN IF NOT EXISTS %I JSONB DEFAULT %L',
               'entity_' || entity_type, field_name, default_value),
        format('ALTER TABLE %I DROP COLUMN IF EXISTS %I',
               'entity_' || entity_type, field_name)
    ) RETURNING migration_id;
    
    -- Execute migration steps
    PERFORM execute_migration_step(migration_id, 'forward');
    
    -- Update existing entities with default value if provided
    IF default_value IS NOT NULL THEN
        UPDATE temporal_entities
        SET content = content || jsonb_build_object(field_name, default_value)
        WHERE entity_type = add_field_backward_compatible.entity_type
          AND valid_to = 'infinity'
          AND NOT is_deleted
          AND NOT (content ? field_name);
    END IF;
    
    -- Register new schema version
    INSERT INTO schema_versions (
        version_number,
        schema_definition,
        is_active,
        backward_compatible_with
    ) VALUES (
        (SELECT version_number FROM schema_versions WHERE is_active = TRUE) || '_patch',
        new_schema,
        TRUE,
        ARRAY[(SELECT version_number FROM schema_versions WHERE is_active = TRUE)]
    );
    
    -- Deactivate old schema
    UPDATE schema_versions
    SET is_active = FALSE
    WHERE is_active = TRUE AND version_number != new_schema->'version';
END;
$$ LANGUAGE plpgsql;

-- Field deprecation with graceful transition
CREATE OR REPLACE FUNCTION deprecate_field(
    entity_type TEXT,
    field_name TEXT,
    deprecation_message TEXT DEFAULT NULL,
    removal_version TEXT DEFAULT NULL
) RETURNS VOID AS $$
BEGIN
    -- Mark field as deprecated in schema
    UPDATE schema_versions
    SET schema_definition = jsonb_deep_merge(
        schema_definition,
        jsonb_build_object(
            'entities', jsonb_build_object(
                entity_type, jsonb_build_object(
                    'fields', jsonb_build_object(
                        field_name, jsonb_build_object(
                            'deprecated', TRUE,
                            'deprecation_message', COALESCE(deprecation_message, 'Field is deprecated'),
                            'removal_version', removal_version,
                            'deprecated_at', NOW()::text
                        )
                    )
                )
            )
        )
    )
    WHERE is_active = TRUE;
    
    -- Create migration to add deprecation warnings
    INSERT INTO knowledge_migrations (
        migration_name,
        version,
        description,
        migration_type,
        forward_script
    ) VALUES (
        'deprecate_' || entity_type || '_' || field_name,
        (SELECT version_number FROM schema_versions WHERE is_active = TRUE) || '_deprecation',
        'Deprecate field ' || field_name || ' in ' || entity_type,
        'SCHEMA',
        format($migration$
            -- Add deprecation metadata to entities using this field
            UPDATE temporal_entities
            SET metadata = metadata || jsonb_build_object(
                'deprecated_fields', 
                COALESCE(metadata->'deprecated_fields', '[]'::jsonb) || 
                jsonb_build_array('%s')
            )
            WHERE entity_type = '%s'
              AND content ? '%s'
              AND valid_to = 'infinity'
              AND NOT is_deleted;
        $migration$, field_name, entity_type, field_name)
    );
END;
$$ LANGUAGE plpgsql;
```

### Data Transformation Pipelines

Sophisticated data transformation during migrations:

```typescript
interface TransformationPipeline {
  name: string;
  steps: TransformationStep[];
  parallel: boolean;
  batchSize: number;
  validation: PipelineValidation;
}

interface TransformationStep {
  name: string;
  type: 'MAP' | 'FILTER' | 'AGGREGATE' | 'JOIN' | 'CUSTOM';
  config: TransformationConfig;
  condition?: string;
  errorHandling: 'SKIP' | 'RETRY' | 'FAIL';
}

class DataTransformationEngine {
  async executePipeline(
    pipeline: TransformationPipeline,
    sourceData: any[],
    context: TransformationContext
  ): Promise<TransformationResult> {
    const executor = new PipelineExecutor(pipeline, context);
    
    try {
      // Pre-pipeline validation
      await this.validateInput(sourceData, pipeline.validation.input);
      
      // Execute transformation steps
      let currentData = sourceData;
      const stepResults: StepResult[] = [];
      
      for (const step of pipeline.steps) {
        const stepResult = await this.executeTransformationStep(
          step,
          currentData,
          context,
          pipeline.batchSize
        );
        
        stepResults.push(stepResult);
        currentData = stepResult.outputData;
        
        // Intermediate validation
        if (step.config.validate) {
          await this.validateStepOutput(currentData, step.config.validation);
        }
      }
      
      // Post-pipeline validation
      await this.validateOutput(currentData, pipeline.validation.output);
      
      return {
        success: true,
        transformedData: currentData,
        stepResults,
        metrics: this.calculateMetrics(stepResults)
      };
      
    } catch (error) {
      return {
        success: false,
        error: error.message,
        partialResults: currentData,
        stepResults
      };
    }
  }

  private async executeTransformationStep(
    step: TransformationStep,
    data: any[],
    context: TransformationContext,
    batchSize: number
  ): Promise<StepResult> {
    const startTime = Date.now();
    const processedItems: any[] = [];
    const errors: TransformationError[] = [];
    
    // Process in batches for large datasets
    const batches = this.createBatches(data, batchSize);
    
    for (const batch of batches) {
      try {
        const batchResult = await this.processBatch(step, batch, context);
        processedItems.push(...batchResult.items);
        errors.push(...batchResult.errors);
      } catch (batchError) {
        if (step.errorHandling === 'FAIL') {
          throw batchError;
        } else if (step.errorHandling === 'RETRY') {
          // Implement retry logic
          const retryResult = await this.retryBatch(step, batch, context, 3);
          processedItems.push(...retryResult.items);
          errors.push(...retryResult.errors);
        }
        // SKIP: Continue with next batch
      }
    }
    
    return {
      stepName: step.name,
      inputCount: data.length,
      outputCount: processedItems.length,
      errorCount: errors.length,
      outputData: processedItems,
      errors,
      duration: Date.now() - startTime
    };
  }

  private async processBatch(
    step: TransformationStep,
    batch: any[],
    context: TransformationContext
  ): Promise<{ items: any[], errors: TransformationError[] }> {
    const items: any[] = [];
    const errors: TransformationError[] = [];
    
    switch (step.type) {
      case 'MAP':
        return this.executeMapTransformation(step, batch, context);
      case 'FILTER':
        return this.executeFilterTransformation(step, batch, context);
      case 'AGGREGATE':
        return this.executeAggregateTransformation(step, batch, context);
      case 'JOIN':
        return this.executeJoinTransformation(step, batch, context);
      case 'CUSTOM':
        return this.executeCustomTransformation(step, batch, context);
      default:
        throw new Error(`Unknown transformation type: ${step.type}`);
    }
  }

  private async executeMapTransformation(
    step: TransformationStep,
    batch: any[],
    context: TransformationContext
  ): Promise<{ items: any[], errors: TransformationError[] }> {
    const items: any[] = [];
    const errors: TransformationError[] = [];
    
    for (const item of batch) {
      try {
        const transformed = await this.applyMappingRules(
          item,
          step.config.mappingRules,
          context
        );
        
        items.push(transformed);
      } catch (error) {
        errors.push({
          itemId: item.id || item.entity_id,
          step: step.name,
          error: error.message,
          originalData: item
        });
      }
    }
    
    return { items, errors };
  }

  private async applyMappingRules(
    item: any,
    mappingRules: MappingRule[],
    context: TransformationContext
  ): Promise<any> {
    let transformed = { ...item };
    
    for (const rule of mappingRules) {
      try {
        switch (rule.type) {
          case 'FIELD_RENAME':
            transformed = this.renameField(transformed, rule.source, rule.target);
            break;
            
          case 'FIELD_TRANSFORM':
            transformed = await this.transformField(
              transformed,
              rule.field,
              rule.transformation,
              context
            );
            break;
            
          case 'FIELD_MERGE':
            transformed = this.mergeFields(
              transformed,
              rule.sourceFields,
              rule.targetField,
              rule.mergeStrategy
            );
            break;
            
          case 'CONDITIONAL_TRANSFORM':
            if (this.evaluateCondition(item, rule.condition)) {
              transformed = await this.applyTransformation(transformed, rule.transformation);
            }
            break;
            
          case 'LOOKUP_TRANSFORM':
            transformed = await this.applyLookupTransformation(
              transformed,
              rule.lookupTable,
              rule.keyField,
              rule.targetField
            );
            break;
            
          default:
            throw new Error(`Unknown mapping rule type: ${rule.type}`);
        }
      } catch (ruleError) {
        throw new Error(`Failed to apply mapping rule ${rule.type}: ${ruleError.message}`);
      }
    }
    
    return transformed;
  }
}
```

## Breaking Change Management

### Breaking Change Detection

Automatically detect breaking changes in schema evolution:

```sql
-- Breaking change detection
CREATE OR REPLACE FUNCTION detect_breaking_changes(
    old_schema JSONB,
    new_schema JSONB
) RETURNS JSONB AS $$
DECLARE
    breaking_changes JSONB := '[]'::jsonb;
    entity_name TEXT;
    field_name TEXT;
    old_field JSONB;
    new_field JSONB;
BEGIN
    -- Check for removed entities
    FOR entity_name IN SELECT jsonb_object_keys(old_schema->'entities') LOOP
        IF NOT (new_schema->'entities' ? entity_name) THEN
            breaking_changes := breaking_changes || jsonb_build_array(
                jsonb_build_object(
                    'type', 'ENTITY_REMOVED',
                    'entity', entity_name,
                    'severity', 'HIGH',
                    'description', 'Entity ' || entity_name || ' was removed'
                )
            );
        END IF;
    END LOOP;
    
    -- Check for field changes in existing entities
    FOR entity_name IN SELECT jsonb_object_keys(old_schema->'entities') LOOP
        IF new_schema->'entities' ? entity_name THEN
            -- Check for removed fields
            FOR field_name IN SELECT jsonb_object_keys((old_schema->'entities'->entity_name)->'fields') LOOP
                IF NOT ((new_schema->'entities'->entity_name)->'fields' ? field_name) THEN
                    breaking_changes := breaking_changes || jsonb_build_array(
                        jsonb_build_object(
                            'type', 'FIELD_REMOVED',
                            'entity', entity_name,
                            'field', field_name,
                            'severity', 'HIGH',
                            'description', 'Field ' || field_name || ' was removed from ' || entity_name
                        )
                    );
                END IF;
            END LOOP;
            
            -- Check for field type changes
            FOR field_name IN SELECT jsonb_object_keys((old_schema->'entities'->entity_name)->'fields') LOOP
                IF (new_schema->'entities'->entity_name)->'fields' ? field_name THEN
                    old_field := (old_schema->'entities'->entity_name)->'fields'->field_name;
                    new_field := (new_schema->'entities'->entity_name)->'fields'->field_name;
                    
                    -- Check type compatibility
                    IF old_field->>'type' != new_field->>'type' THEN
                        breaking_changes := breaking_changes || jsonb_build_array(
                            jsonb_build_object(
                                'type', 'FIELD_TYPE_CHANGED',
                                'entity', entity_name,
                                'field', field_name,
                                'old_type', old_field->>'type',
                                'new_type', new_field->>'type',
                                'severity', CASE 
                                    WHEN is_type_compatible(old_field->>'type', new_field->>'type') 
                                    THEN 'MEDIUM' 
                                    ELSE 'HIGH' 
                                END,
                                'description', 'Field type changed from ' || (old_field->>'type') || ' to ' || (new_field->>'type')
                            )
                        );
                    END IF;
                    
                    -- Check if required field became non-nullable
                    IF (old_field->>'nullable')::boolean = TRUE AND 
                       (new_field->>'nullable')::boolean = FALSE THEN
                        breaking_changes := breaking_changes || jsonb_build_array(
                            jsonb_build_object(
                                'type', 'FIELD_NULLABILITY_CHANGED',
                                'entity', entity_name,
                                'field', field_name,
                                'severity', 'HIGH',
                                'description', 'Field ' || field_name || ' is no longer nullable'
                            )
                        );
                    END IF;
                END IF;
            END LOOP;
        END IF;
    END LOOP;
    
    RETURN breaking_changes;
END;
$$ LANGUAGE plpgsql;

-- Compatibility checking
CREATE OR REPLACE FUNCTION is_type_compatible(old_type TEXT, new_type TEXT) RETURNS BOOLEAN AS $$
BEGIN
    -- Define type compatibility rules
    RETURN CASE 
        WHEN old_type = new_type THEN TRUE
        WHEN old_type = 'integer' AND new_type = 'bigint' THEN TRUE
        WHEN old_type = 'varchar' AND new_type = 'text' THEN TRUE
        WHEN old_type = 'timestamp' AND new_type = 'timestamptz' THEN TRUE
        ELSE FALSE
    END;
END;
$$ LANGUAGE plpgsql;
```

### Migration Safety Checks

Implement comprehensive safety validation:

```typescript
interface SafetyCheck {
  name: string;
  type: 'PRE_MIGRATION' | 'POST_MIGRATION' | 'CONTINUOUS';
  critical: boolean;
  check: (context: MigrationContext) => Promise<SafetyResult>;
}

class MigrationSafetyValidator {
  private safetyChecks: SafetyCheck[] = [
    {
      name: 'DataIntegrityCheck',
      type: 'PRE_MIGRATION',
      critical: true,
      check: this.validateDataIntegrity.bind(this)
    },
    {
      name: 'PerformanceImpactCheck', 
      type: 'PRE_MIGRATION',
      critical: false,
      check: this.assessPerformanceImpact.bind(this)
    },
    {
      name: 'DependencyValidation',
      type: 'PRE_MIGRATION', 
      critical: true,
      check: this.validateDependencies.bind(this)
    },
    {
      name: 'RollbackCapabilityCheck',
      type: 'PRE_MIGRATION',
      critical: true,
      check: this.validateRollbackCapability.bind(this)
    },
    {
      name: 'ContinuousIntegrityMonitor',
      type: 'CONTINUOUS',
      critical: true,
      check: this.monitorIntegrityDuringMigration.bind(this)
    }
  ];

  async validateMigrationSafety(
    migration: MigrationDefinition,
    context: MigrationContext
  ): Promise<SafetyReport> {
    const results: SafetyResult[] = [];
    const criticalIssues: SafetyIssue[] = [];
    
    // Execute pre-migration checks
    for (const check of this.safetyChecks.filter(c => c.type === 'PRE_MIGRATION')) {
      try {
        const result = await check.check(context);
        results.push(result);
        
        if (check.critical && !result.passed) {
          criticalIssues.push(...result.issues.filter(i => i.severity === 'CRITICAL'));
        }
      } catch (error) {
        const failureResult: SafetyResult = {
          checkName: check.name,
          passed: false,
          issues: [{
            severity: 'CRITICAL',
            message: `Safety check failed: ${error.message}`,
            code: 'SAFETY_CHECK_FAILURE'
          }]
        };
        
        results.push(failureResult);
        if (check.critical) {
          criticalIssues.push(...failureResult.issues);
        }
      }
    }
    
    return {
      overallSafety: criticalIssues.length === 0,
      criticalIssues,
      allResults: results,
      recommendations: this.generateSafetyRecommendations(results)
    };
  }

  private async validateDataIntegrity(context: MigrationContext): Promise<SafetyResult> {
    const issues: SafetyIssue[] = [];
    
    try {
      // Check for data consistency before migration
      const { data: inconsistencies } = await supabase.rpc('check_data_consistency');
      
      for (const inconsistency of inconsistencies || []) {
        issues.push({
          severity: inconsistency.severity,
          message: `Data inconsistency found: ${inconsistency.description}`,
          code: 'DATA_INCONSISTENCY',
          details: inconsistency
        });
      }
      
      // Check for orphaned references
      const { data: orphanedRefs } = await supabase.rpc('find_orphaned_references');
      
      for (const orphan of orphanedRefs || []) {
        issues.push({
          severity: 'HIGH',
          message: `Orphaned reference found: ${orphan.source_entity} -> ${orphan.target_entity}`,
          code: 'ORPHANED_REFERENCE',
          details: orphan
        });
      }
      
      // Check for duplicate entities
      const { data: duplicates } = await supabase.rpc('find_duplicate_entities');
      
      for (const duplicate of duplicates || []) {
        issues.push({
          severity: 'MEDIUM',
          message: `Duplicate entities found: ${duplicate.entity_ids.join(', ')}`,
          code: 'DUPLICATE_ENTITIES',
          details: duplicate
        });
      }
      
    } catch (error) {
      issues.push({
        severity: 'CRITICAL',
        message: `Failed to validate data integrity: ${error.message}`,
        code: 'INTEGRITY_CHECK_FAILURE'
      });
    }
    
    return {
      checkName: 'DataIntegrityCheck',
      passed: !issues.some(i => i.severity === 'CRITICAL'),
      issues
    };
  }

  private async assessPerformanceImpact(context: MigrationContext): Promise<SafetyResult> {
    const issues: SafetyIssue[] = [];
    
    try {
      // Estimate migration time based on data size
      const { data: stats } = await supabase.rpc('get_entity_statistics');
      const estimatedDuration = this.estimateMigrationDuration(context.migration, stats);
      
      if (estimatedDuration > 3600) { // More than 1 hour
        issues.push({
          severity: 'HIGH',
          message: `Migration estimated to take ${Math.round(estimatedDuration / 60)} minutes`,
          code: 'LONG_MIGRATION_TIME',
          details: { estimatedDuration, affectedEntities: stats.total_entities }
        });
      }
      
      // Check for potential locking issues
      const potentialLocks = this.analyzePotentialLocks(context.migration);
      for (const lock of potentialLocks) {
        issues.push({
          severity: lock.severity,
          message: `Potential database lock: ${lock.description}`,
          code: 'POTENTIAL_LOCK',
          details: lock
        });
      }
      
      // Memory usage estimation
      const memoryEstimate = this.estimateMemoryUsage(context.migration, stats);
      if (memoryEstimate > 1024 * 1024 * 1024) { // More than 1GB
        issues.push({
          severity: 'MEDIUM',
          message: `High memory usage estimated: ${Math.round(memoryEstimate / (1024 * 1024))}MB`,
          code: 'HIGH_MEMORY_USAGE',
          details: { estimatedMemory: memoryEstimate }
        });
      }
      
    } catch (error) {
      issues.push({
        severity: 'MEDIUM',
        message: `Failed to assess performance impact: ${error.message}`,
        code: 'PERFORMANCE_ASSESSMENT_FAILURE'
      });
    }
    
    return {
      checkName: 'PerformanceImpactCheck',
      passed: !issues.some(i => i.severity === 'CRITICAL'),
      issues
    };
  }

  private async validateRollbackCapability(context: MigrationContext): Promise<SafetyResult> {
    const issues: SafetyIssue[] = [];
    
    // Check if rollback script exists and is valid
    if (!context.migration.rollback || context.migration.rollback.length === 0) {
      issues.push({
        severity: 'CRITICAL',
        message: 'No rollback script provided for migration',
        code: 'NO_ROLLBACK_SCRIPT'
      });
    } else {
      // Validate rollback script syntax
      try {
        await this.validateMigrationScript(context.migration.rollback);
      } catch (error) {
        issues.push({
          severity: 'CRITICAL',
          message: `Invalid rollback script: ${error.message}`,
          code: 'INVALID_ROLLBACK_SCRIPT'
        });
      }
    }
    
    // Check if rollback would cause data loss
    const dataLossRisk = this.assessRollbackDataLossRisk(context.migration);
    if (dataLossRisk.hasRisk) {
      issues.push({
        severity: 'HIGH',
        message: 'Rollback may cause data loss',
        code: 'ROLLBACK_DATA_LOSS_RISK',
        details: dataLossRisk
      });
    }
    
    return {
      checkName: 'RollbackCapabilityCheck',
      passed: !issues.some(i => i.severity === 'CRITICAL'),
      issues
    };
  }

  private generateSafetyRecommendations(results: SafetyResult[]): Recommendation[] {
    const recommendations: Recommendation[] = [];
    
    for (const result of results) {
      for (const issue of result.issues) {
        switch (issue.code) {
          case 'DATA_INCONSISTENCY':
            recommendations.push({
              type: 'FIX_REQUIRED',
              priority: 'HIGH',
              message: 'Fix data inconsistencies before proceeding with migration',
              action: 'RUN_DATA_CLEANUP'
            });
            break;
            
          case 'LONG_MIGRATION_TIME':
            recommendations.push({
              type: 'SCHEDULE_MAINTENANCE',
              priority: 'MEDIUM',
              message: 'Schedule migration during maintenance window',
              action: 'PLAN_DOWNTIME'
            });
            break;
            
          case 'NO_ROLLBACK_SCRIPT':
            recommendations.push({
              type: 'IMPLEMENT_REQUIRED',
              priority: 'CRITICAL',
              message: 'Implement rollback script before migration',
              action: 'CREATE_ROLLBACK_SCRIPT'
            });
            break;
        }
      }
    }
    
    return recommendations;
  }
}
```

## Progressive Migration Strategies

### Blue-Green Migration Pattern

Implement zero-downtime migrations using blue-green deployment:

```sql
-- Blue-green migration setup
CREATE SCHEMA IF NOT EXISTS migration_blue;
CREATE SCHEMA IF NOT EXISTS migration_green;

-- Current active schema tracking
CREATE TABLE active_schema_version (
    id INTEGER PRIMARY KEY DEFAULT 1,
    current_schema TEXT NOT NULL DEFAULT 'main',
    migration_in_progress BOOLEAN DEFAULT FALSE,
    migration_id UUID REFERENCES knowledge_migrations(migration_id),
    switched_at TIMESTAMPTZ,
    
    CONSTRAINT single_active_record CHECK (id = 1)
);

-- Initialize with main schema
INSERT INTO active_schema_version (current_schema) VALUES ('main') ON CONFLICT (id) DO NOTHING;

-- Blue-green migration function
CREATE OR REPLACE FUNCTION execute_blue_green_migration(
    migration_id UUID,
    target_schema TEXT DEFAULT 'green'
) RETURNS JSONB AS $$
DECLARE
    current_schema TEXT;
    migration_record RECORD;
    result JSONB := '{}'::jsonb;
BEGIN
    -- Get current active schema
    SELECT current_schema INTO current_schema FROM active_schema_version WHERE id = 1;
    
    -- Get migration details
    SELECT * INTO migration_record FROM knowledge_migrations WHERE migration_id = migration_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Migration not found: %', migration_id;
    END IF;
    
    -- Mark migration as in progress
    UPDATE active_schema_version 
    SET migration_in_progress = TRUE, migration_id = migration_id
    WHERE id = 1;
    
    BEGIN
        -- Copy current schema to target
        PERFORM copy_schema_to_target(current_schema, target_schema);
        
        -- Apply migration to target schema
        PERFORM apply_migration_to_schema(migration_record, target_schema);
        
        -- Validate target schema
        PERFORM validate_migrated_schema(target_schema, migration_record);
        
        -- Switch traffic to target schema (atomic operation)
        PERFORM switch_active_schema(target_schema);
        
        result := jsonb_build_object(
            'success', true,
            'previous_schema', current_schema,
            'new_schema', target_schema,
            'switched_at', NOW()
        );
        
    EXCEPTION WHEN OTHERS THEN
        -- Rollback on failure
        UPDATE active_schema_version 
        SET migration_in_progress = FALSE, migration_id = NULL
        WHERE id = 1;
        
        RAISE;
    END;
    
    -- Mark migration as completed
    UPDATE active_schema_version 
    SET migration_in_progress = FALSE, migration_id = NULL, switched_at = NOW()
    WHERE id = 1;
    
    UPDATE knowledge_migrations 
    SET status = 'COMPLETED', completed_at = NOW()
    WHERE migration_id = migration_id;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Schema switching function (atomic)
CREATE OR REPLACE FUNCTION switch_active_schema(new_schema TEXT) RETURNS VOID AS $$
BEGIN
    -- Update routing configuration atomically
    UPDATE active_schema_version 
    SET current_schema = new_schema
    WHERE id = 1;
    
    -- Notify application layer of schema switch
    PERFORM pg_notify('schema_switched', new_schema);
END;
$$ LANGUAGE plpgsql;
```

### Canary Migration Pattern

Gradual migration with rollback capability:

```typescript
interface CanaryMigrationConfig {
  migrationId: string;
  canaryPercentage: number;
  validationMetrics: string[];
  successThreshold: number;
  maxDuration: number; // minutes
  rollbackOnFailure: boolean;
}

class CanaryMigrationManager {
  async executeCanaryMigration(config: CanaryMigrationConfig): Promise<CanaryMigrationResult> {
    const startTime = Date.now();
    let currentPercentage = 0;
    const incrementStep = 10; // Increase by 10% each step
    
    try {
      // Start with small percentage
      await this.setCanaryPercentage(config.migrationId, incrementStep);
      currentPercentage = incrementStep;
      
      while (currentPercentage < 100) {
        // Monitor metrics for current percentage
        const metrics = await this.collectCanaryMetrics(
          config.migrationId,
          config.validationMetrics
        );
        
        // Evaluate success criteria
        const evaluation = this.evaluateCanaryMetrics(metrics, config.successThreshold);
        
        if (!evaluation.success) {
          if (config.rollbackOnFailure) {
            await this.rollbackCanaryMigration(config.migrationId);
            return {
              success: false,
              reason: 'Canary metrics failed validation',
              metricsAtFailure: metrics,
              percentageAtFailure: currentPercentage
            };
          } else {
            // Pause and wait for manual intervention
            await this.pauseCanaryMigration(config.migrationId);
            return {
              success: false,
              reason: 'Canary paused for manual review',
              requiresIntervention: true,
              currentPercentage
            };
          }
        }
        
        // Check timeout
        if (Date.now() - startTime > config.maxDuration * 60 * 1000) {
          throw new Error('Canary migration timed out');
        }
        
        // Increase percentage
        currentPercentage = Math.min(100, currentPercentage + incrementStep);
        await this.setCanaryPercentage(config.migrationId, currentPercentage);
        
        // Wait for stabilization
        await new Promise(resolve => setTimeout(resolve, 30000)); // 30 seconds
      }
      
      // Migration completed successfully
      await this.finalizeCanaryMigration(config.migrationId);
      
      return {
        success: true,
        duration: Date.now() - startTime,
        finalMetrics: await this.collectCanaryMetrics(
          config.migrationId,
          config.validationMetrics
        )
      };
      
    } catch (error) {
      if (config.rollbackOnFailure) {
        await this.rollbackCanaryMigration(config.migrationId);
      }
      
      throw error;
    }
  }

  private async setCanaryPercentage(migrationId: string, percentage: number): Promise<void> {
    // Update routing rules to send percentage of traffic to new version
    await supabase.rpc('update_canary_routing', {
      migration_id: migrationId,
      canary_percentage: percentage
    });
    
    // Log the change
    await supabase.from('migration_execution_state').insert({
      migration_id: migrationId,
      step_name: `SetCanaryPercentage${percentage}`,
      step_status: 'COMPLETED',
      new_value: { canary_percentage: percentage }
    });
  }

  private async collectCanaryMetrics(
    migrationId: string,
    metricNames: string[]
  ): Promise<MetricCollection> {
    const metrics: Record<string, any> = {};
    
    for (const metricName of metricNames) {
      switch (metricName) {
        case 'error_rate':
          metrics[metricName] = await this.getErrorRate(migrationId);
          break;
        case 'response_time':
          metrics[metricName] = await this.getResponseTime(migrationId);
          break;
        case 'throughput':
          metrics[metricName] = await this.getThroughput(migrationId);
          break;
        case 'data_consistency':
          metrics[metricName] = await this.getDataConsistencyMetrics(migrationId);
          break;
        default:
          metrics[metricName] = await this.getCustomMetric(migrationId, metricName);
      }
    }
    
    return {
      timestamp: new Date(),
      migrationId,
      metrics
    };
  }

  private evaluateCanaryMetrics(
    metrics: MetricCollection,
    successThreshold: number
  ): { success: boolean; score: number; details: any } {
    let totalScore = 0;
    let weightSum = 0;
    const details: any = {};
    
    // Define metric weights and evaluation logic
    const metricEvaluators: Record<string, (value: any) => { score: number; weight: number }> = {
      error_rate: (value) => ({
        score: value < 0.01 ? 1 : (value < 0.05 ? 0.7 : 0),
        weight: 0.4
      }),
      response_time: (value) => ({
        score: value < 100 ? 1 : (value < 500 ? 0.8 : (value < 1000 ? 0.5 : 0)),
        weight: 0.3
      }),
      throughput: (value) => ({
        score: value > 0.95 ? 1 : (value > 0.8 ? 0.8 : 0),
        weight: 0.2
      }),
      data_consistency: (value) => ({
        score: value > 0.99 ? 1 : 0,
        weight: 0.1
      })
    };
    
    for (const [metricName, metricValue] of Object.entries(metrics.metrics)) {
      if (metricEvaluators[metricName]) {
        const evaluation = metricEvaluators[metricName](metricValue);
        totalScore += evaluation.score * evaluation.weight;
        weightSum += evaluation.weight;
        details[metricName] = {
          value: metricValue,
          score: evaluation.score,
          weight: evaluation.weight
        };
      }
    }
    
    const finalScore = weightSum > 0 ? totalScore / weightSum : 0;
    
    return {
      success: finalScore >= successThreshold,
      score: finalScore,
      details
    };
  }
}
```

This comprehensive migration system provides:

1. **Advanced migration tracking** with detailed execution state
2. **Sophisticated transformation pipelines** for complex data migrations  
3. **Breaking change detection** and compatibility validation
4. **Comprehensive safety checks** including data integrity and performance impact
5. **Zero-downtime blue-green migrations** for critical systems
6. **Canary migration patterns** with automatic rollback capabilities
7. **Complete audit trail** for all migration operations

The system ensures safe, reliable knowledge graph evolution while maintaining system availability and data integrity throughout the migration process.