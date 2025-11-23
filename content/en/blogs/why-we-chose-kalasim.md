---
title: "Why We Chose Kalasim: Our Journey Finding the Right Simulation Engine"
description: "How we evaluated discrete event simulation libraries for AIMatrix digital twins, why Kalasim won out over alternatives, and the integration challenges we faced. A practical comparison of simulation frameworks."
date: 2025-06-15
author: "Elena Rodriguez"
authorTitle: "Simulation Systems Architect"
readTime: "9 min read"
categories: ["Engineering", "Digital Twins", "Simulation"]
tags: ["Kalasim", "Simulation", "Digital Twins", "Kotlin", "SimPy"]
image: "/images/blog/kalasim-simulation.jpg"
featured: false
---

When we started building digital twins for AIMatrix, we knew we needed a robust discrete event simulation engine. What we didn't know was how hard it would be to find the right one.

After evaluating six different simulation frameworks over three months, we settled on Kalasim. Here's the story of why, including the dead ends, surprises, and lessons learned along the way.

## The Digital Twin Challenge

Our digital twins needed to simulate complex real-world processes: manufacturing lines, supply chains, customer service flows. These aren't simple systems - they have:

- Multiple interacting entities (machines, people, orders, inventory)
- Stochastic events (equipment failures, demand spikes)
- Resource constraints (limited capacity, shared equipment)
- Complex scheduling and prioritization logic

We needed a simulation engine that could handle this complexity while integrating with our Kotlin-based AMX Engine.

## The Evaluation Journey

**Initial Requirements:**
- Discrete event simulation capabilities
- Good performance (millions of events)
- Integration with existing Kotlin/JVM ecosystem
- Active community and documentation
- Extensibility for custom behaviors

**The Contenders:**

1. **SimPy (Python)** - Popular, well-documented
2. **SUMO (C++)** - High-performance, traffic-focused
3. **MASON (Java)** - Academic pedigree, agent-based
4. **Kalasim (Kotlin)** - New, promising, JVM-native
5. **Arena/AnyLogic** - Commercial solutions
6. **Custom-built** - Roll our own

## Why SimPy Didn't Work for Us

SimPy was our first choice. It's mature, has great documentation, and a large community. Our initial prototype looked promising:

```python
import simpy

def manufacturing_line(env, name, repair_time):
    """A manufacturing line that breaks down and gets repaired"""
    while True:
        # Work until failure
        working_time = random.exponential(100.0)
        yield env.timeout(working_time)
        
        print(f'{name} broken at {env.now}')
        
        # Request repair
        with repair_crew.request() as req:
            yield req
            yield env.timeout(repair_time)
            print(f'{name} repaired at {env.now}')

# Set up and run
env = simpy.Environment()
repair_crew = simpy.Resource(env, capacity=2)
env.process(manufacturing_line(env, 'Line1', 30))
env.run(until=1000)
```

**The problems:**
- **Language barriers:** Our team was primarily JVM-based. Context switching between Python and Kotlin created friction.
- **Integration complexity:** Getting Python simulation results back into our Kotlin agents required complex serialization.
- **Performance concerns:** For large-scale simulations, Python's GIL became a bottleneck.
- **Deployment overhead:** Managing Python dependencies in our Kubernetes-based infrastructure added complexity.

## The MASON Experiment

MASON seemed perfect - Java-based, agent-oriented, from George Mason University with solid academic backing.

```java
public class ManufacturingSimulation extends SimState {
    public Network productionNetwork = new Network();
    
    public void start() {
        super.start();
        
        // Create manufacturing agents
        for (int i = 0; i < 10; i++) {
            ProductionLine line = new ProductionLine();
            schedule.scheduleRepeating(line);
            productionNetwork.addNode(line);
        }
    }
}
```

**Why it didn't stick:**
- **Steep learning curve:** MASON's agent-based approach required rethinking our simulation model design.
- **Limited discrete event features:** Primarily designed for agent-based modeling, not the process-oriented simulations we needed.
- **Documentation gaps:** Academic documentation, but limited practical examples for business process simulation.
- **Integration friction:** Java interop with Kotlin worked, but wasn't as seamless as pure Kotlin.

## Enter Kalasim

Kalasim caught our attention because it was built specifically for discrete event simulation in Kotlin. The syntax looked clean:

```kotlin
class ManufacturingLine : Component() {
    private val mtbf = 100.0 // Mean time between failures
    private val mttr = 10.0  // Mean time to repair
    
    override fun process() = sequence {
        while (true) {
            // Operating state
            val operatingTime = exponential(mtbf)
            hold(operatingTime)
            
            log("Line failed at ${now}")
            
            // Request repair resource
            request(repairCrew) {
                hold(exponential(mttr))
            }
            
            log("Line repaired at ${now}")
        }
    }
}

// Set up simulation
val env = Environment().apply {
    val repairCrew = Resource(capacity = 2)
    
    repeat(5) {
        ManufacturingLine().apply {
            activate()
        }
    }
}

env.run(until = 1000.0)
```

**What attracted us:**
- **Native Kotlin:** Perfect language alignment with our existing codebase
- **Sequence-based processes:** Intuitive way to model complex workflows
- **Resource management:** Built-in support for constrained resources
- **Statistics collection:** Automatic collection of simulation metrics
- **Coroutine integration:** Leveraged Kotlin's async capabilities

## The Integration Reality

Getting Kalasim working in production wasn't smooth sailing. Here are the challenges we hit:

### Performance Tuning

Our first large-scale simulation (simulating a week of operations for a 50-machine factory) was painfully slow:

