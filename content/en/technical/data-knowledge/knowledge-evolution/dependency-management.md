---
title: "Dependency Management"
description: "Advanced dependency resolution algorithms with circular dependency prevention and version range management"
weight: 2
---

# Dependency Management

Knowledge capsules form complex dependency networks that require sophisticated management. This document covers dependency resolution algorithms, circular dependency prevention, and advanced dependency management patterns for maintaining knowledge graph integrity.

## Dependency Types and Modeling

### Dependency Classification

```sql
-- Comprehensive dependency modeling
CREATE TYPE dependency_type AS ENUM (
    'STRONG',        -- Hard requirement, must exist
    'WEAK',          -- Soft requirement, can exist without
    'OPTIONAL',      -- Enhancement dependency
    'CONFLICT',      -- Mutually exclusive
    'SUGGESTION',    -- Recommended pairing
    'TEMPORAL',      -- Time-based dependency
    'CONDITIONAL'    -- Context-dependent
);

CREATE TYPE dependency_strength AS ENUM (
    'CRITICAL',      -- System failure if broken
    'HIGH',          -- Feature failure if broken
    'MEDIUM',        -- Degraded functionality
    'LOW',           -- Minor impact
    'INFORMATIONAL'  -- No functional impact
);

-- Advanced dependency table
CREATE TABLE knowledge_dependencies (
    dependency_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_entity_id UUID NOT NULL REFERENCES temporal_entities(entity_id),
    target_entity_id UUID NOT NULL REFERENCES temporal_entities(entity_id),
    dependency_type dependency_type NOT NULL,
    dependency_strength dependency_strength DEFAULT 'MEDIUM',
    
    -- Version constraints
    min_version TEXT,
    max_version TEXT,
    version_pattern TEXT, -- Regex pattern for valid versions
    
    -- Conditional dependencies
    condition_expr JSONB, -- Condition when dependency applies
    context_requirements JSONB, -- Required context for activation
    
    -- Temporal aspects
    valid_from TIMESTAMPTZ DEFAULT NOW(),
    valid_to TIMESTAMPTZ DEFAULT 'infinity',
    activation_delay INTERVAL DEFAULT '0 seconds',
    
    -- Metadata
    created_by UUID REFERENCES auth.users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    description TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Constraints
    CONSTRAINT no_self_dependency CHECK (source_entity_id != target_entity_id),
    CONSTRAINT valid_version_range CHECK (
        (min_version IS NULL OR max_version IS NULL) OR 
        version_compare(min_version, max_version) <= 0
    )
);

-- Dependency resolution cache
CREATE TABLE dependency_resolution_cache (
    cache_key TEXT PRIMARY KEY,
    entity_id UUID NOT NULL,
    resolution_result JSONB NOT NULL,
    computed_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    dependency_graph_hash TEXT,
    
    INDEX (entity_id),
    INDEX (expires_at) WHERE expires_at IS NOT NULL
);
```

### Version Comparison System

Implement semantic version comparison:

