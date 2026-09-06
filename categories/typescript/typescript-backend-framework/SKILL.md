---
name: typescript-backend-framework
description: "Use when building or refactoring NestJS apps — controllers, providers, modules, guards, pipes, interceptors, GraphQL, WebSockets, microservices, and testing."
license: MIT
tags:
- typescript
- node
- backend
- dependency-injection
- api
---

## When to use this skill

Use this skill whenever the user wants to:
- Build or refactor a NestJS application
- Implement controllers, providers, and modules
- Apply middleware, pipes, guards, or interceptors
- Configure DI scopes, dynamic modules, or lifecycle hooks
- Add validation, serialization, caching, logging, or queues
- Integrate GraphQL, WebSockets, or microservices
- Document APIs with OpenAPI/Swagger
- Implement authentication/authorization or security hardening
- Write unit or e2e tests for NestJS

## How to use this skill

1. **Identify the topic** from the user's request and find the corresponding example file in the mapping below

2. **Load the appropriate example file** from the `examples/` directory

3. **Follow the specific instructions** in that example file for syntax, structure, and best practices

   **Important Notes**:
   - All examples follow NestJS official documentation structure
   - Examples include both JavaScript and TypeScript versions where applicable
   - Each example file includes key concepts, code examples, and official documentation links
   - Always check the example file for best practices and common patterns

4. **Use templates** from the `templates/` directory to speed up common scaffolding

### Doc mapping (one-to-one with https://docs.nestjs.com/)

**Overview (概览)**
- `examples/overview/introduction.md` → https://docs.nestjs.com/
- `examples/fundamentals/first-steps.md` → https://docs.nestjs.com/first-steps
- `examples/fundamentals/controllers.md` → https://docs.nestjs.com/controllers
- `examples/fundamentals/providers.md` → https://docs.nestjs.com/providers
- `examples/fundamentals/modules.md` → https://docs.nestjs.com/modules
- `examples/fundamentals/middleware.md` → https://docs.nestjs.com/middleware
- `examples/fundamentals/exception-filters.md` → https://docs.nestjs.com/exception-filters
- `examples/fundamentals/pipes.md` → https://docs.nestjs.com/pipes
- `examples/fundamentals/guards.md` → https://docs.nestjs.com/guards
- `examples/fundamentals/interceptors.md` → https://docs.nestjs.com/interceptors
- `examples/overview/custom-decorators.md` → https://docs.nestjs.com/custom-decorators

**Fundamentals (基础)**
- `examples/fundamentals/custom-providers.md` → https://docs.nestjs.com/fundamentals/custom-providers
- `examples/fundamentals/async-providers.md` → https://docs.nestjs.com/fundamentals/async-providers
- `examples/fundamentals/dynamic-modules.md` → https://docs.nestjs.com/fundamentals/dynamic-modules
- `examples/fundamentals/module-ref.md` → https://docs.nestjs.com/fundamentals/module-ref
- `examples/fundamentals/execution-context.md` → https://docs.nestjs.com/fundamentals/execution-context
- `examples/fundamentals/lifecycle-events.md` → https://docs.nestjs.com/fundamentals/lifecycle-events
- `examples/fundamentals/injection-scopes.md` → https://docs.nestjs.com/fundamentals/injection-scopes
- `examples/fundamentals/request-scoped.md` → https://docs.nestjs.com/fundamentals/request-scoped
- `examples/fundamentals/circular-dependency.md` → https://docs.nestjs.com/fundamentals/circular-dependency

