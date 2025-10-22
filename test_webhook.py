import requests
import json


def test_omi_webhook(user_text: str = "I need a ride"):
    """
    Test the Omi webhook endpoint with a sample conversation.

    Args:
        user_text: What the user said to the Omi device
    """
    payload = {
        "id": "memory_test_123",
        "created_at": "2025-10-22T10:30:00Z",
        "transcript": [
            {
                "text": user_text,
                "speaker": "SPEAKER_00",
                "speakerId": 0,
                "is_user": True,
                "start": 0.0,
                "end": 2.5
            }
        ],
        "title": "Ride Request",
        "category": "transportation"
    }

    print(f"Testing webhook with: '{user_text}'")
    print("=" * 60)

    response = requests.post(
        "http://localhost:8000/webhook/omi?uid=user123",
        json=payload
    )

    if response.status_code == 200:
        result = response.json()
        print("\nOmi Device Response:")
        print("-" * 60)
        print(result.get("message"))
        print("-" * 60)
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    # Test different scenarios
    test_cases = [
        "I need a ride",
        "Book me an Uber",
        "Get me a cab to downtown"
    ]

    for test_text in test_cases:
        test_omi_webhook(test_text)
        print("\n")
