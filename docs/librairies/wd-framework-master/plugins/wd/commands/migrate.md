# /wd:migrate - Code Migration Assistant

## Purpose
Code migration between frameworks and technologies with systematic planning and validation.

## Usage
```
/wd:migrate [source-framework] [target-framework] [--strategy incremental|complete|hybrid] [--validate] [--backup]
```

## Auto-Persona Activation
- **Architect**: Migration planning and system design
- **Frontend**: UI framework migrations (React, Vue, Angular)
- **Backend**: Server framework migrations (context-dependent)

## MCP Integration
- **Context7**: Framework patterns and migration best practices
- **Sequential**: Migration planning and systematic execution
- **Magic**: UI component migration and modern framework patterns

## Wave-Enabled
Multi-stage orchestration for complex migration projects with validation checkpoints.

## Arguments
- `[source-framework]` - Current framework or technology
- `[target-framework]` - Target framework or technology
- `--strategy` - Migration approach
  - `incremental`: Gradual migration with coexistence
  - `complete`: Full migration in single phase
  - `hybrid`: Mixed approach based on component complexity
- `--validate` - Enable validation at each step
- `--backup` - Create backup before migration

## Supported Migration Paths

### Frontend Frameworks
- **React ↔ Vue**: Component and state management migration
- **Angular → React/Vue**: Enterprise application modernization
- **jQuery → Modern Framework**: Legacy JavaScript modernization
- **Class Components → Hooks**: React modernization

### Backend Frameworks
- **Express → Fastify/Hapi**: Node.js framework migration
- **Django → FastAPI**: Python framework modernization
- **Spring Boot → Micronaut**: Java microservice migration

### Build Tools & Package Managers
- **Webpack → Vite**: Build tool modernization
- **npm → pnpm/bun**: Package manager migration
- **Babel → SWC/esbuild**: Transpilation tool upgrade

### Database & ORM
- **MySQL → PostgreSQL**: Database engine migration
- **Mongoose → Prisma**: MongoDB ORM modernization
- **Sequelize → TypeORM**: SQL ORM migration

## Migration Process

### 1. Analysis Phase
- Dependency mapping and compatibility assessment
- Breaking changes identification
- Custom code patterns analysis
- Test coverage evaluation

### 2. Planning Phase
- Migration strategy selection and timeline
- Risk assessment and mitigation plans
- Rollback procedures and safety measures
- Team training and knowledge transfer

### 3. Execution Phase
- Systematic code transformation
- Configuration and build tool updates
- Dependency updates and conflict resolution
- Testing and validation at each step

### 4. Validation Phase
- Functional testing and regression validation
- Performance comparison and optimization
- Security audit and compliance check
- Documentation updates and team handoff

## Examples
```bash
# React to Vue migration with incremental strategy
/wd:migrate React Vue --strategy incremental --validate --backup

# Express to Fastify with complete migration
/wd:migrate Express Fastify --strategy complete --validate

# jQuery to React modernization
/wd:migrate jQuery React --strategy hybrid --backup

# Database migration with validation
/wd:migrate MySQL PostgreSQL --validate
```

## Safety Features
- **Automatic Backup**: Code backup before major changes
- **Rollback Support**: Easy reversal of migration steps
- **Validation Checkpoints**: Quality gates at each phase
- **Parallel Development**: Maintain old system during migration
- **Incremental Testing**: Continuous validation throughout process

## Output Deliverables
- **Migration Plan**: Detailed roadmap with timelines
- **Compatibility Report**: Breaking changes and solutions
- **Code Transformation**: Updated codebase with modern patterns
- **Testing Suite**: Comprehensive validation tests
- **Documentation**: Updated guides and API references
- **Performance Report**: Before/after comparison metrics