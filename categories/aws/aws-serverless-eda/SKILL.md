---
name: aws-serverless-eda
description: "AWS serverless and event-driven architecture expert based on Well-Architected Framework. Covers Lambda, API Gateway, DynamoDB, Step Functions, EventBridge, SQS, SNS, and patterns."
license: MIT
tags: [aws, serverless, lambda, event-driven, step-functions]
domain: cloud
subdomain: aws
version: 1.0
author: CommandCodeAI (ported)
date_added: 2026-05-14
---

# AWS Serverless & Event-Driven Architecture

This skill provides comprehensive guidance for building serverless applications and event-driven architectures on AWS based on Well-Architected Framework principles.

## AWS Documentation Requirement

**CRITICAL**: This skill requires AWS MCP tools for accurate, up-to-date AWS information.

### Before Answering AWS Questions

1. **Always verify** using AWS MCP tools (if available):
   - `mcp__aws-mcp__aws___search_documentation` or `mcp__*awsdocs*__aws___search_documentation` - Search AWS docs
   - `mcp__aws-mcp__aws___read_documentation` or `mcp__*awsdocs*__aws___read_documentation` - Read specific pages
   - `mcp__aws-mcp__aws___get_regional_availability` - Check service availability

2. **If AWS MCP tools are unavailable**:
   - Guide user to configure AWS MCP
   - Help determine which option fits their environment:
     - Has uvx + AWS credentials -> Full AWS MCP Server
     - No Python/credentials -> AWS Documentation MCP (no auth)
   - If cannot determine -> Ask user which option to use

## Serverless MCP Servers

This skill can leverage serverless-specific MCP servers for enhanced development workflows:

### AWS Serverless MCP Server
**Purpose**: Complete serverless application lifecycle with SAM CLI
- Initialize new serverless applications
- Deploy serverless applications
- Test Lambda functions locally
- Generate SAM templates
- Manage serverless application lifecycle

### AWS Lambda Tool MCP Server
**Purpose**: Execute Lambda functions as tools
- Invoke Lambda functions directly
- Test Lambda integrations
- Execute workflows requiring private resource access
- Run Lambda-based automation

### AWS Step Functions MCP Server
**Purpose**: Execute complex workflows and orchestration
- Create and manage state machines
- Execute workflow orchestrations
- Handle distributed transactions
- Implement saga patterns
- Coordinate microservices

### Amazon SNS/SQS MCP Server
**Purpose**: Event-driven messaging and queue management
- Publish messages to SNS topics
- Send/receive messages from SQS queues
- Manage event-driven communication
- Implement pub/sub patterns
- Handle asynchronous processing

## When to Use This Skill

Use this skill when:
- Building serverless applications with Lambda
- Designing event-driven architectures
- Implementing microservices patterns
- Creating asynchronous processing workflows
- Orchestrating multi-service transactions
- Building real-time data processing pipelines
- Implementing saga patterns for distributed transactions
- Designing for scale and resilience

## AWS Well-Architected Serverless Design Principles

### 1. Speedy, Simple, Singular

**Functions should be concise and single-purpose**

```typescript
// GOOD - Single purpose, focused function
export const processOrder = async (event: OrderEvent) => {
  const order = await validateOrder(event);
  await saveOrder(order);
  await publishOrderCreatedEvent(order);
  return { statusCode: 200, body: JSON.stringify({ orderId: order.id }) };
};

// BAD - Function does too much
export const handleEverything = async (event: any) => {
  // Handles orders, inventory, payments, shipping...
};
```

### 2. Think Concurrent Requests, Not Total Requests

**Design for concurrency, not volume**

Lambda scales horizontally - design considerations should focus on:
- Concurrent execution limits
- Downstream service throttling
- Shared resource contention
- Connection pool sizing

### 3. Share Nothing

**Function runtime environments are short-lived**

```typescript
// GOOD - Use persistent storage
export const handler = async (event: any) => {
  await s3.putObject({
    Bucket: process.env.BUCKET_NAME,
    Key: 'data.json',
    Body: JSON.stringify(data),
  });
};
```

### 4. Assume No Hardware Affinity

**Applications must be hardware-agnostic**

### 5. Orchestrate with State Machines, Not Function Chaining

**Use Step Functions for orchestration**

### 6. Use Events to Trigger Transactions

**Event-driven over synchronous request/response**

### 7. Design for Failures and Duplicates

**Operations must be idempotent**

## Event-Driven Architecture Patterns

### Pattern 1: Event Router (EventBridge)
### Pattern 2: Queue-Based Processing (SQS)
### Pattern 3: Pub/Sub (SNS + SQS Fan-Out)
### Pattern 4: Saga Pattern with Step Functions
### Pattern 5: Event Sourcing

## Serverless Architecture Patterns

### Pattern 1: API-Driven Microservices
### Pattern 2: Stream Processing
### Pattern 3: Async Task Processing
### Pattern 4: Scheduled Jobs
### Pattern 5: Webhook Processing

## Best Practices

### Error Handling
- Implement partial batch failure handling
- Use Dead Letter Queues for error capture
- Implement retry logic with exponential backoff

### Observability
- Enable X-Ray tracing
- Use Lambda Powertools for structured logging
- Set up CloudWatch alarms

## Additional Resources

This skill includes comprehensive reference documentation based on AWS best practices:

- **Serverless Patterns**: `references/serverless-patterns.md`
- **Event-Driven Architecture Patterns**: `references/eda-patterns.md`
- **Security Best Practices**: `references/security-best-practices.md`
- **Observability Best Practices**: `references/observability-best-practices.md`
- **Performance Optimization**: `references/performance-optimization.md`
- **Deployment Best Practices**: `references/deployment-best-practices.md`

**External Resources**:
- **AWS Well-Architected Serverless Lens**: https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/
- **ServerlessLand.com**: Pre-built serverless patterns
- **AWS Serverless Workshops**: https://serverlessland.com/learn?type=Workshops
@ref(deployment-best-practices.md)
@ref(eda-patterns.md)
@ref(observability-best-practices.md)
@ref(performance-optimization.md)
@ref(security-best-practices.md)
@ref(serverless-patterns.md)
