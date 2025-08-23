---
title: "Web Applications"
description: "Modern web interfaces built with Angular, React, Vue, and Flutter Web, featuring Progressive Web App capabilities, real-time dashboards, and responsive design for AI agent management"
weight: 3
date: 2025-08-23
toc: true
tags: ["web", "pwa", "angular", "react", "vue", "flutter", "dashboard", "responsive"]
---

# AIMatrix Web Applications

## Modern Web Interfaces for Enterprise AI Management

AIMatrix Web Applications deliver powerful, responsive web interfaces for AI agent management and monitoring across all modern browsers. Built with cutting-edge web technologies and Progressive Web App capabilities, these applications provide desktop-class functionality with offline-first design and real-time synchronization.

## Multi-Framework Approach

Our web applications are built using a framework-agnostic architecture, allowing organizations to choose their preferred technology stack:

### 🅰️ **Angular Applications**
Enterprise-grade applications with TypeScript, RxJS, and Angular Material

### ⚛️ **React Applications**  
High-performance interfaces with modern React hooks and Material-UI

### 🟢 **Vue.js Applications**
Intuitive and flexible interfaces with Vue 3 Composition API

### 🐦 **Flutter Web Applications**
Cross-platform consistency with native-feeling performance

## Architecture Overview

```mermaid
graph TB
    subgraph "Presentation Layer"
        ANGULAR[Angular App]
        REACT[React App]
        VUE[Vue App]
        FLUTTER[Flutter Web]
    end
    
    subgraph "Progressive Web App Layer"
        SW[Service Worker]
        CACHE[Cache API]
        PUSH[Push Notifications]
        SYNC[Background Sync]
    end
    
    subgraph "State Management"
        ANGULAR_STATE[NgRx Store]
        REACT_STATE[Redux Toolkit]
        VUE_STATE[Pinia Store]
        FLUTTER_STATE[Riverpod]
    end
    
    subgraph "Communication Layer"
        WS[WebSocket Client]
        REST[REST Client]
        GRAPHQL[GraphQL Client]
        REALTIME[Supabase Realtime]
    end
    
    subgraph "Backend Services"
        SUPABASE[Supabase Backend]
        MCP[MCP Servers]
        EDGE[Edge Functions]
    end
    
    Presentation Layer --> Progressive Web App Layer
    Presentation Layer --> State Management
    State Management --> Communication Layer
    Communication Layer --> Backend Services
    
    Progressive Web App Layer --> Backend Services
```

## Progressive Web App Features

### Service Worker Implementation
```typescript
// Service Worker for offline functionality and caching
const CACHE_NAME = 'aimatrix-web-v1'
const STATIC_CACHE = 'aimatrix-static-v1'
const DYNAMIC_CACHE = 'aimatrix-dynamic-v1'

const STATIC_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  '/assets/css/app.css',
  '/assets/js/app.js',
  '/assets/icons/icon-192x192.png',
  '/assets/icons/icon-512x512.png'
]

// Install event - cache static files
self.addEventListener('install', (event: ExtendableEvent) => {
  console.log('Service Worker installing...')
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(cache => {
        console.log('Caching static files')
        return cache.addAll(STATIC_FILES)
      })
      .then(() => self.skipWaiting())
  )
})

// Activate event - clean up old caches
self.addEventListener('activate', (event: ExtendableEvent) => {
  console.log('Service Worker activating...')
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(name => name !== STATIC_CACHE && name !== DYNAMIC_CACHE)
            .map(name => caches.delete(name))
        )
      })
      .then(() => self.clients.claim())
  )
})

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event: FetchEvent) => {
  const { request } = event
  const url = new URL(request.url)
  
  // Handle API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(handleApiRequest(request))
    return
  }
  
  // Handle static assets
  if (STATIC_FILES.includes(url.pathname)) {
    event.respondWith(
      caches.match(request)
        .then(response => response || fetch(request))
    )
    return
  }
  
  // Handle dynamic content
  event.respondWith(handleDynamicRequest(request))
})

async function handleApiRequest(request: Request): Promise<Response> {
  try {
    // Try network first for API requests
    const networkResponse = await fetch(request)
    
    // Cache successful responses
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE)
      cache.put(request, networkResponse.clone())
    }
    
    return networkResponse
    
  } catch (error) {
    // Fallback to cache for offline support
    const cachedResponse = await caches.match(request)
    
    if (cachedResponse) {
      return cachedResponse
    }
    
    // Return offline response
    return new Response(
      JSON.stringify({ error: 'Offline - cached data not available' }),
      {
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    )
  }
}

async function handleDynamicRequest(request: Request): Promise<Response> {
  try {
    const networkResponse = await fetch(request)
    
    // Cache successful responses
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE)
      cache.put(request, networkResponse.clone())
    }
    
    return networkResponse
    
  } catch (error) {
    // Serve from cache
    const cachedResponse = await caches.match(request)
    
    if (cachedResponse) {
      return cachedResponse
    }
    
    // Fallback to offline page
    return caches.match('/offline.html') || 
           new Response('Offline', { status: 503 })
  }
}

// Background sync for queued actions
self.addEventListener('sync', (event: any) => {
  if (event.tag === 'background-sync-agents') {
    event.waitUntil(syncPendingAgentUpdates())
  }
})

async function syncPendingAgentUpdates() {
  const cache = await caches.open(DYNAMIC_CACHE)
  const requests = await cache.keys()
  
  // Find pending updates
  const pendingUpdates = requests.filter(req => 
    req.url.includes('/api/agents') && req.method === 'PUT'
  )
  
  // Sync each pending update
  for (const request of pendingUpdates) {
    try {
      const response = await fetch(request)
      if (response.ok) {
        // Remove from cache after successful sync
        await cache.delete(request)
      }
    } catch (error) {
      console.error('Failed to sync update:', error)
    }
  }
}
```

