#!/usr/bin/env bash
set -euo pipefail

RESOURCE_GROUP="FRED"

echo
echo "========================================"
echo " FRED Azure Teardown"
echo "========================================"
echo
echo "WARNING:"
echo "This will delete the entire Azure resource group:"
echo
echo "  $RESOURCE_GROUP"
echo
echo "This includes:"
echo "  - Container Apps"
echo "  - Container Apps environment"
echo "  - VNet and subnet"
echo "  - TimescaleDB container data"
echo "  - Grafana runtime data"
echo
echo "Your local repository and GHCR images are NOT affected."
echo

read -r -p "Type DELETE to continue: " CONFIRMATION

if [[ "$CONFIRMATION" != "DELETE" ]]; then
    echo "Teardown cancelled."
    exit 0
fi

echo
echo "Deleting Azure resource group..."

az group delete \
    --name "$RESOURCE_GROUP" \
    --yes \
    --no-wait

echo
echo "Deletion requested."
echo "Azure will continue deleting the resources in the background."
echo
echo "Check completion with:"
echo
echo "  az group exists --name $RESOURCE_GROUP"
echo
echo "When it returns false, the deployment has been removed."