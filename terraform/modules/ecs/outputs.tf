output "api_lb_dns_name" {
  description = "DNS name of the API load balancer"
  value       = aws_lb.main.dns_name
}

output "dashboard_lb_dns_name" {
  description = "DNS name of the dashboard load balancer"
  value       = aws_lb.main.dns_name # In a real scenario, you might use different listeners or hosts
}
