"""
Fare calculator for estimating Uber ride costs and times.
Uses Haversine formula for distance and standard Uber rate cards.
"""
import math
from typing import Dict, List


class FareCalculator:
    """Calculate estimated fares and ETAs for Uber rides."""

    # Uber rate cards (San Francisco area - approximate)
    RATE_CARDS = {
        "UberX": {
            "base_fare": 2.50,
            "per_mile": 1.75,
            "per_minute": 0.35,
            "minimum_fare": 8.00,
            "booking_fee": 2.00,
            "display_name": "UberX"
        },
        "UberXL": {
            "base_fare": 3.50,
            "per_mile": 2.50,
            "per_minute": 0.50,
            "minimum_fare": 12.00,
            "booking_fee": 2.50,
            "display_name": "UberXL"
        },
        "Uber Comfort": {
            "base_fare": 4.00,
            "per_mile": 2.25,
            "per_minute": 0.45,
            "minimum_fare": 10.00,
            "booking_fee": 2.00,
            "display_name": "Uber Comfort"
        },
        "Uber Black": {
            "base_fare": 8.00,
            "per_mile": 3.75,
            "per_minute": 0.65,
            "minimum_fare": 15.00,
            "booking_fee": 3.00,
            "display_name": "Uber Black"
        }
    }

    # Average speeds (mph)
    AVG_CITY_SPEED = 25  # mph in city traffic
    AVG_PICKUP_TIME = 5  # minutes average pickup time

    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two GPS coordinates using Haversine formula.
        Returns distance in miles.
        """
        # Earth radius in miles
        R = 3959.0

        # Convert to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Haversine formula
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))

        distance = R * c
        return distance

    @classmethod
    def estimate_duration(cls, distance_miles: float) -> int:
        """
        Estimate trip duration in minutes based on distance.
        """
        # Time = Distance / Speed
        duration_hours = distance_miles / cls.AVG_CITY_SPEED
        duration_minutes = int(duration_hours * 60)

        return max(duration_minutes, 5)  # Minimum 5 minutes

    @classmethod
    def calculate_fare(cls, distance_miles: float, duration_minutes: int, ride_type: str) -> float:
        """
        Calculate estimated fare for a ride.
        """
        if ride_type not in cls.RATE_CARDS:
            ride_type = "UberX"

        rates = cls.RATE_CARDS[ride_type]

        # Calculate fare components
        base = rates["base_fare"]
        distance_cost = distance_miles * rates["per_mile"]
        time_cost = duration_minutes * rates["per_minute"]
        booking_fee = rates["booking_fee"]

        total = base + distance_cost + time_cost + booking_fee

        # Apply minimum fare
        total = max(total, rates["minimum_fare"])

        return round(total, 2)

    @classmethod
    def get_price_estimates(
        cls,
        start_lat: float,
        start_lon: float,
        end_lat: float,
        end_lon: float
    ) -> List[Dict]:
        """
        Generate price estimates for all ride types.
        Returns list in Uber API format.
        """
        # Calculate distance and duration
        distance_miles = cls.haversine_distance(start_lat, start_lon, end_lat, end_lon)
        duration_minutes = cls.estimate_duration(distance_miles)

        estimates = []

        for ride_type, rates in cls.RATE_CARDS.items():
            low_fare = cls.calculate_fare(distance_miles, duration_minutes, ride_type)
            # Add 15% variance for high estimate
            high_fare = round(low_fare * 1.15, 2)

            estimates.append({
                "localized_display_name": rates["display_name"],
                "estimate": f"${low_fare:.0f}-${high_fare:.0f}",
                "low_estimate": low_fare,
                "high_estimate": high_fare,
                "duration": int(duration_minutes * 60),  # seconds
                "distance": round(distance_miles, 2),
                "display_name": rates["display_name"],
                "product_id": ride_type.lower().replace(" ", "_"),
                "currency_code": "USD"
            })

        print(f"📊 Calculated estimates: {len(estimates)} ride types, {distance_miles:.2f} mi, ~{duration_minutes} min", flush=True)

        return estimates

    @classmethod
    def get_time_estimates(cls, start_lat: float, start_lon: float) -> List[Dict]:
        """
        Generate pickup time estimates for all ride types.
        Returns list in Uber API format.
        """
        estimates = []

        for ride_type, rates in cls.RATE_CARDS.items():
            # Vary pickup time slightly by ride type
            if "Black" in ride_type:
                pickup_time = cls.AVG_PICKUP_TIME + 2
            elif "XL" in ride_type or "Comfort" in ride_type:
                pickup_time = cls.AVG_PICKUP_TIME + 1
            else:
                pickup_time = cls.AVG_PICKUP_TIME

            estimates.append({
                "localized_display_name": rates["display_name"],
                "estimate": pickup_time * 60,  # seconds
                "display_name": rates["display_name"],
                "product_id": ride_type.lower().replace(" ", "_")
            })

        print(f"⏱️  Calculated pickup times: avg {cls.AVG_PICKUP_TIME} min", flush=True)

        return estimates
