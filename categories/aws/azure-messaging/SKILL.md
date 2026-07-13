---
name: azure-messaging
description: "Troubleshoot and resolve issues with Azure Messaging SDKs for Event Hubs and Service Bus. Covers connection failures, authentication errors, message processing issues, and SDK configuration problem..."
license: MIT
tags: [aws]
metadata: None
author: Microsoft
version: 1.0.1
---

# Azure Messaging SDK Troubleshooting

## Quick Reference

| Property | Value |
|----------|-------|
| **Services** | Azure Event Hubs, Azure Service Bus |
| **MCP Tools** | `mcp_azure_mcp_eventhubs`, `mcp_azure_mcp_servicebus` |
| **Best For** | Diagnosing SDK connection, auth, and message processing issues |

## When to Use This Skill

- SDK connection failures, auth errors, or AMQP link errors
- Message lock lost, session lock, or send/receive timeouts
- Event processor or message handler stops processing
- SDK configuration questions (retry, prefetch, batch size)

## MCP Tools

| Tool | Command | Use |
|------|---------|-----|
| `mcp_azure_mcp_eventhubs` | Namespace/hub ops | List namespaces, hubs, consumer groups |
| `mcp_azure_mcp_servicebus` | Queue/topic ops | List namespaces, queues, topics, subscriptions |
| `mcp_azure_mcp_monitor` | `logs_query` | Query diagnostic logs with KQL |
| `mcp_azure_mcp_resourcehealth` | `get` | Check service health status |
| `mcp_azure_mcp_documentation` | Doc search | Search Microsoft Learn for troubleshooting docs |

## Diagnosis Workflow

1. **Identify the SDK and version** — Ask which language SDK and version the user is on
2. **Check resource health** — Use `mcp_azure_mcp_resourcehealth` to verify the namespace is healthy
3. **Review the error message** — Match against language-specific troubleshooting guide
4. **Look up documentation** — Use `mcp_azure_mcp_documentation` to search Microsoft Learn for the error or topic
5. **Check configuration** — Verify connection string, entity name, consumer group
6. **Recommend fix** — Apply remediation, citing documentation found


## Connectivity Troubleshooting

See Service Troubleshooting Guide for ports, WebSocket fallback, IP firewall, private endpoints, and service tags.

## SDK Troubleshooting Guides

- **Event Hubs**: Python | Java | JS | .NET
- **Service Bus**: Python | Java | JS | .NET

## References

Use `mcp_azure_mcp_documentation` to search Microsoft Learn for latest guidance. See Service Troubleshooting Guide for network and service-level docs.