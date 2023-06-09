  AWS_ACCESS_KEY_ID="AKIAYYI727HXBQY3U2KZ"
  AWS_SECRET_ACCESS_KEY="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"
  AWS_DEFAULT_REGION=eu-west-1
  AWS_ECR_URL=601899071982.dkr.ecr.eu-west-1.amazonaws.com/far_repository

  aws ecr get-login-password --region $AWS_DEFAULT | docker login --username AWS --password-stdin $AWS_ECR_URL
  docker build . -t $IMAGE_NAME
  docker tag $IMAGE_NAME:latest $AWS_ECR_URL:latest
  docker push $AWS_ECR_URL:latest
