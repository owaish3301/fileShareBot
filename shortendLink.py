import requests

def short_url(url):
    try:
        # Create a shortened URL
        response = requests.get("https://instantearn.in/api", params={"api": "4bd5334c8bbcd2ea1da78e99fefa7b48bbff377d", "url": url})
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        shortened_url = response
        return shortened_url
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None