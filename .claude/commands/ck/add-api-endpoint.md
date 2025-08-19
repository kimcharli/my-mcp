---
command: "/ck:add-api-endpoint"
category: "Development & API Creation"
purpose: "Create new API endpoint with proper structure, validation, and documentation"
wave-enabled: true
performance-profile: "standard"
agent: "feature-developer"
allowed-tools: Read(*), Write(*), Edit(*), MultiEdit(*), Bash(*), Glob(*), Grep(*), Task(*)
---

## Context

- Existing API structure: !`find . -path "*/api/*" -o -path "*/routes/*" -o -path "*/controllers/*" | head -15`
- API configuration: !`find . -name "*api*" -name "*.py" -o -name "*.js" -o -name "*.ts" | head -10`
- Database models: !`find . -path "*/models/*" -o -path "*/schemas/*" | head -10`
- Current git status: !`git status --porcelain`
- API design documentation: @docs/API_DESIGN.md
- Architecture patterns: @docs/ARCHITECTURE.md
- Requirements specification: @docs/REQUIREMENTS.md

## Task

Create a new API endpoint following established patterns and best practices. This command will:

1. **API Design**: Plan endpoint structure and data flow
2. **Implementation**: Create endpoint with proper validation
3. **Security**: Add authentication and authorization
4. **Testing**: Create comprehensive test coverage
5. **Documentation**: Generate API documentation

## API Endpoint Creation Workflow

### Phase 1: API Design & Planning
- [ ] Define endpoint purpose and functionality
- [ ] Design request/response schema and data models
- [ ] Plan URL structure following REST conventions
- [ ] Identify authentication and authorization requirements
- [ ] Review existing API patterns for consistency

### Phase 2: Core Implementation
- [ ] Create endpoint handler/controller function
- [ ] Implement request validation and sanitization
- [ ] Add proper error handling and status codes
- [ ] Integrate with database models or external services
- [ ] Apply security measures and access controls

### Phase 3: Validation & Security
- [ ] Add input validation for all parameters
- [ ] Implement rate limiting if applicable
- [ ] Add authentication middleware integration
- [ ] Validate authorization and permissions
- [ ] Test security edge cases and attack vectors

### Phase 4: Testing & Quality Assurance
- [ ] Create unit tests for endpoint logic
- [ ] Add integration tests for full request/response cycle
- [ ] Test error scenarios and edge cases
- [ ] Validate API contract and schema compliance
- [ ] Performance test for acceptable response times

### Phase 5: Documentation & Integration
- [ ] Generate/update OpenAPI/Swagger documentation
- [ ] Add endpoint to API documentation
- [ ] Create usage examples and code samples
- [ ] Update API client libraries if applicable
- [ ] Verify integration with existing systems

## API Best Practices

- **REST Conventions**: Follow RESTful design principles
- **Consistent Naming**: Use consistent URL and parameter naming
- **Proper HTTP Methods**: Use appropriate HTTP verbs (GET, POST, PUT, DELETE)
- **Status Codes**: Return meaningful HTTP status codes
- **Error Handling**: Provide clear, actionable error messages
- **Validation**: Validate all input parameters and data
- **Security**: Implement proper authentication and authorization
- **Documentation**: Maintain up-to-date API documentation

## Common API Patterns

### CRUD Operations
```
GET    /api/resource       - List resources
POST   /api/resource       - Create resource
GET    /api/resource/:id   - Get specific resource
PUT    /api/resource/:id   - Update resource
DELETE /api/resource/:id   - Delete resource
```

### Response Format
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message",
  "metadata": {
    "pagination": { ... },
    "total": 100
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": { ... }
  }
}
```

## Usage Examples

```bash
# Create a new user management endpoint
/ck:add-api-endpoint "POST /api/users - Create new user account"

# Create a data retrieval endpoint
/ck:add-api-endpoint "GET /api/reports/:id - Retrieve report by ID"

# Create a file upload endpoint
/ck:add-api-endpoint "POST /api/files/upload - Handle file uploads"
```

## Integration Requirements

- **Database**: Integrate with existing data models and schemas
- **Authentication**: Use established auth middleware and patterns
- **Logging**: Include structured logging for monitoring and debugging
- **Caching**: Apply caching strategies where appropriate
- **Rate Limiting**: Implement rate limiting for public endpoints
- **Monitoring**: Add metrics and health check integration