### Web App Manifest
```json
{
  "name": "AIMatrix Web Application",
  "short_name": "AIMatrix",
  "description": "Enterprise AI Agent Management Platform",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#000000",
  "theme_color": "#00ff41",
  "orientation": "portrait-primary",
  "scope": "/",
  "lang": "en-US",
  
  "icons": [
    {
      "src": "/assets/icons/icon-72x72.png",
      "sizes": "72x72",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/assets/icons/icon-96x96.png",
      "sizes": "96x96",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/assets/icons/icon-128x128.png",
      "sizes": "128x128",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/assets/icons/icon-144x144.png",
      "sizes": "144x144",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/assets/icons/icon-152x152.png",
      "sizes": "152x152",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/assets/icons/icon-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icons/icon-384x384.png",
      "sizes": "384x384",
      "type": "image/png",
      "purpose": "any maskable"
    },
    {
      "src": "/assets/icons/icon-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any maskable"
    }
  ],
  
  "shortcuts": [
    {
      "name": "Agent Dashboard",
      "short_name": "Dashboard",
      "description": "View all AI agents and their status",
      "url": "/dashboard",
      "icons": [
        {
          "src": "/assets/icons/dashboard-96x96.png",
          "sizes": "96x96"
        }
      ]
    },
    {
      "name": "Create Agent",
      "short_name": "New Agent",
      "description": "Create a new AI agent",
      "url": "/agents/create",
      "icons": [
        {
          "src": "/assets/icons/create-96x96.png",
          "sizes": "96x96"
        }
      ]
    },
    {
      "name": "Analytics",
      "short_name": "Analytics",
      "description": "View performance analytics",
      "url": "/analytics",
      "icons": [
        {
          "src": "/assets/icons/analytics-96x96.png",
          "sizes": "96x96"
        }
      ]
    }
  ],
  
  "categories": [
    "business",
    "productivity",
    "utilities"
  ],
  
  "screenshots": [
    {
      "src": "/assets/screenshots/dashboard-desktop.png",
      "sizes": "1280x720",
      "type": "image/png",
      "platform": "wide"
    },
    {
      "src": "/assets/screenshots/dashboard-mobile.png", 
      "sizes": "360x640",
      "type": "image/png",
      "platform": "narrow"
    }
  ],
  
  "related_applications": [
    {
      "platform": "play",
      "url": "https://play.google.com/store/apps/details?id=com.aimatrix.mobile",
      "id": "com.aimatrix.mobile"
    },
    {
      "platform": "itunes",
      "url": "https://apps.apple.com/app/aimatrix/id123456789"
    }
  ]
}
```

## Framework-Specific Implementations

### Angular Application
```typescript
// Angular main application module
import { NgModule } from '@angular/core'
import { BrowserModule } from '@angular/platform-browser'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { ServiceWorkerModule } from '@angular/service-worker'
import { StoreModule } from '@ngrx/store'
import { EffectsModule } from '@ngrx/effects'
import { StoreDevtoolsModule } from '@ngrx/store-devtools'

import { AppComponent } from './app.component'
import { AppRoutingModule } from './app-routing.module'
import { CoreModule } from './core/core.module'
import { SharedModule } from './shared/shared.module'
import { reducers, metaReducers } from './store/reducers'
import { AgentEffects } from './store/effects/agent.effects'

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    CoreModule,
    SharedModule,
    
    // NgRx Store
    StoreModule.forRoot(reducers, {
      metaReducers,
      runtimeChecks: {
        strictStateImmutability: true,
        strictActionImmutability: true,
        strictStateSerializability: true,
        strictActionSerializability: true
      }
    }),
    
    EffectsModule.forRoot([AgentEffects]),
    
    // Development tools
    StoreDevtoolsModule.instrument({
      maxAge: 25,
      logOnly: environment.production
    }),
    
    // Service Worker
    ServiceWorkerModule.register('ngsw-worker.js', {
      enabled: environment.production,
      registrationStrategy: 'registerWhenStable:30000'
    })
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

// Agent dashboard component
@Component({
  selector: 'app-agent-dashboard',
  templateUrl: './agent-dashboard.component.html',
  styleUrls: ['./agent-dashboard.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AgentDashboardComponent implements OnInit, OnDestroy {
  agents$ = this.store.select(selectAllAgents)
  loading$ = this.store.select(selectAgentsLoading)
  error$ = this.store.select(selectAgentsError)
  
  private destroy$ = new Subject<void>()
  
  constructor(
    private store: Store<AppState>,
    private realtimeService: RealtimeService,
    private notificationService: NotificationService
  ) {}
  
  ngOnInit() {
    // Load agents
    this.store.dispatch(AgentActions.loadAgents())
    
    // Subscribe to real-time updates
    this.realtimeService.agentUpdates$
      .pipe(takeUntil(this.destroy$))
      .subscribe(update => {
        this.store.dispatch(AgentActions.agentUpdated({ update }))
      })
    
    // Handle connection status
    this.realtimeService.connectionStatus$
      .pipe(takeUntil(this.destroy$))
      .subscribe(status => {
        if (status === 'disconnected') {
          this.notificationService.show(
            'Connection lost - working offline',
            'warning'
          )
        } else if (status === 'connected') {
          this.notificationService.show(
            'Connection restored',
            'success'
          )
        }
      })
  }
  
  ngOnDestroy() {
    this.destroy$.next()
    this.destroy$.complete()
  }
  
  onCreateAgent() {
    this.store.dispatch(AgentActions.createAgent({
      agent: {
        name: 'New Agent',
        type: AgentType.ANALYTICS,
        capabilities: []
      }
    }))
  }
  
  onRefresh() {
    this.store.dispatch(AgentActions.refreshAgents())
  }
  
  trackByAgentId(index: number, agent: Agent): string {
    return agent.id
  }
}
```

