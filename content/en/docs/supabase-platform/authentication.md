---
title: "Authentication & Authorization"
description: "Complete guide to implementing secure authentication and authorization in AIMatrix with Supabase"
date: 2024-12-06
weight: 2
---

# Authentication & Authorization

Supabase provides a comprehensive authentication system that's perfect for AIMatrix applications, supporting everything from simple email/password authentication to enterprise SSO with fine-grained access control.

## Authentication Overview

### Supported Authentication Methods

- **Email/Password**: Traditional email and password authentication
- **Magic Links**: Passwordless authentication via email
- **OAuth Providers**: Google, GitHub, Microsoft, Apple, and more
- **SAML SSO**: Enterprise single sign-on integration
- **Phone Authentication**: SMS-based authentication
- **Custom JWT**: Bring your own authentication system

## Basic Authentication Setup

### Email/Password Authentication

```typescript
import { supabase } from '@/lib/supabase'

// Sign up new user
const signUp = async (email: string, password: string, userData: any) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        full_name: userData.full_name,
        avatar_url: userData.avatar_url,
        role: 'member'
      }
    }
  })

  if (error) throw error

  // Create user profile in database
  if (data.user) {
    const { error: profileError } = await supabase
      .from('users')
      .upsert({
        id: data.user.id,
        email: data.user.email,
        full_name: userData.full_name,
        avatar_url: userData.avatar_url
      })

    if (profileError) throw profileError
  }

  return data
}

// Sign in
const signIn = async (email: string, password: string) => {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  })

  if (error) throw error
  return data
}

// Sign out
const signOut = async () => {
  const { error } = await supabase.auth.signOut()
  if (error) throw error
}
```

### Magic Link Authentication

```typescript
// Send magic link
const sendMagicLink = async (email: string) => {
  const { data, error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: `${window.location.origin}/auth/callback`
    }
  })

  if (error) throw error
  return data
}

// Verify OTP
const verifyOtp = async (email: string, token: string) => {
  const { data, error } = await supabase.auth.verifyOtp({
    email,
    token,
    type: 'email'
  })

  if (error) throw error
  return data
}
```

## OAuth Integration

### Google OAuth Setup

```typescript
// Google OAuth sign in
const signInWithGoogle = async () => {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${window.location.origin}/auth/callback`,
      queryParams: {
        access_type: 'offline',
        prompt: 'consent'
      }
    }
  })

  if (error) throw error
  return data
}

// Handle OAuth callback
const handleOAuthCallback = async () => {
  const { data, error } = await supabase.auth.getSessionFromUrl()
  
  if (error) {
    console.error('OAuth callback error:', error)
    return
  }

  if (data.session) {
    // User successfully signed in
    console.log('User signed in:', data.session.user)
  }
}
```

### Microsoft Azure AD Integration

```typescript
const signInWithMicrosoft = async () => {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'azure',
    options: {
      redirectTo: `${window.location.origin}/auth/callback`,
      scopes: 'email openid profile'
    }
  })

  if (error) throw error
  return data
}
```

### GitHub OAuth

```typescript
const signInWithGitHub = async () => {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'github',
    options: {
      redirectTo: `${window.location.origin}/auth/callback`
    }
  })

  if (error) throw error
  return data
}
```

## Row Level Security (RLS)

### Multi-tenant Data Isolation

```sql
-- Enable RLS on all tables
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_base ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Organization access policies
CREATE POLICY "Users can only see their organization" ON organizations
    FOR SELECT USING (
        id = (SELECT organization_id FROM users WHERE id = auth.uid())
    );

CREATE POLICY "Admins can update organization" ON organizations
    FOR UPDATE USING (
        id = (SELECT organization_id FROM users WHERE id = auth.uid()) AND
        (SELECT role FROM users WHERE id = auth.uid()) = 'admin'
    );

