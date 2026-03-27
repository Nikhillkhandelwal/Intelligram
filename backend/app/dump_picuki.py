import requests
from bs4 import BeautifulSoup

url = "https://www.picuki.com/profile/instagram"
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36" }
response = requests.get(url, headers=headers, timeout=10)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', class_='box-photo')
    if items:
        print(items[0].prettify())
    else:
        print("No items found. Maybe blocked.")
else:
    print(f"Status: {response.status_code}")
