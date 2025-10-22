"""
Location input module with hardcoded San Francisco locations.
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Location:
    """Represents a geographic location."""
    name: str
    address: str
    latitude: float
    longitude: float


class LocationInput:
    """Handles location input with hardcoded SF locations."""

    # Hardcoded locations (dummy data for testing)
    START_LOCATION = Location(
        name="Home",
        address="1443 Tram Avenue",
        latitude=37.7989,
        longitude=-122.4074
    )

    DESTINATION_LOCATION = Location(
        name="Mission Street",
        address="1885 Mission St, San Francisco, CA",
        latitude=37.7699,
        longitude=-122.4192
    )

    @classmethod
    def get_trip_locations(cls) -> Tuple[Location, Location]:
        """
        Get the hardcoded start and destination locations.

        Returns:
            Tuple of (start_location, destination_location)
        """
        print(f"📍 Start: {cls.START_LOCATION.name} ({cls.START_LOCATION.address})", flush=True)
        print(f"📍 Destination: {cls.DESTINATION_LOCATION.name} ({cls.DESTINATION_LOCATION.address})", flush=True)

        return cls.START_LOCATION, cls.DESTINATION_LOCATION

    @classmethod
    def get_start_coordinates(cls) -> Tuple[float, float]:
        """Get start location coordinates (lat, long)."""
        return cls.START_LOCATION.latitude, cls.START_LOCATION.longitude

    @classmethod
    def get_destination_coordinates(cls) -> Tuple[float, float]:
        """Get destination coordinates (lat, long)."""
        return cls.DESTINATION_LOCATION.latitude, cls.DESTINATION_LOCATION.longitude
