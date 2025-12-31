# Terraform Configuration for Kasparro Backend on Render

terraform {
  required_version = ">= 1.0"
  required_providers {
    render = {
      source  = "render-oss/render"
      version = "~> 0.1"
    }
  }
}

provider "render" {
  api_key = var.render_api_key
}

# Render Web Service Configuration
resource "render_web_service" "kasparro_backend" {
  name              = "kasparro-backend-sumanth-gs"
  owner_id          = var.owner_id
  repo              = "https://github.com/Sumanthgs0005/kasparro-backend-sumanth-gs"
  branch            = "main"
  build_command     = "pip install -r requirements.txt"
  start_command     = "uvicorn app.main:app --host 0.0.0.0 --port 8000"
  environment_slug  = "python-3"
  plan              = "free"
  
  environment_variables = {
    DATABASE_URL     = "sqlite:///./kasparro.db"
    LOG_LEVEL        = "INFO"
    ENVIRONMENT      = "production"
  }

  service_details = {
    instance_type = "free"
  }

  depends_on = []
}

output "service_url" {
  value       = render_web_service.kasparro_backend.service_url
  description = "The URL of the deployed Kasparro Backend"
}