-- User access policies
CREATE POLICY "Users can view organization members" ON users
    FOR SELECT USING (
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (id = auth.uid());

-- AI Agents policies
CREATE POLICY "Users can view organization agents" ON ai_agents
    FOR SELECT USING (
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Users can manage agents they created" ON ai_agents
    FOR ALL USING (
        created_by = auth.uid() OR
        (SELECT role FROM users WHERE id = auth.uid()) = 'admin'
    );

-- Knowledge base policies
CREATE POLICY "Users can access organization knowledge" ON knowledge_base
    FOR SELECT USING (
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Users can add knowledge" ON knowledge_base
    FOR INSERT WITH CHECK (
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );

-- Conversation policies
CREATE POLICY "Users can access their conversations" ON conversations
    FOR SELECT USING (
        user_id = auth.uid() OR
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Users can create conversations" ON conversations
    FOR INSERT WITH CHECK (
        user_id = auth.uid() AND
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );

-- Message policies
CREATE POLICY "Users can view conversation messages" ON messages
    FOR SELECT USING (
        conversation_id IN (
            SELECT id FROM conversations 
            WHERE user_id = auth.uid() OR
            organization_id = (
                SELECT organization_id FROM users WHERE id = auth.uid()
            )
        )
    );

CREATE POLICY "Users can add messages to their conversations" ON messages
    FOR INSERT WITH CHECK (
        conversation_id IN (
            SELECT id FROM conversations WHERE user_id = auth.uid()
        )
    );
```

### Role-based Access Control

```sql
-- Create role enum
CREATE TYPE user_role AS ENUM ('admin', 'member', 'viewer', 'agent');

-- Add role column if not exists
ALTER TABLE users ADD COLUMN IF NOT EXISTS role user_role DEFAULT 'member';

-- Admin-only policies
CREATE POLICY "Only admins can delete agents" ON ai_agents
    FOR DELETE USING (
        (SELECT role FROM users WHERE id = auth.uid()) = 'admin' AND
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );

CREATE POLICY "Only admins can manage organization settings" ON organizations
    FOR UPDATE USING (
        id = (SELECT organization_id FROM users WHERE id = auth.uid()) AND
        (SELECT role FROM users WHERE id = auth.uid()) = 'admin'
    );

-- Member permissions
CREATE POLICY "Members can create agents" ON ai_agents
    FOR INSERT WITH CHECK (
        (SELECT role FROM users WHERE id = auth.uid()) IN ('admin', 'member') AND
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );

-- Viewer restrictions
CREATE POLICY "Viewers have read-only access" ON ai_agents
    FOR SELECT USING (
        organization_id = (
            SELECT organization_id FROM users WHERE id = auth.uid()
        )
    );
```

## Custom Claims and Roles

### JWT Custom Claims

```typescript
// Server-side function to add custom claims
const addCustomClaims = async (userId: string, claims: any) => {
  const { error } = await supabase.auth.admin.updateUserById(userId, {
    app_metadata: {
      claims: {
        role: claims.role,
        organization_id: claims.organization_id,
        permissions: claims.permissions
      }
    }
  })

  if (error) throw error
}

// Client-side access to custom claims
const getUserClaims = () => {
  const { data: { session } } = supabase.auth.getSession()
  return session?.user?.app_metadata?.claims || {}
}
```

### Database Function for Role Management

```sql
-- Function to check user permissions
CREATE OR REPLACE FUNCTION check_user_permission(required_permission TEXT)
RETURNS BOOLEAN AS $$
DECLARE
    user_permissions TEXT[];
    user_role TEXT;
BEGIN
    SELECT role INTO user_role FROM users WHERE id = auth.uid();
    
    -- Admin has all permissions
    IF user_role = 'admin' THEN
        RETURN TRUE;
    END IF;
    
    -- Check specific permissions
    SELECT permissions INTO user_permissions 
    FROM users 
    WHERE id = auth.uid();
    
    RETURN required_permission = ANY(user_permissions);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Usage in RLS policies
CREATE POLICY "Permission-based agent access" ON ai_agents
    FOR ALL USING (check_user_permission('manage_agents'));
```

## Multi-tenancy Patterns

### Organization-based Isolation

```typescript
// Organization management
class OrganizationManager {
  async createOrganization(name: string, ownerEmail: string) {
    const { data: org, error: orgError } = await supabase
      .from('organizations')
      .insert({
        name,
        slug: name.toLowerCase().replace(/\s+/g, '-')
      })
      .select()
      .single()

    if (orgError) throw orgError

    // Update user with organization
    const { error: userError } = await supabase
      .from('users')
      .update({
        organization_id: org.id,
        role: 'admin'
      })
      .eq('email', ownerEmail)

    if (userError) throw userError

    return org
  }

  async inviteUser(email: string, organizationId: string, role: string = 'member') {
    // Send invitation
    const { data, error } = await supabase.auth.admin.inviteUserByEmail(email, {
      data: {
        organization_id: organizationId,
        role: role
      },
      redirectTo: `${process.env.NEXT_PUBLIC_SITE_URL}/auth/callback`
    })

    if (error) throw error
    return data
  }

  async switchOrganization(userId: string, organizationId: string) {
    // Verify user has access to organization
    const { data: membership, error } = await supabase
      .from('organization_members')
      .select('role')
      .eq('user_id', userId)
      .eq('organization_id', organizationId)
      .single()

    if (error || !membership) {
      throw new Error('User does not have access to this organization')
    }

    // Update current organization context
    const { error: updateError } = await supabase
      .from('users')
      .update({ current_organization_id: organizationId })
      .eq('id', userId)

    if (updateError) throw updateError

    return membership
  }
}
```

### Context-aware Database Queries

```typescript
// Helper function to ensure organization context
const withOrgContext = (query: any) => {
  return query.eq('organization_id', getCurrentOrganizationId())
}

// Usage
const getOrganizationAgents = async () => {
  return withOrgContext(
    supabase
      .from('ai_agents')
      .select('*')
  )
}
```

## SSO Integration

### SAML Configuration

```typescript
// SAML SSO setup
const configureSAML = async (organizationId: string, samlConfig: any) => {
  const { data, error } = await supabase.auth.admin.createSSOProvider({
    type: 'saml',
    metadata_xml: samlConfig.metadata_xml,
    attribute_mapping: {
      email: 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress',
      name: 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name'
    },
    domains: [samlConfig.domain]
  })

  if (error) throw error

  // Store SSO configuration
  await supabase
    .from('sso_configurations')
    .upsert({
      organization_id: organizationId,
      provider_id: data.id,
      domain: samlConfig.domain,
      is_active: true
    })

  return data
}

// SSO sign-in
const signInWithSSO = async (domain: string) => {
  const { data, error } = await supabase.auth.signInWithSSO({
    domain,
    options: {
      redirectTo: `${window.location.origin}/auth/sso/callback`
    }
  })

  if (error) throw error
  return data
}
```

### Just-in-Time (JIT) Provisioning

```sql
-- Function for JIT user provisioning
CREATE OR REPLACE FUNCTION handle_sso_user_creation()
RETURNS TRIGGER AS $$
DECLARE
    org_id UUID;
    default_role TEXT := 'member';
BEGIN
    -- Get organization from email domain
    SELECT id INTO org_id
    FROM organizations o
    JOIN sso_configurations s ON s.organization_id = o.id
    WHERE s.domain = split_part(NEW.email, '@', 2)
    AND s.is_active = TRUE;

    -- Create user profile
    INSERT INTO users (
        id,
        email,
        full_name,
        organization_id,
        role,
        created_at
    ) VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email),
        org_id,
        default_role,
        NOW()
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for new auth users
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_sso_user_creation();
```

## Advanced Authentication Patterns

### Session Management

```typescript
class SessionManager {
  private refreshTimer: NodeJS.Timeout | null = null

  async initializeSession() {
    const { data: { session } } = await supabase.auth.getSession()
    
    if (session) {
      this.scheduleTokenRefresh(session)
      await this.loadUserProfile(session.user.id)
    }

    // Listen for auth changes
    supabase.auth.onAuthStateChange((event, session) => {
      this.handleAuthChange(event, session)
    })
  }

  private scheduleTokenRefresh(session: any) {
    if (this.refreshTimer) {
      clearTimeout(this.refreshTimer)
    }

    const expiresIn = session.expires_at - Math.floor(Date.now() / 1000)
    const refreshTime = Math.max(expiresIn - 300, 60) // Refresh 5 minutes before expiry

    this.refreshTimer = setTimeout(async () => {
      const { data, error } = await supabase.auth.refreshSession()
      if (data.session) {
        this.scheduleTokenRefresh(data.session)
      }
    }, refreshTime * 1000)
  }

  private async handleAuthChange(event: string, session: any) {
    switch (event) {
      case 'SIGNED_IN':
        await this.loadUserProfile(session?.user.id)
        this.scheduleTokenRefresh(session)
        break
      case 'SIGNED_OUT':
        if (this.refreshTimer) {
          clearTimeout(this.refreshTimer)
        }
        this.clearUserData()
        break
      case 'TOKEN_REFRESHED':
        this.scheduleTokenRefresh(session)
        break
    }
  }

  private async loadUserProfile(userId: string) {
    const { data: user } = await supabase
      .from('users')
      .select(`
        *,
        organizations (
          id,
          name,
          slug,
          settings
        )
      `)
      .eq('id', userId)
      .single()

    // Store in context/state management
    return user
  }

  private clearUserData() {
    // Clear user data from state management
  }
}
```

### Rate Limiting and Security

```sql
-- Rate limiting function
CREATE OR REPLACE FUNCTION check_rate_limit(
    user_identifier TEXT,
    action_type TEXT,
    max_attempts INT DEFAULT 5,
    window_minutes INT DEFAULT 15
)
RETURNS BOOLEAN AS $$
DECLARE
    attempt_count INT;
    window_start TIMESTAMPTZ;
BEGIN
    window_start := NOW() - INTERVAL '1 minute' * window_minutes;
    
    SELECT COUNT(*)
    INTO attempt_count
    FROM rate_limit_log
    WHERE identifier = user_identifier
    AND action = action_type
    AND created_at >= window_start;
    
    -- Log this attempt
    INSERT INTO rate_limit_log (identifier, action, created_at)
    VALUES (user_identifier, action_type, NOW());
    
    RETURN attempt_count < max_attempts;
END;
$$ LANGUAGE plpgsql;

-- Usage in authentication
CREATE OR REPLACE FUNCTION check_login_rate_limit()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT check_rate_limit(NEW.email, 'login_attempt', 5, 15) THEN
        RAISE EXCEPTION 'Too many login attempts. Please try again later.';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

## Testing Authentication

### Unit Tests

```typescript
// Authentication tests
describe('Authentication', () => {
  beforeEach(async () => {
    await supabase.auth.signOut()
  })

  test('should sign up user with valid credentials', async () => {
    const { data, error } = await signUp(
      'test@example.com',
      'password123',
      { full_name: 'Test User' }
    )

    expect(error).toBeNull()
    expect(data.user?.email).toBe('test@example.com')
  })

  test('should enforce password requirements', async () => {
    const { error } = await signUp(
      'test@example.com',
      '123', // Too short
      { full_name: 'Test User' }
    )

    expect(error).toBeTruthy()
    expect(error?.message).toContain('Password')
  })

  test('should respect rate limiting', async () => {
    // Attempt multiple failed logins
    for (let i = 0; i < 6; i++) {
      await signIn('test@example.com', 'wrongpassword')
    }

    const { error } = await signIn('test@example.com', 'wrongpassword')
    expect(error?.message).toContain('Too many')
  })
})
```

## Next Steps

With authentication set up, you can now:

1. **[Implement Real-time Features](realtime-features/)** - Add live collaboration
2. **[Set up Vector AI](vector-ai/)** - Enable AI-powered features  
3. **[Create Edge Functions](edge-functions/)** - Build secure API endpoints
4. **[Configure Storage](storage-cdn/)** - Handle file uploads
5. **[Set up Monitoring](monitoring-observability/)** - Track authentication metrics

Your authentication system is now ready to handle enterprise-grade security requirements for AIMatrix applications.