### React Application
```tsx
// React application with hooks and context
import React, { createContext, useContext, useReducer, useEffect } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { ThemeProvider, CssBaseline } from '@mui/material'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { theme } from './theme'
import { AgentProvider } from './contexts/AgentContext'
import { RealtimeProvider } from './contexts/RealtimeContext'
import { AgentDashboard } from './pages/AgentDashboard'
import { AgentDetails } from './pages/AgentDetails'

// Query client setup
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: (failureCount, error) => {
        // Retry network errors but not 4xx errors
        return failureCount < 3 && error.response?.status >= 500
      }
    }
  }
})

function App() {
  useEffect(() => {
    // Register service worker
    if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
      navigator.serviceWorker.register('/sw.js')
        .then(registration => {
          console.log('SW registered:', registration)
        })
        .catch(error => {
          console.log('SW registration failed:', error)
        })
    }
  }, [])

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <RealtimeProvider>
          <AgentProvider>
            <Router>
              <Routes>
                <Route path="/" element={<AgentDashboard />} />
                <Route path="/agents/:id" element={<AgentDetails />} />
              </Routes>
            </Router>
          </AgentProvider>
        </RealtimeProvider>
      </ThemeProvider>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}

// Agent context and hooks
interface AgentState {
  agents: Agent[]
  selectedAgent: Agent | null
  loading: boolean
  error: string | null
}

type AgentAction = 
  | { type: 'SET_LOADING'; loading: boolean }
  | { type: 'SET_AGENTS'; agents: Agent[] }
  | { type: 'UPDATE_AGENT'; agent: Agent }
  | { type: 'SET_ERROR'; error: string | null }
  | { type: 'SELECT_AGENT'; agent: Agent | null }

const AgentContext = createContext<{
  state: AgentState
  dispatch: React.Dispatch<AgentAction>
} | null>(null)

function agentReducer(state: AgentState, action: AgentAction): AgentState {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.loading }
    
    case 'SET_AGENTS':
      return { ...state, agents: action.agents, loading: false, error: null }
    
    case 'UPDATE_AGENT':
      return {
        ...state,
        agents: state.agents.map(agent => 
          agent.id === action.agent.id ? action.agent : agent
        )
      }
    
    case 'SET_ERROR':
      return { ...state, error: action.error, loading: false }
    
    case 'SELECT_AGENT':
      return { ...state, selectedAgent: action.agent }
    
    default:
      return state
  }
}

export function AgentProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(agentReducer, {
    agents: [],
    selectedAgent: null,
    loading: false,
    error: null
  })

  return (
    <AgentContext.Provider value={{ state, dispatch }}>
      {children}
    </AgentContext.Provider>
  )
}

export function useAgent() {
  const context = useContext(AgentContext)
  if (!context) {
    throw new Error('useAgent must be used within AgentProvider')
  }
  return context
}

// Agent dashboard component
export function AgentDashboard() {
  const { state, dispatch } = useAgent()
  const { isConnected } = useRealtime()
  
  // Fetch agents with React Query
  const { data: agents, isLoading, error, refetch } = useQuery({
    queryKey: ['agents'],
    queryFn: fetchAgents,
    onSuccess: (data) => {
      dispatch({ type: 'SET_AGENTS', agents: data })
    },
    onError: (error) => {
      dispatch({ type: 'SET_ERROR', error: error.message })
    }
  })
  
  // Handle real-time updates
  useEffect(() => {
    const unsubscribe = subscribeToAgentUpdates((update) => {
      dispatch({ type: 'UPDATE_AGENT', agent: update.agent })
    })
    
    return unsubscribe
  }, [dispatch])

  if (isLoading) {
    return <LoadingSpinner />
  }

  if (error) {
    return (
      <ErrorMessage 
        message={error.message}
        onRetry={() => refetch()}
      />
    )
  }

  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 3 }}>
        <Stack direction="row" justifyContent="space-between" alignItems="center">
          <Typography variant="h4">
            AI Agents
          </Typography>
          
          <Stack direction="row" spacing={2} alignItems="center">
            <ConnectionIndicator connected={isConnected} />
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => {/* Handle create agent */}}
            >
              Create Agent
            </Button>
          </Stack>
        </Stack>
        
        <Grid container spacing={3} sx={{ mt: 2 }}>
          {state.agents.map(agent => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={agent.id}>
              <AgentCard 
                agent={agent}
                onClick={() => dispatch({ type: 'SELECT_AGENT', agent })}
              />
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  )
}
```

### Vue.js Application  
```vue
<!-- Vue 3 Composition API application -->
<template>
  <div id="app">
    <router-view />
    <ConnectionStatus />
    <NotificationContainer />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useServiceWorker } from '@/composables/useServiceWorker'
import ConnectionStatus from '@/components/ConnectionStatus.vue'
import NotificationContainer from '@/components/NotificationContainer.vue'

const { registerSW } = useServiceWorker()

onMounted(async () => {
  // Register service worker in production
  if (import.meta.env.PROD) {
    await registerSW()
  }
})
</script>

<!-- Agent Dashboard Vue Component -->
<template>
  <div class="agent-dashboard">
    <div class="dashboard-header">
      <h1>AI Agents</h1>
      <div class="header-actions">
        <ConnectionIndicator :connected="isConnected" />
        <button 
          @click="createAgent" 
          class="btn-primary"
        >
          <PlusIcon />
          Create Agent
        </button>
      </div>
    </div>
    
    <div v-if="isLoading" class="loading-container">
      <LoadingSpinner />
    </div>
    
    <div v-else-if="error" class="error-container">
      <ErrorMessage 
        :message="error"
        @retry="refetch"
      />
    </div>
    
    <div v-else class="agent-grid">
      <AgentCard
        v-for="agent in agents"
        :key="agent.id"
        :agent="agent"
        @click="selectAgent(agent)"
        @update="updateAgent"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAgentStore } from '@/stores/agent'
import { useRealtimeStore } from '@/stores/realtime'
import { useNotifications } from '@/composables/useNotifications'

import AgentCard from '@/components/AgentCard.vue'
import ConnectionIndicator from '@/components/ConnectionIndicator.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ErrorMessage from '@/components/ErrorMessage.vue'
import PlusIcon from '@/components/icons/PlusIcon.vue'

const agentStore = useAgentStore()
const realtimeStore = useRealtimeStore()
const { notify } = useNotifications()

const { agents, isLoading, error } = storeToRefs(agentStore)
const { isConnected } = storeToRefs(realtimeStore)

let unsubscribeRealtime: (() => void) | null = null

onMounted(async () => {
  // Load agents
  await agentStore.fetchAgents()
  
  // Subscribe to real-time updates
  unsubscribeRealtime = realtimeStore.subscribeToAgentUpdates((update) => {
    agentStore.updateAgent(update.agent)
  })
  
  // Handle connection changes
  realtimeStore.$subscribe((mutation, state) => {
    if (mutation.storeId === 'realtime' && mutation.type === 'direct') {
      if (state.isConnected) {
        notify('Connection restored', 'success')
      } else {
        notify('Working offline', 'warning')
      }
    }
  })
})

onUnmounted(() => {
  unsubscribeRealtime?.()
})

const createAgent = () => {
  agentStore.createAgent({
    name: 'New Agent',
    type: 'analytics',
    capabilities: []
  })
}

const selectAgent = (agent: Agent) => {
  agentStore.setSelectedAgent(agent)
  // Navigate to agent details
}

const updateAgent = (updatedAgent: Agent) => {
  agentStore.updateAgent(updatedAgent)
}

const refetch = () => {
  agentStore.fetchAgents()
}
</script>

<!-- Pinia store for agent management -->
<script lang="ts">
// stores/agent.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Agent, CreateAgentRequest } from '@/types/agent'
import { agentApi } from '@/services/agentApi'

export const useAgentStore = defineStore('agent', () => {
  // State
  const agents = ref<Agent[]>([])
  const selectedAgent = ref<Agent | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  
  // Getters
  const activeAgents = computed(() => 
    agents.value.filter(agent => agent.status === 'active')
  )
  
  const agentCount = computed(() => agents.value.length)
  
  // Actions
  async function fetchAgents() {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await agentApi.getAll()
      agents.value = response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch agents'
    } finally {
      isLoading.value = false
    }
  }
  
  async function createAgent(request: CreateAgentRequest) {
    try {
      const response = await agentApi.create(request)
      agents.value.push(response.data)
      return response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create agent'
      throw err
    }
  }
  
  function updateAgent(updatedAgent: Agent) {
    const index = agents.value.findIndex(agent => agent.id === updatedAgent.id)
    if (index !== -1) {
      agents.value[index] = updatedAgent
    }
    
    if (selectedAgent.value?.id === updatedAgent.id) {
      selectedAgent.value = updatedAgent
    }
  }
  
  function setSelectedAgent(agent: Agent | null) {
    selectedAgent.value = agent
  }
  
  function removeAgent(agentId: string) {
    const index = agents.value.findIndex(agent => agent.id === agentId)
    if (index !== -1) {
      agents.value.splice(index, 1)
    }
    
    if (selectedAgent.value?.id === agentId) {
      selectedAgent.value = null
    }
  }
  
  return {
    // State
    agents,
    selectedAgent,
    isLoading,
    error,
    
    // Getters
    activeAgents,
    agentCount,
    
    // Actions
    fetchAgents,
    createAgent,
    updateAgent,
    setSelectedAgent,
    removeAgent
  }
})
</script>
```

