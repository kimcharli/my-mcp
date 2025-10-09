# How to Create and Use AGENTS.md

This document provides a guide on how to create and use `AGENTS.md` files in your projects. `AGENTS.md` is an open format designed to guide AI coding agents by providing context and instructions for working on a project. It functions as a "README for agents," offering a dedicated and predictable location for AI tools to find information relevant to their tasks.

## Why use AGENTS.md?

`AGENTS.md` complements `README.md` files, which are primarily for human developers. It contains detailed context such as build steps, tests, and conventions that might otherwise clutter a `README`. This separation ensures that `README.md` remains concise and focused on human contributors, while `AGENTS.md` provides precise, agent-focused guidance.

By using `AGENTS.md`, AI agents can follow the same coding standards and rules as human developers, leading to improved code quality and consistency.

## What to include in AGENTS.md?

`AGENTS.md` should include machine-readable steps and information that an AI agent can use to perform its tasks. This includes:

*   **Project Structure:** An overview of the project's directory structure and where key files are located.
*   **Setup and Build Commands:** Instructions on how to set up the development environment and build the project.
*   **Test Commands:** Instructions on how to run the project's tests.
*   **Code Style and Conventions:** Information about the project's coding style, formatting rules, and naming conventions.
*   **Commit Guidelines:** Instructions on how to format commit messages.
*   **Security Policies:** Information about the project's security policies and procedures.
*   **Dependencies:** A list of the project's dependencies and how to manage them.

## AGENTS.md in Monorepos

For large projects or monorepos, nested `AGENTS.md` files can be used for subprojects. Agents will automatically read the nearest `AGENTS.md` file in the directory tree, allowing for context-specific instructions for different parts of the project.

## Example AGENTS.md for a `pnpm`/`turbo` project

Here is an example of an `AGENTS.md` file for a project that uses `pnpm` and `turbo`.

### Project overview and structure

[Provide a brief overview of the project and its structure. You can include a diagram or a tree structure of the directories.]

### Dev environment tips
- Use `pnpm dlx turbo run where <project_name>` to jump to a package instead of scanning with `ls`.
- Run `pnpm install --filter <project_name>` to add the package to your workspace so Vite, ESLint, and TypeScript can see it.
- Use `pnpm create vite@latest <project_name> -- --template react-ts` to spin up a new React + Vite package with TypeScript checks ready.
- Check the name field inside each package's package.json to confirm the right name—skip the top-level one.

### Building and Testing instructions
- Find the CI plan in the .github/workflows folder.
- Run `pnpm turbo run test --filter <project_name>` to run every check defined for that package.
- From the package root you can just call `pnpm test`. The commit should pass all tests before you merge.
- To focus on one step, add the Vitest pattern: `pnpm vitest run -t "<test name>"`.
- Fix any test or type errors until the whole suite is green.
- After moving files or changing imports, run `pnpm lint --filter <project_name>` to be sure ESLint and TypeScript rules still pass.
- Add or update tests for the code you change, even if nobody asked.

### Testing guidelines

[Provide guidelines on how to write tests, what to test, and where to find existing tests.]

### Coding conventions and style guidelines

[Provide information about the project's coding style, formatting rules, and naming conventions.]

### Architecture and design patterns

[Provide an overview of the project's architecture and the design patterns used.]

### Security and compliance considerations

[Provide information about the project's security policies and procedures.]

### PR instructions
- Title format: [<project_name>] <Title>
- Always run `pnpm lint` and `pnpm test` before committing.

## Official Resources

*   [agents.md Official Site](https://agents.md)
*   [GitHub Repository by OpenAI](https://github.com/openai/agents-md)
*   [AIMultiple Guide](https://research.aimultiple.com/agents-md/)
*   [Builder.io Blog](https://www.builder.io/blog/agents-md)
*   [AI Builders Tutorial](https://tutorial.aibuilders.dev/agets-md)