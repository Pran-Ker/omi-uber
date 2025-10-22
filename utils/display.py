"""
Display module for showing Uber ride information.
"""
from typing import List, Dict, Optional
from utils.location_input import Location


class UberDisplay:
    """Handles display formatting for Uber ride information."""

    @staticmethod
    def format_price(estimate: Dict) -> str:
        """Format price estimate for display."""
        display_name = estimate.get("localized_display_name", "Unknown")
        estimate_str = estimate.get("estimate", "N/A")
        duration = estimate.get("duration", 0)
        distance = estimate.get("distance", 0)

        duration_min = duration // 60
        distance_miles = round(distance, 1)

        return f"{display_name}: {estimate_str} (~{duration_min} min, {distance_miles} mi)"

    @staticmethod
    def format_time(estimate: Dict) -> str:
        """Format time estimate for display."""
        display_name = estimate.get("localized_display_name", "Unknown")
        eta_seconds = estimate.get("estimate", 0)
        eta_minutes = eta_seconds // 60

        return f"{display_name}: {eta_minutes} min pickup"

    @staticmethod
    def generate_terminal_output(
        start: Location,
        destination: Location,
        price_estimates: Optional[List[Dict]],
        time_estimates: Optional[List[Dict]],
        deep_link: str,
        web_link: str
    ) -> str:
        """
        Generate formatted terminal output.

        Returns: Formatted string for terminal display.
        """
        lines = []
        lines.append("=" * 60)
        lines.append("🚗 UBER RIDE INFORMATION")
        lines.append("=" * 60)
        lines.append("")
        lines.append(f"📍 FROM: {start.name}")
        lines.append(f"   {start.address}")
        lines.append(f"   ({start.latitude}, {start.longitude})")
        lines.append("")
        lines.append(f"📍 TO: {destination.name}")
        lines.append(f"   {destination.address}")
        lines.append(f"   ({destination.latitude}, {destination.longitude})")
        lines.append("")

        if time_estimates:
            lines.append("⏱️  PICKUP TIME ESTIMATES:")
            for est in time_estimates[:3]:
                lines.append(f"   • {UberDisplay.format_time(est)}")
            lines.append("")

        if price_estimates:
            lines.append("💰 PRICE ESTIMATES:")
            for est in price_estimates:
                lines.append(f"   • {UberDisplay.format_price(est)}")
            lines.append("")

        lines.append("🔗 DEEP LINKS:")
        lines.append(f"   App Link: {deep_link}")
        lines.append(f"   Web Link: {web_link}")
        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)

    @staticmethod
    def generate_html_output(
        start: Location,
        destination: Location,
        price_estimates: Optional[List[Dict]],
        time_estimates: Optional[List[Dict]],
        deep_link: str,
        web_link: str
    ) -> str:
        """
        Generate HTML output for web display.

        Returns: HTML string.
        """
        # Build price estimates HTML
        price_html = ""
        if price_estimates:
            for est in price_estimates:
                display_name = est.get("localized_display_name", "Unknown")
                estimate_str = est.get("estimate", "N/A")
                duration = est.get("duration", 0)
                distance = est.get("distance", 0)
                duration_min = duration // 60
                distance_miles = round(distance, 1)

                price_html += f"""
                <div class="estimate-card">
                    <div class="ride-type">{display_name}</div>
                    <div class="price">{estimate_str}</div>
                    <div class="details">{duration_min} min • {distance_miles} mi</div>
                </div>
                """
        else:
            price_html = '<p class="no-data">Price estimates not available</p>'

        # Build time estimates HTML
        time_html = ""
        if time_estimates:
            for est in time_estimates[:3]:
                display_name = est.get("localized_display_name", "Unknown")
                eta_seconds = est.get("estimate", 0)
                eta_minutes = eta_seconds // 60

                time_html += f"""
                <div class="time-estimate">
                    <span class="ride-type">{display_name}</span>
                    <span class="eta">{eta_minutes} min</span>
                </div>
                """
        else:
            time_html = '<p class="no-data">Pickup time estimates not available</p>'

        html = f"""
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

                .location {{
                    margin-bottom: 15px;
                }}

                .location-label {{
                    font-size: 12px;
                    color: #888;
                    text-transform: uppercase;
                    margin-bottom: 5px;
                }}

                .location-name {{
                    font-size: 18px;
                    font-weight: 600;
                    margin-bottom: 3px;
                }}

                .location-address {{
                    font-size: 14px;
                    color: #aaa;
                }}

                .section-title {{
                    font-size: 16px;
                    font-weight: 600;
                    margin-bottom: 15px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }}

                .estimate-card {{
                    background: #2a2a2a;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 10px;
                    border: 1px solid #444;
                }}

                .ride-type {{
                    font-size: 16px;
                    font-weight: 600;
                    margin-bottom: 5px;
                }}

                .price {{
                    font-size: 24px;
                    font-weight: 700;
                    color: #00ff00;
                    margin-bottom: 5px;
                }}

                .details {{
                    font-size: 14px;
                    color: #888;
                }}

                .time-estimate {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 12px 0;
                    border-bottom: 1px solid #333;
                }}

                .time-estimate:last-child {{
                    border-bottom: none;
                }}

                .eta {{
                    font-weight: 600;
                    color: #00ff00;
                }}

                .btn {{
                    display: block;
                    width: 100%;
                    padding: 16px;
                    background: #000000;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: 600;
                    text-align: center;
                    margin-bottom: 10px;
                    border: 2px solid #ffffff;
                    transition: all 0.2s;
                }}

                .btn:hover {{
                    background: #ffffff;
                    color: #000000;
                }}

                .btn-primary {{
                    background: #ffffff;
                    color: #000000;
                }}

                .btn-primary:hover {{
                    background: #000000;
                    color: #ffffff;
                }}

                .no-data {{
                    text-align: center;
                    color: #666;
                    padding: 20px;
                    font-style: italic;
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
                    <h1>Your Uber Ride</h1>
                    <p>Ready to book</p>
                </div>

                <div class="card">
                    <div class="location">
                        <div class="location-label">📍 From</div>
                        <div class="location-name">{start.name}</div>
                        <div class="location-address">{start.address}</div>
                    </div>
                    <div class="location">
                        <div class="location-label">📍 To</div>
                        <div class="location-name">{destination.name}</div>
                        <div class="location-address">{destination.address}</div>
                    </div>
                </div>

                <div class="card">
                    <div class="section-title">⏱️ Pickup Time</div>
                    {time_html}
                </div>

                <div class="card">
                    <div class="section-title">💰 Price Estimates</div>
                    {price_html}
                </div>

                <div class="card">
                    <div class="section-title">🔗 Book Your Ride</div>
                    <a href="{deep_link}" class="btn btn-primary">Open in Uber App</a>
                    <a href="{web_link}" class="btn">Open in Browser</a>
                </div>

                <div class="footer">
                    <p>Powered by <strong>Omi</strong></p>
                </div>
            </div>
        </body>
        </html>
        """

        return html
