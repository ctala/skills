# my_longbridge_mgnt_skill

## Purpose
Longbridge OpenAPI integration for automated stock management.

## Setup
1. Configure credentials via `openclaw secrets configure`.
2. Ensure `longbridge` is installed (`pip install -r requirements.txt`).

## Functions
- `trade`: Execute, Modify, Cancel orders.
- `market`: Real-time quotes.
- `account`: Asset & Position tracking.
- `push`: Real-time streaming handler.

---
_Warning: Do not hardcode credentials._