**Techniques (技巧)**
- `examples/techniques/configuration.md` → https://docs.nestjs.com/techniques/configuration
- `examples/techniques/validation.md` → https://docs.nestjs.com/techniques/validation
- `examples/techniques/serialization.md` → https://docs.nestjs.com/techniques/serialization
- `examples/techniques/caching.md` → https://docs.nestjs.com/techniques/caching
- `examples/techniques/logger.md` → https://docs.nestjs.com/techniques/logger
- `examples/techniques/events.md` → https://docs.nestjs.com/techniques/events
- `examples/techniques/task-scheduling.md` → https://docs.nestjs.com/techniques/task-scheduling
- `examples/techniques/queues.md` → https://docs.nestjs.com/techniques/queues
- `examples/techniques/file-upload.md` → https://docs.nestjs.com/techniques/file-upload
- `examples/techniques/streaming-files.md` → https://docs.nestjs.com/techniques/streaming-files
- `examples/techniques/database.md` → https://docs.nestjs.com/techniques/database
- `examples/techniques/mongodb.md` → https://docs.nestjs.com/techniques/mongodb
- `examples/techniques/mongoose.md` → https://docs.nestjs.com/techniques/mongoose
- `examples/techniques/sequelize.md` → https://docs.nestjs.com/techniques/sequelize
- `examples/techniques/prisma.md` → https://docs.nestjs.com/recipes/prisma

**Security (安全)**
- `examples/security/authentication.md` → https://docs.nestjs.com/security/authentication
- `examples/security/authorization.md` → https://docs.nestjs.com/security/authorization
- `examples/security/helmet.md` → https://docs.nestjs.com/security/helmet
- `examples/security/cors.md` → https://docs.nestjs.com/security/cors
- `examples/security/rate-limiting.md` → https://docs.nestjs.com/security/rate-limiting

**GraphQL**
- `examples/graphql/quick-start.md` → https://docs.nestjs.com/graphql/quick-start
- `examples/graphql/resolvers.md` → https://docs.nestjs.com/graphql/resolvers
- `examples/graphql/scalars.md` → https://docs.nestjs.com/graphql/scalars
- `examples/graphql/interfaces.md` → https://docs.nestjs.com/graphql/interfaces
- `examples/graphql/unions.md` → https://docs.nestjs.com/graphql/unions
- `examples/graphql/directives.md` → https://docs.nestjs.com/graphql/directives
- `examples/graphql/plugins.md` → https://docs.nestjs.com/graphql/plugins
- `examples/graphql/subscriptions.md` → https://docs.nestjs.com/graphql/subscriptions
- `examples/graphql/federation.md` → https://docs.nestjs.com/graphql/federation
- `examples/graphql/migration.md` → https://docs.nestjs.com/graphql/migration

**WebSockets**
- `examples/websockets/gateways.md` → https://docs.nestjs.com/websockets/gateways
- `examples/websockets/exception-filters.md` → https://docs.nestjs.com/websockets/exception-filters
- `examples/websockets/guards.md` → https://docs.nestjs.com/websockets/guards
- `examples/websockets/interceptors.md` → https://docs.nestjs.com/websockets/interceptors
- `examples/websockets/adapters.md` → https://docs.nestjs.com/websockets/adapters

**Microservices**
- `examples/microservices/basics.md` → https://docs.nestjs.com/microservices/basics
- `examples/microservices/redis.md` → https://docs.nestjs.com/microservices/redis
- `examples/microservices/mqtt.md` → https://docs.nestjs.com/microservices/mqtt
- `examples/microservices/nats.md` → https://docs.nestjs.com/microservices/nats
- `examples/microservices/kafka.md` → https://docs.nestjs.com/microservices/kafka
- `examples/microservices/grpc.md` → https://docs.nestjs.com/microservices/grpc
- `examples/microservices/rabbitmq.md` → https://docs.nestjs.com/microservices/rabbitmq
- `examples/microservices/custom-transport.md` → https://docs.nestjs.com/microservices/custom-transport
- `examples/microservices/hybrid-application.md` → https://docs.nestjs.com/microservices/hybrid-application

**OpenAPI (Swagger)**
- `examples/openapi/introduction.md` → https://docs.nestjs.com/openapi/introduction
- `examples/openapi/operations.md` → https://docs.nestjs.com/openapi/operations
- `examples/openapi/types-and-parameters.md` → https://docs.nestjs.com/openapi/types-and-parameters
- `examples/openapi/security.md` → https://docs.nestjs.com/openapi/security
- `examples/openapi/mapped-types.md` → https://docs.nestjs.com/openapi/mapped-types