### Flutter Web Application
```dart
// Flutter Web main application
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'providers/agent_provider.dart';
import 'providers/realtime_provider.dart';
import 'pages/agent_dashboard_page.dart';
import 'pages/agent_details_page.dart';
import 'theme/app_theme.dart';
import 'services/service_worker_service.dart';

void main() {
  runApp(
    ProviderScope(
      child: AIMatrixApp(),
    ),
  );
}

class AIMatrixApp extends ConsumerStatefulWidget {
  @override
  ConsumerState<AIMatrixApp> createState() => _AIMatrixAppState();
}

class _AIMatrixAppState extends ConsumerState<AIMatrixApp> {
  late final GoRouter _router;
  
  @override
  void initState() {
    super.initState();
    
    // Initialize service worker
    ServiceWorkerService.initialize();
    
    // Setup router
    _router = GoRouter(
      initialLocation: '/',
      routes: [
        GoRoute(
          path: '/',
          builder: (context, state) => const AgentDashboardPage(),
        ),
        GoRoute(
          path: '/agents/:id',
          builder: (context, state) => AgentDetailsPage(
            agentId: state.pathParameters['id']!,
          ),
        ),
      ],
    );
  }
  
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'AIMatrix Web',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      routerConfig: _router,
    );
  }
}

// Agent Dashboard Page
class AgentDashboardPage extends ConsumerStatefulWidget {
  const AgentDashboardPage({Key? key}) : super(key: key);
  
  @override
  ConsumerState<AgentDashboardPage> createState() => _AgentDashboardPageState();
}

class _AgentDashboardPageState extends ConsumerState<AgentDashboardPage> {
  @override
  void initState() {
    super.initState();
    
    // Load agents on page init
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ref.read(agentProvider.notifier).loadAgents();
    });
  }
  
  @override
  Widget build(BuildContext context) {
    final agentState = ref.watch(agentProvider);
    final realtimeState = ref.watch(realtimeProvider);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Agents'),
        actions: [
          // Connection status indicator
          ConnectionStatusWidget(
            isConnected: realtimeState.isConnected,
          ),
          const SizedBox(width: 16),
          
          // Refresh button
          IconButton(
            onPressed: () {
              ref.read(agentProvider.notifier).refreshAgents();
            },
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      
      body: agentState.when(
        loading: () => const Center(
          child: CircularProgressIndicator(),
        ),
        
        error: (error, stackTrace) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.error_outline,
                size: 64,
                color: Theme.of(context).colorScheme.error,
              ),
              const SizedBox(height: 16),
              Text(
                'Error: $error',
                style: Theme.of(context).textTheme.titleMedium,
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: () {
                  ref.read(agentProvider.notifier).loadAgents();
                },
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
        
        data: (agents) => agents.isEmpty 
          ? const EmptyStateWidget()
          : AgentGridView(agents: agents),
      ),
      
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          _showCreateAgentDialog(context);
        },
        child: const Icon(Icons.add),
      ),
    );
  }
  
  void _showCreateAgentDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => CreateAgentDialog(
        onCreateAgent: (agent) {
          ref.read(agentProvider.notifier).createAgent(agent);
        },
      ),
    );
  }
}

// Agent Grid View Widget
class AgentGridView extends StatelessWidget {
  final List<Agent> agents;
  
  const AgentGridView({
    Key? key,
    required this.agents,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        // Responsive grid columns
        int crossAxisCount;
        if (constraints.maxWidth > 1200) {
          crossAxisCount = 4;
        } else if (constraints.maxWidth > 800) {
          crossAxisCount = 3;
        } else if (constraints.maxWidth > 600) {
          crossAxisCount = 2;
        } else {
          crossAxisCount = 1;
        }
        
        return Padding(
          padding: const EdgeInsets.all(16.0),
          child: GridView.builder(
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: crossAxisCount,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              childAspectRatio: 1.2,
            ),
            itemCount: agents.length,
            itemBuilder: (context, index) {
              return AgentCard(
                agent: agents[index],
                onTap: () {
                  context.go('/agents/${agents[index].id}');
                },
              );
            },
          ),
        );
      },
    );
  }
}

// Riverpod providers
@riverpod
class AgentNotifier extends _$AgentNotifier {
  @override
  Future<List<Agent>> build() async {
    // Subscribe to real-time updates
    ref.listen(realtimeProvider, (previous, next) {
      if (next.agentUpdates.isNotEmpty) {
        _handleAgentUpdates(next.agentUpdates);
      }
    });
    
    return _loadAgents();
  }
  
  Future<List<Agent>> _loadAgents() async {
    final agentService = ref.read(agentServiceProvider);
    return await agentService.getAll();
  }
  
  void _handleAgentUpdates(List<AgentUpdate> updates) {
    final currentState = state.value;
    if (currentState == null) return;
    
    final updatedAgents = [...currentState];
    
    for (final update in updates) {
      final index = updatedAgents.indexWhere(
        (agent) => agent.id == update.agentId,
      );
      
      if (index != -1) {
        updatedAgents[index] = update.agent;
      }
    }
    
    state = AsyncValue.data(updatedAgents);
  }
  
  Future<void> loadAgents() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(_loadAgents);
  }
  
  Future<void> refreshAgents() async {
    state = await AsyncValue.guard(_loadAgents);
  }
  
  Future<void> createAgent(CreateAgentRequest request) async {
    final agentService = ref.read(agentServiceProvider);
    
    try {
      final newAgent = await agentService.create(request);
      
      final currentAgents = state.value ?? [];
      state = AsyncValue.data([...currentAgents, newAgent]);
      
    } catch (error, stackTrace) {
      // Handle error
      print('Failed to create agent: $error');
    }
  }
}
```

## Real-Time Dashboards & WebSocket Integration

