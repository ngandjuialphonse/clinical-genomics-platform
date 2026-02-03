output "dashboard_url" {
  description = "URL of the Streamlit dashboard"
  value       = module.ecs.dashboard_lb_dns_name
}

output "api_url" {
  description = "URL of the FastAPI backend"
  value       = module.ecs.api_lb_dns_name
}

output "db_endpoint" {
  description = "Endpoint of the RDS database"
  value       = module.rds.db_endpoint
}
