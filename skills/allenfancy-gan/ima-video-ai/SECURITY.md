# Security Disclosure: ima-video-ai

## Purpose

This document explains endpoint usage, credential flow, and local data behavior for `ima-video-ai`.

## Network Endpoints

| Domain | Used For | Trigger |
|---|---|---|
| `api.imastudio.com` | Product list, task create, task detail polling | All requests |
| `imapi.liveme.com` | Image upload token + binary upload | Only for image tasks with local/non-HTTPS image inputs |

For image tasks that already use HTTPS image URLs, the script does not call the secondary upload domain.

## Credential Flow

| Credential | Where Sent | Why |
|---|---|---|
| `IMA_API_KEY` | `api.imastudio.com` | Open API auth (`Authorization: Bearer ...`) |
| `IMA_API_KEY` | `imapi.liveme.com` | Upload-token auth for local/non-HTTPS image uploads |

The script validates `task_type` and image count before task creation to reduce accidental credential/domain usage.

## Upload Signing Constants

`APP_ID` and `APP_KEY` in script source are request-signing constants for upload APIs (not repository secrets).

## Cross-Skill Reads

This skill is self-contained for core API execution.
If `ima-knowledge-ai` is installed, the agent may optionally read:

- `~/.openclaw/skills/ima-knowledge-ai/references/*`

for mode-selection and visual-consistency guidance only.

## Local Data

| Path | Content | Retention |
|---|---|---|
| `~/.openclaw/memory/ima_prefs.json` | Per-user model preference cache | Until manually removed |
| `~/.openclaw/logs/ima_skills/` | Operational logs | Auto-cleaned by script after 7 days |

No API key is written into repository files.
