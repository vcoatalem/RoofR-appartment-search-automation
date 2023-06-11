  AWS_ACCESS_KEY_ID="AKIAYYI727HXAUOCIKF2"
  AWS_SECRET_ACCESS_KEY="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"
  AWS_DEFAULT_REGION=eu-west-1
  AWS_ECR_URL=601899071982.dkr.ecr.eu-west-1.amazonaws.com/far_repository
  IMAGE_NAME=dariatolo

  aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ECR_URL
  docker build . -t $IMAGE_NAME
  docker tag $IMAGE_NAME:dariatolo $AWS_ECR_URL:dariatolo
  docker push $AWS_ECR_URL:dariatolo
