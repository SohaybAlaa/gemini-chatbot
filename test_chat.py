import requests

url = "http://127.0.0.1:5000/chat"
data = {"question": "hi"}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)

try:
    print("Response:", response.json())
except Exception:
    print("Raw Response Text:", response.text)
