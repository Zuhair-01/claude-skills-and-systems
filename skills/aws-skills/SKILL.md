---
name: aws-skills
description: "AWS development with infrastructure automation and cloud architecture patterns"
risk: safe
source: "https://github.com/zxkane/aws-skills"
date_added: "2026-02-27"
---

# Aws Skills

## Overview

AWS development with infrastructure automation and cloud architecture patterns

## When to Use This Skill

Use this skill when you need to work with aws development with infrastructure automation and cloud architecture patterns.

For deep Terraform module authoring, use `terraform-aws-modules` instead — this skill covers
CDK/CLI-level AWS patterns, not HCL module design.

## Instructions

```typescript
// CDK: least-privilege IAM via grant* methods instead of hand-written policy JSON --
// grantReadWrite scopes the policy to exactly this bucket's ARN, not "Resource": "*"
const bucket = new s3.Bucket(this, 'Data');
const fn = new lambda.Function(this, 'Handler', { /* ... */ });
bucket.grantReadWrite(fn); // generates a scoped policy automatically, no manual ARN typing
```

Pitfall: `iam.PolicyStatement({ resources: ['*'] })` written by hand is the #1 CDK security
regression — it silently passes `cdk diff` and `cdk deploy` with no warning. Always prefer
`bucket.grantRead(fn)` / `table.grantWriteData(fn)` style grants over manual `PolicyStatement`
construction; they're both safer and shorter.

```bash
# aws-cli: assume a cross-account role for scoped access instead of long-lived keys
aws sts assume-role --role-arn arn:aws:iam::123456789012:role/DeployRole \
  --role-session-name deploy --duration-seconds 900
# Then export the returned AccessKeyId/SecretAccessKey/SessionToken as env vars for the session --
# never write assumed-role creds to a shared credentials file.
```

Pitfall: CloudFormation/CDK stack updates that change a resource's `PhysicalResourceId`-driving
property (e.g. renaming an S3 bucket, changing a DynamoDB table's key schema) trigger a
replace-not-update — which deletes the old resource on rollback of a *failed* deploy, not just
on success. Always check `cdk diff` for `[-] `/`[+] ` replacement markers, not just `[~]` updates,
before deploying anything stateful.

For more information, see the [source repository](https://github.com/zxkane/aws-skills).

## Limitations
- Use this skill only when the task clearly matches the scope described above.
- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.
- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.
