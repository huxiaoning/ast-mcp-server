# AST/ASG Code Analysis MCP Server

A Model Context Protocol (MCP) server that provides code structure analysis capabilities using Abstract Syntax Trees (ASTs) and Abstract Semantic Graphs (ASGs).

## Overview

This MCP server provides AI systems with direct access to code structure and semantic information, enabling more accurate:

- Code understanding and analysis
- Bug detection and fixing
- Semantic-aware code generation
- Refactoring suggestions

Research shows that structure-aware models outperform token-only LLMs significantly on code-related tasks, with improvements including:
- 21% fewer syntax errors in code generation
- 33% more bugs fixed in program repair tasks
- Better performance in code search and other tasks

## Features

- Parse code into Abstract Syntax Trees (ASTs) using tree-sitter
- Generate Abstract Semantic Graphs (ASGs) with data flow and control flow information
- Query code structure and semantics
- Get contextualized code insights based on structural information

## Installation

```bash
# 1. Clone this repository
# 2. Create a virtual environment:
 python -m venv .venv

# 3. Activate the virtual environment:
source .venv/bin/activate # On Windows: .venv\Scripts\activate

# 4. Install dependencies:
pip install -r requirements.txt

# 5. Build language parsers:
python build_parsers.py
```

## Usage

## Integration with Claude or other MCP clients

Edit your `claude_desktop_config.json` to include:

```json
{
  "mcpServers": {
    "AstAnalyzer": {
      "command": "/absolute/path/to/python",
      "args": [
        "/absolute/path/to/ast-mcp-server/server.py"
      ]
    }
  }
}
```

See the example JSON for my working config example.

## Supported Languages

- Python
- JavaScript
- TypeScript
- Go
- Rust
- C/C++
- Java

## Dev Usage

To run the MCP server:

```bash
python server.py
```

To run the server with the MCP inspector for testing:

```bash
mcp dev server.py
```

## License

[MIT](https://github.com/angrysky56/ast-mcp-server/blob/main/LICENSE)
