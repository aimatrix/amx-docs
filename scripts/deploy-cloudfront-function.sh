#!/bin/bash

# Deploy CloudFront Function for URL rewriting
# This fixes the issue where S3 doesn't serve index.html for directory URLs

set -e

FUNCTION_NAME="aimatrix-docs-url-rewrite"
DISTRIBUTION_ID="E18XNULEWFKQ3P"

echo "Creating/Updating CloudFront Function..."

# Check if function exists
FUNCTION_EXISTS=$(aws cloudfront list-functions --query "FunctionList.Items[?Name=='${FUNCTION_NAME}'].Name" --output text 2>/dev/null || echo "")

if [ -z "$FUNCTION_EXISTS" ]; then
    echo "Creating new function..."
    
    # Create the function
    aws cloudfront create-function \
        --name "${FUNCTION_NAME}" \
        --function-config Comment="URL rewrite for clean URLs",Runtime="cloudfront-js-1.0" \
        --function-code "$(cat scripts/cloudfront-functions/url-rewrite.js)" \
        --output json > /tmp/cf-function.json
    
    FUNCTION_ARN=$(cat /tmp/cf-function.json | jq -r '.FunctionSummary.FunctionMetadata.FunctionARN')
    ETAG=$(cat /tmp/cf-function.json | jq -r '.ETag')
    
    echo "Function created with ARN: ${FUNCTION_ARN}"
    
    # Publish the function
    echo "Publishing function..."
    aws cloudfront publish-function \
        --name "${FUNCTION_NAME}" \
        --if-match "${ETAG}" \
        --output json > /tmp/cf-function-published.json
    
    FUNCTION_ARN=$(cat /tmp/cf-function-published.json | jq -r '.FunctionSummary.FunctionMetadata.FunctionARN')
    echo "Function published"
    
else
    echo "Function already exists, updating..."
    
    # Get current function details
    aws cloudfront describe-function \
        --name "${FUNCTION_NAME}" \
        --output json > /tmp/cf-function-current.json
    
    ETAG=$(cat /tmp/cf-function-current.json | jq -r '.ETag')
    
    # Update the function code
    aws cloudfront update-function \
        --name "${FUNCTION_NAME}" \
        --function-config Comment="URL rewrite for clean URLs",Runtime="cloudfront-js-1.0" \
        --function-code "$(cat scripts/cloudfront-functions/url-rewrite.js)" \
        --if-match "${ETAG}" \
        --output json > /tmp/cf-function-updated.json
    
    ETAG=$(cat /tmp/cf-function-updated.json | jq -r '.ETag')
    
    # Publish the updated function
    echo "Publishing updated function..."
    aws cloudfront publish-function \
        --name "${FUNCTION_NAME}" \
        --if-match "${ETAG}" \
        --output json > /tmp/cf-function-published.json
    
    FUNCTION_ARN=$(cat /tmp/cf-function-published.json | jq -r '.FunctionSummary.FunctionMetadata.FunctionARN')
    echo "Function updated and published"
fi

echo ""
echo "Attaching function to CloudFront distribution..."

# Get current distribution config
aws cloudfront get-distribution-config --id "${DISTRIBUTION_ID}" --output json > /tmp/cf-dist-config.json

# Extract the config and ETag
DIST_CONFIG=$(cat /tmp/cf-dist-config.json | jq '.DistributionConfig')
DIST_ETAG=$(cat /tmp/cf-dist-config.json | jq -r '.ETag')

# Add the function association to the default cache behavior
echo "$DIST_CONFIG" | jq \
    --arg FUNCTION_ARN "${FUNCTION_ARN}" \
    '.DefaultCacheBehavior.FunctionAssociations = {
        "Quantity": 1,
        "Items": [{
            "EventType": "viewer-request",
            "FunctionARN": $FUNCTION_ARN
        }]
    }' > /tmp/cf-dist-config-updated.json

# Update the distribution
echo "Updating CloudFront distribution..."
aws cloudfront update-distribution \
    --id "${DISTRIBUTION_ID}" \
    --distribution-config file:///tmp/cf-dist-config-updated.json \
    --if-match "${DIST_ETAG}" \
    --output json > /tmp/cf-dist-updated.json

echo "CloudFront distribution updated successfully!"
echo ""
echo "Creating cache invalidation..."

# Create invalidation for all paths
aws cloudfront create-invalidation \
    --distribution-id "${DISTRIBUTION_ID}" \
    --paths "/*" \
    --output json > /tmp/cf-invalidation.json

INVALIDATION_ID=$(cat /tmp/cf-invalidation.json | jq -r '.Invalidation.Id')

echo "Cache invalidation created: ${INVALIDATION_ID}"
echo ""
echo "✅ CloudFront function deployed and attached successfully!"
echo ""
echo "Testing URLs (may take a few minutes to propagate):"
echo "  https://docs.aimatrix.com/docs/ (should work now)"
echo "  https://docs.aimatrix.com/developers/ (should work now)"
echo "  https://docs.aimatrix.com/investors/ (should work now)"