import requests

url = "https://tw.mingzw.net/mzwchapter/41936.html"  # Replace with the desired URL
output_filename = "index.html" # Name of the file to save the HTML

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    with open(output_filename, "w", encoding="utf-8") as file:
        file.write(response.text)

    print(f"HTML content successfully saved to {output_filename}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")