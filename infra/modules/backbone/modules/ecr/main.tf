# Create ECR repository
resource "aws_ecr_repository" "repository" {
  name         = local.repository_name
  force_delete = true
}
