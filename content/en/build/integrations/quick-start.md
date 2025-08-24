---
title: "Quick Start Guide"
description: "Get up and running with Supabase for AIMatrix in minutes"
date: 2024-12-06
weight: 1
---

# Quick Start with Supabase

This guide will help you set up Supabase for your AIMatrix project in under 30 minutes, covering all essential components needed for AI-powered applications.

## Prerequisites

- Node.js 16+ installed
- A Supabase account (free tier available)
- Basic knowledge of JavaScript/TypeScript
- Git for version control

## Step 1: Project Setup

### Create Supabase Project

1. Visit [supabase.com](https://supabase.com) and sign in
2. Click "New Project"
3. Choose your organization
4. Fill in project details:
   - **Name**: `aimatrix-platform`
   - **Database Password**: Generate a strong password
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Start with Free tier

### Install Supabase CLI

```bash
# Install Supabase CLI
npm install -g supabase

# Login to Supabase
supabase login

# Initialize project locally
mkdir aimatrix-supabase
cd aimatrix-supabase
supabase init
```

### Connect to Remote Project

```bash
# Link to your remote project
supabase link --project-ref your-project-ref

# Pull remote schema
supabase db pull
```

## Step 2: Database Schema Design

### Create Core Tables

```sql
-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Organizations table for multi-tenancy
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enhanced users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    organization_id UUID REFERENCES organizations(id),
    role TEXT DEFAULT 'member' CHECK (role IN ('admin', 'member', 'viewer')),
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI Agents table
CREATE TABLE ai_agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    type TEXT NOT NULL CHECK (type IN ('assistant', 'analyst', 'automation', 'monitoring')),
    config JSONB NOT NULL DEFAULT '{}',
    status TEXT DEFAULT 'inactive' CHECK (status IN ('active', 'inactive', 'error')),
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Knowledge base for RAG
CREATE TABLE knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding VECTOR(1536), -- OpenAI embedding dimension
    source_url TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Agent conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) NOT NULL,
    agent_id UUID REFERENCES ai_agents(id),
    user_id UUID REFERENCES users(id),
    title TEXT,
    context JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Messages table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_knowledge_base_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_conversations_organization_id ON conversations(organization_id);
CREATE INDEX idx_ai_agents_organization_id ON ai_agents(organization_id);
CREATE INDEX idx_users_organization_id ON users(organization_id);
```

Save this as `supabase/migrations/001_initial_schema.sql` and run:

```bash
supabase db push
```

## Step 3: Authentication Configuration

### Set up Auth Providers

In your Supabase dashboard:

1. Go to **Authentication > Settings**
2. Configure Site URL: `http://localhost:3000` (development)
3. Add redirect URLs for production
4. Enable desired providers:

```json
{
  "SITE_URL": "https://your-app.com",
  "REDIRECT_URLS": [
    "http://localhost:3000/auth/callback",
    "https://your-app.com/auth/callback"
  ]
}
```

### Enable Social Authentication

```javascript
// OAuth providers configuration
const authConfig = {
  google: {
    enabled: true,
    client_id: "your-google-client-id"
  },
  github: {
    enabled: true,
    client_id: "your-github-client-id"
  },
  microsoft: {
    enabled: true,
    client_id: "your-microsoft-client-id"
  }
}
```

### Row Level Security (RLS)

```sql
-- Enable RLS on all tables
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Create policies for multi-tenant access
CREATE POLICY "Users can view their own organization" ON organizations
    FOR SELECT USING (
        auth.uid() IN (
            SELECT id FROM users WHERE organization_id = organizations.id
        )
    );

CREATE POLICY "Users can view organization members" ON users
    FOR SELECT USING (
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );

-- Agent access policies
CREATE POLICY "Users can manage organization agents" ON ai_agents
    FOR ALL USING (
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );

-- Knowledge base policies  
CREATE POLICY "Users can access organization knowledge" ON knowledge_base
    FOR ALL USING (
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );
```

## Step 4: Storage Setup

### Configure Storage Buckets

```sql
-- Create storage buckets
INSERT INTO storage.buckets (id, name, public)
VALUES 
  ('avatars', 'avatars', true),
  ('documents', 'documents', false),
  ('agent-assets', 'agent-assets', false);
```

### Storage Policies

```sql
-- Avatar policies
CREATE POLICY "Users can upload their own avatar" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'avatars' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Anyone can view avatars" ON storage.objects
    FOR SELECT USING (bucket_id = 'avatars');

-- Document policies
CREATE POLICY "Users can manage organization documents" ON storage.objects
    FOR ALL USING (
        bucket_id = 'documents' AND
        (storage.foldername(name))[1] = (
            SELECT organization_id::text FROM users WHERE id = auth.uid()
        )
    );
```

## Step 5: Real-time Configuration

### Enable Real-time

```sql
-- Enable real-time for tables
ALTER publication supabase_realtime ADD TABLE messages;
ALTER publication supabase_realtime ADD TABLE conversations;
ALTER publication supabase_realtime ADD TABLE ai_agents;
```

### Real-time Policies

```sql
-- Real-time policies
CREATE POLICY "Users can listen to organization messages" ON messages
    FOR SELECT USING (
        conversation_id IN (
            SELECT id FROM conversations 
            WHERE organization_id = (
                SELECT organization_id FROM users WHERE id = auth.uid()
            )
        )
    );
```

## Step 6: Edge Functions Setup

### Create Edge Function

```bash
# Create edge function for AI integration
supabase functions new ai-chat

# Install dependencies
cd supabase/functions/ai-chat
echo '{"imports": {"https://deno.land/x/supabase@1.0.0/mod.ts": "https://deno.land/x/supabase@1.0.0/mod.ts"}}' > import_map.json
```

### Basic AI Chat Function

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
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
    )

    const { conversation_id, message } = await req.json()

    // Get user from JWT
    const { data: { user } } = await supabaseClient.auth.getUser()
    
    if (!user) {
      return new Response('Unauthorized', { status: 401, headers: corsHeaders })
    }

    // Save user message
    const { data: userMessage } = await supabaseClient
      .from('messages')
      .insert({
        conversation_id,
        role: 'user',
        content: message
      })
      .select()
      .single()

    // TODO: Add AI processing here
    const aiResponse = "I'm an AI assistant ready to help!"

    // Save AI response
    const { data: aiMessage } = await supabaseClient
      .from('messages')
      .insert({
        conversation_id,
        role: 'assistant',
        content: aiResponse
      })
      .select()
      .single()

    return new Response(
      JSON.stringify({ success: true, message: aiMessage }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    )
  }
})
```

### Deploy Edge Function

```bash
supabase functions deploy ai-chat --no-verify-jwt
```

## Step 7: Client Integration

### Install Client Libraries

```bash
npm install @supabase/supabase-js
npm install @supabase/auth-helpers-nextjs # if using Next.js
```

### Initialize Client

```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Database types (auto-generated)
export type Database = {
  public: {
    Tables: {
      organizations: {
        Row: {
          id: string
          name: string
          slug: string
          settings: any
          created_at: string
          updated_at: string
        }
        Insert: {
          id?: string
          name: string
          slug: string
          settings?: any
          created_at?: string
          updated_at?: string
        }
        Update: {
          id?: string
          name?: string
          slug?: string
          settings?: any
          updated_at?: string
        }
      }
      // ... other table types
    }
  }
}
```

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

## Step 8: Basic Usage Examples

### Authentication

```typescript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
  options: {
    data: {
      full_name: 'John Doe'
    }
  }
})

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123'
})