### Supabase Realtime Client
```typescript
// Real-time client for live data updates
import { createClient, RealtimeChannel } from '@supabase/supabase-js'

interface RealtimeConfig {
  supabaseUrl: string
  supabaseKey: string
  enableHeartbeat: boolean
  heartbeatInterval: number
  reconnectInterval: number
}

export class RealtimeManager {
  private client: SupabaseClient
  private channels: Map<string, RealtimeChannel> = new Map()
  private connectionStatus: 'connected' | 'disconnected' | 'reconnecting' = 'disconnected'
  private listeners: Map<string, ((data: any) => void)[]> = new Map()
  
  constructor(private config: RealtimeConfig) {
    this.client = createClient(config.supabaseUrl, config.supabaseKey, {
      realtime: {
        params: {
          eventsPerSecond: 50 // Rate limiting
        }
      }
    })
    
    this.setupConnectionMonitoring()
  }
  
  private setupConnectionMonitoring() {
    // Monitor connection status
    setInterval(() => {
      this.checkConnection()
    }, this.config.heartbeatInterval)
  }
  
  private async checkConnection() {
    try {
      const { data, error } = await this.client
        .from('_health_check')
        .select('*')
        .limit(1)
      
      if (error && this.connectionStatus === 'connected') {
        this.connectionStatus = 'disconnected'
        this.notifyStatusChange('disconnected')
      } else if (!error && this.connectionStatus !== 'connected') {
        this.connectionStatus = 'connected'
        this.notifyStatusChange('connected')
      }
      
    } catch (error) {
      if (this.connectionStatus !== 'disconnected') {
        this.connectionStatus = 'disconnected'
        this.notifyStatusChange('disconnected')
      }
    }
  }
  
  async subscribeToTable<T>(
    tableName: string,
    filter?: string,
    callback?: (payload: RealtimePostgresChangesPayload<T>) => void
  ): Promise<string> {
    const channelName = `${tableName}_${filter || 'all'}_${Date.now()}`
    
    const channel = this.client.channel(channelName)
      .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: tableName,
        filter: filter
      }, (payload) => {
        if (callback) {
          callback(payload as RealtimePostgresChangesPayload<T>)
        }
        
        // Notify all listeners
        const listeners = this.listeners.get(channelName) || []
        listeners.forEach(listener => listener(payload))
      })
      .on('system', {}, (payload) => {
        console.log('System event:', payload)
      })
      .subscribe((status) => {
        console.log(`Channel ${channelName} status: ${status}`)
        
        if (status === 'SUBSCRIBED') {
          this.connectionStatus = 'connected'
          this.notifyStatusChange('connected')
        } else if (status === 'CHANNEL_ERROR') {
          this.connectionStatus = 'disconnected'
          this.notifyStatusChange('disconnected')
          
          // Auto-reconnect
          setTimeout(() => {
            this.reconnectChannel(channelName)
          }, this.config.reconnectInterval)
        }
      })
    
    this.channels.set(channelName, channel)
    return channelName
  }
  
  async subscribeToPresence(
    channelName: string,
    userInfo: Record<string, any>,
    onPresenceUpdate?: (presences: Record<string, any[]>) => void
  ): Promise<string> {
    const channel = this.client.channel(channelName)
      .on('presence', { event: 'sync' }, () => {
        const presences = channel.presenceState()
        if (onPresenceUpdate) {
          onPresenceUpdate(presences)
        }
      })
      .on('presence', { event: 'join' }, ({ key, newPresences }) => {
        console.log('User joined:', key, newPresences)
      })
      .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
        console.log('User left:', key, leftPresences)
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          await channel.track(userInfo)
        }
      })
    
    this.channels.set(channelName, channel)
    return channelName
  }
  
  private async reconnectChannel(channelName: string) {
    const channel = this.channels.get(channelName)
    if (channel) {
      this.connectionStatus = 'reconnecting'
      this.notifyStatusChange('reconnecting')
      
      try {
        await channel.unsubscribe()
        await new Promise(resolve => setTimeout(resolve, 1000))
        await channel.subscribe()
      } catch (error) {
        console.error('Failed to reconnect channel:', error)
      }
    }
  }
  
  addListener(channelName: string, listener: (data: any) => void) {
    const listeners = this.listeners.get(channelName) || []
    listeners.push(listener)
    this.listeners.set(channelName, listeners)
  }
  
  removeListener(channelName: string, listener: (data: any) => void) {
    const listeners = this.listeners.get(channelName) || []
    const filteredListeners = listeners.filter(l => l !== listener)
    this.listeners.set(channelName, filteredListeners)
  }
  
  async unsubscribe(channelName: string) {
    const channel = this.channels.get(channelName)
    if (channel) {
      await channel.unsubscribe()
      this.channels.delete(channelName)
      this.listeners.delete(channelName)
    }
  }
  
  async unsubscribeAll() {
    const unsubscribePromises = Array.from(this.channels.keys())
      .map(channelName => this.unsubscribe(channelName))
    
    await Promise.all(unsubscribePromises)
  }
  
  getConnectionStatus() {
    return this.connectionStatus
  }
  
  private notifyStatusChange(status: string) {
    // Dispatch custom event for status changes
    window.dispatchEvent(new CustomEvent('realtime-status-change', {
      detail: { status }
    }))
  }
}

// Usage example
const realtimeManager = new RealtimeManager({
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  supabaseKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  enableHeartbeat: true,
  heartbeatInterval: 30000, // 30 seconds
  reconnectInterval: 5000   // 5 seconds
})

// Subscribe to agent updates
const agentChannelId = await realtimeManager.subscribeToTable(
  'agents',
  'user_id=eq.123',
  (payload) => {
    console.log('Agent updated:', payload)
    // Update UI state
  }
)
```

