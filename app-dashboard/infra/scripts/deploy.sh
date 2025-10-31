#!/usr/bin/env bash
set -euo pipefail

# Expected env vars:
# ACR_NAME, ACR_LOGIN_SERVER, RESOURCE_GROUP, ACA_ENV, IMAGE_NAME, IMAGE_TAG, CONTAINERAPP_NAME, LOCATION
# AZ cli should be logged in and correct subscription set before running

: "${ACR_NAME:?Need to set ACR_NAME}"
: "${ACR_LOGIN_SERVER:?Need to set ACR_LOGIN_SERVER}"
: "${RESOURCE_GROUP:?Need to set RESOURCE_GROUP}"
: "${CONTAINERAPP_NAME:?Need to set CONTAINERAPP_NAME}"
: "${IMAGE_NAME:?Need to set IMAGE_NAME}"
: "${IMAGE_TAG:?Need to set IMAGE_TAG}"

IMAGE="${ACR_LOGIN_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}"

echo "Building image: $IMAGE"
docker build -t "$IMAGE" ./app-api

echo "Logging in to ACR: $ACR_NAME"
az acr login --name "$ACR_NAME"

echo "Pushing image..."
docker push "$IMAGE"

# Create resource group if not exists
az group create --name "$RESOURCE_GROUP" --location "${LOCATION:-eastus}"

# If container app exists, update; else create
if az containerapp show --name "$CONTAINERAPP_NAME" --resource-group "$RESOURCE_GROUP" >/dev/null 2>&1; then
  echo "Updating container app $CONTAINERAPP_NAME with image $IMAGE"
  az containerapp update \
    --name "$CONTAINERAPP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --image "$IMAGE"
else
  echo "Creating new container app $CONTAINERAPP_NAME"
  az containerapp create \
    --name "$CONTAINERAPP_NAME" \
    --resource-group "$RESOURCE_GROUP" \
    --environment "${ACA_ENV}" \
    --image "$IMAGE" \
    --ingress external \
    --target-port 8000 \
    --min-replicas 0 \
    --max-replicas 3 \
    --registry-server "$ACR_LOGIN_SERVER"
fi

echo "Deployment finished. Getting FQDN..."
FQDN=$(az containerapp show --name "$CONTAINERAPP_NAME" --resource-group "$RESOURCE_GROUP" --query properties.configuration.ingress.fqdn -o tsv)
echo "App URL: https://$FQDN"
