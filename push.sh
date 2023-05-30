source .env

aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ECR_URL

docker build . -t $IMAGE_NAME

docker tag $IMAGE_NAME:latest $AWS_ECR_URL:latest

docker push $AWS_ECR_URL:latest