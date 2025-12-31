# Terraform Configuration for Kasparro Backend

## Overview
This directory contains Infrastructure-as-Code (IaC) configurations using Terraform to deploy the Kasparro Backend API to Render.

## Prerequisites
- Terraform >= 1.0
- Render account with API key
- Git repository with deployment credentials

## Files

### main.tf
Main Terraform configuration file that defines:
- **Render Web Service**: Deploys the Kasparro Backend API
- **Service Configuration**: Defines deployment environment, build command, and start command
- **Environment Variables**: Configures API keys and database settings
- **Health Checks**: Ensures service availability

### variables.tf
Variable definitions for the Terraform configuration:
- `render_api_key`: Render API authentication key
- `service_name`: Name of the Render web service
- `github_repo`: GitHub repository URL
- `environment`: Deployment environment (e.g., production, staging)

### terraform.tfvars.example
Example values for Terraform variables. Copy this file to `terraform.tfvars` and update with actual values:
```bash
cp terraform.tfvars.example terraform.tfvars
```

## Deployment Instructions

### 1. Initialize Terraform
```bash
cd terraform
terraform init
```

### 2. Configure Variables
```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your actual values
```

### 3. Plan Deployment
```bash
terraform plan
```

### 4. Apply Configuration
```bash
terraform apply
```

### 5. Verify Deployment
```bash
terraform show
```

## Environment Variables
The following environment variables are managed through Terraform:
- `RENDER_API_KEY`: Render platform API authentication
- `DATABASE_URL`: PostgreSQL connection string
- `LOG_LEVEL`: Application logging level (default: INFO)

## State Management
- Local state file: `terraform.tfstate` (use remote backend for production)
- State backup: `terraform.tfstate.backup`
- Sensitive data: `.gitignore` includes `terraform.tfvars`

## Provider Configuration
- **Provider**: render-oss/render
- **Version**: Latest (compatible with Render API)
- **Source**: Hashicorp Registry

## Troubleshooting

### Terraform Init Fails
- Verify Render provider is accessible
- Check internet connectivity

### Apply Fails
- Verify `terraform.tfvars` has correct API key
- Ensure Render account has necessary permissions
- Check GitHub repository is accessible

### Service Not Deploying
- Review Render deployment logs
- Verify build command in main.tf
- Check environment variables are set correctly

## References
- [Render Documentation](https://render.com/docs)
- [Terraform Documentation](https://www.terraform.io/docs)
- [Render Terraform Provider](https://registry.terraform.io/providers/renderio/render/latest/docs)
