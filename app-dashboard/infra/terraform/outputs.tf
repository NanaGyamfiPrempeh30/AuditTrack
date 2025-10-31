output "acr_login_server" {
  description = "ACR login server"
  value       = azurerm_container_registry.acr.login_server
}

output "containerapp_fqdn" {
  description = "Container App public URL"
  value       = azurerm_container_app.api.configuration[0].ingress[0].fqdn
  # NOTE: structure may vary by terraform provider version; adjust if necessary
}

output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}
