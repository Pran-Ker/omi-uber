# Project Structure Overview

```
omi-uber/
├── main.py                    # FastAPI app with ALL endpoints (existing + new Omi ones)
├── uber_client.py             # [EXISTING] Handles Uber API calls and deep links
├── location_input.py          # [EXISTING] Location data structures
├── display.py                 # [EXISTING] HTML/terminal formatting
├── omi_integration.py         # [NEW] Core Omi voice processing logic
└── requirements.txt           # [UPDATED] Added anthropic SDK
```

---

## File-by-File Breakdown

### 1. **omi_integration.py** (NEW FILE - The Brain)

This is the core logic for voice-to-Uber conversion. Contains 4 main classes:

#### **Class: ConversationState**
- **Purpose**: Tracks ONE user's conversation state
- **Data it stores**:
  - `session_id`: Omi's session identifier
  - `uid`: User's Omi ID
  - `stage`: Where they are in conversation ("idle", "waiting_dropoff", "waiting_pickup", "confirming")
  - `pickup_location`: What they said for pickup (text)
  - `dropoff_location`: What they said for destination (text)
  - `collected_segments`: All the speech segments they've said
  - `triggered`: Boolean - did they say "book an uber"?

#### **Class: SessionManager**
- **Purpose**: Manages multiple users' conversations simultaneously
- **Main functions**:
  - `get_session(session_id, uid)` → Returns the user's current conversation state
  - `cleanup_old_sessions()` → Deletes conversations older than 1 hour

#### **Class: LocationParser**
- **Purpose**: Uses Claude AI to understand what the user said
- **Main function**:
  - `parse_uber_request(text, current_stage)` → Sends text to Claude API, gets back structured data

**Example Flow**:
```python
Input: "Book me an Uber to Mission Street"
↓
Claude analyzes it
↓
Output: {
  "is_uber_request": true,
  "pickup": "current location",
  "dropoff": "Mission Street",
  "confidence": "high"
}
```

#### **Class: OmiNotifier**
- **Purpose**: Sends messages back to the user's Omi device
- **Main function**:
  - `send_notification(uid, message)` → Calls Omi API to send notification

#### **Class: OmiUberIntegration** (THE MAIN ORCHESTRATOR)
- **Purpose**: Coordinates everything - the main entry point
- **Main function**:
  - `process_segment(session_id, uid, segments)` → Processes each voice segment from Omi

**The Flow Inside process_segment()**:
```
1. Get user's conversation state from SessionManager
2. Extract text from the audio segments
3. Check what stage they're at:

   IF stage = "idle":
     - Check if they said trigger phrase ("book an uber")
     - If YES:
       - Use LocationParser to extract pickup/dropoff
       - If we have dropoff → go to booking
       - If missing dropoff → ask "Where to?"

   IF stage = "waiting_dropoff":
     - Parse their response with LocationParser
     - Extract destination
     - Go to booking

   IF stage = "confirming":
     - Call _handle_booking()

4. _handle_booking():
   - Use UberClient to generate deep link
   - Get price estimates
   - Format notification with link
   - Send via OmiNotifier
   - Reset conversation state
```

---

### 2. **main.py** (MODIFIED - Add New Endpoints)

**Existing Endpoints** (keep as-is):
- `GET /` → Web UI form
- `GET /ride` → Show ride info in browser
- `GET /api/ride-info` → JSON API for ride data
- `GET /health` → Health check

**New Endpoints to ADD**:

#### `POST /omi/webhook`
- **What it does**: Receives voice transcription from Omi
- **What it receives**:
```json
{
  "session_id": "abc123",
  "uid": "user456",
  "segments": [
    {"text": "Book me an Uber", "start": 0, "end": 2.5},
    {"text": "to Mission Street", "start": 2.5, "end": 4.0}
  ]
}
```
- **What it does with the data**:
  1. Creates `OmiUberIntegration` instance
  2. Calls `integration.process_segment(session_id, uid, segments)`
  3. Returns `{"status": "ok"}`

