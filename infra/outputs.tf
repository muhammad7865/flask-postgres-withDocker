output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnets" {
  value = aws_subnet.public[*].id
}

output "eks_cluster_name" {
  value       = try(module.eks.cluster_name, null)
  description = "EKS cluster name (if using EKS)"
}

output "db_endpoint" {
  value       = try(aws_db_instance.postgres.endpoint, null)
  description = "PostgreSQL endpoint"
  sensitive   = true
}
