# Cynetics Quick Start Guide

Get Cynetics running in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Git
- API key for Anthropic or OpenAI

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/cynetics.git
cd cynetics
```

### 2. Run Installation Script

```bash
chmod +x install.sh
./install.sh
```

Or manually:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install MCP servers
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-git
npm install -g @modelcontextprotocol/server-shell
npm install -g @modelcontextprotocol/server-memory

# Create environment file
cp .env.example .env
```

### 3. Configure API Keys

Edit `.env` file:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
# OR
OPENAI_API_KEY=sk-your-key-here
```

### 4. Initialize Configuration

```bash
python cynetics.py --init
```

## Your First Project

### Example 1: Simple CLI Tool

```bash
python cynetics.py --description "
Create a command-line tool that converts CSV files to JSON.
Features:
- Read CSV from file or stdin
- Output formatted JSON
- Support filtering by column
- Handle large files efficiently
"
```

**What happens:**
1. Generates specification (30 seconds)
2. Creates technical plan (45 seconds)
3. Breaks into tasks (30 seconds)
4. Implements code (2-3 minutes)

**Output in `workspace/`:**
- `csv_to_json.py` - Main CLI tool
- `converter.py` - Conversion logic
- `tests/` - Test files
- `README.md` - Documentation

### Example 2: REST API

```bash
python cynetics.py \
  --description "Build a REST API for a bookstore with CRUD operations for books and authors" \
  --stack '{"language": "python", "framework": "fastapi", "database": "sqlite"}'
```

**Generated structure:**
```
workspace/
├── main.py
├── models.py
├── routes/
│   ├── books.py
│   └── authors.py
├── database.py
├── tests/
└── requirements.txt
```

### Example 3: With Custom Tech Stack

```bash
python cynetics.py \
  --description "Create a todo list application with user authentication" \
  --stack '{
    "language": "typescript",
    "frontend": "react",
    "backend": "express",
    "database": "mongodb",
    "auth": "jwt"
  }'
```

## Check Progress

```bash
# View logs
tail -f logs/cynetics.log

# Check generated code
ls -la workspace/

# View artifacts
cat artifacts/specification.json
cat artifacts/plan.json
cat artifacts/tasks.json
```

## Common Options

### Specify AI Provider

Edit `cynetics.json`:

```json
{
  "default_provider": "openai"
}
```

### Run Specific Phases

```bash
# Generate specification only
python cynetics.py --description "..." --phase specify

# Generate plan only (requires existing spec)
python cynetics.py --phase plan

# Generate tasks only (requires spec and plan)
python cynetics.py --phase tasks

# Implement only (requires tasks)
python cynetics.py --phase implement
```

## Troubleshooting

### "No module named 'anthropic'"

```bash
pip install anthropic
```

### "MCP server not found"

```bash
npm install -g @modelcontextprotocol/server-filesystem
```

### "API key not found"

Make sure `.env` file exists and contains your API key:

```bash
cat .env | grep API_KEY
```

## Next Steps

- Read [Configuration Guide](configuration.md)
- See [Examples](examples.md)
- Check [Troubleshooting Guide](troubleshooting.md)

## Getting Help

- GitHub Issues: https://github.com/yourusername/cynetics/issues
- Discord: https://discord.gg/cynetics
- Docs: https://docs.cynetics.dev
