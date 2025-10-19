# User Service Example

This directory contains a complete, simple example of a User Service built using the hexagonal architecture principles and prompts from this guide.

## Files

- `01_domain.py`: The core domain logic for the User service.
- `02_ports.py`: The primary and secondary port interfaces.
- `03_postgres_adapter.py`: A PostgreSQL adapter for the `UserRepository` port.
- `04_app.py`: A simple application that uses the domain, ports, and adapters.