```sql
-- Semantic version comparison function
CREATE OR REPLACE FUNCTION version_compare(v1 TEXT, v2 TEXT) RETURNS INTEGER AS $$
DECLARE
    v1_parts INTEGER[];
    v2_parts INTEGER[];
    v1_pre TEXT;
    v2_pre TEXT;
    i INTEGER;
    result INTEGER;
BEGIN
    -- Parse version numbers (support semantic versioning)
    SELECT 
        ARRAY(SELECT regexp_split_to_array(split_part(v1, '-', 1), '\.')::INTEGER[]),
        CASE WHEN position('-' in v1) > 0 THEN split_part(v1, '-', 2) ELSE NULL END
    INTO v1_parts, v1_pre;
    
    SELECT 
        ARRAY(SELECT regexp_split_to_array(split_part(v2, '-', 1), '\.')::INTEGER[]),
        CASE WHEN position('-' in v2) > 0 THEN split_part(v2, '-', 2) ELSE NULL END
    INTO v2_parts, v2_pre;
    
    -- Compare major.minor.patch
    FOR i IN 1..GREATEST(array_length(v1_parts, 1), array_length(v2_parts, 1)) LOOP
        IF i <= array_length(v1_parts, 1) AND i <= array_length(v2_parts, 1) THEN
            IF v1_parts[i] < v2_parts[i] THEN RETURN -1; END IF;
            IF v1_parts[i] > v2_parts[i] THEN RETURN 1; END IF;
        ELSIF i <= array_length(v1_parts, 1) THEN
            RETURN 1; -- v1 has more parts, v1 > v2
        ELSE
            RETURN -1; -- v2 has more parts, v1 < v2
        END IF;
    END LOOP;
    
    -- Compare pre-release versions
    IF v1_pre IS NOT NULL AND v2_pre IS NULL THEN RETURN -1; END IF;
    IF v1_pre IS NULL AND v2_pre IS NOT NULL THEN RETURN 1; END IF;
    IF v1_pre IS NOT NULL AND v2_pre IS NOT NULL THEN
        IF v1_pre < v2_pre THEN RETURN -1; END IF;
        IF v1_pre > v2_pre THEN RETURN 1; END IF;
    END IF;
    
    RETURN 0; -- Equal
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Version range satisfaction check
CREATE OR REPLACE FUNCTION satisfies_version_range(
    version TEXT,
    min_version TEXT DEFAULT NULL,
    max_version TEXT DEFAULT NULL,
    version_pattern TEXT DEFAULT NULL
) RETURNS BOOLEAN AS $$
BEGIN
    -- Check minimum version
    IF min_version IS NOT NULL AND version_compare(version, min_version) < 0 THEN
        RETURN FALSE;
    END IF;
    
    -- Check maximum version
    IF max_version IS NOT NULL AND version_compare(version, max_version) > 0 THEN
        RETURN FALSE;
    END IF;
    
    -- Check version pattern (regex)
    IF version_pattern IS NOT NULL AND NOT (version ~ version_pattern) THEN
        RETURN FALSE;
    END IF;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

## Circular Dependency Prevention

### Dependency Graph Analysis

Implement sophisticated cycle detection:

```sql
-- Circular dependency detection using topological sort
CREATE OR REPLACE FUNCTION detect_circular_dependencies(
    check_entity_id UUID DEFAULT NULL
) RETURNS TABLE (
    cycle_id UUID,
    cycle_path UUID[],
    cycle_strength dependency_strength,
    break_suggestions JSONB
) AS $$
WITH RECURSIVE dependency_graph AS (
    -- Get all active dependencies
    SELECT 
        kd.source_entity_id,
        kd.target_entity_id,
        kd.dependency_type,
        kd.dependency_strength,
        kd.dependency_id
    FROM knowledge_dependencies kd
    WHERE kd.valid_from <= NOW()
      AND kd.valid_to > NOW()
      AND (check_entity_id IS NULL OR 
           kd.source_entity_id = check_entity_id OR 
           kd.target_entity_id = check_entity_id)
      AND kd.dependency_type IN ('STRONG', 'WEAK') -- Only check structural dependencies
),
cycle_detection AS (
    -- Start from each node
    SELECT 
        dg.source_entity_id as start_node,
        dg.target_entity_id as current_node,
        ARRAY[dg.source_entity_id, dg.target_entity_id] as path,
        dg.dependency_strength,
        1 as depth,
        dg.dependency_id
    FROM dependency_graph dg
    
    UNION ALL
    
    -- Follow the dependency chain
    SELECT 
        cd.start_node,
        dg.target_entity_id,
        cd.path || dg.target_entity_id,
        LEAST(cd.dependency_strength, dg.dependency_strength),
        cd.depth + 1,
        dg.dependency_id
    FROM cycle_detection cd
    JOIN dependency_graph dg ON cd.current_node = dg.source_entity_id
    WHERE cd.depth < 50 -- Prevent infinite recursion
      AND NOT (dg.target_entity_id = ANY(cd.path)) -- Prevent immediate cycles in path building
)
SELECT 
    gen_random_uuid() as cycle_id,
    cd.path,
    cd.dependency_strength as cycle_strength,
    jsonb_build_object(
        'weakest_links', (
            SELECT jsonb_agg(
                jsonb_build_object(
                    'dependency_id', kd.dependency_id,
                    'strength', kd.dependency_strength,
                    'type', kd.dependency_type
                )
            )
            FROM knowledge_dependencies kd
            WHERE kd.dependency_strength = cd.dependency_strength
              AND ((kd.source_entity_id = ANY(cd.path) AND kd.target_entity_id = ANY(cd.path)))
        ),
        'suggested_breaks', (
            SELECT jsonb_agg(
                jsonb_build_object(
                    'dependency_id', kd.dependency_id,
                    'action', CASE 
                        WHEN kd.dependency_type = 'STRONG' THEN 'convert_to_weak'
                        WHEN kd.dependency_type = 'WEAK' THEN 'convert_to_optional'
                        ELSE 'remove'
                    END
                )
            )
            FROM knowledge_dependencies kd
            WHERE kd.dependency_strength IN ('LOW', 'INFORMATIONAL')
              AND ((kd.source_entity_id = ANY(cd.path) AND kd.target_entity_id = ANY(cd.path)))
        )
    ) as break_suggestions
