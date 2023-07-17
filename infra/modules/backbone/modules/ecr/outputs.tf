output "ecr_repository_id" {
  value = aws_ecr_repository.repository.id
}

output "ecr_repository_url" {
  value = aws_ecr_repository.repository.repository_url
}

output "ecr_repository_arn" {
  value = aws_ecr_repository.repository.arn
}

output "iam_user_access_key_id" {
  value = aws_iam_access_key.registry_admin_user_key.id
}

output "iam_user_access_key_secret" {
  value = aws_iam_access_key.registry_admin_user_key.secret
  sensitive = true
}