#### `GET /omi/setup-status`
- **What it does**: Tells Omi that setup is complete
- **Returns**: `{"is_setup_completed": true}`

#### `GET /omi/status`
- **What it does**: Health check for Omi integration
- **Returns**: Number of active conversations

---

### 3. **uber_client.py** (NO CHANGES)

**Existing functions** (we reuse these):
- `get_price_estimates()` → Calls Uber API for pricing
- `get_time_estimates()` → Calls Uber API for pickup time
- `generate_deep_link()` → Creates uber:// URL
- `generate_mobile_web_link()` → Creates m.uber.com URL

---

### 4. **location_input.py** (NO CHANGES - But Future Enhancement)

**Current**: Hardcoded SF locations
**Future**: We'll add a geocoding function here to convert "Mission Street" → coordinates

---

### 5. **display.py** (NO CHANGES)

Only used for web UI, not for Omi integration

---

## Complete User Flow Example

**User says**: "Book an Uber to the airport"

```
1. Omi device → sends to your server:
   POST /omi/webhook
   {
     "session_id": "session123",
     "uid": "user456",
     "segments": [{"text": "Book an Uber to the airport"}]
   }

2. main.py receives webhook → calls:
   OmiUberIntegration.process_segment()

3. OmiUberIntegration:
   - Checks session (stage = "idle")
   - Detects trigger "book an uber"
   - Calls LocationParser.parse_uber_request()

4. LocationParser sends to Claude:
   "Parse this: 'Book an Uber to the airport'"

5. Claude returns:
   {
     "is_uber_request": true,
     "pickup": "current location",
     "dropoff": "airport"
   }

6. OmiUberIntegration sees we have both locations:
   - stage = "confirming"
   - Calls _handle_booking()

7. _handle_booking():
   - Gets coordinates (currently hardcoded SF locations)
   - Calls UberClient.generate_deep_link()
   - Calls UberClient.get_price_estimates()
   - Formats message: "🚗 Uber to airport\n💰 ~$35\n⏱️ ~15 min\nTap: uber://..."
   - Calls OmiNotifier.send_notification()

8. User's Omi device receives notification with Uber link!
```

---

## Environment Variables Needed

```env
# Existing
APP_HOST=0.0.0.0
APP_PORT=8000
UBER_SERVER_TOKEN=<your_uber_token>  # For price estimates (optional)

# New - Need to add
ANTHROPIC_API_KEY=<your_claude_key>   # For natural language parsing
OMI_APP_ID=<from_omi_dashboard>       # After you create the app
OMI_API_KEY=<from_omi_dashboard>      # After you create the app
```

---

## Multi-Step Conversation Example

**Scenario**: User only says "Book an Uber"

```
User: "Book an Uber"
  ↓
Integration: Missing destination → stage = "waiting_dropoff"
  ↓
Omi notification: "Where would you like to go?"
  ↓
User: "to Mission Street"
  ↓
Integration: Parses "Mission Street" as dropoff → stage = "confirming"
  ↓
_handle_booking() → sends deep link
  ↓
Omi notification: "🚗 Uber to Mission Street... [link]"
```

---

## Summary of Key Functions

| Function | Location | Purpose |
|----------|----------|---------|
| `process_segment()` | omi_integration.py | Main entry point - processes all voice input |
| `parse_uber_request()` | omi_integration.py | Uses Claude to understand intent |
| `send_notification()` | omi_integration.py | Sends messages to Omi device |
| `_handle_booking()` | omi_integration.py | Final step - generates link & sends |
| `generate_deep_link()` | uber_client.py | Creates Uber app link |
| `get_price_estimates()` | uber_client.py | Gets Uber pricing |

---

## Next Steps

1. Create `omi_integration.py` with all the classes
2. Add new endpoints to `main.py`
3. Update `.env` with API keys
4. Test with Omi webhook
5. Deploy to public URL (ngrok or Railway)
6. Configure in Omi dashboard