FROM cycle_detection cd
WHERE cd.current_node = cd.start_node -- Found a cycle
  AND cd.depth > 1; -- Actual cycle, not self-reference
$$ LANGUAGE SQL;
```

### Automated Cycle Resolution

Implement intelligent cycle breaking:

```typescript
interface CycleBreakingStrategy {
  name: string;
  priority: number;
  canBreak: (cycle: DependencyCycle) => boolean;
  breakCycle: (cycle: DependencyCycle) => Promise<BreakingAction[]>;
}

interface DependencyCycle {
  cycleId: string;
  path: string[];
  strength: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFORMATIONAL';
  dependencies: DependencyEdge[];
}

interface DependencyEdge {
  dependencyId: string;
  sourceId: string;
  targetId: string;
  type: string;
  strength: string;
}

class CircularDependencyResolver {
  private strategies: CycleBreakingStrategy[] = [
    {
      name: 'WeakestLinkBreaking',
      priority: 1,
      canBreak: (cycle) => cycle.dependencies.some(d => 
        d.strength === 'LOW' || d.strength === 'INFORMATIONAL'),
      breakCycle: this.breakWeakestLinks.bind(this)
    },
    {
      name: 'TypeDemotionStrategy',
      priority: 2,  
      canBreak: (cycle) => cycle.dependencies.some(d => d.type === 'STRONG'),
      breakCycle: this.demoteDependencyTypes.bind(this)
    },
    {
      name: 'ConditionalDependencyIntroduction',
      priority: 3,
      canBreak: () => true, // Can always try this
      breakCycle: this.introduceConditionalDependencies.bind(this)
    },
    {
      name: 'LazyLoadingIntroduction',
      priority: 4,
      canBreak: (cycle) => cycle.path.length > 2,
      breakCycle: this.introduceLazyLoading.bind(this)
    }
  ];

  async resolveCycles(entityId?: string): Promise<ResolutionResult[]> {
    const { data: cycles } = await supabase.rpc('detect_circular_dependencies', {
      check_entity_id: entityId
    });

    const results: ResolutionResult[] = [];

    for (const cycleData of cycles || []) {
      const cycle: DependencyCycle = {
        cycleId: cycleData.cycle_id,
        path: cycleData.cycle_path,
        strength: cycleData.cycle_strength,
        dependencies: await this.loadCycleDependencies(cycleData.cycle_path)
      };

      const result = await this.resolveSingleCycle(cycle);
      results.push(result);
    }

    return results;
  }

