# Hexagonal Architecture for Clean AI Code (Ports and Adapters)

This guide provides a structured, three-step prompt workflow to direct AI coding agents (like Claude, Cursor, or Gemini) to generate clean, maintainable code based on the **Hexagonal Architecture** (Ports and Adapters) pattern.

## 🎯 The Goal

To prevent AI from generating "messy" code with mixed dependencies, we force it to generate code in distinct, isolated layers:

1.  **Domain:** Pure business logic.
2.  **Ports:** Abstract interfaces/contracts.
3.  **Adapters:** Technology-specific implementations.

This directory contains the prompts for each stage.

## 🤔 Why Use This Approach?

- **Maintainability:** Business logic is decoupled from technology. You can change the database or web framework without touching the core domain.
- **Testability:** The domain can be tested in isolation, without needing a database or other external services.
- **Technology Independence:** Swap technologies (e.g., from PostgreSQL to MongoDB) by simply writing a new adapter.

## 🚀 How to Use

1.  **Stage 1: Domain:** Use [`01_domain_prompt.md`](./01_domain_prompt.md) to generate your core business logic.
2.  **Stage 2: Ports:** Copy the domain code from Stage 1 into [`02_ports_prompt.md`](./02_ports_prompt.md) to define the necessary interfaces.
3.  **Stage 3: Adapters:** Copy the port interface from Stage 2 into [`03_adapters_prompt.md`](./03_adapters_prompt.md) to generate the concrete, technology-specific implementation.

Repeat Stage 3 for each piece of technology your application needs to connect to.

## Primary and Secondary Ports

- **Primary Ports (Driving Adapters):** These are the entry points to your application. They are called by the outside world to execute business logic (e.g., a REST controller that calls an application service).
- **Secondary Ports (Driven Adapters):** These are the exit points from your application. The application uses them to connect to external tools like databases or messaging queues (e.g., a `UserRepository` implementation).

For a more detailed explanation of terms, see the [`glossary.md`](./glossary.md).