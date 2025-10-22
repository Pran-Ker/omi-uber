"""
Uber API Client for price estimates, time estimates, and deep link generation.
"""
import os
import requests
from typing import Optional, Dict, List
from dotenv import load_dotenv
from utils.fare_calculator import FareCalculator

load_dotenv()


class UberClient:
    """Handles Uber API interactions and deep link generation."""

    def __init__(self):
        self.server_token = os.getenv("UBER_SERVER_TOKEN")
        self.base_url = "https://api.uber.com/v1.2"

    def get_price_estimates(
        self,
        start_latitude: float,
        start_longitude: float,
        end_latitude: float,
        end_longitude: float
    ) -> Optional[List[Dict]]:
        """
        Get price estimates for a trip.
        Falls back to calculator if API token not available.
        Returns list of ride options with pricing.
        """
        if not self.server_token:
            print("⚠️  UBER_SERVER_TOKEN not set - using fare calculator", flush=True)
            return FareCalculator.get_price_estimates(
                start_latitude, start_longitude,
                end_latitude, end_longitude
            )

        url = f"{self.base_url}/estimates/price"
        headers = {
            "Authorization": f"Token {self.server_token}",
            "Accept-Language": "en_US",
            "Content-Type": "application/json"
        }
        params = {
            "start_latitude": start_latitude,
            "start_longitude": start_longitude,
            "end_latitude": end_latitude,
            "end_longitude": end_longitude
        }

        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                prices = data.get("prices", [])
                print(f"✅ Got {len(prices)} price estimates from Uber API", flush=True)
                return prices
            else:
                print(f"❌ Uber API error: {response.status_code} - falling back to calculator", flush=True)
                return FareCalculator.get_price_estimates(
                    start_latitude, start_longitude,
                    end_latitude, end_longitude
                )

        except Exception as e:
            print(f"❌ Error fetching price estimates: {e} - falling back to calculator", flush=True)
            return FareCalculator.get_price_estimates(
                start_latitude, start_longitude,
                end_latitude, end_longitude
            )

    def get_time_estimates(
        self,
        start_latitude: float,
        start_longitude: float
    ) -> Optional[List[Dict]]:
        """
        Get ETA estimates for pickup at start location.
        Falls back to calculator if API token not available.
        Returns list of products with pickup time.
        """
        if not self.server_token:
            print("⚠️  UBER_SERVER_TOKEN not set - using fare calculator", flush=True)
            return FareCalculator.get_time_estimates(start_latitude, start_longitude)

        url = f"{self.base_url}/estimates/time"
        headers = {
            "Authorization": f"Token {self.server_token}",
            "Accept-Language": "en_US",
            "Content-Type": "application/json"
        }
        params = {
            "start_latitude": start_latitude,
            "start_longitude": start_longitude
        }

        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                times = data.get("times", [])
                print(f"✅ Got {len(times)} time estimates from Uber API", flush=True)
                return times
            else:
                print(f"❌ Uber API error: {response.status_code} - falling back to calculator", flush=True)
                return FareCalculator.get_time_estimates(start_latitude, start_longitude)

        except Exception as e:
            print(f"❌ Error fetching time estimates: {e} - falling back to calculator", flush=True)
            return FareCalculator.get_time_estimates(start_latitude, start_longitude)

    @staticmethod
    def generate_deep_link(
        pickup_latitude: float,
        pickup_longitude: float,
        dropoff_latitude: float,
        dropoff_longitude: float,
        pickup_nickname: Optional[str] = None,
        dropoff_nickname: Optional[str] = None,
        pickup_address: Optional[str] = None,
        dropoff_address: Optional[str] = None
    ) -> str:
        """
        Generate Uber deep link for direct booking.
        Note: dropoff[nickname] or dropoff[formatted_address] is REQUIRED for pins to show.

        Returns: Deep link URL that opens Uber app or web.
        """
        params = []
        params.append("action=setPickup")

        # Pickup parameters
        params.append(f"pickup[latitude]={pickup_latitude}")
        params.append(f"pickup[longitude]={pickup_longitude}")

        if pickup_nickname:
            params.append(f"pickup[nickname]={pickup_nickname.replace(' ', '+')}")
        if pickup_address:
            params.append(f"pickup[formatted_address]={pickup_address.replace(' ', '+')}")

        # Dropoff parameters - nickname or address is REQUIRED for pin to display
        params.append(f"dropoff[latitude]={dropoff_latitude}")
        params.append(f"dropoff[longitude]={dropoff_longitude}")

        if dropoff_nickname:
            params.append(f"dropoff[nickname]={dropoff_nickname.replace(' ', '+')}")
        if dropoff_address:
            params.append(f"dropoff[formatted_address]={dropoff_address.replace(' ', '+')}")

        deep_link = f"uber://?{'&'.join(params)}"
        print(f"🔗 Generated deep link: {deep_link}", flush=True)

        return deep_link

    @staticmethod
    def generate_mobile_web_link(
        pickup_latitude: float,
        pickup_longitude: float,
        dropoff_latitude: float,
        dropoff_longitude: float
    ) -> str:
        """
        Generate Uber mobile web link (fallback if app not installed).
        """
        params = []
        params.append(f"pickup[latitude]={pickup_latitude}")
        params.append(f"pickup[longitude]={pickup_longitude}")
        params.append(f"dropoff[latitude]={dropoff_latitude}")
        params.append(f"dropoff[longitude]={dropoff_longitude}")
        params.append("action=setPickup")

        web_link = f"https://m.uber.com/ul/?{'&'.join(params)}"

        return web_link
