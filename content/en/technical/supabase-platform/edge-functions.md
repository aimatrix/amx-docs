---
title: "Edge Functions & Serverless"
description: "Build serverless API endpoints with Supabase Edge Functions for AIMatrix applications"
date: 2024-12-06
weight: 5
---

# Edge Functions & Serverless with Supabase

Supabase Edge Functions provide a serverless runtime for building API endpoints, webhooks, and background jobs that scale automatically and run close to your users worldwide.

## Edge Functions Architecture

```mermaid
graph TB
    subgraph "Client Applications"
        WEB[Web Apps]
        MOBILE[Mobile Apps]
        AGENTS[AI Agents]
    end
    
    subgraph "Edge Locations"
        EDGE1[US East]
        EDGE2[EU West]
        EDGE3[Asia Pacific]
    end
    
    subgraph "Edge Functions"
        AUTH_FN[Authentication]
        AI_FN[AI Processing]
        WEBHOOK[Webhooks]
        CRON[Scheduled Jobs]
    end
    
    subgraph "Supabase Services"
        DB[(Database)]
        STORAGE[Storage]
        REALTIME[Real-time]
    end
    
    subgraph "External APIs"
        OPENAI[OpenAI]
        STRIPE[Stripe]
        SLACK[Slack]
    end
    
    WEB --> EDGE1
    MOBILE --> EDGE2
    AGENTS --> EDGE3
    
    EDGE1 --> AUTH_FN
    EDGE2 --> AI_FN
    EDGE3 --> WEBHOOK
    
    AUTH_FN --> DB
    AI_FN --> DB
    WEBHOOK --> STORAGE
    CRON --> REALTIME
    
    AI_FN --> OPENAI
    WEBHOOK --> STRIPE
    CRON --> SLACK
```

## Getting Started with Edge Functions

### Project Setup

```bash
# Install Supabase CLI
npm install -g supabase

# Initialize functions in existing project
supabase functions new my-function

# Local development
supabase start
supabase functions serve --env-file .env.local
```

### Basic Function Structure

```typescript
// supabase/functions/hello-world/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // Handle CORS preflight requests
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { name } = await req.json()
    
    const data = {
      message: `Hello ${name}!`,
      timestamp: new Date().toISOString(),
    }

    return new Response(
      JSON.stringify(data),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200 
      },
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 400 
      },
    )
  }
})
```

### Deploy and Test

```bash
# Deploy function
supabase functions deploy hello-world

# Test function
curl -X POST 'https://your-project.supabase.co/functions/v1/hello-world' \
  -H 'Authorization: Bearer YOUR_ANON_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"name":"World"}'
```

## AI Integration Functions

### OpenAI Chat Completion

```typescript
// supabase/functions/ai-chat/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.4'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Initialize Supabase client
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
    )

    // Get user from JWT
    const { data: { user }, error: authError } = await supabaseClient.auth.getUser()
    if (authError || !user) {
      return new Response('Unauthorized', { status: 401, headers: corsHeaders })
    }

    const { message, conversation_id, model = 'gpt-3.5-turbo' } = await req.json()

    // Get conversation context
    const { data: context } = await supabaseClient
      .from('messages')
      .select('role, content')
      .eq('conversation_id', conversation_id)
      .order('created_at', { ascending: true })
      .limit(20)

    // Prepare messages for OpenAI
    const messages = [
      { role: 'system', content: 'You are a helpful AI assistant for AIMatrix.' },
      ...(context || []),
      { role: 'user', content: message }
    ]

    // Call OpenAI
    const openAIResponse = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${Deno.env.get('OPENAI_API_KEY')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model,
        messages,
        temperature: 0.7,
        max_tokens: 500,
      }),
    })

    const aiResponse = await openAIResponse.json()
    const assistantMessage = aiResponse.choices[0].message.content

    // Save messages to database
    await supabaseClient
      .from('messages')
      .insert([
        {
          conversation_id,
          role: 'user',
          content: message,
        },
        {
          conversation_id,
          role: 'assistant',
          content: assistantMessage,
        }
      ])

    return new Response(
      JSON.stringify({
        message: assistantMessage,
        usage: aiResponse.usage
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    console.error('Error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500 
      }
    )
  }
})
```

### RAG-Powered Q&A System