// OAuth sign in
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: `${window.location.origin}/auth/callback`
  }
})
```

### Database Operations

```typescript
// Create organization and user
const createOrganization = async (name: string, userEmail: string) => {
  const { data: org } = await supabase
    .from('organizations')
    .insert({ name, slug: name.toLowerCase().replace(/\s+/g, '-') })
    .select()
    .single()

  const { data: user } = await supabase
    .from('users')
    .update({ organization_id: org.id })
    .eq('email', userEmail)
    .select()
    .single()

  return { org, user }
}

// Create AI agent
const createAgent = async (name: string, type: string, config: any) => {
  const { data } = await supabase
    .from('ai_agents')
    .insert({
      name,
      type,
      config,
      organization_id: user.organization_id
    })
    .select()
    .single()

  return data
}
```

### Real-time Subscriptions

```typescript
// Subscribe to new messages
const subscribeToMessages = (conversationId: string) => {
  return supabase
    .channel('messages')
    .on('postgres_changes', 
      { 
        event: 'INSERT', 
        schema: 'public', 
        table: 'messages',
        filter: `conversation_id=eq.${conversationId}`
      }, 
      (payload) => {
        console.log('New message:', payload.new)
      }
    )
    .subscribe()
}
```

## Next Steps

Now that you have Supabase set up, explore these advanced topics:

1. **[Authentication](authentication/)** - Implement advanced auth patterns
2. **[Real-time Features](realtime-features/)** - Build collaborative experiences  
3. **[Vector AI](vector-ai/)** - Add semantic search and RAG
4. **[Edge Functions](edge-functions/)** - Create serverless AI endpoints
5. **[Storage & CDN](storage-cdn/)** - Handle files and media
6. **[Monitoring](monitoring-observability/)** - Set up production monitoring

## Troubleshooting

### Common Issues

**Connection Issues**
```bash
# Check connection
supabase status

# Reset local database
supabase db reset
```

**RLS Policies Not Working**
- Ensure RLS is enabled on tables
- Check policy conditions match your use case
- Test policies with different user contexts

**Edge Functions Timeout**
- Check function logs: `supabase functions logs ai-chat`
- Increase timeout in function config
- Optimize database queries

### Getting Help

- [Supabase Documentation](https://supabase.com/docs)
- [Community Discord](https://discord.supabase.com)
- [GitHub Discussions](https://github.com/supabase/supabase/discussions)

Your Supabase setup is now ready for building AI-powered applications with AIMatrix!