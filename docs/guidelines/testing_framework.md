# Framework de Tests Unitaires - Meilleures Pratiques Cloud Code

**Version:** 1.0  
**Objectif:** Tester la conformité de ton plugin cloud code aux meilleures pratiques

---

## Architecture des Tests

```javascript
// test-structure.js
// Arborescence recommandée:

tests/
├── unit/
│   ├── commands/
│   │   ├── command-frontmatter.test.js
│   │   ├── command-validation.test.js
│   │   ├── command-error-handling.test.js
│   │   └── command-idempotence.test.js
│   ├── skills/
│   │   ├── skill-frontmatter.test.js
│   │   ├── skill-auto-invocation.test.js
│   │   ├── skill-progressive-loading.test.js
│   │   └── skill-permissions.test.js
│   ├── agents/
│   │   ├── agent-definition.test.js
│   │   ├── agent-communication.test.js
│   │   └── agent-orchestration.test.js
│   └── core/
│       ├── security.test.js
│       ├── context-management.test.js
│       └── resource-limits.test.js
├── integration/
│   ├── multi-agent-workflow.test.js
│   ├── command-composition.test.js
│   └── skill-loading-pipeline.test.js
├── e2e/
│   ├── full-workflow.test.js
│   └── error-recovery.test.js
└── conformity/
    ├── best-practices-checklist.test.js
    └── security-audit.test.js
```

---

## Tests Unitaires Détaillés

### 1. COMMAND FRONTMATTER VALIDATION

