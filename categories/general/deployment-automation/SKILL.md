---
name: deployment-automation
description: Automate application deployment to cloud platforms and servers. Use when
  setting up CI/CD pipelines, deploying to Docker/Kubernetes, or configuring cloud
  infrastructure. Handles GitHub Actions, Doc...
license: MIT
tags:
- deployment
- ci-cd
- docker
- kubernetes
- automation
metadata: None
platforms: Claude, ChatGPT, Gemini
---

apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**Deployment Script** (deploy.sh):
```bash
#!/bin/bash
set -e

# Variables
NAMESPACE="production"
IMAGE_TAG="${1:-latest}"

echo "Deploying myapp:${IMAGE_TAG} to ${NAMESPACE}..."

# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Update image
kubectl set image deployment/myapp myapp=ghcr.io/username/myapp:${IMAGE_TAG} -n ${NAMESPACE}

# Wait for rollout
kubectl rollout status deployment/myapp -n ${NAMESPACE} --timeout=5m

# Verify
kubectl get pods -n ${NAMESPACE} -l app=myapp

echo "Deployment completed successfully!"
```

### Step 4: Vercel/Netlify (Frontend)

Simply deploy static sites and Next.js apps.

**vercel.json**:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "env": {
    "DATABASE_URL": "@database-url",
    "API_KEY": "@api-key"
  },
  "regions": ["sin1", "icn1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "permanent": true
    }
  ]
}
```

**CLI Deployment**:
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Set environment variable
vercel env add DATABASE_URL
```

### Step 5: Zero-Downtime Deployment Strategy

Deploy new versions without service interruption.

**Blue-Green Deployment** (docker-compose):
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app-blue
      - app-green

  app-blue:
    image: myapp:blue
    environment:
      - NODE_ENV=production
      - COLOR=blue

  app-green:
    image: myapp:green
    environment:
      - NODE_ENV=production
      - COLOR=green
```

**switch.sh** (Blue/Green Switch):
```bash
#!/bin/bash

CURRENT_COLOR=$(cat current_color.txt)
NEW_COLOR=$([[ "$CURRENT_COLOR" == "blue" ]] && echo "green" || echo "blue")

# Deploy new version to inactive environment
docker-compose up -d app-${NEW_COLOR}

# Wait for health check
sleep 10

# Health check
if curl -f http://localhost:8080/health; then
  # Update nginx to point to new environment
  sed -i "s/${CURRENT_COLOR}/${NEW_COLOR}/g" nginx.conf
  docker-compose exec nginx nginx -s reload

  # Update current color
  echo ${NEW_COLOR} > current_color.txt

  # Stop old environment after 5 minutes (rollback window)
  sleep 300
  docker-compose stop app-${CURRENT_COLOR}

  echo "Deployment successful! Switched to ${NEW_COLOR}"
else
  echo "Health check failed! Keeping ${CURRENT_COLOR}"
  docker-compose stop app-${NEW_COLOR}
  exit 1
fi
```

## Output format

### Deployment Checklist

```markdown
## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing (unit, integration, E2E)
- [ ] Code review approved
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Rollback plan documented

### Deployment
- [ ] Docker image built and tagged
- [ ] Image pushed to container registry
- [ ] Kubernetes manifests applied
- [ ] Rolling update started
- [ ] Pods healthy and ready

### Post-Deployment
- [ ] Health check endpoint responding
- [ ] Metrics/logs monitoring active
- [ ] Performance baseline established
- [ ] Old pods terminated (after grace period)
- [ ] Deployment documented in changelog
```

## Constraints

### Required Rules (MUST)

1. **Health Checks**: Health check endpoint for all services
   ```typescript
   app.get('/health', (req, res) => {
     res.status(200).json({ status: 'ok' });
   });
   ```

2. **Graceful Shutdown**: Handle SIGTERM signal
   ```javascript
   process.on('SIGTERM', async () => {
     console.log('SIGTERM received, shutting down gracefully');
     await server.close();
     await db.close();
     process.exit(0);
   });
   ```

3. **Environment Variable Separation**: No hardcoding; use .env files

### Prohibited Rules (MUST NOT)

1. **No Committing Secrets**: Never commit API keys or passwords to Git
2. **No Debug Mode in Production**: `NODE_ENV=production` is required
3. **Avoid latest tag only**: Use version tags (v1.0.0, sha-abc123)

## Best practices

1. **Multi-stage Docker builds**: Minimize image size
2. **Immutable infrastructure**: Redeploy instead of modifying servers
3. **Blue-Green deployment**: Zero-downtime deployment and easy rollback
4. **Monitoring required**: Prometheus, Grafana, Datadog

## References

- [Docker Docs](https://docs.docker.com/)
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Vercel](https://vercel.com/docs)
- [12 Factor App](https://12factor.net/)

## Metadata

### Version
- **Current Version**: 1.0.0
- **Last Updated**: 2025-01-01
- **Compatible Platforms**: Claude, ChatGPT, Gemini

### Related Skills
- [monitoring](SKILL.md): Post-deployment monitoring
- [security](SKILL.md): Deployment security

### Tags
`#deployment` `#CI/CD` `#Docker` `#Kubernetes` `#automation` `#infrastructure`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