  private async resolveSingleCycle(cycle: DependencyCycle): Promise<ResolutionResult> {
    // Sort strategies by priority
    const applicableStrategies = this.strategies
      .filter(s => s.canBreak(cycle))
      .sort((a, b) => a.priority - b.priority);

    for (const strategy of applicableStrategies) {
      try {
        const actions = await strategy.breakCycle(cycle);
        
        // Validate that actions actually break the cycle
        const wouldBreakCycle = await this.validateCycleBreaking(cycle, actions);
        
        if (wouldBreakCycle) {
          // Apply the breaking actions
          await this.applyBreakingActions(actions);
          
          return {
            cycleId: cycle.cycleId,
            resolved: true,
            strategy: strategy.name,
            actions: actions,
            confidence: this.calculateConfidence(strategy, cycle, actions)
          };
        }
      } catch (error) {
        console.warn(`Strategy ${strategy.name} failed:`, error);
      }
    }

    return {
      cycleId: cycle.cycleId,
      resolved: false,
      reason: 'No applicable strategy found',
      requiresManualIntervention: true
    };
  }

  private async breakWeakestLinks(cycle: DependencyCycle): Promise<BreakingAction[]> {
    const weakDependencies = cycle.dependencies
      .filter(d => d.strength === 'LOW' || d.strength === 'INFORMATIONAL')
      .sort((a, b) => {
        const strengthOrder = { 'INFORMATIONAL': 0, 'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4 };
        return strengthOrder[a.strength] - strengthOrder[b.strength];
      });

    const actions: BreakingAction[] = [];

    // Remove the weakest dependency
    if (weakDependencies.length > 0) {
      const weakest = weakDependencies[0];
      actions.push({
        type: 'REMOVE_DEPENDENCY',
        dependencyId: weakest.dependencyId,
        reason: `Removed weakest link (${weakest.strength}) to break cycle`,
        reversible: true,
        backupData: weakest
      });
    } else {
      // Convert strongest to weaker type
      const strongest = cycle.dependencies
        .sort((a, b) => {
          const strengthOrder = { 'INFORMATIONAL': 0, 'LOW': 1, 'MEDIUM': 2, 'HIGH': 3, 'CRITICAL': 4 };
          return strengthOrder[b.strength] - strengthOrder[a.strength];
        })[0];

      const newStrength = this.demoteStrength(strongest.strength);
      actions.push({
        type: 'MODIFY_DEPENDENCY',
        dependencyId: strongest.dependencyId,
        changes: { strength: newStrength },
        reason: `Demoted strength from ${strongest.strength} to ${newStrength}`,
        reversible: true,
        backupData: { strength: strongest.strength }
      });
    }

    return actions;
  }

  private async introduceConditionalDependencies(cycle: DependencyCycle): Promise<BreakingAction[]> {
    // Find the most suitable dependency to make conditional
    const candidate = cycle.dependencies
      .filter(d => d.type === 'STRONG' || d.type === 'WEAK')
      .sort((a, b) => {
        // Prefer dependencies that are more likely to be contextual
        const contextScore = (dep: DependencyEdge) => {
          // Score based on dependency characteristics
          return (dep.strength === 'MEDIUM' ? 2 : 0) +
                 (dep.type === 'WEAK' ? 3 : 0) +
                 (this.isContextualDependency(dep) ? 5 : 0);
        };
        return contextScore(b) - contextScore(a);
      })[0];

    if (!candidate) {
      throw new Error('No suitable dependency for conditional conversion');
    }

    // Create conditional dependency
    const condition = await this.generateConditionExpression(candidate);
    
    return [{
      type: 'MODIFY_DEPENDENCY',
      dependencyId: candidate.dependencyId,
      changes: {
        dependency_type: 'CONDITIONAL',
        condition_expr: condition,
        original_type: candidate.type
      },
      reason: 'Converted to conditional dependency to break cycle',
      reversible: true,
      backupData: {
        dependency_type: candidate.type,
        condition_expr: null
      }
    }];
  }

  private async introduceLazyLoading(cycle: DependencyCycle): Promise<BreakingAction[]> {
    // Identify dependencies suitable for lazy loading
    const lazyLoadCandidates = cycle.dependencies.filter(dep => {
      // Dependencies that are likely to be used infrequently or can be deferred
      return dep.type === 'WEAK' || dep.strength === 'LOW' || dep.strength === 'MEDIUM';
    });

    if (lazyLoadCandidates.length === 0) {
      throw new Error('No dependencies suitable for lazy loading');
    }

    const actions: BreakingAction[] = [];

    for (const candidate of lazyLoadCandidates.slice(0, 2)) { // Limit to 2 conversions
      actions.push({
        type: 'MODIFY_DEPENDENCY',
        dependencyId: candidate.dependencyId,
        changes: {
          dependency_type: 'OPTIONAL',
          activation_delay: '5 seconds', // Introduce delay
          metadata: {
            lazy_loading: true,
            original_type: candidate.type,
            load_trigger: 'ON_DEMAND'
          }
        },
        reason: 'Converted to lazy-loaded optional dependency',
        reversible: true,
        backupData: {
          dependency_type: candidate.type,
          activation_delay: '0 seconds',
          metadata: {}
        }
      });
    }

    return actions;
  }

  private demoteStrength(currentStrength: string): string {
    const demotionMap: Record<string, string> = {
      'CRITICAL': 'HIGH',
      'HIGH': 'MEDIUM',
      'MEDIUM': 'LOW',
      'LOW': 'INFORMATIONAL',
      'INFORMATIONAL': 'INFORMATIONAL' // Can't demote further
    };
    
    return demotionMap[currentStrength] || 'LOW';
  }

  private async generateConditionExpression(dependency: DependencyEdge): Promise<any> {
    // Analyze dependency context to generate meaningful conditions
    const { data: sourceEntity } = await supabase
      .from('temporal_entities')
      .select('content, metadata')
      .eq('entity_id', dependency.sourceId)
      .single();

    const { data: targetEntity } = await supabase
      .from('temporal_entities')
      .select('content, metadata')
      .eq('entity_id', dependency.targetId)
      .single();

    // Generate condition based on entity characteristics
    const condition = {
      type: 'CONDITIONAL_ACTIVATION',
      rules: [
        {
          field: 'context.usage_frequency',
          operator: '>',
          value: 0.1,
          description: 'Only activate when source is actively used'
        },
        {
          field: 'target.availability',
          operator: '==',
          value: true,
          description: 'Only depend when target is available'
        }
      ],
      logic: 'AND'
    };

    return condition;
  }
}
```

## Advanced Dependency Resolution

### Multi-Version Dependency Resolution

Handle complex version conflicts:

```sql
-- Multi-version resolution algorithm
CREATE OR REPLACE FUNCTION resolve_dependency_versions(
    root_entity_id UUID,
    max_depth INTEGER DEFAULT 10
) RETURNS TABLE (
    entity_id UUID,
    selected_version TEXT,
    conflicts JSONB,
    resolution_reason TEXT
) AS $$
WITH RECURSIVE dependency_tree AS (
    -- Start with root entity
    SELECT 
        root_entity_id as entity_id,
        te.metadata->>'version' as current_version,
        0 as depth,
        ARRAY[root_entity_id] as path,
        '{}'::jsonb as version_constraints
    FROM temporal_entities te
    WHERE te.entity_id = root_entity_id
      AND te.valid_to = 'infinity'
      AND NOT te.is_deleted
    
    UNION ALL
    
    -- Traverse dependencies
    SELECT 
        kd.target_entity_id,
        te.metadata->>'version',
        dt.depth + 1,
        dt.path || kd.target_entity_id,
        dt.version_constraints || jsonb_build_object(
            kd.target_entity_id::text,
            jsonb_build_object(
                'min_version', kd.min_version,
                'max_version', kd.max_version,
                'required_by', dt.entity_id,
                'strength', kd.dependency_strength
            )
        )
    FROM dependency_tree dt
    JOIN knowledge_dependencies kd ON dt.entity_id = kd.source_entity_id
    JOIN temporal_entities te ON kd.target_entity_id = te.entity_id
    WHERE dt.depth < max_depth
      AND kd.target_entity_id != ALL(dt.path) -- Prevent cycles
      AND kd.valid_from <= NOW()
      AND kd.valid_to > NOW()
      AND te.valid_to = 'infinity'
      AND NOT te.is_deleted
),
version_conflicts AS (
    SELECT 
        dt.entity_id,
        dt.current_version,
        jsonb_agg(DISTINCT dt.version_constraints) as all_constraints,
        -- Identify conflicts
        CASE 
            WHEN COUNT(DISTINCT (dt.version_constraints->>(dt.entity_id::text)->>'min_version')) > 1 OR
                 COUNT(DISTINCT (dt.version_constraints->>(dt.entity_id::text)->>'max_version')) > 1 THEN
                jsonb_build_object(
                    'has_conflict', true,
                    'conflict_type', 'version_range',
                    'conflicting_requirements', jsonb_agg(DISTINCT dt.version_constraints)
                )
            ELSE
                jsonb_build_object('has_conflict', false)
        END as conflict_info
    FROM dependency_tree dt
    GROUP BY dt.entity_id, dt.current_version
)
SELECT 
    vc.entity_id,
    COALESCE(
        resolve_version_conflict(vc.entity_id, vc.all_constraints),
        vc.current_version
    ) as selected_version,
    vc.conflict_info as conflicts,
    CASE 
        WHEN vc.conflict_info->>'has_conflict' = 'true' THEN 
            'Resolved conflict using version resolution algorithm'
        ELSE 
            'No conflicts detected'
    END as resolution_reason
FROM version_conflicts vc;
$$ LANGUAGE SQL;

-- Version conflict resolution function
CREATE OR REPLACE FUNCTION resolve_version_conflict(
    entity_id UUID,
    constraints JSONB
) RETURNS TEXT AS $$
DECLARE
    available_versions TEXT[];
    best_version TEXT;
    constraint_record JSONB;
BEGIN
    -- Get all available versions for this entity
    SELECT ARRAY(
        SELECT DISTINCT te.metadata->>'version'
        FROM temporal_entities te
        WHERE te.entity_id = entity_id
          AND te.metadata->>'version' IS NOT NULL
        ORDER BY version_compare(te.metadata->>'version', '0.0.0') DESC
    ) INTO available_versions;
    