\`\`\`javascript
// tests/unit/commands/command-frontmatter.test.js

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

describe('Command Frontmatter Validation', () => {
  let commandFiles;
  
  beforeAll(() => {
    const commandsDir = path.join(__dirname, '../../.claude/commands');
    commandFiles = fs.readdirSync(commandsDir)
      .filter(f => f.endsWith('.md'))
      .map(f => ({
        name: f.replace('.md', ''),
        path: path.join(commandsDir, f),
        content: fs.readFileSync(path.join(commandsDir, f), 'utf8')
      }));
  });

  describe('Required Fields', () => {
    test('All commands should have frontmatter', () => {
      commandFiles.forEach(cmd => {
        expect(cmd.content).toMatch(/^---\n/);
        expect(cmd.content).toMatch(/\n---\n/);
      });
    });

    test('name field should be unique and kebab-case', () => {
      const names = new Set();
      commandFiles.forEach(cmd => {
        const frontmatter = extractFrontmatter(cmd.content);
        expect(frontmatter.name).toBeDefined();
        expect(frontmatter.name).toMatch(/^[a-z0-9\-]+$/);
        expect(names.has(frontmatter.name)).toBe(false);
        names.add(frontmatter.name);
      });
    });

    test('description should exist and be concise', () => {
      commandFiles.forEach(cmd => {
        const frontmatter = extractFrontmatter(cmd.content);
        expect(frontmatter.description).toBeDefined();
        expect(frontmatter.description.length).toBeGreaterThan(20);
        expect(frontmatter.description.length).toBeLessThan(200);
      });
    });

    test('type field should be valid', () => {
      const validTypes = ['prompt', 'code', 'workflow'];
      commandFiles.forEach(cmd => {
        const frontmatter = extractFrontmatter(cmd.content);
        expect(validTypes).toContain(frontmatter.type);
      });
    });

    test('user-invocable should be boolean', () => {
      commandFiles.forEach(cmd => {
        const frontmatter = extractFrontmatter(cmd.content);
        expect(typeof frontmatter['user-invocable']).toBe('boolean');
      });
    });

    test('disable-model-invocation should be boolean', () => {
      commandFiles.forEach(cmd => {
        const frontmatter = extractFrontmatter(cmd.content);
        expect(typeof frontmatter['disable-model-invocation']).toBe('boolean');
      });
    });

    test('version should follow SemVer', () => {
      const semverRegex = /^\d+\.\d+\.\d+$/;
      commandFiles.forEach(cmd => {
        const frontmatter = extractFrontmatter(cmd.content);
        expect(frontmatter.version).toMatch(semverRegex);
      });
    });

    test('timeout should be specified in milliseconds', () => {
      commandFiles.forEach(cmd => {
        const frontmatter = extractFrontmatter(cmd.content);
        if (frontmatter.timeout) {
          expect(typeof frontmatter.timeout).toBe('number');
          expect(frontmatter.timeout).toBeGreaterThan(0);
          expect(frontmatter.timeout).toBeLessThan(300000); // <5min
        }
      });
    });

    test('dependencies should be array of strings', () => {
      commandFiles.forEach(cmd => {
        const frontmatter = extractFrontmatter(cmd.content);
        if (frontmatter.dependencies) {
          expect(Array.isArray(frontmatter.dependencies)).toBe(true);
          frontmatter.dependencies.forEach(dep => {
            expect(typeof dep).toBe('string');
          });
        }
      });
    });
  });

  describe('Content Structure', () => {
    test('Should have descriptive header after frontmatter', () => {
      commandFiles.forEach(cmd => {
        const content = cmd.content.split('---')[2];
        expect(content).toMatch(/^[^\n]*#/);
      });
    });

    test('Should have usage/examples section', () => {
      commandFiles.forEach(cmd => {
        const content = cmd.content.toLowerCase();
        expect(content).toMatch(/(usage|example|usage example)/);
      });
    });

    test('Should document error cases', () => {
      commandFiles.forEach(cmd => {
        const content = cmd.content.toLowerCase();
        expect(content).toMatch(/(error|fail|invalid|exception)/);
      });
    });
  });
});

function extractFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---\n/);
  if (!match) throw new Error('No frontmatter found');
  return yaml.load(match[1]);
}
\`\`\`

---

### 2. SKILL AUTO-INVOCATION VALIDATION

\`\`\`javascript
// tests/unit/skills/skill-auto-invocation.test.js

describe('Skill Auto-Invocation Rules', () => {
  let skillFiles;

  beforeAll(() => {
    skillFiles = loadAllSkills();
  });

  describe('Auto-Invocation Control', () => {
    test('Skills with disable-model-invocation:false should have descriptive keywords', () => {
      skillFiles
        .filter(s => s.metadata['disable-model-invocation'] === false)
        .forEach(skill => {
          const description = skill.metadata.description.toLowerCase();
          const keywords = ['generate', 'create', 'refactor', 'analyze', 'check', 'scan'];
          const hasKeyword = keywords.some(kw => description.includes(kw));
          expect(hasKeyword).toBe(true);
        });
    });

    test('Skills with disable-model-invocation:true should have side effects or require approval', () => {
      skillFiles
        .filter(s => s.metadata['disable-model-invocation'] === true)
        .forEach(skill => {
          // Vérifier que le skill a une raison légitime (ex: dangerous operation)
          expect(skill.metadata.description).toMatch(/(manual|approval|dangerous|explicitly)/i);
        });
    });

    test('Dangerous skills should require user-invocable:true', () => {
      skillFiles.forEach(skill => {
        if (skill.metadata.description.toLowerCase().includes('delete') ||
            skill.metadata.description.toLowerCase().includes('destructive')) {
          expect(skill.metadata['disable-model-invocation']).toBe(true);
          expect(skill.metadata['user-invocable']).toBe(true);
        }
      });
    });
  });

  describe('Trigger Keywords', () => {
    test('Auto-invoked skills should have clear trigger conditions', () => {
      const triggerKeywords = [
        'when to use', 'trigger', 'invoke when', 'use this'
      ];

      skillFiles
        .filter(s => !s.metadata['disable-model-invocation'])
        .forEach(skill => {
          const hasWhenToUse = skill.metadata['when-to-use'] ||
                               skill.content.toLowerCase().includes('when to use');
          expect(hasWhenToUse).toBeTruthy();
        });
    });

    test('Auto-invoked skill descriptions should not be ambiguous', () => {
      skillFiles
        .filter(s => !s.metadata['disable-model-invocation'])
        .forEach(skill => {
          const description = skill.metadata.description;
          // Vérifier qu'il n'y a pas de langage vague
          expect(description).not.toMatch(/(might|could|perhaps|maybe)/i);
          expect(description.length).toBeGreaterThan(30);
        });
    });
  });

  describe('Progressive Loading Requirements', () => {
    test('Skills should have minimal frontmatter size', () => {
      skillFiles.forEach(skill => {
        const frontmatterSize = skill.metadata;
        // Frontmatter devrait être <1KB
        const size = JSON.stringify(frontmatter).length;
        expect(size).toBeLessThan(1000);
      });
    });

    test('Dependencies should be listed in frontmatter', () => {
      skillFiles.forEach(skill => {
        if (skill.content.includes('require') || skill.content.includes('import')) {
          expect(skill.metadata.dependencies || skill.metadata.supports).toBeDefined();
        }
      });
    });

    test('Referenced files should be documented', () => {
      skillFiles.forEach(skill => {
        const references = skill.content.match(/\.\/\w+\.\w+/g) || [];
        if (references.length > 0) {
          expect(skill.metadata.files || skill.metadata.assets).toBeDefined();
        }
      });
    });
  });
});
\`\`\`

---

### 3. INPUT VALIDATION TESTING

\`\`\`javascript
// tests/unit/commands/command-validation.test.js

describe('Input Validation for Commands', () => {
  let commands;

  beforeAll(() => {
    commands = loadAllCommands();
  });

  describe('String Input Sanitization', () => {
    test('Should reject paths with traversal attacks', async () => {
      const maliciousInputs = [
        '../../../etc/passwd',
        '..\\..\\windows\\system32',
        '/absolute/path/to/file',
        'file\x00.txt'
      ];

      for (const input of maliciousInputs) {
        const result = await validateInput(input, 'filepath');
        expect(result.valid).toBe(false);
        expect(result.reason).toMatch(/path|traversal/i);
      }
    });

    test('Should reject HTML/script injection', async () => {
      const injectionInputs = [
        '<script>alert("xss")</script>',
        'javascript:alert(1)',
        '<img src=x onerror="alert(1)">',
        '${malicious}'
      ];

      for (const input of injectionInputs) {
        const result = await validateInput(input, 'string');
        expect(result.valid).toBe(false);
      }
    });

    test('Should enforce size limits', async () => {
      const hugeInput = 'A'.repeat(10000);
      const result = await validateInput(hugeInput, 'string');
      expect(result.valid).toBe(false);
    });

    test('Should validate JSON strictly', async () => {
      const invalidJSON = [
        '{invalid}',
        "{'singlequote': 1}",
        '{trailing: comma,}',
        '{undefined}'
      ];

      for (const json of invalidJSON) {
        const result = await validateInput(json, 'json');
        expect(result.valid).toBe(false);
      }
    });
  });

  describe('Type Validation', () => {
    test('Should enforce correct argument types', async () => {
      const schema = {
        count: { type: 'number', min: 0, max: 1000 },
        name: { type: 'string', minLength: 1, maxLength: 100 },
        enabled: { type: 'boolean' }
      };

      const testCases = [
        { input: { count: 'not a number' }, valid: false },
        { input: { count: -1 }, valid: false },
        { input: { count: 500 }, valid: true },
        { input: { name: '' }, valid: false },
        { input: { enabled: 'true' }, valid: false }
      ];

      for (const test of testCases) {
        const result = validateAgainstSchema(test.input, schema);
        expect(result.valid).toBe(test.valid);
      }
    });

    test('Should validate enum values', async () => {
      const schema = {
        level: { type: 'enum', values: ['low', 'medium', 'high'] }
      };

      expect(validateAgainstSchema({ level: 'low' }, schema).valid).toBe(true);
      expect(validateAgainstSchema({ level: 'critical' }, schema).valid).toBe(false);
    });
  });

  describe('Required Fields', () => {
    test('Should reject missing required arguments', async () => {
      const schema = {
        filePath: { required: true },
        options: { required: false }
      };

      const result = validateAgainstSchema({}, schema);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('filePath');
    });
  });
});
\`\`\`

---

### 4. ERROR HANDLING STANDARDIZATION

\`\`\`javascript
// tests/unit/commands/command-error-handling.test.js

describe('Error Handling Standardization', () => {
  let commands;

  describe('Error Response Format', () => {
    test('All error responses should have standard structure', async () => {
      const testCases = [
        { input: { filePath: null }, expectedError: 'INVALID_ARGS' },
        { input: { filePath: '/nonexistent/file' }, expectedError: 'FILE_NOT_FOUND' },
        { input: { filePath: '/root/secret' }, expectedError: 'PERMISSION_DENIED' }
      ];

      for (const test of testCases) {
        const result = await executeCommand(test.input);
        expect(result).toHaveProperty('success');
        expect(result).toHaveProperty('errorCode');
        expect(result).toHaveProperty('errorMessage');
        expect(result).toHaveProperty('metadata');
        expect(result.errorCode).toBe(test.expectedError);
      }
    });

    test('Error messages should be explicit and helpful', async () => {
      const result = await executeCommand({ invalidParam: true });
      expect(result.errorMessage.length).toBeGreaterThan(20);
      expect(result.errorMessage).not.toMatch(/undefined|null|error/i);
    });

    test('Metadata should include execution context', async () => {
      const result = await executeCommand({ /* invalid */ });
      expect(result.metadata).toHaveProperty('executionTime');
      expect(result.metadata).toHaveProperty('timestamp');
      expect(result.metadata).toHaveProperty('commandVersion');
      expect(new Date(result.metadata.timestamp)).toBeInstanceOf(Date);
    });
  });

  describe('No Secret Leakage', () => {
    test('Should not expose secrets in error messages', async () => {
      process.env.API_KEY = 'secret-key-12345';
      const result = await executeCommand({ apiKey: 'secret-key-12345' });
      expect(JSON.stringify(result)).not.toContain('secret-key-12345');
    });

    test('Should not expose file paths of sensitive files', async () => {
      // Assuming sensitive path
      const result = await executeCommand({ filePath: '/root/.ssh/id_rsa' });
      expect(result.errorMessage).not.toContain('/root/');
    });

    test('Stack traces should not be in user output', async () => {
      const result = await executeCommand({ /* trigger error */ });
      expect(result.errorMessage).not.toMatch(/at /);
      expect(result.errorMessage).not.toMatch(/\/src\//);
    });
  });

  describe('Idempotency Guarantees', () => {
    test('Idempotent commands should produce identical results', async () => {
      const input = { filePath: './test.txt' };
      const result1 = await executeCommand(input);
      const result2 = await executeCommand(input);
      expect(result1.data).toEqual(result2.data);
    });

    test('Non-idempotent commands should document side effects', async () => {
      // Charger command frontmatter
      const cmd = getCommand('create-file');
      expect(cmd.metadata.idempotent).toBe(false);
      expect(cmd.content).toMatch(/(creates|modifies|deletes|side effect)/i);
    });
  });
});
\`\`\`

---

### 5. SECURITY AUDIT TESTS

\`\`\`javascript
// tests/unit/core/security.test.js

describe('Security Audit', () => {
  describe('Secret Detection', () => {
    test('Should not commit any hardcoded secrets', () => {
      const projectFiles = walkDirectory('.claude');
      const secretPatterns = [
        /api[_-]?key\s*[:=]\s*['\"][\w\-]{20,}/i,
        /password\s*[:=]\s*['\"][^'\"]+['\"]/i,
        /token\s*[:=]\s*['\"][\w\-\.]+['\"]/i,
        /secret\s*[:=]\s*['\"][^'\"]+['\"]/i,
        /sk[-_][a-zA-Z0-9]{24,}/  // OpenAI format
      ];

      projectFiles.forEach(file => {
        const content = fs.readFileSync(file, 'utf8');
        secretPatterns.forEach(pattern => {
          expect(content).not.toMatch(pattern);
        });
      });
    });

    test('Should use .env.example without secrets', () => {
      const envExample = fs.readFileSync('.env.example', 'utf8');
      expect(envExample).not.toMatch(/=[a-z0-9]{20,}/i);
    });
  });

  describe('Input Sanitization', () => {
    test('All string inputs should have sanitization', () => {
      const commandFiles = fs.readdirSync('.claude/commands');
      commandFiles.forEach(file => {
        const content = fs.readFileSync(file, 'utf8');
        // Vérifier présence de sanitization
        expect(content).toMatch(/(sanitize|validate|escape|trim|filter)/i);
      });
    });
  });

  describe('Permission Model', () => {
    test('Commands should follow least privilege', () => {
      const commands = loadAllCommands();
      commands.forEach(cmd => {
        if (cmd.metadata.permissions) {
          // Vérifier que ce ne sont pas des permissions larges
          expect(cmd.metadata.permissions.write).not.toContain('workspace');
          expect(cmd.metadata.permissions.execute).not.toContain('shell');
        }
      });
    });
  });

  describe('Audit Trail', () => {
    test('Should log sensitive operations', () => {
      const logFile = fs.readFileSync('./audit.log', 'utf8');
      const logs = logFile.split('\n').map(l => JSON.parse(l));
      
      logs.forEach(log => {
        expect(log).toHaveProperty('timestamp');
        expect(log).toHaveProperty('action');
        expect(log).toHaveProperty('userId');
        expect(log).not.toHaveProperty('secret');
        expect(log).not.toHaveProperty('password');
      });
    });
  });
});
\`\`\`

---

### 6. PERFORMANCE TESTS

\`\`\`javascript
// tests/unit/core/performance.test.js

describe('Performance & Resource Management', () => {
  describe('Context Size', () => {
    test('Initial context should be <15% of budget', () => {
      const contextBudget = 100000; // tokens
      const initialContext = measureInitialContext();
      expect(initialContext).toBeLessThan(contextBudget * 0.15);
    });

    test('Metadata loading should be <1s', () => {
      const start = Date.now();
      loadMetadataForAllSkills();
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(1000);
    });

    test('Full skill loading should be <5s', () => {
      const start = Date.now();
      loadFullSkill('code-analyzer');
      const duration = Date.now() - start;
      expect(duration).toBeLessThan(5000);
    });
  });

  describe('Timeout Enforcement', () => {
    test('Commands should respect timeout settings', async () => {
      const cmd = getCommand('long-running-task');
      const timeout = cmd.metadata.timeout;
      expect(timeout).toBeDefined();
      expect(timeout).toBeGreaterThan(0);
      expect(timeout).toBeLessThan(300000); // <5 min
    });

    test('Should cleanup resources on timeout', async () => {
      // Test that no orphaned processes exist after timeout
      // Implementation depends on your setup
    });
  });

  describe('Memory & Resource Limits', () => {
    test('Should not exceed memory limits', async () => {
      const memBefore = process.memoryUsage().heapUsed;
      // Run memory-intensive command
      const memAfter = process.memoryUsage().heapUsed;
      const increase = memAfter - memBefore;
      expect(increase).toBeLessThan(512 * 1024 * 1024); // 512MB
    });
  });
});
\`\`\`

---

## Commande NPM pour Lancer Tests

\`\`\`json
{
  "scripts": {
    "test": "jest",
    "test:unit": "jest tests/unit",
    "test:integration": "jest tests/integration",
    "test:e2e": "jest tests/e2e",
    "test:conformity": "jest tests/conformity",
    "test:coverage": "jest --coverage",
    "test:watch": "jest --watch",
    "test:security": "jest tests/unit/core/security.test.js",
    "test:performance": "jest tests/unit/core/performance.test.js",
    "validate": "npm run lint && npm run test:conformity && npm run test:coverage",
    "validate:strict": "npm run validate && npm run test:security",
    "lint": "eslint .claude/",
    "format": "prettier --write .claude/"
  }
}
\`\`\`

---

## Exemple d'Exécution

\`\`\`bash
# Lancer tous les tests
$ npm test

# Lancer tests de conformité uniquement
$ npm run test:conformity

# Lancer avec coverage
$ npm run test:coverage

# Mode watch (redémarrage automatique)
$ npm run test:watch

# Validation complète stricte
$ npm run validate:strict
\`\`\`

---

## Critères de Succès

✅ **Tous les tests passent**
✅ **Coverage >80%**
✅ **Aucune secret détecté**
✅ **Tous les timeouts respectés**
✅ **Input validation en place**
✅ **Error handling standardisé**
✅ **Auto-invocation controllé**
✅ **Progressive loading fonctionnel**
