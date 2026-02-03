output "db_endpoint" {
  description = "Endpoint of the RDS database"
  value       = aws_db_instance.main.endpoint
}

output "db_url" {
  description = "Database URL for the application"
  value       = "postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.main.endpoint}/clinical_genomics"
  sensitive   = true
}