### Real-Time Analytics Dashboard
```tsx
// Real-time analytics dashboard component
import React, { useState, useEffect, useCallback } from 'react'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar
} from 'recharts'
import { Grid, Card, CardContent, Typography, Box } from '@mui/material'

interface DashboardMetrics {
  activeAgents: number
  totalWorkflows: number
  successRate: number
  avgResponseTime: number
  cpuUtilization: number
  memoryUsage: number
  errorCount: number
  throughput: number
}

interface TimeSeriesData {
  timestamp: string
  cpu: number
  memory: number
  throughput: number
  errors: number
}

export function AnalyticsDashboard() {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null)
  const [timeSeriesData, setTimeSeriesData] = useState<TimeSeriesData[]>([])
  const [isConnected, setIsConnected] = useState(false)
  
  const updateMetrics = useCallback((newMetrics: DashboardMetrics) => {
    setMetrics(newMetrics)
    
    // Add to time series (keep last 50 points)
    setTimeSeriesData(prev => {
      const newDataPoint: TimeSeriesData = {
        timestamp: new Date().toISOString(),
        cpu: newMetrics.cpuUtilization,
        memory: newMetrics.memoryUsage,
        throughput: newMetrics.throughput,
        errors: newMetrics.errorCount
      }
      
      const updated = [...prev, newDataPoint]
      return updated.slice(-50) // Keep last 50 points
    })
  }, [])
  
  useEffect(() => {
    let eventSource: EventSource | null = null
    
    // Setup Server-Sent Events for real-time metrics
    const connectToMetrics = () => {
      eventSource = new EventSource('/api/metrics/stream')
      
      eventSource.onopen = () => {
        setIsConnected(true)
      }
      
      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          updateMetrics(data)
        } catch (error) {
          console.error('Error parsing metrics data:', error)
        }
      }
      
      eventSource.onerror = () => {
        setIsConnected(false)
        
        // Reconnect after 5 seconds
        setTimeout(connectToMetrics, 5000)
      }
    }
    
    connectToMetrics()
    
    return () => {
      if (eventSource) {
        eventSource.close()
      }
    }
  }, [updateMetrics])
  
  if (!metrics) {
    return <DashboardSkeleton />
  }
  
  return (
    <Box sx={{ p: 3 }}>
      {/* Connection status */}
      <ConnectionBanner isConnected={isConnected} />
      
      {/* Key metrics cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Active Agents"
            value={metrics.activeAgents}
            unit=""
            color="#00ff41"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Success Rate"
            value={metrics.successRate}
            unit="%"
            color="#4caf50"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Avg Response"
            value={metrics.avgResponseTime}
            unit="ms"
            color="#ff9800"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Throughput"
            value={metrics.throughput}
            unit="/sec"
            color="#2196f3"
          />
        </Grid>
      </Grid>
      
      {/* Charts */}
      <Grid container spacing={3}>
        {/* Performance over time */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Performance Metrics
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={timeSeriesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="timestamp" 
                    tick={false}
                  />
                  <YAxis />
                  <Tooltip 
                    labelFormatter={(value) => 
                      new Date(value).toLocaleTimeString()
                    }
                  />
                  <Line 
                    type="monotone" 
                    dataKey="cpu" 
                    stroke="#ff5722" 
                    name="CPU %"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="memory" 
                    stroke="#9c27b0" 
                    name="Memory %"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="throughput" 
                    stroke="#00bcd4" 
                    name="Throughput/sec"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        {/* System utilization pie chart */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Utilization
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={[
                      { name: 'CPU', value: metrics.cpuUtilization },
                      { name: 'Memory', value: metrics.memoryUsage },
                      { name: 'Available', value: 100 - Math.max(metrics.cpuUtilization, metrics.memoryUsage) }
                    ]}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    dataKey="value"
                    label={({ name, value }) => `${name}: ${value}%`}
                  >
                    <Cell fill="#ff5722" />
                    <Cell fill="#9c27b0" />
                    <Cell fill="#4caf50" />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Error rate chart */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Error Trends
              </Typography>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={timeSeriesData.slice(-20)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="timestamp" 
                    tick={false}
                  />
                  <YAxis />
                  <Tooltip 
                    labelFormatter={(value) => 
                      new Date(value).toLocaleTimeString()
                    }
                  />
                  <Bar 
                    dataKey="errors" 
                    fill="#f44336"
                    name="Errors"
                  />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

function MetricCard({ 
  title, 
  value, 
  unit, 
  color 
}: {
  title: string
  value: number
  unit: string
  color: string
}) {
  return (
    <Card>
      <CardContent>
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          {title}
        </Typography>
        <Typography 
          variant="h4" 
          component="div"
          sx={{ color, fontFamily: 'monospace' }}
        >
          {value.toLocaleString()}{unit}
        </Typography>
      </CardContent>
    </Card>
  )
}

function ConnectionBanner({ isConnected }: { isConnected: boolean }) {
  if (isConnected) return null
  
  return (
    <Box 
      sx={{ 
        p: 2, 
        mb: 3, 
        backgroundColor: 'warning.main',
        color: 'warning.contrastText',
        borderRadius: 1
      }}
    >
      <Typography variant="body2">
        ⚠️ Connection lost - displaying cached data
      </Typography>
    </Box>
  )
}
```

## Responsive Design Implementation

### CSS Grid & Flexbox Layout
```scss
// Modern responsive layout with CSS Grid and Flexbox
.dashboard-container {
  display: grid;
  grid-template-areas: 
    "header header header"
    "sidebar main main"
    "footer footer footer";
  grid-template-rows: auto 1fr auto;
  grid-template-columns: 250px 1fr 1fr;
  min-height: 100vh;
  gap: 1rem;
  padding: 1rem;
  
  @media (max-width: 1024px) {
    grid-template-areas: 
      "header"
      "main"
      "footer";
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
  }
  
  @media (max-width: 768px) {
    padding: 0.5rem;
    gap: 0.5rem;
  }
}

.dashboard-header {
  grid-area: header;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: var(--surface-color);
  border-radius: 8px;
  
  h1 {
    margin: 0;
    font-size: clamp(1.5rem, 4vw, 2.5rem);
  }
  
  .header-actions {
    display: flex;
    gap: 1rem;
    align-items: center;
    
    @media (max-width: 600px) {
      flex-direction: column;
      gap: 0.5rem;
    }
  }
}

.dashboard-sidebar {
  grid-area: sidebar;
  background: var(--surface-color);
  border-radius: 8px;
  padding: 1rem;
  
  @media (max-width: 1024px) {
    display: none;
  }
}

.dashboard-main {
  grid-area: main;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

// Agent card responsive design
.agent-card {
  background: var(--surface-color);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 255, 65, 0.2);
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
    
    h3 {
      margin: 0;
      font-size: 1.25rem;
      color: var(--text-primary);
    }
    
    .status-indicator {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--success-color);
      
      &.inactive {
        background: var(--error-color);
      }
      
      &.warning {
        background: var(--warning-color);
      }
    }
  }
  
  .card-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 1rem;
    
    @media (max-width: 480px) {
      grid-template-columns: 1fr;
      gap: 0.5rem;
    }
    
    .metric {
      text-align: center;
      
      .value {
        font-family: 'JetBrains Mono', monospace;
        font-weight: bold;
        font-size: 1.1rem;
        color: var(--accent-color);
      }
      
      .label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }
    }
  }
}

// Responsive navigation
.nav-container {
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--surface-color);
  border-bottom: 1px solid var(--border-color);
  
  .nav-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    max-width: 1400px;
    margin: 0 auto;
    
    @media (max-width: 768px) {
      padding: 1rem;
    }
  }
  
  .nav-menu {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 2rem;
    
    @media (max-width: 768px) {
      display: none;
    }
    
    a {
      text-decoration: none;
      color: var(--text-primary);
      font-weight: 500;
      transition: color 0.3s ease;
      
      &:hover,
      &.active {
        color: var(--accent-color);
      }
    }
  }
  
  .mobile-menu-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    
    @media (max-width: 768px) {
      display: block;
    }
  }
}

// Mobile menu
.mobile-menu {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--surface-color);
  z-index: 1000;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  
  &.open {
    transform: translateX(0);
  }
  
  .menu-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
  }
  
  .menu-items {
    padding: 2rem 1rem;
    
    a {
      display: block;
      padding: 1rem 0;
      text-decoration: none;
      color: var(--text-primary);
      font-size: 1.25rem;
      border-bottom: 1px solid var(--border-color);
      
      &:hover,
      &.active {
        color: var(--accent-color);
      }
    }
  }
}
```