```typescript
// supabase/functions/rag-qa/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.4'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

interface EmbeddingResponse {
  data: Array<{ embedding: number[] }>
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    const { question, organization_id, context_limit = 5 } = await req.json()

    // Generate embedding for the question
    const embeddingResponse = await fetch('https://api.openai.com/v1/embeddings', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${Deno.env.get('OPENAI_API_KEY')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'text-embedding-ada-002',
        input: question,
      }),
    })

    const embeddingData: EmbeddingResponse = await embeddingResponse.json()
    const questionEmbedding = embeddingData.data[0].embedding

    // Search for relevant context
    const { data: contextData, error: contextError } = await supabaseClient.rpc(
      'match_documents',
      {
        query_embedding: questionEmbedding,
        match_threshold: 0.7,
        match_count: context_limit
      }
    )

    if (contextError) throw contextError

    // Prepare context for prompt
    const context = contextData
      .map((doc: any, index: number) => `[${index + 1}] ${doc.content}`)
      .join('\n\n')

    // Generate answer using GPT
    const prompt = `Context information:
${context}

Based on the context above, answer the following question. If the context doesn't contain enough information to answer the question, say so clearly.

Question: ${question}

Answer:`

    const completionResponse = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${Deno.env.get('OPENAI_API_KEY')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages: [
          { role: 'system', content: 'You are a helpful AI assistant that answers questions based on provided context.' },
          { role: 'user', content: prompt }
        ],
        temperature: 0.1,
        max_tokens: 500,
      }),
    })

    const completionData = await completionResponse.json()
    const answer = completionData.choices[0].message.content

    // Log the Q&A for analytics
    await supabaseClient
      .from('qa_sessions')
      .insert({
        question,
        answer,
        context_documents: contextData.map((doc: any) => doc.id),
        organization_id,
      })

    return new Response(
      JSON.stringify({
        answer,
        sources: contextData,
        confidence: contextData.length > 0 ? 0.8 : 0.3
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    console.error('RAG Q&A Error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500 
      }
    )
  }
})
```

### Image Analysis with Vision API

```typescript
// supabase/functions/analyze-image/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.4'

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
    )

    const { image_url, analysis_type = 'general' } = await req.json()

    // Analyze image with OpenAI Vision
    const visionResponse = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${Deno.env.get('OPENAI_API_KEY')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4-vision-preview',
        messages: [
          {
            role: 'user',
            content: [
              {
                type: 'text',
                text: getAnalysisPrompt(analysis_type)
              },
              {
                type: 'image_url',
                image_url: {
                  url: image_url,
                  detail: 'high'
                }
              }
            ]
          }
        ],
        max_tokens: 500,
      }),
    })

    const analysisResult = await visionResponse.json()
    const description = analysisResult.choices[0].message.content

    // Store analysis result
    const { data: analysis, error } = await supabaseClient
      .from('image_analysis')
      .insert({
        image_url,
        analysis_type,
        description,
        metadata: {
          model_used: 'gpt-4-vision-preview',
          timestamp: new Date().toISOString()
        }
      })
      .select()
      .single()

    if (error) throw error

    return new Response(
      JSON.stringify({
        analysis_id: analysis.id,
        description,
        analysis_type
      }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    console.error('Image Analysis Error:', error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { 
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500 
      }
    )
  }
})

function getAnalysisPrompt(type: string): string {
  const prompts = {
    general: 'Describe this image in detail, focusing on key elements, colors, composition, and overall mood.',
    technical: 'Analyze this image from a technical perspective: quality, resolution, artifacts, and technical characteristics.',
    accessibility: 'Describe this image for accessibility purposes, focusing on helping visually impaired users understand the content.',
    OCR: 'Extract and transcribe any text visible in this image.',
    safety: 'Analyze this image for safety concerns, inappropriate content, or potential risks.'
  }
  
  return prompts[type] || prompts.general
}
```

## Webhook Handlers

### Stripe Payment Webhooks

