---
description: Create and manage a comprehensive rule engine with subject-condition-action patterns
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(mkdir:*), Bash(cp:*), Read(*), Write(*), Edit(*), MultiEdit(*), Grep(*), Glob(*), WebFetch(*)
---

## Context

- Project structure: !`ls -la`
- Existing rule files: !`find . -name "*rule*" -o -name "*decision*" -o -name "*condition*"`
- Configuration files: !`find . -name "*.json" -o -name "*.yaml" -o -name "*.yml"`

## Your task

Create a comprehensive **Rule Engine Management System** with the following components:

### 1. Rule Schema Definition
Create a standardized rule format with:
- **Subject**: What entity/object the rule applies to
- **Condition**: When the rule should trigger (boolean logic, comparisons, patterns)
- **Action**: What should happen when condition is met
- **Metadata**: Priority, category, description, enabled/disabled status

Example rule structure:
```json
{
  "id": "rule_001",
  "name": "High Value Customer Discount",
  "subject": "customer",
  "condition": {
    "and": [
      {"field": "total_purchases", "operator": ">", "value": 1000},
      {"field": "account_type", "operator": "==", "value": "premium"}
    ]
  },
  "action": {
    "type": "apply_discount",
    "parameters": {"percentage": 15, "reason": "high_value_customer"}
  },
  "priority": 100,
  "enabled": true,
  "category": "customer_rewards"
}
```

### 2. Default Rule Book Creation
Generate a comprehensive default rulebook with:
- **Customer Management Rules**: Segmentation, rewards, notifications
- **Order Processing Rules**: Validation, pricing, fulfillment
- **Inventory Rules**: Restock alerts, price adjustments
- **Security Rules**: Access control, fraud detection
- **System Rules**: Performance monitoring, error handling
- **Content Rules**: Content moderation, recommendations

### 3. Rule Management Interface
Implement CRUD operations for rules:

#### View Rules
- List all rules with filtering (by category, status, priority)
- Display rule details in human-readable format
- Show rule execution history and statistics
- Validate rule syntax and dependencies

#### Download Rules
- Export rules as JSON, YAML, or CSV
- Generate rule documentation (markdown format)
- Create backup archives with timestamps
- Support selective export by category/criteria

#### Upload/Import Rules
- Parse and validate uploaded rule files
- Handle multiple formats (JSON, YAML, CSV)
- Merge rules with conflict resolution
- Validate rule syntax and cross-references
- Preview changes before applying

#### Revise Rules
- Edit existing rules with validation
- Test rules against sample data
- Version control for rule changes
- Rollback capabilities
- Rule dependency management

### 4. Rule Execution Engine
Create a rule processor that:
- Evaluates conditions against input data
- Handles complex boolean logic (AND, OR, NOT)
- Supports multiple operators (==, !=, >, <, >=, <=, contains, matches, in)
- Processes rules by priority order
- Logs execution results and performance metrics
- Handles rule conflicts and exceptions
- Supports nested conditions and dynamic values

### 5. Integration Components

#### Data Input Interface
- Accept JSON/XML/form data for rule evaluation
- Support batch processing for multiple subjects
- Handle real-time event streams
- Validate input against subject schemas

#### Action Execution System
- Execute actions based on rule outcomes
- Support multiple action types (HTTP calls, database updates, notifications)
- Handle action failures and retries
- Log action results and side effects

#### Monitoring & Analytics
- Rule execution statistics and performance metrics
- Success/failure rates per rule
- Most/least triggered rules analysis
- Performance bottleneck identification
- Alert system for rule failures

### 6. Configuration & Settings
Provide configuration for:
- Rule evaluation timeout settings
- Action execution timeout and retry policies
- Logging levels and retention policies
- Performance monitoring thresholds
- Security settings and access controls

### 7. Testing & Validation Framework
Include testing capabilities:
- Rule unit testing with sample data
- Regression testing for rule changes
- Performance testing with load simulation
- Rule conflict detection and resolution
- Dry-run mode for safe rule testing

### Implementation Requirements:
- Choose appropriate technology stack (Node.js/Python/Go)
- Design scalable architecture (can handle 1000+ rules)
- Implement proper error handling and logging
- Create comprehensive documentation
- Add configuration management
- Include security considerations (input validation, access control)
- Support for rule versioning and auditing

### Deliverables:
1. Complete rule engine implementation
2. Default rulebook with 20+ sample rules
3. Management interface (CLI or web-based)
4. Documentation and usage examples
5. Test suite with sample data
6. Configuration files and deployment scripts