### Container Queries for Component-Level Responsiveness
```css
/* Modern container queries for component responsiveness */
.agent-dashboard {
  container-type: inline-size;
  container-name: dashboard;
}

.agent-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

/* Container query breakpoints */
@container dashboard (max-width: 600px) {
  .agent-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-header h1 {
    font-size: 1.5rem;
  }
  
  .header-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
}

@container dashboard (min-width: 900px) {
  .agent-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@container dashboard (min-width: 1200px) {
  .agent-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* Component-specific container queries */
.agent-card {
  container-type: inline-size;
  container-name: card;
}

@container card (max-width: 250px) {
  .card-metrics {
    grid-template-columns: 1fr;
  }
  
  .metric .value {
    font-size: 1rem;
  }
}

@container card (min-width: 350px) {
  .card-metrics {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## Performance Optimization

### Code Splitting & Lazy Loading
```typescript
// Dynamic imports for code splitting
import { lazy, Suspense } from 'react'

// Lazy load heavy components
const AnalyticsDashboard = lazy(() => import('../pages/AnalyticsDashboard'))
const AgentDetails = lazy(() => import('../pages/AgentDetails'))
const WorkflowBuilder = lazy(() => import('../pages/WorkflowBuilder'))

// Route-based code splitting
const AppRouter = () => {
  return (
    <Router>
      <Suspense fallback={<PageLoadingSpinner />}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route 
            path="/analytics" 
            element={<AnalyticsDashboard />} 
          />
          <Route 
            path="/agents/:id" 
            element={<AgentDetails />} 
          />
          <Route 
            path="/workflows/builder" 
            element={<WorkflowBuilder />} 
          />
        </Routes>
      </Suspense>
    </Router>
  )
}

// Component-level lazy loading
const LazyChartComponent = lazy(async () => {
  // Dynamically import chart library only when needed
  const [
    { default: Chart },
    { default: chartConfig }
  ] = await Promise.all([
    import('react-chartjs-2'),
    import('../config/chartConfig')
  ])
  
  return {
    default: ({ data, options }: ChartProps) => (
      <Chart data={data} options={{ ...chartConfig, ...options }} />
    )
  }
})
```

### Bundle Optimization
```javascript
// Webpack configuration for optimized bundles
const path = require('path')
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')

module.exports = {
  entry: {
    app: './src/index.tsx',
    vendor: ['react', 'react-dom']
  },
  
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].[contenthash].js',
    chunkFilename: '[name].[contenthash].chunk.js',
    clean: true
  },
  
  optimization: {
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          priority: 10,
          reuseExistingChunk: true
        },
        common: {
          name: 'common',
          minChunks: 2,
          priority: 5,
          reuseExistingChunk: true
        },
        charts: {
          test: /[\\/]node_modules[\\/](recharts|chart\.js|react-chartjs-2)[\\/]/,
          name: 'charts',
          chunks: 'all',
          priority: 15
        }
      }
    },
    runtimeChunk: {
      name: 'runtime'
    },
    minimize: true,
    usedExports: true,
    sideEffects: false
  },
  
  plugins: [
    // Analyze bundle size
    process.env.ANALYZE && new BundleAnalyzerPlugin(),
    
    // Preload critical resources
    new PreloadWebpackPlugin({
      rel: 'preload',
      include: 'initial',
      fileBlacklist: [/\.map$/, /hot-update\.js$/]
    }),
    
    // Service worker generation
    new WorkboxWebpackPlugin.GenerateSW({
      clientsClaim: true,
      skipWaiting: true,
      runtimeCaching: [
        {
          urlPattern: /^https:\/\/api\.aimatrix\.com/,
          handler: 'NetworkFirst',
          options: {
            cacheName: 'api-cache',
            networkTimeoutSeconds: 3,
            expiration: {
              maxEntries: 50,
              maxAgeSeconds: 5 * 60 // 5 minutes
            }
          }
        }
      ]
    })
  ].filter(Boolean)
}
```

### Caching Strategies
```typescript
// Advanced caching with React Query and service worker
import { QueryClient } from '@tanstack/react-query'
import { persistQueryClient } from '@tanstack/react-query-persist-client-core'
import { createSyncStoragePersister } from '@tanstack/query-sync-storage-persister'

// Setup persistent query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: (failureCount, error) => {
        // Don't retry for client errors
        if (error?.response?.status < 500) return false
        return failureCount < 3
      },
      refetchOnWindowFocus: false,
      refetchOnMount: 'always'
    }
  }
})

const persister = createSyncStoragePersister({
  storage: window.localStorage,
  key: 'AIMATRIX_QUERY_CACHE',
  throttleTime: 1000
})

persistQueryClient({
  queryClient,
  persister,
  maxAge: 1000 * 60 * 60 * 24 // 24 hours
})

// Cache-first data fetching
export function useAgents() {
  return useQuery({
    queryKey: ['agents'],
    queryFn: async () => {
      // Try cache first, then network
      const cachedData = await getCachedAgents()
      if (cachedData && !isStale(cachedData)) {
        // Return cached data immediately, refresh in background
        backgroundRefresh('agents')
        return cachedData.agents
      }
      
      // Fetch from network
      const response = await fetch('/api/agents')
      if (!response.ok) {
        throw new Error('Failed to fetch agents')
      }
      
      const data = await response.json()
      
      // Cache the response
      await cacheAgents(data)
      
      return data.agents
    },
    staleTime: 5 * 60 * 1000,
    cacheTime: 30 * 60 * 1000
  })
}

