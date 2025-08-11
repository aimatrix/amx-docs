# S3 Deployment Troubleshooting Guide

## Current Status Analysis

✅ **Region Verified**: `ap-southeast-5` (Malaysia) is a valid AWS region  
✅ **S3 Bucket Exists**: `docs.aimatrix.com` bucket is accessible  
✅ **Hugo Build**: Local builds work perfectly  
✅ **Workflows**: GitHub Actions are properly configured  
❌ **Deployment**: Both workflows failed during deployment  

## Common S3 Permission Issues & Fixes

### 1. IAM User Permissions

Your IAM user needs these minimal permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:DeleteObject",
                "s3:ListBucket",
                "s3:GetBucketLocation",
                "s3:GetBucketWebsite",
                "s3:PutBucketWebsite",
                "s3:PutBucketCORS",
                "s3:GetBucketCORS"
            ],
            "Resource": [
                "arn:aws:s3:::docs.aimatrix.com",
                "arn:aws:s3:::docs.aimatrix.com/*"
            ]
        }
    ]
}
```

### 2. S3 Bucket Policy

Your S3 bucket needs this public read policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::docs.aimatrix.com/*"
        }
    ]
}
```

### 3. S3 Bucket Settings

Ensure these settings are configured:

```bash
# Block Public Access Settings (should be DISABLED for website hosting)
aws s3api put-public-access-block \
  --bucket docs.aimatrix.com \
  --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"

# Static Website Hosting
aws s3api put-bucket-website \
  --bucket docs.aimatrix.com \
  --website-configuration '{
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "404.html"}
  }'

# CORS Configuration
aws s3api put-bucket-cors \
  --bucket docs.aimatrix.com \
  --cors-configuration '{
    "CORSRules": [{
      "AllowedOrigins": ["https://docs.aimatrix.com", "https://aimatrix.com"],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3600
    }]
  }'
```

## Diagnostic Steps

### Step 1: Check AWS Credentials

```bash
# Test credentials (run this in GitHub Actions or locally)
aws sts get-caller-identity
```

Expected output:
```json
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-user-name"
}
```

### Step 2: Test S3 Access

```bash
# List bucket contents
aws s3 ls s3://docs.aimatrix.com/ --region ap-southeast-5

# Test upload
echo "test" | aws s3 cp - s3://docs.aimatrix.com/test.txt --region ap-southeast-5

# Test delete
aws s3 rm s3://docs.aimatrix.com/test.txt --region ap-southeast-5
```

### Step 3: Check Bucket Configuration

```bash
# Check bucket policy
aws s3api get-bucket-policy --bucket docs.aimatrix.com --region ap-southeast-5

# Check public access block
aws s3api get-public-access-block --bucket docs.aimatrix.com --region ap-southeast-5

# Check website configuration
aws s3api get-bucket-website --bucket docs.aimatrix.com --region ap-southeast-5
```

## Most Likely Issues Based on Symptoms

### Issue 1: Block Public Access Enabled
**Symptom**: 403 Forbidden when accessing website  
**Fix**: Disable "Block all public access" in S3 bucket settings

### Issue 2: Missing Bucket Policy
**Symptom**: Files upload but website returns Access Denied  
**Fix**: Add the public read bucket policy above

### Issue 3: IAM Permission Insufficient
**Symptom**: AWS CLI commands fail with Access Denied  
**Fix**: Add the IAM permissions policy above

### Issue 4: Wrong Region in Secrets
**Symptom**: NoSuchBucket or region errors  
**Fix**: Verify `AWS_REGION_S3_DOCS_AIMATRIX_COM` is set to `ap-southeast-5`

### Issue 5: Website Hosting Not Enabled
**Symptom**: XML error pages instead of website  
**Fix**: Enable static website hosting with index.html

## Quick Fix Commands

Run these commands to fix common issues:

```bash
# 1. Fix public access block
aws s3api delete-public-access-block --bucket docs.aimatrix.com --region ap-southeast-5

# 2. Set bucket policy for public read
aws s3api put-bucket-policy --bucket docs.aimatrix.com --region ap-southeast-5 --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::docs.aimatrix.com/*"
  }]
}'

# 3. Enable website hosting
aws s3api put-bucket-website --bucket docs.aimatrix.com --region ap-southeast-5 --website-configuration '{
  "IndexDocument": {"Suffix": "index.html"},
  "ErrorDocument": {"Key": "404.html"}
}'

# 4. Test deployment
aws s3 sync ./public s3://docs.aimatrix.com/ --region ap-southeast-5 --delete
```

## GitHub Secrets Verification

Ensure these secrets are set correctly:
- `AWS_ACCESS_KEY_ID_S3_DOCS_AIMATRIX_COM`: Your access key ID
- `AWS_SECRET_ACCESS_KEY_S3_DOCS_AIMATRIX_COM`: Your secret access key  
- `AWS_REGION_S3_DOCS_AIMATRIX_COM`: `ap-southeast-5`

## CloudFront Configuration (If Used)

If you're using CloudFront, you'll also need:

```bash
# Invalidate CloudFront cache after deployment
aws cloudfront create-invalidation \
  --distribution-id YOUR_DISTRIBUTION_ID \
  --paths "/*"
```

## Testing the Fix

1. Fix the permission issues above
2. Push a small change to trigger the workflow
3. Monitor the GitHub Actions logs
4. Test the website at https://docs.aimatrix.com

## Next Steps

1. Check your AWS IAM user has the required permissions
2. Verify S3 bucket public access settings
3. Test manual deployment with AWS CLI
4. Re-run the GitHub Actions workflow