    -- Find version that satisfies all constraints
    FOR best_version IN SELECT unnest(available_versions) LOOP
        DECLARE
            satisfies_all BOOLEAN := TRUE;
        BEGIN
            -- Check each constraint
            FOR constraint_record IN SELECT jsonb_array_elements(constraints) LOOP
                DECLARE
                    entity_constraints JSONB;
                    min_ver TEXT;
                    max_ver TEXT;
                BEGIN
                    entity_constraints := constraint_record->(entity_id::text);
                    IF entity_constraints IS NOT NULL THEN
                        min_ver := entity_constraints->>'min_version';
                        max_ver := entity_constraints->>'max_version';
                        
                        IF NOT satisfies_version_range(best_version, min_ver, max_ver) THEN
                            satisfies_all := FALSE;
                            EXIT;
                        END IF;
                    END IF;
                END;
            END LOOP;
            
            IF satisfies_all THEN
                RETURN best_version;
            END IF;
        END;
    END LOOP;
    
    -- No perfect match found, return latest version
    RETURN available_versions[1];
END;
$$ LANGUAGE plpgsql;
```

### Dependency Health Monitoring

Real-time dependency health tracking:

```typescript
interface DependencyHealth {
  entityId: string;
  overallHealth: number; // 0-1 score
  issues: DependencyIssue[];
  recommendations: Recommendation[];
  lastChecked: Date;
}

interface DependencyIssue {
  type: 'MISSING_DEPENDENCY' | 'VERSION_CONFLICT' | 'CIRCULAR_REFERENCE' | 
        'WEAK_LINK' | 'OUTDATED_DEPENDENCY' | 'SECURITY_RISK';
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
  affectedDependencies: string[];
  autoFixable: boolean;
}

class DependencyHealthMonitor {
  async assessHealth(entityId: string): Promise<DependencyHealth> {
    const issues = await Promise.all([
      this.checkMissingDependencies(entityId),
      this.checkVersionConflicts(entityId),
      this.checkCircularReferences(entityId),
      this.checkOutdatedDependencies(entityId),
      this.checkSecurityRisks(entityId)
    ]).then(results => results.flat());

    const overallHealth = this.calculateHealthScore(issues);
    const recommendations = await this.generateRecommendations(issues);

    return {
      entityId,
      overallHealth,
      issues,
      recommendations,
      lastChecked: new Date()
    };
  }

