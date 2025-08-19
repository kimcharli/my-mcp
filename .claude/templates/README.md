# {PROJECT_TITLE}

{PROJECT_DESCRIPTION}

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test
```

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Application pages/routes
├── services/      # Business logic and API calls
├── utils/         # Helper functions
└── types/         # TypeScript type definitions
```

## Development

### Prerequisites

- Node.js {NODE_VERSION}+
- npm 9+
- {DATABASE} 14+

### Environment Setup

1. Copy `.env.example` to `.env`
2. Update database connection details
3. Run `npm run db:migrate` to set up database

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run test` - Run test suite
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler

## API Documentation

See [API_DESIGN.md](docs/API_DESIGN.md) for detailed API documentation.

## Contributing

1. Read [REQUIREMENTS.md](docs/REQUIREMENTS.md) to understand project goals
2. Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) for technical decisions
3. Follow the testing strategy in [TESTING_STRATEGY.md](docs/TESTING_STRATEGY.md)
4. See [CLAUDE.md](CLAUDE.md) for AI assistance workflows

## Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment instructions.

## License

{LICENSE}