```kotlin
// Our initial naive approach
class Factory : Component() {
    val machines = (1..50).map { MachineSimulation(it) }
    
    override fun process() = sequence {
        machines.forEach { it.activate() }
        
        // This created too many simultaneous events
        while (true) {
            hold(1.0) // Check every minute
            collectMetrics() // Expensive operation
        }
    }
}
```

**Optimization strategies that worked:**

1. **Event batching:** Group similar events together
```kotlin
class OptimizedFactory : Component() {
    private val eventBatch = mutableListOf<SimulationEvent>()
    
    override fun process() = sequence {
        while (true) {
            hold(60.0) // Batch events every hour
            processBatchedEvents()
        }
    }
}
```

2. **Selective monitoring:** Only track metrics we actually need
```kotlin
class MachineMonitor : Component() {
    override fun process() = sequence {
        while (true) {
            // Only sample key metrics, not everything
            if (currentTime % 480.0 < 1.0) { // Once per 8-hour shift
                recordMetrics()
            }
            hold(60.0)
        }
    }
}
```

### Memory Management

Long-running simulations led to memory accumulation. Kalasim's event scheduling could pile up events in memory:

```kotlin
class MemoryEfficientSimulation : Component() {
    private val eventHistory = RingBuffer<Event>(capacity = 1000)
    
    override fun process() = sequence {
        while (true) {
            // Process events
            processCurrentEvents()
            
            // Clean up old events periodically
            if (now % 1440.0 < 1.0) { // Once per day
                cleanupOldEvents()
            }
            
            hold(1.0)
        }
    }
}
```

### Custom Distribution Support

Kalasim's built-in distributions didn't cover all our use cases. We needed custom failure distributions based on real equipment data:

```kotlin
class CustomDistribution(private val historicalData: List<Double>) : Distribution {
    private val empiricalCDF = buildCDF(historicalData)
    
    override fun sample(): Double {
        val u = Random.nextDouble()
        return invertCDF(empiricalCDF, u)
    }
}

class RealisticMachine : Component() {
    private val failureDistribution = CustomDistribution(realFailureData)
    
    override fun process() = sequence {
        while (true) {
            val timeToFailure = failureDistribution.sample()
            hold(timeToFailure)
            
            // Handle failure...
        }
    }
}
```

## Integration with AMX Engine

The biggest win was integrating Kalasim simulations directly with our AI agents:

```kotlin
class DigitalTwinAgent(private val simulation: Environment) : Agent {
    
    suspend fun predictOutcome(scenario: Scenario): PredictionResult {
        // Configure simulation based on scenario
        val simConfig = createSimulationConfig(scenario)
        
        // Run simulation
        val results = withContext(Dispatchers.Default) {
            simulation.runWithConfig(simConfig)
        }
        
        // Return predictions to agent
        return PredictionResult(
            expectedThroughput = results.averageThroughput,
            bottlenecks = results.identifiedBottlenecks,
            recommendations = generateRecommendations(results)
        )
    }
}
```

This allowed our agents to run quick "what-if" simulations to inform their decisions.

## Current Limitations and Workarounds

**What we're still struggling with:**

1. **Debugging complex models:** When simulations produce unexpected results, tracing the cause through thousands of events is challenging.

2. **Visualization:** Kalasim has limited built-in visualization. We built custom dashboards for monitoring simulation runs.

3. **Model validation:** Ensuring our simulations accurately represent reality requires constant calibration against real-world data.

4. **Documentation gaps:** As a newer framework, some advanced use cases lack documentation. We've contributed back several examples.

**Our workarounds:**

```kotlin
class DebuggableSimulation : Environment() {
    private val eventTrace = mutableListOf<TracedEvent>()
    
    override fun schedule(event: Event) {
        if (debugMode) {
            eventTrace.add(TracedEvent(event, currentStackTrace()))
        }
        super.schedule(event)
    }
    
    fun analyzeProblem(timeRange: ClosedRange<Double>): DebugReport {
        val relevantEvents = eventTrace.filter { it.time in timeRange }
        return DebugReport(
            eventSequence = relevantEvents,
            possibleCauses = identifyAnomalies(relevantEvents)
        )
    }
}
```

## Would We Choose Kalasim Again?

Yes, with caveats. For our specific use case - discrete event simulation integrated with Kotlin-based AI systems - Kalasim was the right choice. The language alignment and seamless integration with our existing code made it worth the rough edges.

**Choose Kalasim if:**
- You're already in the JVM ecosystem
- You need discrete event simulation (not agent-based modeling)
- You can invest time in learning a newer framework
- Integration with your existing codebase is important

**Look elsewhere if:**
- You need battle-tested stability (SimPy is more mature)
- You want extensive built-in visualization
- You're doing primarily agent-based modeling
- You need commercial support

## What's Next

We're working on:
- **Better debugging tools:** Custom visualization and tracing capabilities
- **Model validation frameworks:** Automated comparison against real-world data
- **Performance optimization:** Exploring parallel execution for large simulations
- **Contributing back:** Sharing our extensions and improvements with the Kalasim community

Building digital twins with simulation engines is complex, regardless of which tool you choose. Kalasim gave us the foundation we needed, but success required significant engineering investment to make it production-ready.

The payoff has been worth it - our agents can now predict outcomes, identify bottlenecks, and recommend optimizations based on sophisticated simulation models. That capability is transforming how our customers use AIMatrix for process optimization. As we evolve toward Enterprise Agentic Twins—autonomous digital representations that can simulate, predict, and optimize entire organizational processes—the simulation capabilities we've built with Kalasim provide the foundational "what-if" reasoning that enables these systems to make informed autonomous decisions. The journey from basic digital twins to fully agentic Enterprise Twins requires exactly this kind of robust simulation infrastructure.