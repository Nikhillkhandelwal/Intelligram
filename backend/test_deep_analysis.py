import requests
import json

def test_deep_analysis():
    url = "http://127.0.0.1:5000/deep_analysis"
    payload = {"hashtag": "fitness"}
    
    print(f"Testing {url} with hashtag 'fitness'...")
    try:
        response = requests.post(url, json=payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            print("SUCCESS: Received response")
            print(f"Hashtags analyzed: {data.get('hashtags_analyzed')}")
            print(f"Total posts: {data.get('total_posts')}")
            print("Strategy Report Preview:")
            print(data.get('strategy_report', '')[:500] + "...")
        else:
            print(f"FAILED: Status Code {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_deep_analysis()