**CLI & Testing & Recipes**
- `examples/cli/overview.md` → https://docs.nestjs.com/cli/overview
- `examples/testing/unit-testing.md` → https://docs.nestjs.com/fundamentals/testing
- `examples/testing/e2e-testing.md` → https://docs.nestjs.com/fundamentals/testing
- `examples/recipes/cqrs.md` → https://docs.nestjs.com/recipes/cqrs
- `examples/recipes/mikroorm.md` → https://docs.nestjs.com/recipes/mikroorm
- `examples/recipes/terminus.md` → https://docs.nestjs.com/recipes/terminus
- `examples/faq.md` → https://docs.nestjs.com/faq

## Examples and Templates

This skill includes detailed examples organized to match the NestJS official documentation structure (https://docs.nestjs.com/). All examples are in the `examples/` directory, organized by topic (see mapping above).

**To use examples:**
- Identify the topic from the user's request
- Load the appropriate example file from the mapping above
- Follow the instructions, syntax, and best practices in that file
- Adapt the code examples to your specific use case

**To use templates:**
- Reference templates in `templates/` directory for common scaffolding
- Templates include: controller, provider, module, middleware, guard, pipe, interceptor, exception filter, DTO, and project structure
- Adapt templates to your specific needs and coding style

## Best Practices

1. **Use dependency injection**: Leverage NestJS DI container for better testability and maintainability
2. **Organize by modules**: Group related functionality into feature modules
3. **Use decorators consistently**: Follow NestJS decorator patterns for controllers, providers, and routes
4. **Validate input data**: Use ValidationPipe and DTOs for request validation
5. **Handle errors gracefully**: Implement global exception filters for consistent error handling
6. **Use guards for authorization**: Protect routes with guards rather than inline checks
7. **Leverage interceptors**: Use interceptors for cross-cutting concerns like logging and transformation
8. **Type safety**: Use TypeScript for better type safety and developer experience
9. **Test thoroughly**: Write unit tests for services and E2E tests for API endpoints
10. **Follow official patterns**: Refer to official documentation for recommended patterns and practices

## Resources

- **Official Documentation**: https://docs.nestjs.com/
- **GitHub Repository**: https://github.com/nestjs/nest

## Keywords

NestJS, Node.js, framework, controller, provider, module, middleware, exception filter, pipe, guard, interceptor, dependency injection, GraphQL, WebSocket, microservice, OpenAPI, Swagger, testing, validation, caching, logging, TypeScript, decorator, DI, IoC, 控制器, 提供者, 模块, 中间件, 守卫, 管道, 拦截器, 依赖注入

## 能力边界

### ✅ 适用场景
- 当你需要使用此技能对应的技术栈时
- 当项目需要遵循最佳实践时
- 当需要快速上手或深入理解核心概念时

### ⚠️ 需要注意
- 复杂业务逻辑需要结合具体场景调整
- 性能优化需要根据实际数据量评估

### ❌ 不适用场景
- 不相关的技术栈或框架
- 需要完全自定义的特殊场景

## 常见陷阱 (Gotchas)

1. **版本兼容性**：注意框架版本与依赖库的兼容性，不同版本 API 可能有差异
2. **配置文件格式**：配置文件格式错误是最常见的问题，建议使用编辑器的语法检查
3. **环境变量**：确保所有必要的环境变量已正确设置，敏感信息不要硬编码
4. **依赖冲突**：多版本共存时注意依赖冲突，使用 lock 文件锁定版本
5. **性能陷阱**：大数据量场景下注意性能优化，避免 N+1 查询等常见问题

## 使用流程

### Step 1: 环境准备
确保开发环境已安装必要的依赖和工具。

### Step 2: 配置初始化
根据项目需求进行基础配置。

### Step 3: 核心功能使用
按照示例代码实现核心功能。

### Step 4: 测试验证
运行测试确保功能正常。

### Step 5: 部署上线
完成开发后进行部署和监控。
