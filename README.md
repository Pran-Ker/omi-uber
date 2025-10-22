# 🚗 Uber Deep Link Generator for OMI

Generate Uber deep links with price and time estimates for seamless ride booking through your OMI device.

## ✨ Features

- **🔗 Deep Link Generation** - Create direct Uber app/web links
- **💰 Price Estimates** - Get fare estimates for different ride types (with API token)
- **⏱️ Pickup Time Estimates** - See how long until your ride arrives (with API token)
- **📍 Hardcoded SF Locations** - Pre-configured start and destination
- **📱 Mobile-First UI** - Beautiful responsive web interface
- **🔄 Stateless** - No user authentication or data storage required
- **⚡ Fast** - Works instantly without Uber OAuth

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- (Optional) Uber API Server Token for price/time estimates

### Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env if you have an Uber API token (optional)
```

### Run the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
python3 main.py
```

Visit:
- **Web Interface**: http://localhost:8000
- **API Endpoint**: http://localhost:8000/api/ride-info

## 📍 Hardcoded Locations

The application currently uses these San Francisco locations:

- **Start**: 1443 Grant Ave, San Francisco, CA (37.7989, -122.4074)
- **Destination**: 1885 Mission St, San Francisco, CA (37.7699, -122.4192)

To change locations, edit `location_input.py:14-27`

## 🎯 Project Structure

The project is segregated into three parts as requested:

### 1. Input Module (`location_input.py`)
- Handles location input with hardcoded coordinates
- Returns start and destination locations
- Easy to extend for dynamic user input later

### 2. Uber API Client (`uber_client.py`)
- Calls Uber API for price estimates
- Calls Uber API for time estimates
- Generates deep links (works without API token)
- Generates mobile web links as fallback

### 3. Display Module (`display.py`)
- Formats data for terminal output
- Generates HTML for web display
- Shows ETA, cost, and booking links

### Main Application (`main.py`)
- FastAPI web server
- Ties together all three modules
- Provides web UI and JSON API endpoints

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface with ride information |
| `/api/ride-info` | GET | JSON API with all ride data |
| `/health` | GET | Health check endpoint |

## 📱 Web Interface

The web interface displays:
- Start and destination locations
- Pickup time estimates (if API token configured)
- Price estimates for different ride types (if API token configured)
- "Open in Uber App" button (deep link)
- "Open in Browser" button (mobile web link)

## 🔑 Uber API Token (Optional)

To get price and time estimates, you need an Uber Server Token:

1. Go to [Uber Developer Portal](https://developer.uber.com/)
2. Create an app
3. Get your Server Token
4. Add to `.env`:
   ```
   UBER_SERVER_TOKEN=your_token_here
   ```

**Note**: Deep links work WITHOUT a token! The token is only needed for price/time estimates.

## 📊 Terminal Output

The application prints ride information to the terminal:

```
============================================================
🚗 UBER RIDE INFORMATION
============================================================

📍 FROM: Grant Avenue
   1443 Grant Ave, San Francisco, CA
   (37.7989, -122.4074)

📍 TO: Mission Street
   1885 Mission St, San Francisco, CA
   (37.7699, -122.4192)

⏱️  PICKUP TIME ESTIMATES:
   • UberX: 3 min pickup
   • UberXL: 5 min pickup

💰 PRICE ESTIMATES:
   • UberX: $12-15 (~8 min, 2.1 mi)
   • UberXL: $18-22 (~8 min, 2.1 mi)

🔗 DEEP LINKS:
   App Link: uber://?pickup[latitude]=...
   Web Link: https://m.uber.com/ul/?pickup[latitude]=...

============================================================
```

## 🔧 Configuration

Edit `.env` file:

```env
# Optional: Uber API Server Token (for price/time estimates)
UBER_SERVER_TOKEN=your_uber_server_token

# Server settings
APP_HOST=0.0.0.0
APP_PORT=8000
```

## 🚀 Deployment

### Local Development
```bash
python3 main.py
```

### Railway/Cloud Deployment
1. Push to GitHub
2. Connect to Railway
3. Set environment variables
4. Deploy!

Environment variables for production:
```
UBER_SERVER_TOKEN=your_token (optional)
APP_HOST=0.0.0.0
APP_PORT=8000
```

## 🛠️ Next Steps (Future Enhancements)

Based on your requirements, here are planned enhancements:

1. **Dynamic User Input**
   - Voice command integration with OMI
   - Web form for manual location entry
   - GPS coordinate input from device

2. **Geocoding Service**
   - Convert addresses to coordinates
   - Support natural language locations
   - Autocomplete for addresses

3. **Display Integration**
   - Integrate with omi.app display
   - Mobile app integration
   - Push notifications

4. **Enhanced Features**
   - Multiple destination support
   - Ride history (with storage)
   - Favorite locations
   - Real-time ride tracking

## 📖 Usage Examples

### Web Browser
1. Navigate to http://localhost:8000
2. View ride information
3. Click "Open in Uber App" to book

### API Call
```bash
curl http://localhost:8000/api/ride-info | python3 -m json.tool
```

Response:
```json
{
    "start_location": {
        "name": "Grant Avenue",
        "address": "1443 Grant Ave, San Francisco, CA",
        "latitude": 37.7989,
        "longitude": -122.4074
    },
    "destination": {
        "name": "Mission Street",
        "address": "1885 Mission St, San Francisco, CA",
        "latitude": 37.7699,
        "longitude": -122.4192
    },
    "price_estimates": [...],
    "time_estimates": [...],
    "deep_link": "uber://?...",
    "web_link": "https://m.uber.com/ul/?..."
}
```

## 🔐 Security Notes

- No user authentication required
- No data storage (stateless)
- API token kept in environment variables
- Deep links work without any credentials

## 🐛 Troubleshooting

### "UBER_SERVER_TOKEN not set - skipping API call"
This is normal if you don't have an Uber API token. Deep links will still work!

### Deep link doesn't open Uber app
1. Make sure Uber app is installed
2. Try the "Open in Browser" link instead
3. Check that location permissions are enabled

### Port already in use
Change `APP_PORT` in `.env` to a different port (e.g., 8001)

## 📝 File Structure

```
omi-uber/
├── main.py                 # FastAPI application
├── location_input.py       # Input module (hardcoded locations)
├── uber_client.py          # Uber API client
├── display.py              # Display formatting
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── .env                   # Your configuration (not in git)
└── README.md              # This file
```

## 🎉 Credits

Built for [OMI](https://omi.me) - The AI wearable that extends your memory and capabilities.

## 📄 License

MIT License - see LICENSE file for details.

---

**Made with ❤️ for seamless Uber booking with OMI**