```typescript
// supabase/functions/stripe-webhook/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.4'

const cryptoProvider = Deno.env.get('DENO_DEPLOYMENT_ID') ? crypto : crypto.webcrypto

serve(async (req) => {
  const signature = req.headers.get('stripe-signature')
  const body = await req.text()
  
  if (!signature) {
    return new Response('Missing stripe-signature header', { status: 400 })
  }

  try {
    // Verify webhook signature
    const event = await verifyStripeSignature(body, signature)
    
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // Handle different event types
    switch (event.type) {
      case 'payment_intent.succeeded':
        await handlePaymentSuccess(supabaseClient, event.data.object)
        break
      
      case 'customer.subscription.created':
        await handleSubscriptionCreated(supabaseClient, event.data.object)
        break
      
      case 'customer.subscription.updated':
        await handleSubscriptionUpdated(supabaseClient, event.data.object)
        break
      
      case 'customer.subscription.deleted':
        await handleSubscriptionCanceled(supabaseClient, event.data.object)
        break
      
      default:
        console.log(`Unhandled event type: ${event.type}`)
    }

    return new Response('OK', { status: 200 })

  } catch (error) {
    console.error('Webhook Error:', error)
    return new Response(`Webhook Error: ${error.message}`, { status: 400 })
  }
})

async function verifyStripeSignature(body: string, signature: string): Promise<any> {
  const elements = signature.split(',')
  const signatureElements = elements.reduce((acc, element) => {
    const [key, value] = element.split('=')
    return { ...acc, [key]: value }
  }, {} as any)

  if (!signatureElements.t || !signatureElements.v1) {
    throw new Error('Invalid signature format')
  }

  const timestamp = signatureElements.t
  const expectedSignature = signatureElements.v1

  // Create signature
  const payload = `${timestamp}.${body}`
  const secret = Deno.env.get('STRIPE_WEBHOOK_SECRET')
  
  const key = await cryptoProvider.subtle.importKey(
    'raw',
    new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  )

  const signature_bytes = await cryptoProvider.subtle.sign(
    'HMAC',
    key,
    new TextEncoder().encode(payload)
  )

  const signature_hex = Array.from(new Uint8Array(signature_bytes))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('')

  if (signature_hex !== expectedSignature) {
    throw new Error('Invalid signature')
  }

  return JSON.parse(body)
}

async function handlePaymentSuccess(supabase: any, paymentIntent: any) {
  const { error } = await supabase
    .from('payments')
    .update({
      status: 'completed',
      stripe_payment_intent_id: paymentIntent.id,
      amount: paymentIntent.amount,
      updated_at: new Date().toISOString()
    })
    .eq('stripe_payment_intent_id', paymentIntent.id)

  if (error) {
    console.error('Error updating payment:', error)
  }
}

async function handleSubscriptionCreated(supabase: any, subscription: any) {
  const { error } = await supabase
    .from('subscriptions')
    .insert({
      stripe_subscription_id: subscription.id,
      stripe_customer_id: subscription.customer,
      status: subscription.status,
      current_period_start: new Date(subscription.current_period_start * 1000).toISOString(),
      current_period_end: new Date(subscription.current_period_end * 1000).toISOString(),
      created_at: new Date().toISOString()
    })

  if (error) {
    console.error('Error creating subscription:', error)
  }
}
```

### GitHub Webhook Integration

```typescript
// supabase/functions/github-webhook/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.4'

serve(async (req) => {
  const signature = req.headers.get('x-hub-signature-256')
  const event = req.headers.get('x-github-event')
  const body = await req.text()

  if (!signature || !event) {
    return new Response('Missing GitHub headers', { status: 400 })
  }

  try {
    // Verify GitHub signature
    await verifyGitHubSignature(body, signature)

    const payload = JSON.parse(body)
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    )

    // Handle different GitHub events
    switch (event) {
      case 'push':
        await handlePushEvent(supabaseClient, payload)
        break
      
      case 'pull_request':
        await handlePullRequestEvent(supabaseClient, payload)
        break
      
      case 'issues':
        await handleIssueEvent(supabaseClient, payload)
        break
      
      default:
        console.log(`Unhandled GitHub event: ${event}`)
    }

    return new Response('OK', { status: 200 })

  } catch (error) {
    console.error('GitHub Webhook Error:', error)
    return new Response(`Webhook Error: ${error.message}`, { status: 400 })
  }
})

async function verifyGitHubSignature(body: string, signature: string): Promise<void> {
  const secret = Deno.env.get('GITHUB_WEBHOOK_SECRET')
  const expectedSignature = signature.replace('sha256=', '')

  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  )

  const signatureBuffer = await crypto.subtle.sign(
    'HMAC',
    key,
    new TextEncoder().encode(body)
  )

  const actualSignature = Array.from(new Uint8Array(signatureBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('')

  if (actualSignature !== expectedSignature) {
    throw new Error('Invalid GitHub signature')
  }
}

async function handlePushEvent(supabase: any, payload: any) {
  const { repository, commits, pusher } = payload

  // Store repository activity
  await supabase
    .from('repository_events')
    .insert({
      event_type: 'push',
      repository_name: repository.full_name,
      author: pusher.name,
      commits_count: commits.length,
      metadata: {
        ref: payload.ref,
        before: payload.before,
        after: payload.after
      }
    })

  // Trigger CI/CD pipeline or other automations
  if (payload.ref === 'refs/heads/main') {
    await triggerDeployment(repository.full_name)
  }
}

async function triggerDeployment(repository: string) {
  // Call deployment webhook or trigger build process
  console.log(`Triggering deployment for ${repository}`)
}
```

## Background Jobs and Scheduled Tasks

### Cron Job Function

```typescript
// supabase/functions/scheduled-tasks/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.38.4'

serve(async (req) => {
  // Verify this is a scheduled request
  const authHeader = req.headers.get('authorization')
  if (authHeader !== `Bearer ${Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')}`) {
    return new Response('Unauthorized', { status: 401 })
  }

  const { task } = await req.json()
  
  const supabaseClient = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
  )

  try {
    switch (task) {
      case 'cleanup_old_sessions':
        await cleanupOldSessions(supabaseClient)
        break
      
      case 'generate_daily_reports':
        await generateDailyReports(supabaseClient)
        break
      
      case 'update_ai_embeddings':
        await updateAIEmbeddings(supabaseClient)
        break
      
      case 'backup_data':
        await backupData(supabaseClient)
        break
      
      default:
        throw new Error(`Unknown task: ${task}`)
    }

    return new Response('Task completed successfully', { status: 200 })

  } catch (error) {
    console.error(`Error executing task ${task}:`, error)
    return new Response(`Task failed: ${error.message}`, { status: 500 })
  }
})

async function cleanupOldSessions(supabase: any) {
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

  const { error } = await supabase
    .from('user_sessions')
    .delete()
    .lt('last_activity', thirtyDaysAgo.toISOString())

  if (error) throw error
  console.log('Old sessions cleaned up')
}

async function generateDailyReports(supabase: any) {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  
  // Generate analytics report
  const { data: stats } = await supabase
    .rpc('generate_daily_stats', { date: yesterday.toISOString() })

  // Send report via email or store in database
  await supabase
    .from('daily_reports')
    .insert({
      report_date: yesterday.toISOString(),
      stats,
      created_at: new Date().toISOString()
    })

  console.log('Daily report generated')
}

async function updateAIEmbeddings(supabase: any) {
  // Find documents without embeddings
  const { data: documents } = await supabase
    .from('documents')
    .select('id, content')
    .is('embedding', null)
    .limit(50)

  if (!documents?.length) {
    console.log('No documents need embedding updates')
    return
  }

  // Generate embeddings
  for (const doc of documents) {
    const embeddingResponse = await fetch('https://api.openai.com/v1/embeddings', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${Deno.env.get('OPENAI_API_KEY')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'text-embedding-ada-002',
        input: doc.content,
      }),
    })

    const embeddingData = await embeddingResponse.json()
    const embedding = embeddingData.data[0].embedding

    await supabase
      .from('documents')
      .update({ embedding })
      .eq('id', doc.id)
  }

  console.log(`Updated embeddings for ${documents.length} documents`)
}
```

### Set up Cron Jobs with GitHub Actions

```yaml
# .github/workflows/scheduled-tasks.yml
name: Scheduled Tasks

on:
  schedule:
    # Run cleanup daily at 2 AM UTC
    - cron: '0 2 * * *'
    # Run reports daily at 6 AM UTC
    - cron: '0 6 * * *'
    # Run embedding updates every 4 hours
    - cron: '0 */4 * * *'

jobs:
  cleanup-sessions:
    runs-on: ubuntu-latest
    if: github.event.schedule == '0 2 * * *'
    steps:
      - name: Cleanup Old Sessions
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{"task":"cleanup_old_sessions"}' \
            ${{ secrets.SUPABASE_URL }}/functions/v1/scheduled-tasks

  generate-reports:
    runs-on: ubuntu-latest
    if: github.event.schedule == '0 6 * * *'
    steps:
      - name: Generate Daily Reports
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{"task":"generate_daily_reports"}' \
            ${{ secrets.SUPABASE_URL }}/functions/v1/scheduled-tasks

  update-embeddings:
    runs-on: ubuntu-latest
    if: github.event.schedule == '0 */4 * * *'
    steps:
      - name: Update AI Embeddings
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{"task":"update_ai_embeddings"}' \
            ${{ secrets.SUPABASE_URL }}/functions/v1/scheduled-tasks
```

## API Gateway and Routing

### Multi-Function Router

```typescript
// supabase/functions/api-gateway/index.ts
import { serve } from "https://deno.land/std@0.177.0/http/server.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

