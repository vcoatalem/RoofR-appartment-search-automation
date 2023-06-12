AWS_ACCESS_KEY_ID="AKIAYYI727HXHMJI32OZ"
AWS_SECRET_ACCESS_KEY="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"
AWS_DEFAULT_REGION=eu-west-1
AWS_ECR_URL=601899071982.dkr.ecr.eu-west-1.amazonaws.com/far_repository
IMAGE_NAME=dariatolo

aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ECR_URL
docker build . -t $IMAGE_NAME
docker tag $IMAGE_NAME $AWS_ECR_URL:$IMAGE_NAME
docker push $AWS_ECR_URL:$IMAGE_NAME
