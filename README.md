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

# client configuration

## gemini

~/.gemini/settings.json
```json
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
```


## Claude Code

```sh
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

## Claude Desktop
claude_desktop_config.json

```json
    "context7": {
      "command": "npx",
      "args": [
        "-y",
        "@upstash/context7-mcp"
      ]
    },
```

# servers

## vscode
https://code.visualstudio.com/mcp


## context7
https://github.com/upstash/context7

```
"Make a Next.js 14 API route with App Router"
```

## supabase
https://supabase.com/docs/guides/getting-started/mcp


## browser MCP
https://docs.browsermcp.io/welcome


## Task-Master
https://www.task-master.dev/


## Exa MCP
https://docs.exa.ai/reference/exa-mcp


# within repo

## gemini

user scope
```
claude mcp add gemini -s user -e GEMINI_API_KEY=XXXX -- npx -y github:kimcharli/mcp-server-gemini 
```

```
claude mcp add gemini -e GEMINI_API_KEY=XXXXXXX -- npx -y github:kimcharli/mcp-server-gemini
```

