# Glossary of Terms


- **Hexagonal Architecture (Ports and Adapters):** An architectural pattern that isolates the core business logic (the hexagon) from external concerns like databases, UIs, or third-party services. This is achieved by defining "Ports" (interfaces) that the domain logic uses, and creating "Adapters" that implement these interfaces for specific technologies.


- **Domain Logic:** The core business rules and processes of the application. This code should be pure and have no dependencies on external technologies.


- **Ports:** Abstract interfaces that define a contract for interaction between the domain and the outside world. There are two types of ports:

    - **Primary Ports (Driving Ports):** These define how the outside world can interact with the application (e.g., an application service interface).

    - **Secondary Ports (Driven Ports):** These define what the application needs from the outside world (e.g., a repository interface for data persistence).


- **Adapters:** Concrete implementations of the ports. They translate between the port's interface and a specific technology.

    - **Driving Adapters:** These drive the application by calling the primary ports (e.g., a REST controller).

    - **Driven Adapters:** These are driven by the application and implement the secondary ports (e.g., a PostgreSQL implementation of a repository).


- **Value Objects:** Simple, immutable objects that represent a descriptive aspect of the domain (e.g., an `Email` or `Money` object). They have no identity and are defined by their attributes.
