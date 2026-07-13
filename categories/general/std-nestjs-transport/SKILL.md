---
name: std-nestjs-transport
description: "Configure gRPC, RabbitMQ, and monorepo contract patterns for NestJS microservices. Use when setting up gRPC service-to-service calls, RabbitMQ event-driven messaging, shared contract libraries, or ..."
license: MIT
tags: [general]
metadata: None
triggers: None
files: None
keywords: None
---

# Microservices & Transport Standards

## **Priority: P0 (FOUNDATIONAL)**


- **Synchronous (RPC)**: Use **gRPC** for low-latency, internal service-to-service calls (10x faster than REST/JSON).
- **Asynchronous (Events)**: Use **RabbitMQ** or **Kafka** for decoupling domains via fire-and-forget (`emit()`).

## gRPC Setup

See implementation examples

## RabbitMQ Setup

See implementation examples

## Monorepo Contracts

- Store all DTOs, `.proto` files, and Interfaces in `libs/contracts`.
- Services never import from sibling services — only from `contracts`.
- Semantic versioning of messages mandatory. Never change field type; add new field.

## Exception Handling

Standard `HttpException` lost over RPC/TCP. Use `RpcException` with global filters:

See implementation examples

## Serialization

- Apply `useGlobalPipes(new ValidationPipe({ transform: true }))` in `MicroserviceOptions` setup, not HTTP.

## Anti-Patterns

- **No cross-service imports**: Services must import only from `libs/contracts`, never from sibling services.
- **No HttpException in RPC**: Use `RpcException` with global `RpcExceptionFilter` for microservice errors.
- **No unversioned message schema**: Add new fields; never change existing field types — consumers will break.