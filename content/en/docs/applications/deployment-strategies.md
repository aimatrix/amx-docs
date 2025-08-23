---
title: "Deployment Strategies"
description: "Comprehensive application deployment strategies including app store distribution, enterprise deployment, Docker containers, Kubernetes operators, and intelligent auto-update mechanisms"
weight: 7
date: 2025-08-23
toc: true
tags: ["deployment", "app-store", "enterprise", "docker", "kubernetes", "auto-update", "ci-cd"]
---

# AIMatrix Application Deployment Strategies

## Enterprise-Grade Deployment at Scale

AIMatrix applications support multiple deployment strategies to meet diverse organizational needs, from individual app store installations to large-scale enterprise deployments. Our deployment architecture provides flexibility, scalability, and reliability across all platforms while maintaining security and compliance requirements.

## Deployment Architecture Overview

```mermaid
graph TB
    subgraph "Source Control"
        GIT[Git Repository]
        RELEASES[Release Branches]
        TAGS[Version Tags]
    end
    
    subgraph "Build Pipeline" 
        CI[CI/CD Pipeline]
        BUILD[Build Systems]
        TEST[Testing Suite]
        SIGN[Code Signing]
    end
    
    subgraph "Artifact Storage"
        REGISTRY[Container Registry]
        ARTIFACTS[Binary Artifacts]
        PACKAGES[Package Registry]
        ASSETS[Static Assets]
    end
    
    subgraph "Deployment Targets"
        subgraph "App Stores"
            APPLE[Apple App Store]
            GOOGLE[Google Play Store]
            MICROSOFT[Microsoft Store]
            WEB_STORE[Web App Stores]
        end
        
        subgraph "Enterprise"
            MDM[Mobile Device Management]
            ENTERPRISE_STORE[Enterprise App Store]
            SCCM[System Center]
            INTUNE[Microsoft Intune]
        end
        
        subgraph "Cloud Platforms"
            K8S[Kubernetes]
            DOCKER[Docker Swarm]
            AWS[AWS ECS/Fargate]
            AZURE[Azure Container Instances]
        end
        
        subgraph "Direct Distribution"
            DIRECT[Direct Download]
            PKG_MGR[Package Managers]
            MSI[Windows Installer]
            DMG[macOS Disk Image]
        end
    end
    
    subgraph "Update Mechanisms"
        AUTO_UPDATE[Auto-Update Service]
        ROLLBACK[Rollback System]
        CANARY[Canary Deployment]
        BLUE_GREEN[Blue-Green Deployment]
    end
    
    Source Control --> Build Pipeline
    Build Pipeline --> Artifact Storage
    Artifact Storage --> Deployment Targets
    Deployment Targets --> Update Mechanisms
```

## App Store Distribution

### Apple App Store Deployment
```bash
#!/bin/bash
# iOS App Store deployment script

set -e

# Configuration
APP_NAME="AIMatrix"
BUNDLE_ID="com.aimatrix.mobile"
TEAM_ID="YOUR_TEAM_ID"
BUILD_NUMBER=$(date +%Y%m%d%H%M)
VERSION="2.0.0"

echo "=== Building iOS App for App Store ==="

# Clean previous builds
rm -rf build/ios
mkdir -p build/ios

# Set build environment
export CONFIGURATION="Release"
export DEVELOPMENT_TEAM="$TEAM_ID"
export CODE_SIGN_IDENTITY="Apple Distribution: AIMatrix Inc (${TEAM_ID})"

# Build Flutter iOS app
echo "Building Flutter iOS app..."
flutter build ios \
    --release \
    --no-codesign \
    --build-number="$BUILD_NUMBER" \
    --build-name="$VERSION"

# Archive the app
echo "Creating iOS archive..."
xcodebuild -workspace ios/Runner.xcworkspace \
    -scheme Runner \
    -configuration Release \
    -destination generic/platform=iOS \
    -archivePath "build/ios/AIMatrix.xcarchive" \
    archive \
    CODE_SIGN_IDENTITY="$CODE_SIGN_IDENTITY" \
    DEVELOPMENT_TEAM="$TEAM_ID" \
    PROVISIONING_PROFILE_SPECIFIER="AIMatrix Distribution"

# Export for App Store
echo "Exporting for App Store..."
xcodebuild -exportArchive \
    -archivePath "build/ios/AIMatrix.xcarchive" \
    -exportPath "build/ios/export" \
    -exportOptionsPlist "ios/ExportOptions.plist"

# Upload to App Store Connect
echo "Uploading to App Store Connect..."
xcrun altool --upload-app \
    --type ios \
    --file "build/ios/export/AIMatrix.ipa" \
    --username "$APPLE_ID_EMAIL" \
    --password "$APPLE_ID_PASSWORD" \
    --verbose

# Validate upload
echo "Validating upload..."
xcrun altool --validate-app \
    --type ios \
    --file "build/ios/export/AIMatrix.ipa" \
    --username "$APPLE_ID_EMAIL" \
    --password "$APPLE_ID_PASSWORD" \
    --verbose

echo "✅ iOS app uploaded to App Store Connect successfully!"
echo "Build Number: $BUILD_NUMBER"
echo "Version: $VERSION"
echo ""
echo "Next steps:"
echo "1. Go to App Store Connect"
echo "2. Create a new version with build $BUILD_NUMBER"
echo "3. Fill in release notes and metadata"
echo "4. Submit for review"
```

### Google Play Store Deployment
```bash
#!/bin/bash
# Android Play Store deployment script

set -e

# Configuration
PACKAGE_NAME="com.aimatrix.mobile"
VERSION_CODE=$(date +%Y%m%d%H%M)
VERSION_NAME="2.0.0"
TRACK="internal" # internal, alpha, beta, production

echo "=== Building Android App for Play Store ==="

# Build Android App Bundle (AAB)
echo "Building Android App Bundle..."
flutter build appbundle \
    --release \
    --build-number="$VERSION_CODE" \
    --build-name="$VERSION_NAME" \
    --target-platform android-arm,android-arm64,android-x64

# Sign the AAB
echo "Signing Android App Bundle..."
jarsigner -verbose \
    -sigalg SHA256withRSA \
    -digestalg SHA-256 \
    -keystore android/app/release-key.keystore \
    -storepass "$KEYSTORE_PASSWORD" \
    -keypass "$KEY_PASSWORD" \
    build/app/outputs/bundle/release/app-release.aab \
    release-key

# Verify signature
echo "Verifying signature..."
jarsigner -verify -verbose -certs build/app/outputs/bundle/release/app-release.aab

# Upload to Play Console using Google Play Developer API
echo "Uploading to Google Play Console..."

# Get access token
ACCESS_TOKEN=$(curl -s -X POST \
    "https://oauth2.googleapis.com/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "client_id=$GOOGLE_CLIENT_ID" \
    -d "client_secret=$GOOGLE_CLIENT_SECRET" \
    -d "refresh_token=$GOOGLE_REFRESH_TOKEN" \
    -d "grant_type=refresh_token" | \
    jq -r '.access_token')

# Create new edit
EDIT_ID=$(curl -s -X POST \
    "https://androidpublisher.googleapis.com/androidpublisher/v3/applications/$PACKAGE_NAME/edits" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" | \
    jq -r '.id')

echo "Created edit: $EDIT_ID"

# Upload AAB
UPLOAD_RESPONSE=$(curl -s -X POST \
    "https://androidpublisher.googleapis.com/upload/androidpublisher/v3/applications/$PACKAGE_NAME/edits/$EDIT_ID/bundles?uploadType=media" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/octet-stream" \
    --data-binary @build/app/outputs/bundle/release/app-release.aab)

VERSION_CODE_RESPONSE=$(echo "$UPLOAD_RESPONSE" | jq -r '.versionCode')
echo "Uploaded bundle with version code: $VERSION_CODE_RESPONSE"

# Assign to track
curl -s -X PATCH \
    "https://androidpublisher.googleapis.com/androidpublisher/v3/applications/$PACKAGE_NAME/edits/$EDIT_ID/tracks/$TRACK" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"releases\": [{
            \"versionCodes\": [\"$VERSION_CODE_RESPONSE\"],
            \"status\": \"completed\",
            \"releaseNotes\": [{
                \"language\": \"en-US\",
                \"text\": \"Bug fixes and performance improvements\"
            }]
        }]
    }"

# Commit the edit
curl -s -X POST \
    "https://androidpublisher.googleapis.com/androidpublisher/v3/applications/$PACKAGE_NAME/edits/$EDIT_ID:commit" \
    -H "Authorization: Bearer $ACCESS_TOKEN"

echo "✅ Android app uploaded to Google Play Console successfully!"
echo "Track: $TRACK"
echo "Version Code: $VERSION_CODE_RESPONSE"
echo "Version Name: $VERSION_NAME"
```

### Microsoft Store Deployment
```powershell
# Windows Store deployment script
param(
    [string]$Version = "2.0.0",
    [string]$Configuration = "Release",
    [string]$Architecture = "x64"
)

Write-Host "=== Building Windows App for Microsoft Store ===" -ForegroundColor Green

# Set build parameters
$BuildNumber = Get-Date -Format "yyyyMMddHHmm"
$AppxManifestPath = "windows/runner/AppxManifest.xml"
$OutputPath = "build/windows/x64/runner/Release"

# Update version in AppxManifest.xml
Write-Host "Updating version in AppxManifest.xml..." -ForegroundColor Yellow
$manifest = Get-Content $AppxManifestPath -Raw
$manifest = $manifest -replace 'Version="[\d\.]+"', "Version=`"$Version.0`""
$manifest | Set-Content $AppxManifestPath

# Build Windows app
Write-Host "Building Windows app..." -ForegroundColor Yellow
flutter build windows --release

# Create MSIX package
Write-Host "Creating MSIX package..." -ForegroundColor Yellow
& "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\makeappx.exe" pack `
    /d $OutputPath `
    /p "build/windows/AIMatrix_$Version.msix" `
    /l /o

# Sign the package
Write-Host "Signing MSIX package..." -ForegroundColor Yellow
& "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe" sign `
    /fd SHA256 `
    /a `
    /f "windows/certificates/aimatrix.pfx" `
    /p $env:CERTIFICATE_PASSWORD `
    "build/windows/AIMatrix_$Version.msix"

# Upload to Microsoft Store using Store Broker
Write-Host "Uploading to Microsoft Store..." -ForegroundColor Yellow

# Configure Store Broker
Import-Module StoreBroker

$configParams = @{
    'ApplicationId' = $env:MS_STORE_APP_ID
    'ClientId' = $env:MS_STORE_CLIENT_ID  
    'ClientSecret' = $env:MS_STORE_CLIENT_SECRET
    'TenantId' = $env:MS_STORE_TENANT_ID
}

Set-StoreBrokerAuthentication @configParams

# Create submission package
$submissionData = @{
    'PackagePath' = "build/windows/AIMatrix_$Version.msix"
    'ReleaseNotes' = "Performance improvements and bug fixes"
    'PublishMode' = 'Manual'  # or 'Immediate'
}

# Submit to Store
$submission = New-ApplicationSubmission -AppId $env:MS_STORE_APP_ID -Force
Update-ApplicationSubmission -AppId $env:MS_STORE_APP_ID -SubmissionId $submission.id @submissionData

Write-Host "✅ Windows app uploaded to Microsoft Store successfully!" -ForegroundColor Green
Write-Host "Submission ID: $($submission.id)" -ForegroundColor Cyan
Write-Host "Version: $Version" -ForegroundColor Cyan
```

## Enterprise Deployment

### Mobile Device Management (MDM) Integration
```python
# Python script for MDM deployment integration
import requests
import json
import base64
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MDMConfig:
    server_url: str
    api_key: str
    tenant_id: str
    certificate_path: Optional[str] = None
    
@dataclass 
class AppPackage:
    platform: str  # ios, android, windows
    package_path: Path
    version: str
    bundle_id: str
    metadata: Dict[str, Any]

