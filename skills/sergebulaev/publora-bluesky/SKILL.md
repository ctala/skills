---
name: publora-bluesky
description: >
  Post or schedule content to Bluesky using the Publora API. Use this skill
  when the user wants to publish or schedule Bluesky posts via Publora.
---

# Publora — Bluesky

Bluesky (AT Protocol) platform skill for the Publora API. For auth, core scheduling, media upload, and workspace/webhook docs, see the `publora` core skill.

**Base URL:** `https://api.publora.com/api/v1`  
**Header:** `x-publora-key: sk_YOUR_KEY`  
**Platform ID format:** `bluesky-{did}`

Where `{did}` is your Bluesky Decentralized Identifier (DID), assigned on connection.

## Requirements

- A Bluesky account connected via **username + app password** (not your main password)
- Generate an app password: Bluesky Settings → App Passwords
- Connected through the Publora dashboard

## Platform Limits (API)

| Property | Limit | Notes |
|----------|-------|-------|
| Text | **300 characters** | Links do NOT count toward limit |
| Images | Up to **4** × **1 MB** | JPEG, PNG, WebP (max 2000×2000 px) |
| Video | **3 min** / **100 MB** | MP4; email verification required |
| Video (short) | <60s → 50 MB | Size tiers apply |
| Text only | ✅ Yes | — |
| Daily video limit | 25 videos / 10 GB | — |
| Rate limit | 3,000 req/5 min | — |

**Common errors:**
- `429 Too Many Requests` — rate limit exceeded, wait and retry
- Video `JOB_STATE_FAILED` — check format (MP4) and size tier

## Post a Skeet (text post)

```javascript
await fetch('https://api.publora.com/api/v1/create-post', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' },
  body: JSON.stringify({
    content: 'Building in public on Bluesky today! Links, hashtags, and mentions all auto-detected. #buildinpublic',
    platforms: ['bluesky-did:plc:abc123']
  })
});
```

Publora automatically detects hashtags, URLs, and @mentions and creates proper AT Protocol facets.

## Schedule a Post

```javascript
body: JSON.stringify({
  content: 'Your Bluesky post here',
  platforms: ['bluesky-did:plc:abc123'],
  scheduledTime: '2026-03-20T11:00:00.000Z'
})
```

## Post with Image

> ⚠️ Bluesky has a strict **1 MB limit per image**. Compress to 80–85% JPEG quality.

```python
import requests

HEADERS = { 'Content-Type': 'application/json', 'x-publora-key': 'sk_YOUR_KEY' }

# Step 1: Create post
post = requests.post('https://api.publora.com/api/v1/create-post', headers=HEADERS, json={
    'content': 'Check out this photo! 📸',
    'platforms': ['bluesky-did:plc:abc123']
}).json()

# Step 2: Get upload URL (make sure image is <1 MB and JPEG/PNG/WebP)
upload = requests.post('https://api.publora.com/api/v1/get-upload-url', headers=HEADERS, json={
    'postGroupId': post['postGroupId'],
    'fileName': 'photo.jpg',
    'contentType': 'image/jpeg',
    'type': 'image'
}).json()

# Step 3: Upload
with open('photo_compressed.jpg', 'rb') as f:
    requests.put(upload['uploadUrl'], headers={'Content-Type': 'image/jpeg'}, data=f)
```

## Platform Quirks

- **Links don't count** toward the 300-char limit — great for posts with URLs
- **Auto-facets**: Publora automatically detects #hashtags, @mentions, and URLs and creates proper Bluesky facets
- **Image size is strict**: 1 MB hard limit per image. Always compress before upload.
- **Image dimensions**: Max 2000×2000 pixels
- **App password required**: Never use your main Bluesky password; create a dedicated app password
- **Email verification**: Required before you can upload videos (one-time step in Bluesky settings)
- **DID format**: Platform ID uses the full DID, e.g. `bluesky-did:plc:abc123xyz`
