# bs-webctl

Standalone browser-control CLI for AI agents. Extracted from [GenericAgent](https://github.com/dailyheros/GenericAgent).

Control a real Chrome browser (preserving login sessions) via a Chrome MV3 extension + WebSocket bridge. Any AI agent can use it: `pip install bs-webctl`, load the extension, run commands.

## Install

```bash
pip install bs-webctl
```

## Quick Start

### 1. Install the Chrome extension

```bash
bs-webctl install-extension
```

This extracts the extension to `~/.bs-webctl/extension/` and prints Chrome loading instructions.

### 2. Start the server

```bash
bs-webctl server
```

Keep this running in a terminal. It opens WebSocket on `127.0.0.1:18765` and HTTP on `127.0.0.1:18766`.

### 3. Load the extension in Chrome

1. Open `chrome://extensions`
2. Enable **Developer mode** (top right)
3. Click **Load unpacked**
4. Select `~/.bs-webctl/extension/`
5. Open any normal URL (e.g. `https://example.com`) — the extension auto-connects to the server

### 4. Use the CLI

```bash
# List connected tabs
bs-webctl sessions

# Get simplified page HTML
bs-webctl scan

# Get text only
bs-webctl scan --text-only

# Execute JavaScript
bs-webctl exec "document.title"
bs-webctl exec "JSON.stringify(document.cookie)" --save-to cookies.json

# Execute JS from file
bs-webctl exec-file script.js
```

All commands output JSON on stdout (debug info on stderr), making them easy to parse programmatically.

## Commands

| Command | Description |
|---------|-------------|
| `server` | Start TMWebDriver master server in foreground |
| `sessions` | List all connected browser tabs |
| `scan` | Get simplified HTML/text of the active tab |
| `exec` | Execute JavaScript in the browser, return result + DOM diff |
| `exec-file` | Execute JavaScript from a file |
| `install-extension` | Extract Chrome extension to `~/.bs-webctl/extension/` |

## How It Works

```
┌─────────────────────┐      WebSocket       ┌─────────────────────┐
│  bs-webctl CLI       │  ← 127.0.0.1:18765 →  │  Chrome extension   │
│  (Python)            │      HTTP :18766      │  (tmwd_cdp_bridge)  │
└─────────────────────┘                       └─────────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────────┐
                                                │  Real Chrome tabs   │
                                                │  (login preserved)  │
                                                └─────────────────────┘
```

The extension injects into your real Chrome browser — no Selenium, no Playwright, no separate browser instance. Your cookies, login sessions, and extensions stay intact.

## Dependencies

- `bottle` — HTTP server
- `beautifulsoup4` — HTML parsing/optimization

The WebSocket server is inlined from `simple_websocket_server` (pure stdlib, ~700 lines) to avoid depending on an unmaintained PyPI package.

## License

MIT
