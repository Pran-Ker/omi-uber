# Project Structure

## Core Flow

1. **User Input** - Location pickup and destination (voice or text)
2. **Coordinate Calculation** - Google Maps API converts addresses to exact coordinates
3. **Cost Estimate** - Python calculation (base price + cost per mile)
4. **Deep Link Generation** - Creates Uber/Lyft app link with pre-filled locations
5. **User Confirmation** - User opens link and books ride

## Input Parameters

- Pickup location
- Destination location
- ~~Scheduled time~~ (future)
- ~~Ride type~~ (future)

## API Limitations

- Uber Developer API only supports deep links (no direct booking)
- Workaround: Agent automation to select options after deep link opens

## Multi-Step Conversation

The system asks clarifying questions:
- "Where are you going?"
- "Where should we pick you up?"
- "When do you need the ride?" (future)
- "What type of ride?" (future)

## Omi Integration

- Voice transcription via Omi app
- Processes natural language commands
- Multi-turn conversations for missing details 