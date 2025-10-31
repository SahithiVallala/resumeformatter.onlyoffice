# Azure Hosting Guide - Resume Formatter 🚀

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Cost Breakdown](#cost-breakdown)
4. [Prerequisites](#prerequisites)
5. [Deployment Steps](#deployment-steps)
6. [Configuration](#configuration)
7. [Scaling & Performance](#scaling--performance)
8. [Monitoring](#monitoring)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This guide covers deploying the Resume Formatter application to **Microsoft Azure** using:
- **Azure App Service** for backend (Python Flask)
- **Azure Static Web Apps** for frontend (React)
- **Azure Blob Storage** for file storage
- **Azure Application Insights** for monitoring

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USERS                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Azure Front Door (Optional CDN)                 │
│                    - Global load balancing                   │
│                    - SSL/TLS termination                     │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌──────────────────┐           ┌──────────────────┐
│  Static Web App  │           │   App Service    │
│   (React Frontend)│◄─────────┤  (Flask Backend) │
│                  │   API     │                  │
│  - React build   │   calls   │  - Python 3.10   │
│  - DOCX preview  │           │  - Flask API     │
│  - Static assets │           │  - ML models     │
└──────────────────┘           └────────┬─────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │  Blob Storage    │
                               │                  │
                               │  - Resumes       │
                               │  - Templates     │
                               │  - Output files  │
                               └──────────────────┘
                                        │
                                        ▼
                               ┌──────────────────┐
                               │ App Insights     │
                               │  - Logs          │
                               │  - Metrics       │
                               │  - Alerts        │
                               └──────────────────┘
```

---

## Cost Breakdown

### Monthly Costs (USD)

#### Option 1: Basic Setup (Development/Testing)
| Service | Tier | Specs | Monthly Cost |
|---------|------|-------|--------------|
| **App Service** | B1 Basic | 1 Core, 1.75GB RAM | $13.14 |
| **Static Web App** | Free | 100GB bandwidth | $0.00 |
| **Blob Storage** | Standard LRS | 10GB storage | $0.18 |
| **App Insights** | Basic | 5GB data/month | $0.00 (free tier) |
| **TOTAL** | | | **~$13.32/month** |
| **YEARLY** | | | **~$159.84/year** |

#### Option 2: Production Setup (Small Business)
| Service | Tier | Specs | Monthly Cost |
|---------|------|-------|--------------|
| **App Service** | S1 Standard | 1 Core, 1.75GB RAM, Auto-scale | $69.35 |
| **Static Web App** | Standard | 100GB bandwidth | $9.00 |
| **Blob Storage** | Standard LRS | 50GB storage | $0.92 |
| **App Insights** | Basic | 20GB data/month | $5.75 |
| **Front Door** | Standard | CDN + SSL | $35.00 |
| **TOTAL** | | | **~$120.02/month** |
| **YEARLY** | | | **~$1,440.24/year** |

#### Option 3: Enterprise Setup (High Traffic)
| Service | Tier | Specs | Monthly Cost |
|---------|------|-------|--------------|
| **App Service** | P1V2 Premium | 1 Core, 3.5GB RAM, Auto-scale | $146.00 |
| **Static Web App** | Standard | 500GB bandwidth | $9.00 |
| **Blob Storage** | Premium | 200GB storage | $40.96 |
| **App Insights** | Enterprise | 100GB data/month | $28.75 |
| **Front Door** | Premium | CDN + WAF | $329.00 |
| **TOTAL** | | | **~$553.71/month** |
| **YEARLY** | | | **~$6,644.52/year** |

### Cost Optimization Tips

1. **Use Free Tier for Development**
   - Static Web Apps: Free tier (100GB bandwidth)
   - App Insights: Free tier (5GB data/month)
   - Blob Storage: Pay only for what you use

2. **Reserved Instances**
   - Save 30-40% with 1-year commitment
   - Save 50-60% with 3-year commitment

3. **Auto-Scaling**
   - Scale down during off-hours
   - Scale up during peak hours
   - Potential 40-60% cost savings

4. **Storage Lifecycle Management**
   - Move old files to cool/archive tier
   - Delete temporary files after 30 days
   - Save 50-80% on storage costs

---

## Prerequisites

### 1. Azure Account
- Create free account: https://azure.microsoft.com/free/
- $200 free credit for 30 days
- Free services for 12 months

### 2. Required Tools

**Azure CLI**:
```bash
# Windows (PowerShell)
Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi
Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'

# macOS
brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

**Verify Installation**:
```bash
az --version
```

**Login to Azure**:
```bash
az login
```

### 3. GitHub Account (for CI/CD)
- Create account: https://github.com
- Fork/clone your repository

---

## Deployment Steps

### Step 1: Create Resource Group

```bash
# Set variables
$RESOURCE_GROUP="resume-formatter-rg"
$LOCATION="eastus"  # or "westus2", "centralus", etc.

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION
```

### Step 2: Deploy Backend (App Service)

#### 2.1 Create App Service Plan

```bash
# Basic tier (development)
az appservice plan create `
  --name resume-formatter-plan `
  --resource-group $RESOURCE_GROUP `
  --sku B1 `
  --is-linux

# Production tier (recommended)
az appservice plan create `
  --name resume-formatter-plan `
  --resource-group $RESOURCE_GROUP `
  --sku S1 `
  --is-linux
```

#### 2.2 Create Web App

```bash
az webapp create `
  --resource-group $RESOURCE_GROUP `
  --plan resume-formatter-plan `
  --name resume-formatter-api `
  --runtime "PYTHON:3.10"
```

#### 2.3 Configure App Settings

```bash
# Set Python version
az webapp config set `
  --resource-group $RESOURCE_GROUP `
  --name resume-formatter-api `
  --linux-fx-version "PYTHON|3.10"

# Set startup command
az webapp config set `
  --resource-group $RESOURCE_GROUP `
  --name resume-formatter-api `
  --startup-file "gunicorn --bind=0.0.0.0 --timeout 600 app:app"

# Add app settings
az webapp config appsettings set `
  --resource-group $RESOURCE_GROUP `
  --name resume-formatter-api `
  --settings `
    FLASK_ENV=production `
    PYTHONUNBUFFERED=1 `
    SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

#### 2.4 Deploy Backend Code

**Option A: Using Git**

```bash
cd Backend

# Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# Get deployment credentials
az webapp deployment source config-local-git `
  --name resume-formatter-api `
  --resource-group $RESOURCE_GROUP

# Add Azure remote
git remote add azure <deployment-url-from-above>

# Push to Azure
git push azure main
```

**Option B: Using ZIP Deploy**

```bash
cd Backend

# Create deployment package
Compress-Archive -Path * -DestinationPath deploy.zip

# Deploy
az webapp deployment source config-zip `
  --resource-group $RESOURCE_GROUP `
  --name resume-formatter-api `
  --src deploy.zip
```

#### 2.5 Install ML Dependencies

Create `requirements.txt` in Backend folder:
```txt
Flask==2.3.0
python-docx==0.8.11
pdfplumber==0.9.0
sentence-transformers==2.2.2
fuzzywuzzy==0.18.0
python-Levenshtein==0.21.0
spacy==3.5.0
numpy==1.24.0
gunicorn==20.1.0
```

Create `startup.sh`:
```bash
#!/bin/bash
python -m spacy download en_core_web_sm
gunicorn --bind=0.0.0.0 --timeout 600 app:app
```

Update App Service startup command:
```bash
az webapp config set `
  --resource-group $RESOURCE_GROUP `
  --name resume-formatter-api `
  --startup-file "startup.sh"
```

### Step 3: Deploy Frontend (Static Web App)

#### 3.1 Create Static Web App

```bash
az staticwebapp create `
  --name resume-formatter-frontend `
  --resource-group $RESOURCE_GROUP `
  --source https://github.com/<your-username>/<your-repo> `
  --location "eastus2" `
  --branch main `
  --app-location "/Frontend" `
  --output-location "build" `
  --login-with-github
```

#### 3.2 Configure Environment Variables

Create `staticwebapp.config.json` in Frontend folder:
```json
{
  "navigationFallback": {
    "rewrite": "/index.html"
  },
  "routes": [
    {
      "route": "/api/*",
      "allowedRoles": ["anonymous"]
    }
  ],
  "globalHeaders": {
    "content-security-policy": "default-src 'self' https://*.azurestaticapps.net https://*.azurewebsites.net"
  },
  "responseOverrides": {
    "404": {
      "rewrite": "/index.html"
    }
  }
}
```

Update `.env.production` in Frontend:
```env
REACT_APP_API_URL=https://resume-formatter-api.azurewebsites.net
```

#### 3.3 Build and Deploy

```bash
cd Frontend

# Install dependencies
npm install

# Build for production
npm run build

# Deploy (automatic via GitHub Actions)
git add .
git commit -m "Deploy to Azure Static Web Apps"
git push origin main
```

### Step 4: Setup Blob Storage

#### 4.1 Create Storage Account

```bash
az storage account create `
  --name resumeformatterstorage `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION `
  --sku Standard_LRS
```

#### 4.2 Create Containers

```bash
# Get connection string
$CONNECTION_STRING = az storage account show-connection-string `
  --name resumeformatterstorage `
  --resource-group $RESOURCE_GROUP `
  --query connectionString -o tsv

# Create containers
az storage container create `
  --name resumes `
  --connection-string $CONNECTION_STRING

az storage container create `
  --name templates `
  --connection-string $CONNECTION_STRING

az storage container create `
  --name output `
  --connection-string $CONNECTION_STRING
```

#### 4.3 Configure CORS

```bash
az storage cors add `
  --services b `
  --methods GET POST PUT `
  --origins https://resume-formatter-frontend.azurestaticapps.net `
  --allowed-headers "*" `
  --exposed-headers "*" `
  --max-age 3600 `
  --connection-string $CONNECTION_STRING
```

#### 4.4 Update Backend to Use Blob Storage

Add to `requirements.txt`:
```txt
azure-storage-blob==12.16.0
```

Update `app.py`:
```python
from azure.storage.blob import BlobServiceClient

# Initialize blob client
connection_string = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Upload file
def upload_to_blob(file, container_name, blob_name):
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_name
    )
    blob_client.upload_blob(file, overwrite=True)
    return blob_client.url
```

Add connection string to App Service:
```bash
az webapp config appsettings set `
  --resource-group $RESOURCE_GROUP `
  --name resume-formatter-api `
  --settings AZURE_STORAGE_CONNECTION_STRING=$CONNECTION_STRING
```

### Step 5: Setup Application Insights

#### 5.1 Create Application Insights

```bash
az monitor app-insights component create `
  --app resume-formatter-insights `
  --location $LOCATION `
  --resource-group $RESOURCE_GROUP `
  --application-type web
```

#### 5.2 Get Instrumentation Key

```bash
$INSTRUMENTATION_KEY = az monitor app-insights component show `
  --app resume-formatter-insights `
  --resource-group $RESOURCE_GROUP `
  --query instrumentationKey -o tsv
```

#### 5.3 Configure Backend

Add to `requirements.txt`:
```txt
applicationinsights==0.11.10
opencensus-ext-azure==1.1.9
opencensus-ext-flask==0.8.1
```

Update `app.py`:
```python
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware

# Configure Application Insights
app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = os.environ.get('APPINSIGHTS_INSTRUMENTATIONKEY')
middleware = FlaskMiddleware(app)

# Add logging
import logging
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string=f'InstrumentationKey={app.config["APPINSIGHTS_INSTRUMENTATIONKEY"]}'
))
```

Add to App Service settings:
```bash
az webapp config appsettings set `
  --resource-group $RESOURCE_GROUP `
  --name resume-formatter-api `
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=$INSTRUMENTATION_KEY
```

### Step 6: Configure Custom Domain (Optional)

#### 6.1 Add Custom Domain

```bash
# For App Service
az webapp config hostname add `
  --webapp-name resume-formatter-api `
  --resource-group $RESOURCE_GROUP `
  --hostname api.yourdomain.com

# For Static Web App
az staticwebapp hostname set `
  --name resume-formatter-frontend `
  --resource-group $RESOURCE_GROUP `
  --hostname www.yourdomain.com
```

#### 6.2 Configure SSL

```bash
# Managed certificate (free)
az webapp config ssl bind `
  --certificate-thumbprint auto `
  --ssl-type SNI `
  --name resume-formatter-api `
  --resource-group $RESOURCE_GROUP
```

---

## Configuration

### Environment Variables

#### Backend (App Service)

```bash
FLASK_ENV=production
PYTHONUNBUFFERED=1
AZURE_STORAGE_CONNECTION_STRING=<connection-string>
APPINSIGHTS_INSTRUMENTATIONKEY=<instrumentation-key>
MAX_CONTENT_LENGTH=10485760  # 10MB
UPLOAD_FOLDER=/tmp/uploads
```

#### Frontend (Static Web App)

```env
REACT_APP_API_URL=https://resume-formatter-api.azurewebsites.net
REACT_APP_MAX_FILE_SIZE=10485760
```

### CORS Configuration

Update `app.py`:
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://resume-formatter-frontend.azurestaticapps.net",
            "https://www.yourdomain.com"
        ]
    }
})
```

---

## Scaling & Performance

### Auto-Scaling Rules

```bash
# Scale out when CPU > 70%
az monitor autoscale create `
  --resource-group $RESOURCE_GROUP `
  --resource resume-formatter-api `
  --resource-type Microsoft.Web/serverfarms `
  --name autoscale-cpu `
  --min-count 1 `
  --max-count 5 `
  --count 1

az monitor autoscale rule create `
  --resource-group $RESOURCE_GROUP `
  --autoscale-name autoscale-cpu `
  --condition "Percentage CPU > 70 avg 5m" `
  --scale out 1
```

### Performance Optimization

1. **Enable Application Insights Profiler**
2. **Use Azure CDN for static assets**
3. **Enable compression**
4. **Implement caching**
5. **Use connection pooling**

---

## Monitoring

### View Logs

```bash
# Stream logs
az webapp log tail `
  --name resume-formatter-api `
  --resource-group $RESOURCE_GROUP

# Download logs
az webapp log download `
  --name resume-formatter-api `
  --resource-group $RESOURCE_GROUP `
  --log-file logs.zip
```

### Application Insights Queries

```kusto
// Failed requests
requests
| where success == false
| summarize count() by resultCode

// Slow requests
requests
| where duration > 5000
| project timestamp, name, duration, resultCode

// Exception tracking
exceptions
| summarize count() by type
| order by count_ desc
```

---

## Troubleshooting

### Common Issues

#### 1. Deployment Failed

**Check logs**:
```bash
az webapp log tail --name resume-formatter-api --resource-group $RESOURCE_GROUP
```

#### 2. 500 Internal Server Error

**Check Application Insights** → Failures → Exceptions

#### 3. CORS Errors

**Update CORS settings** in `app.py` and redeploy

#### 4. Out of Memory

**Upgrade App Service Plan** to higher tier

---

## Backup & Disaster Recovery

### Automated Backups

```bash
# Configure backup
az webapp config backup create `
  --resource-group $RESOURCE_GROUP `
  --webapp-name resume-formatter-api `
  --backup-name daily-backup `
  --container-url "<storage-container-sas-url>" `
  --frequency 1d `
  --retention 30
```

---

## Security Best Practices

1. **Enable HTTPS only**
2. **Use Managed Identities**
3. **Implement rate limiting**
4. **Enable Web Application Firewall (WAF)**
5. **Regular security updates**
6. **Monitor with Azure Security Center**

---

## Next Steps

1. ✅ Deploy to Azure
2. ✅ Configure custom domain
3. ✅ Setup monitoring
4. ✅ Implement CI/CD
5. ✅ Configure auto-scaling
6. ✅ Setup backups

---

**Estimated Total Setup Time**: 2-4 hours
**Monthly Cost (Basic)**: ~$13-15
**Monthly Cost (Production)**: ~$120-150
**Yearly Cost (Basic)**: ~$160-180
**Yearly Cost (Production)**: ~$1,440-1,800

---

**Last Updated**: October 30, 2025
**Azure CLI Version**: 2.53.0
**Status**: Production Ready ✅
