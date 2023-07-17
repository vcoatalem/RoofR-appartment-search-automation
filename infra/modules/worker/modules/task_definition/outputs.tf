output "task_name" {
    value = aws_ecs_task_definition.task_definition.family
}