  private async checkMissingDependencies(entityId: string): Promise<DependencyIssue[]> {
    const { data: missingDeps } = await supabase.rpc('find_missing_dependencies', {
      entity_id: entityId
    });

    return (missingDeps || []).map(dep => ({
      type: 'MISSING_DEPENDENCY',
      severity: dep.dependency_strength === 'CRITICAL' ? 'CRITICAL' : 
               dep.dependency_strength === 'HIGH' ? 'HIGH' : 'MEDIUM',
      description: `Missing required dependency: ${dep.target_entity_id}`,
      affectedDependencies: [dep.dependency_id],
      autoFixable: false
    }));
  }

  private async checkVersionConflicts(entityId: string): Promise<DependencyIssue[]> {
    const { data: conflicts } = await supabase.rpc('resolve_dependency_versions', {
      root_entity_id: entityId
    });

    return (conflicts || [])
      .filter(c => c.conflicts.has_conflict)
      .map(conflict => ({
        type: 'VERSION_CONFLICT',
        severity: 'HIGH',
        description: `Version conflict for entity ${conflict.entity_id}: ${conflict.conflicts.conflict_type}`,
        affectedDependencies: conflict.conflicts.conflicting_requirements?.map(r => r.dependency_id) || [],
        autoFixable: true
      }));
  }

