# my-mcp

This example found in Claude MCP section didn't work. Claude was utilizing its own web search instead.

# npx upgrade

```sh
npm ls npx
npm cache clean --force
npm install -g npm@latest
```

# apify test

```sh
export $(cat ~/.env)
npx -y @apify/actors-mcp-server --actors apify/web-scraper
```

