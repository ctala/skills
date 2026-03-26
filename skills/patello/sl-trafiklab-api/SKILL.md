---
name: sl-trafiklab-api
description: "Manage SL (Stockholm public transport) user preferences and fetch strictly relevant deviation information."
metadata: {"openclaw": {"requires": {"bins": ["curl", "jq"]}}}
---

# SL Trafiklab API

This skill manages the user's public transport preferences (SL) and retrieves disruption information. Execute all API calls via your built-in bash execution capability. The most critical task when handling routes is to filter out noise. The user should not be informed about canceled or moved stops that are not on their specific route, unless the entire line is delayed or canceled.

## State Storage
Preferences must be maintained in `{workDir}/sl_preferences.json`. The configuration is divided into two distinct modes: `general_tracking` (broad monitoring of stations/lines) and `specific_routes` (highly targeted journeys requiring both names and Site IDs).

Format:
```json
{
  "general_tracking": {
    "sites": [
      { "id": 9001, "name": "T-Centralen" },
      { "id": 9117, "name": "Odenplan" }
    ],
    "lines": [18, 4],
    "transport_modes": ["METRO", "BUS", "TRAIN"]
  },
  "specific_routes": [
    {
      "name": "Commute to University",
      "legs": [
        { 
          "lines": [4, 66], 
          "from": { "id": 9192, "name": "Gullmarsplan" }, 
          "to": { "id": 9117, "name": "Odenplan" } 
        },
        { 
          "lines": [43], 
          "from": { "id": 9117, "name": "Odenplan" }, 
          "to": { "id": 9509, "name": "Solna station" } 
        }
      ]
    }
  ]
}
```
*(Note: Allowed `transport_modes` are strictly limited to: `BUS`, `METRO`, `TRAM`, `TRAIN`, `SHIP`, `FERRY`, `TAXI`)*

*Initialize this file with empty arrays if it does not exist.*

---

## Action: `search_sl_sites`
**Purpose:** Finds the numeric Site ID for a given stop name. The Deviations API requires numeric IDs when searching for specific locations.

**CRITICAL WARNING:** The `/sites` endpoint returns a massive JSON payload containing every stop in Stockholm. NEVER attempt to read the entire response directly into the context window. This will overload the session. You MUST pipe the response through `jq` to filter it locally.

**Inputs:** `<SEARCH_TERM>` (string)

**Execution:**
```bash
read -r SEARCH_TERM << 'EOF'
<SEARCH_TERM>
EOF

curl -s "[https://transport.integration.sl.se/v1/sites](https://transport.integration.sl.se/v1/sites)" | \
jq -c --arg st "$SEARCH_TERM" '.[] | select(.name | test($st; "i")) | {id, name}' | head -n 5
```

**Output Handling:** Present the matching IDs from the `jq` filtering to the user. If adding to `specific_routes`, ensure both the ID and the Name are captured for the storage format.

---

## Action: `manage_preferences`
**Purpose:** Saves updates to the user's lines, stations, and specific routes.

**Inputs:** `<UPDATED_JSON>` (Valid JSON string containing the merged arrays without duplicates, strictly following the two-mode structure with ID/Name pairs).

**Execution:**
```bash
read -r NEW_PREFS << 'EOF'
<UPDATED_JSON>
EOF

echo "$NEW_PREFS" > sl_preferences.json
```

---

## Action: `fetch_deviations`
**Purpose:** Fetches and performs strict filtering of disruption information based on the user's preferences.

**Inputs:**
- `<FUTURE_FLAG>`: `false` for active disruptions, `true` for planned maintenance.
- `<QUERY_PARAMS>`: Formatted string based on the unique lines and sites found in both `general_tracking` and `specific_routes`. Extract all unique IDs and lines to build the parameters (e.g., `site=9001&line=4&line=18`).

**Execution:**
```bash
read -r QUERY_PARAMS << 'EOF'
<QUERY_PARAMS>
EOF

curl -s "[https://deviations.integration.sl.se/v1/messages?future=](https://deviations.integration.sl.se/v1/messages?future=)<FUTURE_FLAG>&${QUERY_PARAMS}"
```

**Assessment Logic & Filtering (CRITICAL):**
Analyze the JSON array and extract `message_variants[].header`, `message_variants[].details`, and `scope.stop_areas[]`. You must then use your analytical capabilities to filter out irrelevant information based on the user's `specific_routes`:
- **Ignore (Silence):** If the disruption text only describes problems at a localized stop (e.g., "stop moved 30 meters", "withdrawn stop", "does not stop at [Stop X]") AND this stop ID does not match any of the boarding, alighting, or transfer Site IDs for that specific line in their saved `specific_routes`.
- **Report:** If the disruption affects the entire line generally (e.g., "canceled departures", "diverted traffic affecting total travel time", "vehicle fault", "major delays") OR if it explicitly affects the specific Site IDs the user intends to use. Disruptions matching items in `general_tracking` should always be reported. Note: Since `lines` in `specific_routes` is a list, check for any disruption matching ANY of the line numbers in the list.

---

## Autonomous Directives
During autonomous execution (e.g., background heartbeat or cron job):
1. Run `fetch_deviations` using the extracted parameters from `sl_preferences.json`.
2. Apply the strict assessment logic to weed out local stop disruptions that do not affect the user's actual route Site IDs.
3. Compare the returned and approved `deviation_case_id`s against your context memory.
4. Only send a notification if a new, relevant disruption is detected. Remain silent if the list is empty after filtering or only contains previously reported disruptions.
5. Adhere to Trafiklab's limit of maximum 1 request per minute.