variable "rg_name" {
  description = "Resource group name"
  type        = string
  default     = "audittrack-rg"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "acr_name" {
  description = "ACR name"
  type        = string
  default = "audittrackregisty33"
}

variable "aca_env_name" {
  description = "Container Apps Environment name"
  type        = string
  default     = "audittrack-aca-env"
}

variable "image_tag" {
  description = "Container image tag to deploy (short SHA)"
  type        = string
  default     = "latest"
}

variable "api_container_name" {
  description = "Container app name for API"
  type        = string
  default     = "audittrack-api"
}
