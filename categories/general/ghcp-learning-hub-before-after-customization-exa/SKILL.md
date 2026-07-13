---
name: ghcp-learning-hub-before-after-customization-exa
description: See real-world transformations showing how custom agents, skills, and
  instructions dramatically improve GitHub Copilot effectiveness.
license: MIT
tags:
- general
title: Before/After Customization Examples
authors: None
lastUpdated: 2025-12-12
estimatedReadingTime: 12 minutes
relatedArticles: None
---

# review-pr

Analyze the current git diff and provide a structured code review with:

**Structure**:
1. **Summary**: Brief overview of changes
2. **Positive Feedback**: What's done well
3. **Issues Found**: Problems categorized by severity (Critical/Major/Minor)
4. **Suggestions**: Specific improvements with code examples
5. **Questions**: Clarifications needed

**Review Focus**:
- Code correctness and logic errors
- Security vulnerabilities
- Performance implications
- Test coverage
- Code style and maintainability
- Error handling
- Documentation needs

**Tone**:
- Be constructive and helpful
- Explain the "why" behind suggestions
- Offer specific fixes, not just critique
- Acknowledge good patterns

**Format**:
Use markdown with code blocks for suggestions. For each issue, provide:
- Clear description of the problem
- Why it matters
- Suggested fix with code example

See references/review-checklist.md for the standard review checklist.

Example format:
## 🔴 Critical Issues

### Missing Input Validation
**Problem**: The `processUser` function doesn't validate the email format.
**Impact**: Could lead to invalid data in the database.
**Fix**:
```typescript
function processUser(user: User) {
  if (!isValidEmail(user.email)) {
    throw new ValidationError('Invalid email format');
  }
  // ... rest of function
}
```
````

Using this skill on a PR (via `/review-pr` or agent invocation) generates structured, actionable feedback:

````markdown
## Summary
This PR adds user authentication with JWT tokens. The implementation includes login, token generation, and middleware for protected routes.

## 🎉 Positive Feedback
- Good separation of concerns with separate auth service and middleware
- Comprehensive error handling in the login flow
- Clear function naming that makes the code self-documenting

## 🔴 Critical Issues

### 1. Hardcoded Secret Key
**Problem**: The JWT secret is hardcoded in `auth.service.ts`:
```typescript
const secret = 'my-secret-key'; // ❌ Hardcoded
```
**Impact**: Security vulnerability - secrets should never be in source code.
**Fix**:
```typescript
const secret = process.env.JWT_SECRET;
if (!secret) {
  throw new Error('JWT_SECRET environment variable is required');
}
```

### 2. Missing Password Hashing Salt Rounds
**Problem**: Password hashing uses default bcrypt rounds which may be too low.
**Impact**: Weak password protection if defaults are insufficient.
**Fix**:
```typescript
const SALT_ROUNDS = 12; // Explicit configuration
const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);
```

## ⚠️ Major Issues

### 3. No Token Expiration Validation
**Problem**: The auth middleware doesn't check token expiration explicitly.
**Impact**: Expired tokens might be accepted if JWT library doesn't verify.
**Fix**: Add explicit expiration check in the middleware.

## 💡 Suggestions

### 4. Consider Adding Refresh Tokens
The current implementation uses only access tokens. Consider implementing refresh tokens for better security and user experience:
- Short-lived access tokens (15 minutes)
- Longer-lived refresh tokens (7 days)
- Token rotation on refresh

### 5. Add Rate Limiting
The login endpoint should have rate limiting to prevent brute force attacks:
```typescript
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, please try again later'
});

app.post('/login', loginLimiter, authController.login);
```

## ❓ Questions
1. What's the intended token expiration time for production?
2. Should we implement token revocation for logout functionality?
3. Are there plans for multi-factor authentication in the future?
````

**Benefits**:
- Consistent review quality
- Faster review process (5-10 minutes)
- Structured, actionable feedback
- Includes code examples for fixes
- Identifies security issues systematically
- Maintains constructive tone

## Key Takeaways

These examples demonstrate how customization transforms GitHub Copilot from a general-purpose assistant into a team-specific expert:

1. **Instructions** embed your team's patterns into every suggestion automatically
2. **Skills** standardize workflows with bundled resources and enable agent discovery
3. **Agents** bring specialized expertise for complex domains
4. **Combination** of all three creates a comprehensive development assistant

The investment in creating customizations pays dividends through:
- Faster development with fewer manual corrections
- Consistent code quality across the team
- Automatic adherence to best practices
- Reduced onboarding time for new team members
- Better security and maintainability
