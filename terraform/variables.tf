# Terraform Variables for Kasparro Backend

variable "render_api_key" {
  description = "Render API Key for authentication"
  type        = string
  sensitive   = true
}

variable "owner_id" {
  description = "Render Owner/Account ID"
  type        = string
  sensitive   = true
}
