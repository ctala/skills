---
name: venn
description: Safely connects Gmail, Calendar, Drive, Atlassian (Jira/Confluence), Notion, GitHub, Salesforce, and dozens of other enterprise tools via a single MCP endpoint. Free, register @ https://venn.ai
version: 1.0.4
metadata:
  openclaw:
    emoji: "🦉"
    # 1. LIFECYCLE GATING
    # Prevents execution if the URL is missing or mcporter isn't installed.
    requires:
      env:
        - VENN_UNIVERSAL_URL
      bins:
        - mcporter-manual

    # 2. AUTOMATED SETUP PROTOCOLS
    # This handles the "Discovery & Fix" flow if the skill is blocked.
    setup:
      on_missing:
        - message: "I need your Venn Universal URL to begin. You can find this in your Venn.ai settings under 'Integrations'."
          variable: VENN_UNIVERSAL_URL
          store: "openclaw.json"
      on_ready:
        - command: "bash ~/.openclaw/workspace/skills/venn/scripts/install-mcporter-manual.sh"
          help: "Install/build mcporter-manual (device_code-capable fork)"

        - command: "~/.local/bin/mcporter-manual config add venn \"$VENN_UNIVERSAL_URL\" --deviceCodeGrant"
          help: "Register the Venn MCP server using mcporter-manual"

        - command: "~/.local/bin/mcporter-manual auth venn --reset"
          help: "Authenticate Venn via device code (headless-safe)"

        - command: "~/.local/bin/mcporter-manual list --output json"
          help: "Verify Venn is healthy"

    # 3. UI DASHBOARD CONFIGURATION
    # Maps the environment variable to a visible text field in the Web UI.
    fields:
      - name: VENN_UNIVERSAL_URL
        label: "Venn Universal URL"
        type: string
        ui: "config"
        placeholder: "https://gateway.venn.ai/..."
        help: "Your unique Venn Gateway URL. Ensure it starts with https://"

    # 4. DEPENDENCY MANAGEMENT
    # Ensures users like your friend can install mcporter directly from the UI.
    install:
      - id: mcporter
        kind: npm
        package: "mcporter"
        global: true
        label: "Install MCP Porter CLI"

    # 5. EXAMPLE PROMPTS TO GET STARTED
    examples:
      - prompt: "@venn which services do I have connected?"
        label: "Check connected services"
      - prompt: "@venn check my recent emails and summarize any action items"
        label: "Check recent emails"
      - prompt: "@venn find jira tickets assigned to me that need attention"
        label: "Check for work in Jira"
      - prompt: "@venn summarize this figma figjam session. The URL was [FIGJAM_SESSION_URL_HERE]"
        label: "Review figma figjam session"

    primaryEnv: VENN_UNIVERSAL_URL
    auth:
      method: oauth
      provider: venn
---

# Venn Your Universal MCP Server

## Overview
You are the architectural bridge between the user and their enterprise SaaS stack. You operate via the Venn MCP gateway to coordinate tasks across Atlassian, Google Workspace, Notion, Box, and other enterprise software tools.

## ⚡️ Quick Start Prompts
Copy and paste these to get started:

* **First Time Setup:** `@venn setup. Here is my URL: [PASTE_UNIVERSAL_URL_HERE]`
* **Reauthenticate:** `@venn authenticate`
* **Discovery:** `@venn Show me all my connected services`

## Core Activation Loop
When `@venn` is mentioned, or the user asks for data from a connected SaaS service (Gmail, Jira, Notion, etc.):

1. **Verify Environment:** Check if `VENN_UNIVERSAL_URL` is set. If not, follow the **Setup Flow**.
2. **The Discovery Loop:** Since Venn is a "Server of Servers," you must discover tools dynamically:
    - **Search:** Use `mcporter call venn.search_tools --args '{"query":"..."}'` for every new request.
    - **Describe:** Use `mcporter call venn.describe_tools` to validate JSON schemas before execution.
    - **Governance:** Check for `write_operation: "audit"`. If present, you MUST pause for user confirmation.

## Setup Request with Venn Universal URL & Bootstrap
If the user provides a URL in response to a setup request:
1. **Save & Sync:** Confirm you have saved the URL as an environment variable `VENN_UNIVERSAL_URL`
2. **Register:** Immediately run `~/.local/bin/mcporter-manual config add venn --url <URL> --auth oauth --deviceCodeGrant`.
3. **Authenticate:** Follow Venn Authentication.
4. **Verify Health:** Run `mcporter list` and confirm the `venn` status is "ok" before proceeding.

## Setup Request with Missing Venn Universal URL
If `VENN_UNIVERSAL_URL` is missing or the connection is broken:
1. **Request URL:** Prompt the user for their Venn Universal URL from Venn.ai.
2. **Register Server:** Once provided, run:
   `~/.local/bin/mcporter-manual config add venn --url "$VENN_UNIVERSAL_URL" --auth oauth --deviceCodeGrant`
3. **Initiate OAuth:** Check browser availability (see above).
   - **Browser available:** Run `mcporter auth venn` to launch the browser authorization.
   - **No browser:** Follow **Headless Authentication** below.
4. **Verify Health:** Run `mcporter list` and confirm the `venn` status is "ok" before proceeding.

## Venn Authentication

### Step 1 — Build mcporter-manual (once)
Check if the build already exists. If `~/.local/share/mcporter-manual/dist/cli.js` is missing, run:
```bash ~/.openclaw/workspace/skills/venn/scripts/install-mcporter-manual.sh"

### Step 2 — Authenticate
```bash
~/.local/bin/mcporter-manual auth venn --reset
```
This will:
1. Print: "To authorize, visit [[authorization_url]]"
2. Print: "Waiting for authorization..."

Tell the user: "Open this URL in a browser to complete authentication: [[authorization_url]]"

Once the authorization is complete the auth and refresh tokens are saved to `~/config/mcporter.json` and normal `mcporter` commands work immediately.

## Execution Protocols

### 1. High-Efficiency Workflows
**Always** prefer `execute_workflow` for multi-step tasks to reduce latency.
- **Context Guardrail:** Extract only necessary keys (e.g., `id`, `subject`, `summary`). Do not return full raw API payloads to the user.
- **Timeout Management:** Enterprise SaaS calls can be slow. If using a `run` tool, set a 30s timeout for Venn workflows.

### 2. Single Tool Calls via `venn.execute_tool`
For individual operations, use this syntax:
```bash
~/.local/bin/mcporter-manual call venn.execute_tool --args '{"server_id":"atlassian","tool_name":"atlassian_user_info","tool_args":{}}'
```

### 3. Discover which services are connected to Venn via `venn.help` tool
To list all services that user has connected to their Venn account, use this syntax:
```bash
~/.local/bin/mcporter-manual call venn.help --args '{"action":"LIST_SERVERS"}'
```
