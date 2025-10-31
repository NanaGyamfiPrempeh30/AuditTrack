resource "azurerm_log_analytics_workspace" "law" {
  name                = "${var.rg_name}-law"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "env" {
  name                = var.aca_env_name
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  log_analytics {
    workspace_id = azurerm_log_analytics_workspace.law.id
    primary_shared_key = azurerm_log_analytics_workspace.law.primary_shared_key
  }
}

resource "azurerm_container_app" "api" {
  name                = "audittrack-api"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  container_app_environment_id = azurerm_container_app_environment.env.id

  configuration {
    ingress {
      external_enabled = true
      target_port = 8000
    }
  }

  template {
    container {
      name  = "api"
      image = "${azurerm_container_registry.acr.login_server}/audittrack-api:${var.image_tag}"
      cpu   = 0.5
      memory = "1.0Gi"
    }
    scale {
      min_replicas = 0
      max_replicas = 3
    }
  }
}
