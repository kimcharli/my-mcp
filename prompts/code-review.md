
**Prompt for Code Review and Normalization:**

"Review the codebase in the [specific directory or files, e.g., `juniper_network_tools/etl/extract/`] for the Darden Apstra Data Center Migration project. Focus on identifying and reducing code duplication while normalizing the structure. Specifically:

1. **Identify Duplications**: Scan for repeated code patterns, functions, or logic across files (e.g., similar data processing methods in processors like `DeviceProcessor`, `BGPProcessor`, etc.). Suggest extracting common functionality into shared utilities or base classes.

2. **Normalization Goals**:
   - Standardize naming conventions (e.g., consistent function/method names, variable naming using snake_case or camelCase as per project standards).
   - Ensure consistent code structure, such as uniform error handling, logging, and data validation patterns.
   - Align with the project's profile system and ETL architecture (e.g., ensure all processors support profile-aware configurations).
   - Optimize imports and dependencies to avoid redundancy.

3. **Analysis Criteria**:
   - Look for opportunities to refactor duplicated logic into reusable modules (e.g., create a base processor class for common ETL operations).
   - Check for inconsistencies in data handling, such as varying ways to process configurations or routes.
   - Ensure adherence to the project's rules (e.g., using `uv` for dependencies, persistent DuckDB, and environment separation).

4. **Output Requirements**:
   - Provide a summary of identified duplications and normalization issues.
   - Suggest specific refactoring steps, including code snippets for proposed changes.
   - Prioritize changes that improve maintainability without breaking existing functionality.
   - If applicable, propose new file structures or utility modules to centralize common code.

Use tools like `read_file`, `search_files`, and `list_code_definition_names` to analyze the code thoroughly before suggesting improvements."

