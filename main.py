from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import os
import sys
from dotenv import load_dotenv
from typing import Optional

# Force unbuffered output for instant logs
sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, 'reconfigure') else None

from utils.location_input import LocationInput, Location
from utils.uber_client import UberClient
from utils.display import UberDisplay

load_dotenv()

app = FastAPI(
    title="OMI Uber Integration",
    description="Generate Uber deep links with price and time estimates",
    version="1.0.0"
)

# Initialize services
uber_client = UberClient()


def get_input_form_html():
    """Generate HTML form for location input."""
    start = LocationInput.START_LOCATION
    dest = LocationInput.DESTINATION_LOCATION

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Uber Ride - Omi</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
                color: #ffffff;
                padding: 20px;
                min-height: 100vh;
            }}

            .container {{
                max-width: 600px;
                margin: 0 auto;
            }}

            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}

            .header h1 {{
                font-size: 32px;
                margin-bottom: 10px;
            }}

            .header .icon {{
                font-size: 48px;
                margin-bottom: 10px;
            }}

            .card {{
                background: #1e1e1e;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                border: 1px solid #333;
            }}

            .form-group {{
                margin-bottom: 20px;
            }}

            label {{
                display: block;
                font-size: 14px;
                color: #aaa;
                margin-bottom: 8px;
                font-weight: 600;
            }}

            input[type="text"],
            input[type="number"] {{
                width: 100%;
                padding: 12px;
                background: #2a2a2a;
                border: 1px solid #444;
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
            }}

            input[type="text"]:focus,
            input[type="number"]:focus {{
                outline: none;
                border-color: #ffffff;
            }}

            .btn {{
                display: block;
                width: 100%;
                padding: 16px;
                background: #ffffff;
                color: #000000;
                text-decoration: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                text-align: center;
                margin-bottom: 10px;
                border: 2px solid #ffffff;
                transition: all 0.2s;
                cursor: pointer;
            }}

            .btn:hover {{
                background: #000000;
                color: #ffffff;
            }}

            .coords-row {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }}

            .note {{
                font-size: 12px;
                color: #666;
                margin-top: 5px;
            }}

            .footer {{
                text-align: center;
                margin-top: 40px;
                color: #666;
                font-size: 14px;
            }}

            @media (max-width: 480px) {{
                body {{
                    padding: 12px;
                }}

                .header h1 {{
                    font-size: 24px;
                }}

                .card {{
                    padding: 15px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="icon">🚗</div>
                <h1>Uber Ride Booking</h1>
                <p>Enter locations or use defaults</p>
            </div>

            <form id="locationForm">
                <div class="card">
                    <h2 style="margin-bottom: 20px; font-size: 18px;">📍 Pickup Location</h2>

                    <div class="form-group">
                        <label>Location Name</label>
                        <input type="text" id="start_name" name="start_name" value="{start.name}" placeholder="e.g., Grant Avenue">
                    </div>

                    <div class="form-group">
                        <label>Address</label>
                        <input type="text" id="start_address" name="start_address" value="{start.address}" placeholder="e.g., 1443 Grant Ave, San Francisco, CA">
                    </div>

                    <div class="coords-row">
                        <div class="form-group">
                            <label>Latitude</label>
                            <input type="number" step="0.0001" id="start_lat" name="start_lat" value="{start.latitude}" placeholder="37.7989">
                        </div>
                        <div class="form-group">
                            <label>Longitude</label>
                            <input type="number" step="0.0001" id="start_lon" name="start_lon" value="{start.longitude}" placeholder="-122.4074">
                        </div>
                    </div>
                </div>

                <div class="card">
                    <h2 style="margin-bottom: 20px; font-size: 18px;">📍 Destination</h2>

                    <div class="form-group">
                        <label>Location Name</label>
                        <input type="text" id="dest_name" name="dest_name" value="{dest.name}" placeholder="e.g., Mission Street">
                    </div>

                    <div class="form-group">
                        <label>Address</label>
                        <input type="text" id="dest_address" name="dest_address" value="{dest.address}" placeholder="e.g., 1885 Mission St, San Francisco, CA">
                    </div>

                    <div class="coords-row">
                        <div class="form-group">
                            <label>Latitude</label>
                            <input type="number" step="0.0001" id="dest_lat" name="dest_lat" value="{dest.latitude}" placeholder="37.7699">
                        </div>
                        <div class="form-group">
                            <label>Longitude</label>
                            <input type="number" step="0.0001" id="dest_lon" name="dest_lon" value="{dest.longitude}" placeholder="-122.4192">
                        </div>
                    </div>
                </div>

                <button type="submit" class="btn">Get Uber Ride Info</button>
            </form>

            <div class="footer">
                <p>Powered by <strong>Omi</strong></p>
            </div>
        </div>

        <script>
            document.getElementById('locationForm').addEventListener('submit', function(e) {{
                e.preventDefault();

                const params = new URLSearchParams({{
                    start_name: document.getElementById('start_name').value,
                    start_address: document.getElementById('start_address').value,
                    start_lat: document.getElementById('start_lat').value,
                    start_lon: document.getElementById('start_lon').value,
                    dest_name: document.getElementById('dest_name').value,
                    dest_address: document.getElementById('dest_address').value,
                    dest_lat: document.getElementById('dest_lat').value,
                    dest_lon: document.getElementById('dest_lon').value
                }});

                window.location.href = '/ride?' + params.toString();
            }});
        </script>
    </body>
    </html>
    """


@app.get("/")
async def root():
    """Root endpoint - shows input form."""
    return HTMLResponse(content=get_input_form_html())


@app.get("/ride")
async def get_ride(
    start_name: str = Query(None),
    start_address: str = Query(None),
    start_lat: float = Query(None),
    start_lon: float = Query(None),
    dest_name: str = Query(None),
    dest_address: str = Query(None),
    dest_lat: float = Query(None),
    dest_lon: float = Query(None)
):
    """
    Display ride information with user-provided or default locations.
    """
    print("🚀 Generating Uber ride information...", flush=True)

    # Use provided values or defaults
    if not all([start_lat, start_lon, dest_lat, dest_lon]):
        start, destination = LocationInput.get_trip_locations()
    else:
        start = Location(
            name=start_name or "Pickup",
            address=start_address or "Unknown",
            latitude=start_lat,
            longitude=start_lon
        )
        destination = Location(
            name=dest_name or "Destination",
            address=dest_address or "Unknown",
            latitude=dest_lat,
            longitude=dest_lon
        )
        print(f"📍 Start: {start.name} ({start.address})", flush=True)
        print(f"📍 Destination: {destination.name} ({destination.address})", flush=True)

    # Fetch price estimates from Uber API
    print("💰 Fetching price estimates...", flush=True)
    price_estimates = uber_client.get_price_estimates(
        start_latitude=start.latitude,
        start_longitude=start.longitude,
        end_latitude=destination.latitude,
        end_longitude=destination.longitude
    )

    # Fetch time estimates from Uber API
    print("⏱️  Fetching time estimates...", flush=True)
    time_estimates = uber_client.get_time_estimates(
        start_latitude=start.latitude,
        start_longitude=start.longitude
    )

    # Generate deep links with user-selected locations
    deep_link = UberClient.generate_deep_link(
        pickup_latitude=start.latitude,
        pickup_longitude=start.longitude,
        dropoff_latitude=destination.latitude,
        dropoff_longitude=destination.longitude,
        pickup_nickname=start.name,
        dropoff_nickname=destination.name,
        pickup_address=start.address,
        dropoff_address=destination.address
    )

    web_link = UberClient.generate_mobile_web_link(
        pickup_latitude=start.latitude,
        pickup_longitude=start.longitude,
        dropoff_latitude=destination.latitude,
        dropoff_longitude=destination.longitude
    )

    # Print terminal output
    terminal_output = UberDisplay.generate_terminal_output(
        start=start,
        destination=destination,
        price_estimates=price_estimates,
        time_estimates=time_estimates,
        deep_link=deep_link,
        web_link=web_link
    )
    print(terminal_output, flush=True)

    # Return HTML
    html_output = UberDisplay.generate_html_output(
        start=start,
        destination=destination,
        price_estimates=price_estimates,
        time_estimates=time_estimates,
        deep_link=deep_link,
        web_link=web_link
    )

    return HTMLResponse(content=html_output)


@app.get("/api/ride-info")
async def get_ride_info(
    start_lat: Optional[float] = Query(None),
    start_lon: Optional[float] = Query(None),
    dest_lat: Optional[float] = Query(None),
    dest_lon: Optional[float] = Query(None),
    start_name: Optional[str] = Query(None),
    dest_name: Optional[str] = Query(None)
):
    """
    API endpoint - returns JSON with ride information.
    Accepts optional location parameters.
    """
    print("📡 API request for ride info...", flush=True)

    # Use provided values or defaults
    if not all([start_lat, start_lon, dest_lat, dest_lon]):
        start, destination = LocationInput.get_trip_locations()
    else:
        start = Location(
            name=start_name or "Pickup",
            address="Custom location",
            latitude=start_lat,
            longitude=start_lon
        )
        destination = Location(
            name=dest_name or "Destination",
            address="Custom location",
            latitude=dest_lat,
            longitude=dest_lon
        )
        print(f"📍 Custom locations - Start: ({start_lat}, {start_lon}), Dest: ({dest_lat}, {dest_lon})", flush=True)

    # Fetch estimates
    price_estimates = uber_client.get_price_estimates(
        start_latitude=start.latitude,
        start_longitude=start.longitude,
        end_latitude=destination.latitude,
        end_longitude=destination.longitude
    )

    time_estimates = uber_client.get_time_estimates(
        start_latitude=start.latitude,
        start_longitude=start.longitude
    )

    # Generate links
    deep_link = UberClient.generate_deep_link(
        pickup_latitude=start.latitude,
        pickup_longitude=start.longitude,
        dropoff_latitude=destination.latitude,
        dropoff_longitude=destination.longitude,
        pickup_nickname=start.name,
        dropoff_nickname=destination.name,
        pickup_address=start.address,
        dropoff_address=destination.address
    )

    web_link = UberClient.generate_mobile_web_link(
        pickup_latitude=start.latitude,
        pickup_longitude=start.longitude,
        dropoff_latitude=destination.latitude,
        dropoff_longitude=destination.longitude
    )

    return {
        "start_location": {
            "name": start.name,
            "address": start.address,
            "latitude": start.latitude,
            "longitude": start.longitude
        },
        "destination": {
            "name": destination.name,
            "address": destination.address,
            "latitude": destination.latitude,
            "longitude": destination.longitude
        },
        "price_estimates": price_estimates,
        "time_estimates": time_estimates,
        "deep_link": deep_link,
        "web_link": web_link
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "omi-uber"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("APP_PORT", 8000))
    host = os.getenv("APP_HOST", "0.0.0.0")

    print("🚗 OMI Uber Integration", flush=True)
    print("=" * 50, flush=True)
    print(f"🚀 Starting on {host}:{port}", flush=True)
    print("=" * 50, flush=True)

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )
