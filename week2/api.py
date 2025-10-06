import requests

BASE_URL = "https://api.spacexdata.com/v4/launches/upcoming"

def get_upcoming_launches():
    """
    Fetch and display upcoming SpaceX launches.

    Fetches upcoming SpaceX launches and prints mission name, date, and flight number for the first five.

    Returns:
        None
    """
    response = requests.get(BASE_URL)

    if response.status_code == 200:
        launches = response.json()

        if not launches:
            print("No upcoming launches found.")
            return

        print(f"\n Upcoming SpaceX Launches ({len(launches)} found):\n")
        for launch in launches[:5]:
            print(f"Mission Name: {launch.get('name', 'N/A')}")
            print(f"Date (UTC): {launch.get('date_utc', 'N/A')}")
            print(f"Flight Number: {launch.get('flight_number', 'N/A')}")
            print("-" * 40)
    else:
        print("Failed to fetch data from SpaceX API!")

if __name__ == "__main__":
    get_upcoming_launches()