// Route handlers
const routes = new Map([
  ['/ai/chat', handleAIChat],
  ['/ai/analyze', handleAnalyze],
  ['/webhooks/stripe', handleStripeWebhook],
  ['/webhooks/github', handleGitHubWebhook],
  ['/analytics/report', handleAnalyticsReport],
])

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const url = new URL(req.url)
    const handler = routes.get(url.pathname)
    
    if (!handler) {
      return new Response(
        JSON.stringify({ error: 'Route not found' }),
        { 
          status: 404,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        }
      )
    }

    return await handler(req)

  } catch (error) {
    console.error('Gateway Error:', error)
    return new Response(
      JSON.stringify({ error: 'Internal server error' }),
      { 
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    )
  }
})

async function handleAIChat(req: Request): Promise<Response> {
  // AI chat logic
  return new Response('AI Chat', { headers: corsHeaders })
}

async function handleAnalyze(req: Request): Promise<Response> {
  // Analysis logic
  return new Response('Analyze', { headers: corsHeaders })
}

async function handleStripeWebhook(req: Request): Promise<Response> {
  // Stripe webhook logic
  return new Response('Stripe Webhook', { headers: corsHeaders })
}

async function handleGitHubWebhook(req: Request): Promise<Response> {
  // GitHub webhook logic
  return new Response('GitHub Webhook', { headers: corsHeaders })
}

async function handleAnalyticsReport(req: Request): Promise<Response> {
  // Analytics report logic
  return new Response('Analytics Report', { headers: corsHeaders })
}
```

## Error Handling and Logging

### Comprehensive Error Handler

```typescript
// Utility functions for error handling
class EdgeFunctionError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message)
    this.name = 'EdgeFunctionError'
  }
}

function createErrorResponse(error: unknown, req: Request) {
  console.error('Function Error:', {
    error: error instanceof Error ? error.message : 'Unknown error',
    stack: error instanceof Error ? error.stack : undefined,
    url: req.url,
    method: req.method,
    timestamp: new Date().toISOString()
  })

  if (error instanceof EdgeFunctionError) {
    return new Response(
      JSON.stringify({
        error: error.message,
        code: error.code,
        timestamp: new Date().toISOString()
      }),
      {
        status: error.statusCode,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      }
    )
  }

  return new Response(
    JSON.stringify({
      error: 'Internal server error',
      timestamp: new Date().toISOString()
    }),
    {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    }
  )
}

// Usage in functions
serve(async (req) => {
  try {
    // Function logic here
    return new Response('Success')
  } catch (error) {
    return createErrorResponse(error, req)
  }
})
```

### Structured Logging

```typescript
interface LogLevel {
  DEBUG: 'debug'
  INFO: 'info'
  WARN: 'warn'
  ERROR: 'error'
}

const LogLevel: LogLevel = {
  DEBUG: 'debug',
  INFO: 'info',
  WARN: 'warn',
  ERROR: 'error'
}

class Logger {
  static log(level: keyof LogLevel, message: string, metadata?: any) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      metadata: metadata || {},
      function: Deno.env.get('SUPABASE_FUNCTION_NAME') || 'unknown'
    }

    console.log(JSON.stringify(logEntry))

    // Send to external logging service if configured
    if (Deno.env.get('LOGGING_WEBHOOK_URL')) {
      this.sendToLogService(logEntry).catch(console.error)
    }
  }

  static debug(message: string, metadata?: any) {
    this.log('DEBUG', message, metadata)
  }

  static info(message: string, metadata?: any) {
    this.log('INFO', message, metadata)
  }

  static warn(message: string, metadata?: any) {
    this.log('WARN', message, metadata)
  }

  static error(message: string, metadata?: any) {
    this.log('ERROR', message, metadata)
  }

  private static async sendToLogService(logEntry: any) {
    try {
      await fetch(Deno.env.get('LOGGING_WEBHOOK_URL')!, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(logEntry)
      })
    } catch (error) {
      console.error('Failed to send log to external service:', error)
    }
  }
}
```

## Testing Edge Functions

### Local Testing Setup

```typescript
// tests/functions/ai-chat.test.ts
import { assertEquals } from "https://deno.land/std@0.177.0/testing/asserts.ts"

const FUNCTION_URL = 'http://localhost:54321/functions/v1/ai-chat'