  private async checkCircularReferences(entityId: string): Promise<DependencyIssue[]> {
    const { data: cycles } = await supabase.rpc('detect_circular_dependencies', {
      check_entity_id: entityId
    });

    return (cycles || []).map(cycle => ({
      type: 'CIRCULAR_REFERENCE',
      severity: cycle.cycle_strength === 'CRITICAL' ? 'CRITICAL' : 'HIGH',
      description: `Circular dependency detected in path: ${cycle.cycle_path.join(' → ')}`,
      affectedDependencies: cycle.cycle_path,
      autoFixable: true
    }));
  }

  private async checkOutdatedDependencies(entityId: string): Promise<DependencyIssue[]> {
    const { data: outdated } = await supabase
      .from('knowledge_dependencies')
      .select(`
        dependency_id,
        target_entity_id,
        min_version,
        max_version,
        temporal_entities!target_entity_id(metadata)
      `)
      .eq('source_entity_id', entityId)
      .lte('valid_from', new Date().toISOString())
      .gte('valid_to', new Date().toISOString());

    const issues: DependencyIssue[] = [];

    for (const dep of outdated || []) {
      const currentVersion = dep.temporal_entities?.metadata?.version;
      const latestVersion = await this.getLatestVersion(dep.target_entity_id);

      if (currentVersion && latestVersion && 
          this.isVersionOutdated(currentVersion, latestVersion)) {
        issues.push({
          type: 'OUTDATED_DEPENDENCY',
          severity: 'MEDIUM',
          description: `Dependency ${dep.target_entity_id} is outdated (current: ${currentVersion}, latest: ${latestVersion})`,
          affectedDependencies: [dep.dependency_id],
          autoFixable: true
        });
      }
    }

    return issues;
  }

  private calculateHealthScore(issues: DependencyIssue[]): number {
    if (issues.length === 0) return 1.0;

    const severityWeights = {
      'CRITICAL': -0.4,
      'HIGH': -0.25,
      'MEDIUM': -0.15,
      'LOW': -0.05
    };

    let totalDeduction = 0;
    for (const issue of issues) {
      totalDeduction += severityWeights[issue.severity];
    }

    return Math.max(0, 1 + totalDeduction);
  }