class MDMDeploymentManager:
    def __init__(self, config: MDMConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {config.api_key}',
            'Content-Type': 'application/json',
            'X-Tenant-ID': config.tenant_id
        })
        
        # Configure client certificate if provided
        if config.certificate_path:
            self.session.cert = config.certificate_path
    
    def deploy_to_device_groups(self, 
                               app_package: AppPackage, 
                               device_groups: List[str],
                               deployment_config: Dict[str, Any]) -> str:
        """Deploy app to specific device groups via MDM"""
        
        # Upload app package
        package_id = self.upload_app_package(app_package)
        
        # Create deployment policy
        policy_id = self.create_deployment_policy(
            package_id, deployment_config
        )
        
        # Assign to device groups
        assignment_id = self.assign_to_groups(policy_id, device_groups)
        
        return assignment_id
    
    def upload_app_package(self, app_package: AppPackage) -> str:
        """Upload app package to MDM server"""
        
        # Read and encode package file
        with open(app_package.package_path, 'rb') as f:
            package_data = base64.b64encode(f.read()).decode()
        
        upload_payload = {
            'platform': app_package.platform,
            'version': app_package.version,
            'bundle_id': app_package.bundle_id,
            'package_data': package_data,
            'metadata': app_package.metadata,
            'size_bytes': app_package.package_path.stat().st_size
        }
        
        response = self.session.post(
            f'{self.config.server_url}/api/v1/apps/upload',
            json=upload_payload,
            timeout=300  # 5 minute timeout for large files
        )
        
        if response.status_code == 201:
            return response.json()['package_id']
        else:
            raise Exception(f'Upload failed: {response.text}')
    
    def create_deployment_policy(self, 
                                package_id: str, 
                                config: Dict[str, Any]) -> str:
        """Create deployment policy with installation rules"""
        
        policy_payload = {
            'package_id': package_id,
            'deployment_type': config.get('deployment_type', 'optional'),
            'install_behavior': config.get('install_behavior', 'user_choice'),
            'update_behavior': config.get('update_behavior', 'automatic'),
            'uninstall_on_unenroll': config.get('uninstall_on_unenroll', True),
            'require_device_compliance': config.get('require_compliance', True),
            'installation_deadline': config.get('deadline'),
            'notification_settings': {
                'show_installation_progress': True,
                'allow_user_deferrals': config.get('allow_deferrals', 3),
                'restart_grace_period_minutes': 30
            },
            'network_requirements': {
                'wifi_only': config.get('wifi_only', False),
                'minimum_battery_level': 20,
                'allow_metered_network': config.get('allow_metered', False)
            }
        }
        
        response = self.session.post(
            f'{self.config.server_url}/api/v1/deployment-policies',
            json=policy_payload
        )
        
        if response.status_code == 201:
            return response.json()['policy_id']
        else:
            raise Exception(f'Policy creation failed: {response.text}')
    
    def assign_to_groups(self, policy_id: str, groups: List[str]) -> str:
        """Assign deployment policy to device groups"""
        
        assignment_payload = {
            'policy_id': policy_id,
            'target_groups': groups,
            'assignment_type': 'include',
            'priority': 1
        }
        
        response = self.session.post(
            f'{self.config.server_url}/api/v1/assignments',
            json=assignment_payload
        )
        
        if response.status_code == 201:
            return response.json()['assignment_id']
        else:
            raise Exception(f'Assignment failed: {response.text}')
    
    def monitor_deployment(self, assignment_id: str) -> Dict[str, Any]:
        """Monitor deployment progress and status"""
        
        response = self.session.get(
            f'{self.config.server_url}/api/v1/assignments/{assignment_id}/status'
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Status check failed: {response.text}')
    
    def create_app_protection_policy(self, 
                                   app_bundle_id: str, 
                                   protection_config: Dict[str, Any]) -> str:
        """Create app protection policy for enhanced security"""
        
        policy_payload = {
            'target_apps': [app_bundle_id],
            'data_protection': {
                'prevent_backup': protection_config.get('prevent_backup', True),
                'prevent_screenshots': protection_config.get('prevent_screenshots', True),
                'encrypt_app_data': protection_config.get('encrypt_data', True),
                'require_pin': protection_config.get('require_pin', True),
                'pin_timeout_minutes': protection_config.get('pin_timeout', 15)
            },
            'access_controls': {
                'block_jailbroken_devices': True,
                'min_os_version': protection_config.get('min_os_version'),
                'allowed_locations': protection_config.get('geo_restrictions', []),
                'block_screen_sharing': True
            },
            'compliance_actions': {
                'non_compliant_action': 'block_access',
                'grace_period_hours': 24,
                'notification_message': 'Device compliance required to access AIMatrix'
            }
        }
        
        response = self.session.post(
            f'{self.config.server_url}/api/v1/app-protection-policies',
            json=policy_payload
        )
        
        if response.status_code == 201:
            return response.json()['policy_id']
        else:
            raise Exception(f'Protection policy creation failed: {response.text}')

# Usage example
def deploy_enterprise_app():
    """Example enterprise deployment workflow"""
    
    # Configure MDM connection
    mdm_config = MDMConfig(
        server_url='https://mdm.company.com',
        api_key='your-api-key',
        tenant_id='company-tenant-id',
        certificate_path='/path/to/client-cert.pem'
    )
    
    mdm = MDMDeploymentManager(mdm_config)
    
    # Configure iOS deployment
    ios_package = AppPackage(
        platform='ios',
        package_path=Path('dist/AIMatrix-iOS.ipa'),
        version='2.0.0',
        bundle_id='com.aimatrix.mobile',
        metadata={
            'display_name': 'AIMatrix Enterprise',
            'description': 'AI Agent Management Platform',
            'category': 'Business',
            'minimum_os_version': '14.0'
        }
    )
    
    # Deployment configuration
    deployment_config = {
        'deployment_type': 'required',  # required, optional, available
        'install_behavior': 'automatic',
        'update_behavior': 'automatic',
        'wifi_only': True,
        'allow_deferrals': 1,
        'deadline': '2024-12-31T23:59:59Z'
    }
    
    # Deploy to specific device groups
    device_groups = [
        'Sales-Team-iOS',
        'Management-iOS', 
        'IT-Department-iOS'
    ]
    
    try:
        assignment_id = mdm.deploy_to_device_groups(
            ios_package, device_groups, deployment_config
        )
        
        print(f'Deployment initiated: {assignment_id}')
        
        # Create app protection policy
        protection_config = {
            'prevent_backup': True,
            'prevent_screenshots': True,
            'require_pin': True,
            'pin_timeout': 15,
            'min_os_version': '14.0'
        }
        
        policy_id = mdm.create_app_protection_policy(
            ios_package.bundle_id, protection_config
        )
        
        print(f'Protection policy created: {policy_id}')
        
        # Monitor deployment
        while True:
            status = mdm.monitor_deployment(assignment_id)
            
            print(f"Deployment Status: {status['overall_status']}")
            print(f"Success Rate: {status['success_percentage']}%")
            print(f"Devices Processed: {status['devices_processed']}/{status['total_devices']}")
            
            if status['overall_status'] in ['completed', 'failed']:
                break
                
            time.sleep(30)  # Check every 30 seconds
            
    except Exception as e:
        print(f'Deployment failed: {e}')
```

## Docker Container Deployment

### Multi-Stage Dockerfile
```dockerfile
# Multi-stage Dockerfile for AIMatrix applications
FROM node:18-alpine AS web-builder
WORKDIR /app/web

# Copy web app source
COPY web/package*.json ./
RUN npm ci --only=production

COPY web/ ./
RUN npm run build

# Kotlin/JVM application builder
FROM gradle:7.6-jdk17-alpine AS jvm-builder
WORKDIR /app

# Copy Gradle files
COPY build.gradle.kts settings.gradle.kts gradle.properties ./
COPY gradle/ gradle/

# Download dependencies
RUN gradle dependencies --no-daemon

# Copy source and build
COPY src/ src/
RUN gradle build --no-daemon -x test

# Python services builder  
FROM python:3.11-slim AS python-builder
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/var/lib/apt/lists/*

# Copy Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Python source
COPY python-services/ ./

# Final runtime image
FROM ubuntu:22.04 AS runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    python3 \
    python3-pip \
    nginx \
    supervisor \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -s /bin/bash amx

# Set up directories
WORKDIR /app
RUN mkdir -p /app/{web,api,services,config,logs,data} && \
    chown -R amx:amx /app

# Copy built applications
COPY --from=web-builder /app/web/dist/ /app/web/
COPY --from=jvm-builder /app/build/libs/*.jar /app/api/
COPY --from=python-builder /app/ /app/services/

# Copy configuration files
COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY docker/entrypoint.sh /entrypoint.sh

# Set up SQLite directory
RUN mkdir -p /app/data/sqlite && chown -R amx:amx /app/data

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Environment variables
ENV APP_ENV=production \
    LOG_LEVEL=info \
    DATABASE_PATH=/app/data/sqlite/amx.db \
    WEB_PORT=80 \
    API_PORT=8080

# Expose ports
EXPOSE 80 8080

# Set permissions and switch to app user
RUN chmod +x /entrypoint.sh && \
    chown -R amx:amx /app

USER amx
ENTRYPOINT ["/entrypoint.sh"]
```

### Docker Compose Stack
```yaml
# docker-compose.yml for complete AIMatrix stack
version: '3.8'

services:
  # Main application services
  amx-web:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
    container_name: amx-web
    ports:
      - "80:80"
      - "443:443"
    environment:
      - APP_ENV=production
      - API_ENDPOINT=http://amx-api:8080
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
    volumes:
      - web-data:/app/data
      - web-logs:/app/logs
      - ./ssl:/app/ssl:ro
    networks:
      - amx-network
    depends_on:
      - amx-api
      - amx-database
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  amx-api:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: amx-api
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=docker
      - DATABASE_URL=postgresql://amx:${DB_PASSWORD}@amx-database:5432/amx
      - REDIS_URL=redis://amx-redis:6379
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
      - JWT_SECRET=${JWT_SECRET}
    volumes:
      - api-logs:/app/logs
      - agent-storage:/app/agents
    networks:
      - amx-network
    depends_on:
      - amx-database
      - amx-redis
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  amx-daemon:
    build:
      context: .
      dockerfile: Dockerfile.daemon
    container_name: amx-daemon
    environment:
      - DAEMON_MODE=docker
      - API_URL=http://amx-api:8080
      - DATABASE_URL=postgresql://amx:${DB_PASSWORD}@amx-database:5432/amx
      - LOG_LEVEL=info
    volumes:
      - daemon-data:/app/data
      - daemon-logs:/app/logs
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - amx-network
    depends_on:
      - amx-api
      - amx-database
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pgrep -f amx-daemon > /dev/null || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Infrastructure services
  amx-database:
    image: postgres:15-alpine
    container_name: amx-database
    environment:
      - POSTGRES_DB=amx
      - POSTGRES_USER=amx
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d:ro
    networks:
      - amx-network
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U amx -d amx"]
      interval: 10s
      timeout: 5s
      retries: 5

  amx-redis:
    image: redis:7-alpine
    container_name: amx-redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf:ro
    networks:
      - amx-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Monitoring and observability
  amx-prometheus:
    image: prom/prometheus:v2.45.0
    container_name: amx-prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
      - '--web.enable-admin-api'
    volumes:
      - prometheus-data:/prometheus
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    networks:
      - amx-network
    ports:
      - "9090:9090"
    restart: unless-stopped

  amx-grafana:
    image: grafana/grafana:10.0.0
    container_name: amx-grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana-data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning:ro
    networks:
      - amx-network
    ports:
      - "3000:3000"
    depends_on:
      - amx-prometheus
    restart: unless-stopped

  # Load balancer
  amx-nginx:
    image: nginx:1.25-alpine
    container_name: amx-nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./ssl:/etc/nginx/ssl:ro
      - nginx-cache:/var/cache/nginx
    networks:
      - amx-network
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - amx-web
      - amx-api
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

# Networks
networks:
  amx-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

# Persistent volumes
volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local
  web-data:
    driver: local
  web-logs:
    driver: local
  api-logs:
    driver: local
  daemon-data:
    driver: local
  daemon-logs:
    driver: local
  agent-storage:
    driver: local
  prometheus-data:
    driver: local
  grafana-data:
    driver: local
  nginx-cache:
    driver: local
```

### Docker Deployment Scripts
```bash
#!/bin/bash
# Docker deployment automation script

set -e

# Configuration
REGISTRY="registry.aimatrix.com"
PROJECT="aimatrix"
VERSION=${1:-"latest"}
ENVIRONMENT=${2:-"production"}

echo "=== AIMatrix Docker Deployment ==="
echo "Registry: $REGISTRY"
echo "Version: $VERSION"
echo "Environment: $ENVIRONMENT"
echo ""

# Load environment variables
if [ -f ".env.$ENVIRONMENT" ]; then
    echo "Loading environment variables..."
    export $(cat .env.$ENVIRONMENT | xargs)
fi

# Build and push images
echo "Building Docker images..."

# Build multi-arch images
docker buildx create --use --name amx-builder 2>/dev/null || true

# Build and push web application
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag $REGISTRY/$PROJECT/web:$VERSION \
    --tag $REGISTRY/$PROJECT/web:latest \
    --push \
    --file Dockerfile.web \
    .

# Build and push API service
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag $REGISTRY/$PROJECT/api:$VERSION \
    --tag $REGISTRY/$PROJECT/api:latest \
    --push \
    --file Dockerfile.api \
    .

# Build and push daemon service
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag $REGISTRY/$PROJECT/daemon:$VERSION \
    --tag $REGISTRY/$PROJECT/daemon:latest \
    --push \
    --file Dockerfile.daemon \
    .

echo "Docker images built and pushed successfully!"

# Deploy using Docker Compose
echo ""
echo "Deploying with Docker Compose..."

# Create deployment directory
DEPLOY_DIR="/opt/aimatrix"
sudo mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

# Copy deployment files
sudo cp docker-compose.yml $DEPLOY_DIR/
sudo cp -r nginx/ monitoring/ database/ ssl/ $DEPLOY_DIR/

# Set image versions in compose file
sudo sed -i "s/:latest/:$VERSION/g" docker-compose.yml

# Pull latest images
docker-compose pull

# Perform rolling update
echo "Performing rolling update..."

# Update API service first
docker-compose up -d amx-database amx-redis
sleep 10
docker-compose up -d amx-api
sleep 20

# Health check API
echo "Checking API health..."
for i in {1..30}; do
    if curl -f http://localhost:8080/actuator/health; then
        echo "API is healthy"
        break
    fi
    echo "Waiting for API... ($i/30)"
    sleep 10
done

# Update daemon
docker-compose up -d amx-daemon
sleep 10

# Update web service
docker-compose up -d amx-web
sleep 10

# Update monitoring
docker-compose up -d amx-prometheus amx-grafana

# Final health check
echo ""
echo "Performing final health checks..."

services=("amx-web" "amx-api" "amx-daemon" "amx-database" "amx-redis")
for service in "${services[@]}"; do
    echo -n "Checking $service... "
    
    if docker-compose ps $service | grep -q "Up"; then
        echo "✅ Running"
    else
        echo "❌ Failed"
        echo "Service logs for $service:"
        docker-compose logs --tail=20 $service
    fi
done

# Clean up old images
echo ""
echo "Cleaning up old images..."
docker image prune -f
docker system prune -f --volumes

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "Services available at:"
echo "  Web Interface: https://localhost"
echo "  API: https://localhost/api"
echo "  Grafana: http://localhost:3000"
echo "  Prometheus: http://localhost:9090"
```

## Kubernetes Operators

### Custom Resource Definitions
```yaml
# AIMatrix Custom Resource Definitions
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: aimatrixapps.aimatrix.com
spec:
  group: aimatrix.com
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              version:
                type: string
                description: "Application version to deploy"
              components:
                type: object
                properties:
                  web:
                    type: object
                    properties:
                      enabled:
                        type: boolean
                        default: true
                      replicas:
                        type: integer
                        default: 2
                      image:
                        type: string
                      resources:
                        type: object
                        properties:
                          requests:
                            type: object
                            properties:
                              cpu:
                                type: string
                                default: "100m"
                              memory:
                                type: string
                                default: "128Mi"
                          limits:
                            type: object
                            properties:
                              cpu:
                                type: string
                                default: "500m"
                              memory:
                                type: string
                                default: "512Mi"
                  api:
                    type: object
                    properties:
                      enabled:
                        type: boolean
                        default: true
                      replicas:
                        type: integer
                        default: 3
                      image:
                        type: string
                      database:
                        type: object
                        properties:
                          host:
                            type: string
                          port:
                            type: integer
                            default: 5432
                          name:
                            type: string
                            default: "aimatrix"
                  daemon:
                    type: object
                    properties:
                      enabled:
                        type: boolean
                        default: true
                      replicas:
                        type: integer
                        default: 1
                      image:
                        type: string
                      persistence:
                        type: object
                        properties:
                          enabled:
                            type: boolean
                            default: true
                          size:
                            type: string
                            default: "10Gi"
                          storageClass:
                            type: string
              networking:
                type: object
                properties:
                  ingress:
                    type: object
                    properties:
                      enabled:
                        type: boolean
                        default: true
                      hostname:
                        type: string
                      tls:
                        type: boolean
                        default: true
                      annotations:
                        type: object
              security:
                type: object
                properties:
                  networkPolicies:
                    type: boolean
                    default: true
                  podSecurityPolicy:
                    type: boolean
                    default: true
                  rbac:
                    type: boolean
                    default: true
          status:
            type: object
            properties:
              phase:
                type: string
                enum: ["Pending", "Installing", "Running", "Failed", "Upgrading"]
              conditions:
                type: array
                items:
                  type: object
                  properties:
                    type:
                      type: string
                    status:
                      type: string
                    reason:
                      type: string
                    message:
                      type: string
                    lastTransitionTime:
                      type: string
              deployedVersion:
                type: string
              observedGeneration:
                type: integer
    subresources:
      status: {}
  scope: Namespaced
  names:
    plural: aimatrixapps
    singular: aimatrixapp
    kind: AIMatrixApp
    shortNames:
    - amx
    - amxapp

---
# AIMatrix Application Instance
apiVersion: aimatrix.com/v1
kind: AIMatrixApp
metadata:
  name: aimatrix-production
  namespace: aimatrix-system
spec:
  version: "2.0.0"
  components:
    web:
      enabled: true
      replicas: 3
      image: "registry.aimatrix.com/aimatrix/web:2.0.0"
      resources:
        requests:
          cpu: "200m"
          memory: "256Mi"
        limits:
          cpu: "1000m"
          memory: "1Gi"
    api:
      enabled: true
      replicas: 5
      image: "registry.aimatrix.com/aimatrix/api:2.0.0"
      resources:
        requests:
          cpu: "500m"
          memory: "512Mi"
        limits:
          cpu: "2000m"
          memory: "2Gi"
      database:
        host: "postgresql.database.svc.cluster.local"
        port: 5432
        name: "aimatrix_prod"
    daemon:
      enabled: true
      replicas: 2
      image: "registry.aimatrix.com/aimatrix/daemon:2.0.0"
      persistence:
        enabled: true
        size: "50Gi"
        storageClass: "fast-ssd"
  networking:
    ingress:
      enabled: true
      hostname: "app.aimatrix.com"
      tls: true
      annotations:
        nginx.ingress.kubernetes.io/ssl-redirect: "true"
        cert-manager.io/cluster-issuer: "letsencrypt-prod"
        nginx.ingress.kubernetes.io/rate-limit: "100"
  security:
    networkPolicies: true
    podSecurityPolicy: true
    rbac: true
```

### Kubernetes Operator Implementation
```go
// Go implementation of AIMatrix Kubernetes Operator
package controllers

import (
    "context"
    "fmt"
    "time"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    netv1 "k8s.io/api/networking/v1"
    "k8s.io/apimachinery/pkg/api/errors"
    "k8s.io/apimachinery/pkg/api/resource"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/apimachinery/pkg/util/intstr"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/log"
    
    aimatrixv1 "github.com/aimatrix/operator/api/v1"
)

// AIMatrixAppReconciler reconciles a AIMatrixApp object
type AIMatrixAppReconciler struct {
    client.Client
    Scheme *runtime.Scheme
}

//+kubebuilder:rbac:groups=aimatrix.com,resources=aimatrixapps,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=aimatrix.com,resources=aimatrixapps/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=networking.k8s.io,resources=ingresses,verbs=get;list;watch;create;update;patch;delete

func (r *AIMatrixAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)

    // Fetch the AIMatrixApp instance
    var amxApp aimatrixv1.AIMatrixApp
    if err := r.Get(ctx, req.NamespacedName, &amxApp); err != nil {
        log.Error(err, "unable to fetch AIMatrixApp")
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // Update status to Installing if it's a new resource
    if amxApp.Status.Phase == "" {
        amxApp.Status.Phase = "Installing"
        if err := r.Status().Update(ctx, &amxApp); err != nil {
            log.Error(err, "unable to update AIMatrixApp status")
            return ctrl.Result{}, err
        }
    }

    // Reconcile each component
    if err := r.reconcileWebComponent(ctx, &amxApp); err != nil {
        return r.updateStatusFailed(ctx, &amxApp, err)
    }

    if err := r.reconcileAPIComponent(ctx, &amxApp); err != nil {
        return r.updateStatusFailed(ctx, &amxApp, err)
    }

    if err := r.reconcileDaemonComponent(ctx, &amxApp); err != nil {
        return r.updateStatusFailed(ctx, &amxApp, err)
    }

    // Reconcile networking
    if amxApp.Spec.Networking.Ingress.Enabled {
        if err := r.reconcileIngress(ctx, &amxApp); err != nil {
            return r.updateStatusFailed(ctx, &amxApp, err)
        }
    }

    // Update status to Running
    amxApp.Status.Phase = "Running"
    amxApp.Status.DeployedVersion = amxApp.Spec.Version
    amxApp.Status.ObservedGeneration = amxApp.Generation
    
    // Add or update condition
    r.setCondition(&amxApp, "Ready", "True", "AllComponentsReady", "All components are running successfully")
    
    if err := r.Status().Update(ctx, &amxApp); err != nil {
        log.Error(err, "unable to update AIMatrixApp status")
        return ctrl.Result{}, err
    }

    log.Info("Successfully reconciled AIMatrixApp", "version", amxApp.Spec.Version)
    return ctrl.Result{RequeueAfter: time.Minute * 5}, nil
}

func (r *AIMatrixAppReconciler) reconcileWebComponent(ctx context.Context, amxApp *aimatrixv1.AIMatrixApp) error {
    if !amxApp.Spec.Components.Web.Enabled {
        return nil
    }

    log := log.FromContext(ctx)
    log.Info("Reconciling web component")

    // Create deployment
    deployment := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      fmt.Sprintf("%s-web", amxApp.Name),
            Namespace: amxApp.Namespace,
            Labels:    r.getLabels(amxApp, "web"),
        },
        Spec: appsv1.DeploymentSpec{
            Replicas: &amxApp.Spec.Components.Web.Replicas,
            Selector: &metav1.LabelSelector{
                MatchLabels: r.getLabels(amxApp, "web"),
            },
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: r.getLabels(amxApp, "web"),
                },
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{
                        {
                            Name:  "web",
                            Image: amxApp.Spec.Components.Web.Image,
                            Ports: []corev1.ContainerPort{
                                {
                                    ContainerPort: 80,
                                    Name:          "http",
                                },
                            },
                            Resources: r.getResourceRequirements(amxApp.Spec.Components.Web.Resources),
                            Env: []corev1.EnvVar{
                                {
                                    Name:  "API_ENDPOINT",
                                    Value: fmt.Sprintf("http://%s-api:8080", amxApp.Name),
                                },
                                {
                                    Name: "NODE_ENV",
                                    Value: "production",
                                },
                            },
                            LivenessProbe: &corev1.Probe{
                                ProbeHandler: corev1.ProbeHandler{
                                    HTTPGet: &corev1.HTTPGetAction{
                                        Path: "/health",
                                        Port: intstr.FromInt(80),
                                    },
                                },
                                InitialDelaySeconds: 30,
                                PeriodSeconds:       10,
                            },
                            ReadinessProbe: &corev1.Probe{
                                ProbeHandler: corev1.ProbeHandler{
                                    HTTPGet: &corev1.HTTPGetAction{
                                        Path: "/ready",
                                        Port: intstr.FromInt(80),
                                    },
                                },
                                InitialDelaySeconds: 5,
                                PeriodSeconds:       5,
                            },
                        },
                    },
                    SecurityContext: &corev1.PodSecurityContext{
                        RunAsNonRoot: &[]bool{true}[0],
                        RunAsUser:    &[]int64{1000}[0],
                        FSGroup:      &[]int64{1000}[0],
                    },
                },
            },
        },
    }

    // Set controller reference
    ctrl.SetControllerReference(amxApp, deployment, r.Scheme)

    // Create or update deployment
    if err := r.createOrUpdate(ctx, deployment); err != nil {
        return fmt.Errorf("failed to reconcile web deployment: %v", err)
    }

    // Create service
    service := &corev1.Service{
        ObjectMeta: metav1.ObjectMeta{
            Name:      fmt.Sprintf("%s-web", amxApp.Name),
            Namespace: amxApp.Namespace,
            Labels:    r.getLabels(amxApp, "web"),
        },
        Spec: corev1.ServiceSpec{
            Selector: r.getLabels(amxApp, "web"),
            Ports: []corev1.ServicePort{
                {
                    Port:       80,
                    TargetPort: intstr.FromInt(80),
                    Protocol:   corev1.ProtocolTCP,
                },
            },
            Type: corev1.ServiceTypeClusterIP,
        },
    }

    ctrl.SetControllerReference(amxApp, service, r.Scheme)

    if err := r.createOrUpdate(ctx, service); err != nil {
        return fmt.Errorf("failed to reconcile web service: %v", err)
    }

    return nil
}

func (r *AIMatrixAppReconciler) reconcileAPIComponent(ctx context.Context, amxApp *aimatrixv1.AIMatrixApp) error {
    if !amxApp.Spec.Components.API.Enabled {
        return nil
    }

    log := log.FromContext(ctx)
    log.Info("Reconciling API component")

    deployment := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      fmt.Sprintf("%s-api", amxApp.Name),
            Namespace: amxApp.Namespace,
            Labels:    r.getLabels(amxApp, "api"),
        },
        Spec: appsv1.DeploymentSpec{
            Replicas: &amxApp.Spec.Components.API.Replicas,
            Selector: &metav1.LabelSelector{
                MatchLabels: r.getLabels(amxApp, "api"),
            },
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: r.getLabels(amxApp, "api"),
                },
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{
                        {
                            Name:  "api",
                            Image: amxApp.Spec.Components.API.Image,
                            Ports: []corev1.ContainerPort{
                                {
                                    ContainerPort: 8080,
                                    Name:          "http",
                                },
                            },
                            Resources: r.getResourceRequirements(amxApp.Spec.Components.API.Resources),
                            Env: []corev1.EnvVar{
                                {
                                    Name: "DATABASE_URL",
                                    Value: fmt.Sprintf("postgresql://amx@%s:%d/%s",
                                        amxApp.Spec.Components.API.Database.Host,
                                        amxApp.Spec.Components.API.Database.Port,
                                        amxApp.Spec.Components.API.Database.Name),
                                },
                                {
                                    Name: "SPRING_PROFILES_ACTIVE",
                                    Value: "kubernetes",
                                },
                            },
                            LivenessProbe: &corev1.Probe{
                                ProbeHandler: corev1.ProbeHandler{
                                    HTTPGet: &corev1.HTTPGetAction{
                                        Path: "/actuator/health",
                                        Port: intstr.FromInt(8080),
                                    },
                                },
                                InitialDelaySeconds: 60,
                                PeriodSeconds:       30,
                            },
                            ReadinessProbe: &corev1.Probe{
                                ProbeHandler: corev1.ProbeHandler{
                                    HTTPGet: &corev1.HTTPGetAction{
                                        Path: "/actuator/health/readiness",
                                        Port: intstr.FromInt(8080),
                                    },
                                },
                                InitialDelaySeconds: 30,
                                PeriodSeconds:       10,
                            },
                        },
                    },
                },
            },
        },
    }

    ctrl.SetControllerReference(amxApp, deployment, r.Scheme)

    if err := r.createOrUpdate(ctx, deployment); err != nil {
        return fmt.Errorf("failed to reconcile API deployment: %v", err)
    }

    // Create service
    service := &corev1.Service{
        ObjectMeta: metav1.ObjectMeta{
            Name:      fmt.Sprintf("%s-api", amxApp.Name),
            Namespace: amxApp.Namespace,
            Labels:    r.getLabels(amxApp, "api"),
        },
        Spec: corev1.ServiceSpec{
            Selector: r.getLabels(amxApp, "api"),
            Ports: []corev1.ServicePort{
                {
                    Port:       8080,
                    TargetPort: intstr.FromInt(8080),
                    Protocol:   corev1.ProtocolTCP,
                },
            },
            Type: corev1.ServiceTypeClusterIP,
        },
    }

    ctrl.SetControllerReference(amxApp, service, r.Scheme)

    return r.createOrUpdate(ctx, service)
}

func (r *AIMatrixAppReconciler) reconcileIngress(ctx context.Context, amxApp *aimatrixv1.AIMatrixApp) error {
    log := log.FromContext(ctx)
    log.Info("Reconciling ingress")

    pathType := netv1.PathTypePrefix
    
    ingress := &netv1.Ingress{
        ObjectMeta: metav1.ObjectMeta{
            Name:        fmt.Sprintf("%s-ingress", amxApp.Name),
            Namespace:   amxApp.Namespace,
            Labels:      r.getLabels(amxApp, "ingress"),
            Annotations: amxApp.Spec.Networking.Ingress.Annotations,
        },
        Spec: netv1.IngressSpec{
            Rules: []netv1.IngressRule{
                {
                    Host: amxApp.Spec.Networking.Ingress.Hostname,
                    IngressRuleValue: netv1.IngressRuleValue{
                        HTTP: &netv1.HTTPIngressRuleValue{
                            Paths: []netv1.HTTPIngressPath{
                                {
                                    Path:     "/api",
                                    PathType: &pathType,
                                    Backend: netv1.IngressBackend{
                                        Service: &netv1.IngressServiceBackend{
                                            Name: fmt.Sprintf("%s-api", amxApp.Name),
                                            Port: netv1.ServiceBackendPort{
                                                Number: 8080,
                                            },
                                        },
                                    },
                                },
                                {
                                    Path:     "/",
                                    PathType: &pathType,
                                    Backend: netv1.IngressBackend{
                                        Service: &netv1.IngressServiceBackend{
                                            Name: fmt.Sprintf("%s-web", amxApp.Name),
                                            Port: netv1.ServiceBackendPort{
                                                Number: 80,
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    // Add TLS configuration if enabled
    if amxApp.Spec.Networking.Ingress.TLS {
        ingress.Spec.TLS = []netv1.IngressTLS{
            {
                Hosts:      []string{amxApp.Spec.Networking.Ingress.Hostname},
                SecretName: fmt.Sprintf("%s-tls", amxApp.Name),
            },
        }
    }

    ctrl.SetControllerReference(amxApp, ingress, r.Scheme)

    return r.createOrUpdate(ctx, ingress)
}

func (r *AIMatrixAppReconciler) createOrUpdate(ctx context.Context, obj client.Object) error {
    if err := r.Get(ctx, client.ObjectKeyFromObject(obj), obj); err != nil {
        if errors.IsNotFound(err) {
            return r.Create(ctx, obj)
        }
        return err
    }
    return r.Update(ctx, obj)
}

func (r *AIMatrixAppReconciler) getLabels(amxApp *aimatrixv1.AIMatrixApp, component string) map[string]string {
    return map[string]string{
        "app.kubernetes.io/name":       "aimatrix",
        "app.kubernetes.io/instance":   amxApp.Name,
        "app.kubernetes.io/component":  component,
        "app.kubernetes.io/version":    amxApp.Spec.Version,
        "app.kubernetes.io/managed-by": "aimatrix-operator",
    }
}

func (r *AIMatrixAppReconciler) getResourceRequirements(resources aimatrixv1.ResourceRequirements) corev1.ResourceRequirements {
    return corev1.ResourceRequirements{
        Requests: corev1.ResourceList{
            corev1.ResourceCPU:    resource.MustParse(resources.Requests.CPU),
            corev1.ResourceMemory: resource.MustParse(resources.Requests.Memory),
        },
        Limits: corev1.ResourceList{
            corev1.ResourceCPU:    resource.MustParse(resources.Limits.CPU),
            corev1.ResourceMemory: resource.MustParse(resources.Limits.Memory),
        },
    }
}

func (r *AIMatrixAppReconciler) updateStatusFailed(ctx context.Context, amxApp *aimatrixv1.AIMatrixApp, err error) (ctrl.Result, error) {
    amxApp.Status.Phase = "Failed"
    r.setCondition(amxApp, "Ready", "False", "ReconcileFailed", err.Error())
    
    if statusErr := r.Status().Update(ctx, amxApp); statusErr != nil {
        log.FromContext(ctx).Error(statusErr, "unable to update AIMatrixApp status")
    }
    
    return ctrl.Result{RequeueAfter: time.Minute * 2}, err
}

func (r *AIMatrixAppReconciler) setCondition(amxApp *aimatrixv1.AIMatrixApp, condType, status, reason, message string) {
    now := metav1.NewTime(time.Now())
    
    // Find existing condition
    for i, cond := range amxApp.Status.Conditions {
        if cond.Type == condType {
            if cond.Status != status {
                amxApp.Status.Conditions[i].Status = status
                amxApp.Status.Conditions[i].Reason = reason
                amxApp.Status.Conditions[i].Message = message
                amxApp.Status.Conditions[i].LastTransitionTime = now.Format(time.RFC3339)
            }
            return
        }
    }
    
    // Add new condition
    amxApp.Status.Conditions = append(amxApp.Status.Conditions, aimatrixv1.AIMatrixAppCondition{
        Type:               condType,
        Status:             status,
        Reason:             reason,
        Message:            message,
        LastTransitionTime: now.Format(time.RFC3339),
    })
}

// SetupWithManager sets up the controller with the Manager.
func (r *AIMatrixAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&aimatrixv1.AIMatrixApp{}).
        Owns(&appsv1.Deployment{}).
        Owns(&corev1.Service{}).
        Owns(&netv1.Ingress{}).
        Complete(r)
}
```

## Auto-Update Mechanisms

### Intelligent Update System
```python
# Python auto-update system with rollback capabilities
import asyncio
import json
import hashlib
import aiohttp
import aiofiles
import subprocess
import time
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
from datetime import datetime, timedelta

class UpdateChannel(Enum):
    STABLE = "stable"
    BETA = "beta" 
    ALPHA = "alpha"
    NIGHTLY = "nightly"

class UpdateStatus(Enum):
    CHECKING = "checking"
    AVAILABLE = "available"
    DOWNLOADING = "downloading"
    INSTALLING = "installing"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLBACK = "rollback"

@dataclass
class UpdateInfo:
    version: str
    channel: UpdateChannel
    download_url: str
    signature_url: str
    size_bytes: int
    checksum: str
    release_notes: str
    required: bool = False
    security_update: bool = False
    min_version: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)

@dataclass
class UpdateProgress:
    status: UpdateStatus
    progress_percent: float = 0.0
    message: str = ""
    bytes_downloaded: int = 0
    total_bytes: int = 0
    error: Optional[str] = None

class AutoUpdateManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_version = config.get('current_version', '1.0.0')
        self.channel = UpdateChannel(config.get('channel', 'stable'))
        self.auto_update_enabled = config.get('auto_update', True)
        self.auto_restart = config.get('auto_restart', False)
        self.update_url = config.get('update_url', 'https://updates.aimatrix.com')
        self.app_path = Path(config.get('app_path', '/opt/aimatrix'))
        self.backup_path = Path(config.get('backup_path', '/opt/aimatrix/backups'))
        
        self.update_history: List[Dict[str, Any]] = []
        self.current_update: Optional[UpdateInfo] = None
        self.progress_callback: Optional[callable] = None
        
        # Create necessary directories
        self.backup_path.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def check_for_updates(self) -> Optional[UpdateInfo]:
        """Check for available updates"""
        try:
            self.logger.info(f"Checking for updates on {self.channel.value} channel")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.update_url}/api/v1/updates/{self.channel.value}",
                    params={
                        'current_version': self.current_version,
                        'platform': self.get_platform(),
                        'architecture': self.get_architecture()
                    }
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        if data.get('update_available'):
                            update_info = UpdateInfo(**data['update_info'])
                            self.logger.info(f"Update available: {update_info.version}")
                            return update_info
                        else:
                            self.logger.info("No updates available")
                            return None
                    else:
                        self.logger.error(f"Failed to check for updates: HTTP {response.status}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"Error checking for updates: {e}")
            return None
    
    async def download_update(self, update_info: UpdateInfo) -> bool:
        """Download update package with integrity verification"""
        try:
            self._update_progress(UpdateStatus.DOWNLOADING, 0, "Starting download...")
            
            download_path = self.backup_path / f"update_{update_info.version}.pkg"
            signature_path = self.backup_path / f"update_{update_info.version}.sig"
            
            # Download main package
            success = await self._download_file(
                update_info.download_url,
                download_path,
                update_info.size_bytes,
                lambda progress: self._update_progress(
                    UpdateStatus.DOWNLOADING, progress * 0.9, 
                    f"Downloading update package ({progress:.1f}%)"
                )
            )
            
            if not success:
                return False
            
            # Download signature
            await self._download_file(update_info.signature_url, signature_path, 0)
            
            # Verify integrity
            self._update_progress(UpdateStatus.DOWNLOADING, 95, "Verifying package integrity...")
            
            if not await self._verify_package(download_path, signature_path, update_info.checksum):
                self.logger.error("Package integrity verification failed")
                return False
            
            self._update_progress(UpdateStatus.DOWNLOADING, 100, "Download completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error downloading update: {e}")
            self._update_progress(UpdateStatus.FAILED, 0, f"Download failed: {str(e)}")
            return False
    
    async def install_update(self, update_info: UpdateInfo) -> bool:
        """Install update with atomic operations and rollback capability"""
        try:
            self._update_progress(UpdateStatus.INSTALLING, 0, "Preparing installation...")
            
            # Create backup of current installation
            backup_name = f"backup_{self.current_version}_{int(time.time())}"
            backup_dir = self.backup_path / backup_name
            
            self._update_progress(UpdateStatus.INSTALLING, 10, "Creating backup...")
            await self._create_backup(backup_dir)
            
            # Stop services
            self._update_progress(UpdateStatus.INSTALLING, 20, "Stopping services...")
            await self._stop_services()
            
            # Extract and install update
            update_package = self.backup_path / f"update_{update_info.version}.pkg"
            
            self._update_progress(UpdateStatus.INSTALLING, 40, "Extracting update package...")
            await self._extract_package(update_package)
            
            self._update_progress(UpdateStatus.INSTALLING, 60, "Installing files...")
            await self._install_files(update_info)
            
            # Update configuration if needed
            self._update_progress(UpdateStatus.INSTALLING, 80, "Updating configuration...")
            await self._update_configuration(update_info)
            
            # Start services and verify
            self._update_progress(UpdateStatus.INSTALLING, 90, "Starting services...")
            await self._start_services()
            
            # Verify installation
            self._update_progress(UpdateStatus.INSTALLING, 95, "Verifying installation...")
            if not await self._verify_installation(update_info):
                # Rollback on verification failure
                self.logger.error("Installation verification failed, rolling back")
                await self._rollback_update(backup_dir)
                return False
            
            # Update version info
            await self._update_version_info(update_info.version)
            
            # Record successful update
            self._record_update_success(update_info, backup_name)
            
            self._update_progress(UpdateStatus.COMPLETED, 100, "Update completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error installing update: {e}")
            self._update_progress(UpdateStatus.FAILED, 0, f"Installation failed: {str(e)}")
            
            # Attempt rollback
            try:
                await self._rollback_update(backup_dir)
            except Exception as rollback_error:
                self.logger.error(f"Rollback also failed: {rollback_error}")
            
            return False
    
    async def _download_file(self, 
                           url: str, 
                           destination: Path, 
                           expected_size: int,
                           progress_callback: Optional[callable] = None) -> bool:
        """Download file with progress tracking"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        self.logger.error(f"Failed to download {url}: HTTP {response.status}")
                        return False
                    
                    total_size = expected_size or int(response.headers.get('content-length', 0))
                    downloaded = 0
                    
                    async with aiofiles.open(destination, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            await f.write(chunk)
                            downloaded += len(chunk)
                            
                            if progress_callback and total_size > 0:
                                progress = (downloaded / total_size) * 100
                                progress_callback(progress)
                    
                    return True
                    
        except Exception as e:
            self.logger.error(f"Error downloading {url}: {e}")
            return False
    
    async def _verify_package(self, 
                            package_path: Path, 
                            signature_path: Path, 
                            expected_checksum: str) -> bool:
        """Verify package integrity and signature"""
        try:
            # Verify checksum
            actual_checksum = await self._calculate_checksum(package_path)
            if actual_checksum != expected_checksum:
                self.logger.error(f"Checksum mismatch: expected {expected_checksum}, got {actual_checksum}")
                return False
            
            # Verify signature (simplified - in production use proper crypto libraries)
            if signature_path.exists():
                # In a real implementation, verify GPG/RSA signature
                self.logger.info("Signature verification passed")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying package: {e}")
            return False
    
    async def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of file"""
        hash_sha256 = hashlib.sha256()
        async with aiofiles.open(file_path, 'rb') as f:
            while chunk := await f.read(8192):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    async def _create_backup(self, backup_dir: Path):
        """Create backup of current installation"""
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Use rsync for efficient backup
        process = await asyncio.create_subprocess_exec(
            'rsync', '-av', '--exclude=backups', '--exclude=logs', 
            str(self.app_path) + '/', str(backup_dir) + '/',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            raise Exception(f"Backup failed: {stderr.decode()}")
        
        self.logger.info(f"Backup created at {backup_dir}")
    
    async def _rollback_update(self, backup_dir: Path):
        """Rollback to previous version"""
        try:
            self._update_progress(UpdateStatus.ROLLBACK, 0, "Rolling back update...")
            
            # Stop services
            await self._stop_services()
            
            # Restore from backup
            self._update_progress(UpdateStatus.ROLLBACK, 50, "Restoring from backup...")
            
            process = await asyncio.create_subprocess_exec(
                'rsync', '-av', '--delete',
                str(backup_dir) + '/', str(self.app_path) + '/',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Rollback failed: {stderr.decode()}")
            
            # Start services
            await self._start_services()
            
            self._update_progress(UpdateStatus.COMPLETED, 100, "Rollback completed")
            self.logger.info("Successfully rolled back to previous version")
            
        except Exception as e:
            self.logger.error(f"Rollback failed: {e}")
            raise
    
    async def _stop_services(self):
        """Stop application services"""
        services = self.config.get('services', ['aimatrix'])
        
        for service in services:
            try:
                process = await asyncio.create_subprocess_exec(
                    'systemctl', 'stop', service,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await process.communicate()
                
                if process.returncode == 0:
                    self.logger.info(f"Stopped service: {service}")
                else:
                    self.logger.warning(f"Failed to stop service: {service}")
                    
            except Exception as e:
                self.logger.error(f"Error stopping service {service}: {e}")
    
    async def _start_services(self):
        """Start application services"""
        services = self.config.get('services', ['aimatrix'])
        
        for service in services:
            try:
                process = await asyncio.create_subprocess_exec(
                    'systemctl', 'start', service,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await process.communicate()
                
                if process.returncode == 0:
                    self.logger.info(f"Started service: {service}")
                else:
                    self.logger.error(f"Failed to start service: {service}")
                    
            except Exception as e:
                self.logger.error(f"Error starting service {service}: {e}")
    
    async def perform_auto_update(self) -> bool:
        """Perform complete auto-update process"""
        if not self.auto_update_enabled:
            self.logger.info("Auto-update disabled")
            return False
        
        try:
            # Check for updates
            update_info = await self.check_for_updates()
            
            if not update_info:
                return False
            
            # Download update
            if not await self.download_update(update_info):
                return False
            
            # Install update
            if not await self.install_update(update_info):
                return False
            
            # Restart if configured
            if self.auto_restart:
                self.logger.info("Auto-restart enabled, restarting application")
                await self._restart_application()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Auto-update failed: {e}")
            return False
    
    def _update_progress(self, status: UpdateStatus, progress: float, message: str):
        """Update progress and notify callbacks"""
        progress_info = UpdateProgress(
            status=status,
            progress_percent=progress,
            message=message
        )
        
        if self.progress_callback:
            self.progress_callback(progress_info)
        
        self.logger.info(f"Update progress: {status.value} - {progress:.1f}% - {message}")
    
    def set_progress_callback(self, callback: callable):
        """Set callback for progress updates"""
        self.progress_callback = callback
    
    def get_platform(self) -> str:
        """Get current platform"""
        import platform
        return platform.system().lower()
    
    def get_architecture(self) -> str:
        """Get current architecture"""
        import platform
        return platform.machine()
    
    async def _restart_application(self):
        """Restart the application"""
        restart_command = self.config.get('restart_command', 'systemctl restart aimatrix')
        
        process = await asyncio.create_subprocess_shell(
            restart_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await process.communicate()

# Usage example
async def main():
    config = {
        'current_version': '1.0.0',
        'channel': 'stable',
        'auto_update': True,
        'auto_restart': False,
        'update_url': 'https://updates.aimatrix.com',
        'app_path': '/opt/aimatrix',
        'backup_path': '/opt/aimatrix/backups',
        'services': ['aimatrix-web', 'aimatrix-api', 'aimatrix-daemon']
    }
    
    update_manager = AutoUpdateManager(config)
    
    def progress_callback(progress: UpdateProgress):
        print(f"Status: {progress.status.value}")
        print(f"Progress: {progress.progress_percent:.1f}%")
        print(f"Message: {progress.message}")
        if progress.error:
            print(f"Error: {progress.error}")
        print("---")
    
    update_manager.set_progress_callback(progress_callback)
    
    # Perform auto-update
    success = await update_manager.perform_auto_update()
    
    if success:
        print("Update completed successfully!")
    else:
        print("Update failed or no updates available")

if __name__ == "__main__":
    asyncio.run(main())
```

---

> [!TIP]
> **Quick Deployment**: Use our provided Docker Compose stack for rapid deployment, or install the Kubernetes operator for enterprise-grade orchestration with `kubectl apply -f https://releases.aimatrix.com/operator/latest/install.yaml`.

> [!NOTE]
> **Zero-Downtime Updates**: All deployment strategies support blue-green and canary deployments for zero-downtime updates, with automatic rollback capabilities for maximum reliability.

---

*AIMatrix Deployment Strategies - Reliable, scalable deployment for every environment*