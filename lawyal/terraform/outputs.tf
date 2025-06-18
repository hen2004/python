output "cluster_name" {
  value = aws_eks_cluster.eks.name
}

output "cluster_endpoint" {
  value = aws_eks_cluster.eks.endpoint
}

output "ecr_url" {
  value = aws_ecr_repository.app.repository_url
}

output "iam_role_arn" {
  value = aws_iam_role.eks_cluster_role.arn
}