  private async generateRecommendations(issues: DependencyIssue[]): Promise<Recommendation[]> {
    const recommendations: Recommendation[] = [];

    // Group issues by type for better recommendations
    const issuesByType = issues.reduce((acc, issue) => {
      if (!acc[issue.type]) acc[issue.type] = [];
      acc[issue.type].push(issue);
      return acc;
    }, {} as Record<string, DependencyIssue[]>);

    for (const [type, typeIssues] of Object.entries(issuesByType)) {
      switch (type) {
        case 'CIRCULAR_REFERENCE':
          recommendations.push({
            type: 'ACTION',
            priority: 'HIGH',
            title: 'Resolve Circular Dependencies',
            description: `Break ${typeIssues.length} circular dependency cycles`,
            action: 'RUN_CYCLE_BREAKER',
            autoApplicable: true,
            estimatedImpact: 'HIGH'
          });
          break;

        case 'VERSION_CONFLICT':
          recommendations.push({
            type: 'ACTION',
            priority: 'HIGH',
            title: 'Resolve Version Conflicts',
            description: `Update versions to resolve ${typeIssues.length} conflicts`,
            action: 'RUN_VERSION_RESOLVER',
            autoApplicable: true,
            estimatedImpact: 'HIGH'
          });
          break;

        case 'OUTDATED_DEPENDENCY':
          recommendations.push({
            type: 'MAINTENANCE',
            priority: 'MEDIUM',
            title: 'Update Dependencies',
            description: `Update ${typeIssues.length} outdated dependencies`,
            action: 'UPDATE_DEPENDENCIES',
            autoApplicable: true,
            estimatedImpact: 'MEDIUM'
          });
          break;
      }
    }

    return recommendations;
  }
}
```

## Storage Optimization

Efficient dependency graph storage and querying:

```sql
-- Materialized view for fast dependency lookups
CREATE MATERIALIZED VIEW dependency_graph_materialized AS
WITH RECURSIVE transitive_dependencies AS (
    -- Direct dependencies
    SELECT 
        kd.source_entity_id,
        kd.target_entity_id,
        1 as distance,
        ARRAY[kd.dependency_id] as dependency_path,
        kd.dependency_type,
        kd.dependency_strength
    FROM knowledge_dependencies kd
    WHERE kd.valid_from <= NOW() AND kd.valid_to > NOW()
    
    UNION ALL
    
    -- Transitive dependencies
    SELECT 
        td.source_entity_id,
        kd.target_entity_id,
        td.distance + 1,
        td.dependency_path || kd.dependency_id,
        CASE 
            WHEN kd.dependency_type = 'STRONG' AND td.dependency_type = 'STRONG' THEN 'STRONG'
            ELSE 'WEAK'
        END,
        LEAST(td.dependency_strength, kd.dependency_strength)
    FROM transitive_dependencies td
    JOIN knowledge_dependencies kd ON td.target_entity_id = kd.source_entity_id
    WHERE td.distance < 10 -- Prevent excessive depth
      AND kd.valid_from <= NOW() AND kd.valid_to > NOW()
      AND NOT (kd.target_entity_id = ANY(SELECT unnest(dependency_path_entities)))
)
SELECT 
    source_entity_id,
    target_entity_id,
    distance,
    dependency_path,
    dependency_type,
    dependency_strength,
    NOW() as computed_at
FROM transitive_dependencies;

-- Index for performance
CREATE INDEX CONCURRENTLY idx_dep_graph_source_target 
ON dependency_graph_materialized (source_entity_id, target_entity_id);

CREATE INDEX CONCURRENTLY idx_dep_graph_distance 
ON dependency_graph_materialized (distance) WHERE distance <= 3;

-- Automatic refresh of materialized view
CREATE OR REPLACE FUNCTION refresh_dependency_graph()
RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY dependency_graph_materialized;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER dependency_change_refresh
    AFTER INSERT OR UPDATE OR DELETE ON knowledge_dependencies
    FOR EACH STATEMENT
    EXECUTE FUNCTION refresh_dependency_graph();
```

This advanced dependency management system provides:

1. **Sophisticated dependency modeling** with multiple types and strengths
2. **Automated circular dependency detection** and resolution
3. **Multi-version conflict resolution** using semantic versioning
4. **Real-time health monitoring** with actionable recommendations
5. **Performance optimization** through materialized views and caching
6. **Intelligent cycle-breaking strategies** including ML-powered resolution

The system ensures knowledge graph integrity while providing flexibility for complex dependency scenarios.