# Playwright MCP Server

## Overview

Playwright provides E2E testing automation and browser control capabilities.

| Attribute | Value |
|-----------|-------|
| **Function** | E2E testing, browser automation |
| **Tools** | `browser_navigate`, `browser_click`, `browser_snapshot`, `browser_type`, etc. |
| **Timeout** | 20 seconds |
| **Fallback** | Manual test suggestions |

## When to Use

- End-to-end test creation
- Browser automation
- Accessibility testing
- Visual regression testing
- User flow validation

## Auto-Triggers

### Keywords
`e2e`, `browser`, `accessibility`, `test`, `automation`, `screenshot`, `click`, `navigate`, `a11y`, `wcag`

### Files
`*.spec.ts`, `*.e2e.ts`, `*.test.ts`, `**/tests/**`, `**/e2e/**`

### Personas
- **qa** (primary)
- **frontend** (secondary)

## Available Tools

### Navigation
- `browser_navigate` — Go to URL
- `browser_click` — Click element
- `browser_type` — Type text

### Capture
- `browser_snapshot` — Capture page state
- `browser_screenshot` — Take screenshot

### Interaction
- `browser_scroll` — Scroll page
- `browser_hover` — Hover element
- `browser_select` — Select dropdown option

## Workflow

```
1. Define user journey from requirements
2. Automate browser interactions
3. Capture snapshots and metrics
4. Assert expected outcomes
5. Generate test report
```

## Example Usage

**Brief**: "Create E2E test for user registration"
**Persona**: `--persona-qa`

```
 Playwright activated (auto: qa)
 Creating registration test:
   1. Navigate to /register
   2. Fill form fields
   3. Submit registration
   4. Verify success message
   5. Check accessibility (a11y)
 Generated: tests/e2e/registration.spec.ts
```

## Test Structure

Generated tests follow best practices:

```typescript
test.describe('User Registration', () => {
  test('should register new user', async ({ page }) => {
    // Arrange
    await page.goto('/register');

    // Act
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.click('[type="submit"]');

    // Assert
    await expect(page.locator('.success')).toBeVisible();
  });

  test('should be accessible', async ({ page }) => {
    await page.goto('/register');
    const violations = await checkA11y(page);
    expect(violations).toHaveLength(0);
  });
});
```

## Accessibility Testing

Playwright tests include a11y checks:
- WCAG 2.1 compliance
- Keyboard navigation
- Screen reader compatibility
- Color contrast

## Fallback

If Playwright is unavailable:

```
 [MCP] Playwright unavailable, suggesting manual tests
```

Generates manual test steps instead of automation:

```markdown
## Manual Test: User Registration

1. Navigate to /register
2. Fill email field with valid email
3. Fill password with secure password
4. Click Submit button
5. Verify: Success message appears
6. Verify: User redirected to dashboard
```

## Best Practices

1. **Isolate tests** — Each test independent
2. **Use selectors wisely** — Prefer data-testid
3. **Include a11y** — Always test accessibility
4. **Capture failures** — Screenshots on error

## Configuration

```json
{
  "playwright": {
    "enabled": true,
    "auto_activate": true,
    "timeout_seconds": 20
  }
}
```

---

*Playwright Reference — F12 MCP Integration*