// Service worker caching strategies
self.addEventListener('fetch', (event) => {
  const { request } = event
  const url = new URL(request.url)
  
  // API requests - Network First with fallback
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then(response => {
          if (response.ok) {
            const responseClone = response.clone()
            caches.open('api-cache').then(cache => {
              cache.put(request, responseClone)
            })
          }
          return response
        })
        .catch(() => {
          return caches.match(request)
            .then(cachedResponse => {
              if (cachedResponse) {
                return cachedResponse
              }
              return new Response('Offline', { status: 503 })
            })
        })
    )
  }
  
  // Static assets - Cache First
  if (request.destination === 'script' || 
      request.destination === 'style' ||
      request.destination === 'image') {
    event.respondWith(
      caches.match(request)
        .then(cachedResponse => {
          if (cachedResponse) {
            return cachedResponse
          }
          
          return fetch(request).then(response => {
            if (response.ok) {
              const responseClone = response.clone()
              caches.open('static-cache').then(cache => {
                cache.put(request, responseClone)
              })
            }
            return response
          })
        })
    )
  }
})
```

## Deployment & CDN Configuration

### Docker Multi-Stage Build
```dockerfile
# Multi-stage Docker build for production
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY yarn.lock ./

# Install dependencies
RUN yarn install --frozen-lockfile --production=false

# Copy source code
COPY . .

# Build application
RUN yarn build

# Production stage
FROM nginx:alpine AS production

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy SSL certificates (if using HTTPS)
COPY --from=builder /app/certs /etc/nginx/certs

# Expose port
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

### Nginx Configuration
```nginx
# nginx.conf for optimized web app serving
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    
    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';
    access_log /var/log/nginx/access.log main;
    
    # Performance optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        application/javascript
        application/json
        application/xml
        text/css
        text/javascript
        text/xml
        text/plain;
    
    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    server {
        listen 80;
        listen [::]:80;
        server_name aimatrix-web.com www.aimatrix-web.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }
    
    server {
        listen 443 ssl http2;
        listen [::]:443 ssl http2;
        server_name aimatrix-web.com www.aimatrix-web.com;
        
        # SSL configuration
        ssl_certificate /etc/nginx/certs/fullchain.pem;
        ssl_certificate_key /etc/nginx/certs/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        
        # Document root
        root /usr/share/nginx/html;
        index index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            add_header X-Content-Type-Options nosniff;
        }
        
        # API proxy
        location /api/ {
            proxy_pass https://api.aimatrix.com/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_cache_bypass $http_upgrade;
            
            # Timeout settings
            proxy_connect_timeout 60s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }
        
        # WebSocket proxy for real-time features
        location /ws/ {
            proxy_pass https://realtime.aimatrix.com/;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
        
        # SPA routing - serve index.html for all routes
        location / {
            try_files $uri $uri/ /index.html;
            
            # PWA cache headers for HTML files
            add_header Cache-Control "no-cache, no-store, must-revalidate";
            add_header Pragma "no-cache";
            add_header Expires "0";
        }
        
        # Service Worker
        location /sw.js {
            add_header Cache-Control "no-cache, no-store, must-revalidate";
            add_header Pragma "no-cache";
            add_header Expires "0";
        }
        
        # Web App Manifest
        location /manifest.json {
            add_header Cache-Control "no-cache, no-store, must-revalidate";
            add_header Pragma "no-cache";
            add_header Expires "0";
        }
        
        # Health check endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
```

### CloudFront Distribution
```yaml
# AWS CloudFormation template for CloudFront distribution
AWSTemplateFormatVersion: '2010-09-09'
Description: 'CloudFront distribution for AIMatrix Web Application'

Resources:
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Aliases:
          - aimatrix-web.com
          - www.aimatrix-web.com
        
        Origins:
          - Id: S3Origin
            DomainName: !GetAtt S3Bucket.DomainName
            S3OriginConfig:
              OriginAccessIdentity: !Sub 'origin-access-identity/cloudfront/${OriginAccessIdentity}'
          
          - Id: APIOrigin
            DomainName: api.aimatrix.com
            CustomOriginConfig:
              HTTPPort: 443
              OriginProtocolPolicy: https-only
              OriginSSLProtocols:
                - TLSv1.2
        
        DefaultCacheBehavior:
          TargetOriginId: S3Origin
          ViewerProtocolPolicy: redirect-to-https
          Compress: true
          AllowedMethods:
            - GET
            - HEAD
            - OPTIONS
          CachedMethods:
            - GET
            - HEAD
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          TrustedSigners:
            - self
          
          # Cache policy for SPA
          CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad  # Managed-CachingDisabled
          ResponseHeadersPolicyId: 67f7725c-6f97-4210-82d7-5512b31e9d03  # Managed-SecurityHeadersPolicy
        
        CacheBehaviors:
          # API routes
          - PathPattern: '/api/*'
            TargetOriginId: APIOrigin
            ViewerProtocolPolicy: https-only
            AllowedMethods:
              - GET
              - HEAD
              - OPTIONS
              - PUT
              - POST
              - PATCH
              - DELETE
            CachedMethods:
              - GET
              - HEAD
            CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad  # Managed-CachingDisabled
            OriginRequestPolicyId: 88a5eaf4-2fd4-4709-b370-b4c650ea3fcf  # Managed-CORS-S3Origin
          
          # Static assets with long-term caching
          - PathPattern: '/assets/*'
            TargetOriginId: S3Origin
            ViewerProtocolPolicy: https-only
            Compress: true
            AllowedMethods:
              - GET
              - HEAD
            CachedMethods:
              - GET
              - HEAD
            CachePolicyId: 658327ea-f89d-4fab-a63d-7e88639e58f6  # Managed-CachingOptimized
            
        CustomErrorResponses:
          # SPA routing - redirect 404s to index.html
          - ErrorCode: 404
            ResponseCode: 200
            ResponsePagePath: '/index.html'
            ErrorCachingMinTTL: 300
          
          - ErrorCode: 403
            ResponseCode: 200
            ResponsePagePath: '/index.html'
            ErrorCachingMinTTL: 300
        
        DefaultRootObject: index.html
        Enabled: true
        HttpVersion: http2
        PriceClass: PriceClass_All
        
        ViewerCertificate:
          AcmCertificateArn: !Ref SSLCertificate
          SslSupportMethod: sni-only
          MinimumProtocolVersion: TLSv1.2_2021
        
        WebACLId: !GetAtt WebACL.Arn
        
        Logging:
          Bucket: !GetAtt LoggingBucket.DomainName
          IncludeCookies: false
          Prefix: 'cloudfront-access-logs/'
```

---

> [!TIP]
> **Getting Started**: Access the AIMatrix web application at [https://app.aimatrix.com](https://app.aimatrix.com) or deploy your own instance using our provided Docker images and configuration templates.

> [!NOTE]
> **PWA Installation**: All web applications can be installed as Progressive Web Apps on desktop and mobile devices, providing app-like experiences with offline capabilities and native OS integration.

---

*AIMatrix Web Applications - Modern web interfaces for enterprise AI management*