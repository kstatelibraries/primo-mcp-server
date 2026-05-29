# primo-mcp-server

MCP server for Ex Libris Primo library discovery -- search university catalogues and subscribed databases (ProQuest, Elsevier, Crossref, Gale, Springer, IEEE, etc.) via the Model Context Protocol.

## Features

- **Search** the full university catalogue and Primo Central Index (millions of records)
- **Get record details** including abstract, authors, identifiers, and availability
- **Autocomplete** search suggestions
- **Generate citations** in APA 7th, Harvard, Chicago, IEEE, and Vancouver styles
- **Export** to BibTeX, RIS, or CSV for import into reference managers

## Installation

```bash
git clone https://github.com/geheharidas/primo-mcp-server.git
cd primo-mcp-server
pip install -e .
```

## Register in Claude Code

Add to `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "primo": {
      "command": "python",
      "args": ["-m", "primo_mcp_server"]
    }
  }
}
```

Restart Claude Code. The tools will appear as `mcp__primo__primo_search`, etc.

## Tools

| Tool               | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| `primo_search`     | Search the library catalogue with filters (type, date, peer-reviewed)  |
| `primo_get_record` | Get full details for a record by ID                                    |
| `primo_suggest`    | Autocomplete search suggestions                                        |
| `primo_cite`       | Generate formatted citations (APA7, Harvard, Chicago, IEEE, Vancouver) |
| `primo_export`     | Export records as BibTeX, RIS, or CSV                                  |

## Usage Examples

From a Claude Code conversation:

- "Search the library for articles about machine learning in entrepreneurship published after 2020"
- "Get the full details for record cdi_crossref_primary_10_1234"
- "Generate APA7 citations for these records"
- "Export the search results as BibTeX"

## Configuration

This application **requires a `.env` file** to initialize. All hardcoded defaults have been removed. If any required environment variable is missing, the server will fail to start with a clear  
 initialization error.

### Setup

1.  Copy the example file: `cp .env.example .env`
2.  Open `.env` and update the values to match your institution's Primo VE configuration.  


### Required Variables

| Variable                        | Description                                       |
| ------------------------------- | ------------------------------------------------- |
| `PRIMO_BASE_URL`                | Primo REST API endpoint                           |
| `PRIMO_VID`                     | Primo View ID                                     |
| `PRIMO_INSTITUTION_NAME`        | Display name shown in responses                   |
| `PRIMO_REQUEST_TIMEOUT`         | HTTP request timeout in seconds (e.g., `30.0`)    |
| `PRIMO_MAX_RESULTS_PER_REQUEST` | Max results per API request (e.g., `50`)          |
| `PRIMO_DEFAULT_RESULTS`         | Default number of results returned (e.g., `10`)   |
| `PRIMO_TAB_EVERYTHING`          | Search tab identifier for "Everything"            |
| `PRIMO_TAB_CATALOGUE`           | Search tab identifier for "Catalogue"             |
| `PRIMO_SCOPE_COMBINED`          | Search scope identifier for combined/index search |
| `PRIMO_SCOPE_LOCAL`             | Search scope identifier for local search          |
| `PRIMO_LANGUAGE`                | Language code for search results (e.g., `en`)     |

### Optional Variables

| Variable           | Description                                                              |
| ------------------ | ------------------------------------------------------------------------ |
| `PRIMO_USER_AGENT` | HTTP User-Agent string (defaults to `primo-mcp-server/0.1.0` if omitted) |

## Running Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Licence

MIT