Deno.test('AI Chat Function', async (t) => {
  await t.step('should respond to valid request', async () => {
    const response = await fetch(FUNCTION_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-key'
      },
      body: JSON.stringify({
        message: 'Hello',
        conversation_id: '123'
      })
    })

    assertEquals(response.status, 200)
    
    const data = await response.json()
    assertEquals(typeof data.message, 'string')
  })

  await t.step('should handle missing parameters', async () => {
    const response = await fetch(FUNCTION_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer test-key'
      },
      body: JSON.stringify({})
    })

    assertEquals(response.status, 400)
  })

  await t.step('should handle CORS preflight', async () => {
    const response = await fetch(FUNCTION_URL, {
      method: 'OPTIONS'
    })

    assertEquals(response.status, 200)
    assertEquals(response.headers.get('Access-Control-Allow-Origin'), '*')
  })
})
```

### Integration Testing

```bash
#!/bin/bash
# test-functions.sh

# Start local Supabase
supabase start

# Run function tests
deno test --allow-net --allow-env tests/functions/

# Test specific function
curl -X POST 'http://localhost:54321/functions/v1/ai-chat' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Test message","conversation_id":"test-123"}'

# Test webhook
curl -X POST 'http://localhost:54321/functions/v1/stripe-webhook' \
  -H 'stripe-signature: t=test,v1=test' \
  -d '{"type":"payment_intent.succeeded"}'

# Stop local Supabase
supabase stop
```

## Performance Optimization

### Function Warming and Caching

```typescript
// Global cache for frequently accessed data
const cache = new Map<string, { data: any, expires: number }>()

function getCached<T>(key: string, ttl: number = 300000): T | null {
  const cached = cache.get(key)
  if (cached && cached.expires > Date.now()) {
    return cached.data as T
  }
  cache.delete(key)
  return null
}

function setCache(key: string, data: any, ttl: number = 300000) {
  cache.set(key, {
    data,
    expires: Date.now() + ttl
  })
}

// Connection pooling for database
let supabaseClient: any = null

function getSupabaseClient() {
  if (!supabaseClient) {
    supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '',
      {
        db: {
          schema: 'public'
        },
        global: {
          headers: {
            'Connection': 'keep-alive'
          }
        }
      }
    )
  }
  return supabaseClient
}

// Optimized function example
serve(async (req) => {
  try {
    // Check cache first
    const cacheKey = `query_${await hashRequest(req)}`
    let result = getCached(cacheKey)
    
    if (!result) {
      // Process request
      result = await processRequest(req)
      setCache(cacheKey, result)
    }

    return new Response(
      JSON.stringify(result),
      { headers: corsHeaders }
    )
  } catch (error) {
    return createErrorResponse(error, req)
  }
})

async function hashRequest(req: Request): Promise<string> {
  const body = await req.text()
  const hashBuffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(body))
  return Array.from(new Uint8Array(hashBuffer))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('')
}
```

### Bundle Optimization

```typescript
// import_map.json for function dependencies
{
  "imports": {
    "https://esm.sh/@supabase/supabase-js@2.38.4": "https://esm.sh/@supabase/supabase-js@2.38.4?bundle&target=deno",
    "openai": "https://esm.sh/openai@4.24.0?target=deno",
    "zod": "https://esm.sh/zod@3.22.4?target=deno"
  }
}

// Optimize imports in your functions
import type { Database } from '../types/database.ts'
import { z } from 'zod'

// Use schema validation for better performance and type safety
const ChatRequestSchema = z.object({
  message: z.string().min(1).max(1000),
  conversation_id: z.string().uuid(),
  model: z.string().optional().default('gpt-3.5-turbo')
})

serve(async (req) => {
  try {
    const body = await req.json()
    const validatedData = ChatRequestSchema.parse(body)
    
    // Process validated data
    return await processChatRequest(validatedData)
  } catch (error) {
    if (error instanceof z.ZodError) {
      return new Response(
        JSON.stringify({ error: 'Invalid request data', details: error.errors }),
        { status: 400, headers: corsHeaders }
      )
    }
    return createErrorResponse(error, req)
  }
})
```

## Next Steps

With Edge Functions set up, you can now:

1. **[Configure Storage & CDN](storage-cdn/)** - Handle file uploads and processing
2. **[Set up Monitoring](monitoring-observability/)** - Track function performance
3. **[Implement Real-time Features](realtime-features/)** - Connect functions to real-time events
4. **[Enhance Vector AI](vector-ai/)** - Use functions for AI processing pipelines

Your serverless API layer is now ready to handle AI processing, webhooks, background jobs, and third-party integrations at global scale.