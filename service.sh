#!/bin/bash
REGISTRY_URL="registry.deti"
NAMESPACE="egs-docmanager"

# Load arguments
if [ "$#" -ne 1 ]; then
	echo "Usage: $0 <version>"
	exit 1
fi
IMAGE_NAME=
VERSION=$1


# Build and push image
#Notifications
cd Notifications
IMAGE_NAME=notifications
SERVICE="${REGISTRY_URL}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
docker buildx build --platform linux/amd64 --network=host -t ${SERVICE} -f Dockerfile.app .
docker push ${SERVICE}
IMAGE_NAME=notifications.cronjob
SERVICE="${REGISTRY_URL}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
docker buildx build --platform linux/amd64 --network=host -t ${SERVICE} -f Dockerfile.cronjob .
docker push ${SERVICE}
cd ..

#meetings
cd meetings
IMAGE_NAME=meetings
SERVICE="${REGISTRY_URL}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
docker buildx build --platform linux/amd64 --network=host -t ${SERVICE} -f Dockerfile .
docker push ${SERVICE}
cd ..

#FrontEnd
cd FrontEnd
IMAGE_NAME=frontend
SERVICE="${REGISTRY_URL}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
docker buildx build --platform linux/amd64 --network=host -t ${SERVICE} -f Dockerfile .
docker push ${SERVICE}
cd ..

#Composer
cd composer
IMAGE_NAME=composer
SERVICE="${REGISTRY_URL}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
docker buildx build --platform linux/amd64 --network=host -t ${SERVICE} -f Dockerfile .
docker push ${SERVICE}
cd ..

#auth
cd auth
IMAGE_NAME=auth
SERVICE="${REGISTRY_URL}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
docker buildx build --platform linux/amd64 --network=host -t ${SERVICE} -f Dockerfile .
docker push ${SERVICE}
cd ..

#TodoList
cd TodoList
IMAGE_NAME=todo
SERVICE="${REGISTRY_URL}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
docker buildx build --platform linux/amd64 --network=host -t ${SERVICE} -f Dockerfile .
docker push ${SERVICE}
cd ..

#documents
cd documents
IMAGE_NAME=documents
SERVICE="${REGISTRY_URL}/${NAMESPACE}/${IMAGE_NAME}:${VERSION}"
docker buildx build --platform linux/amd64 --network=host -t ${SERVICE} -f Dockerfile .
docker push ${SERVICE}
cd ..
