import requests

url = "http://localhost:8000/chat"
payload = {"query": "Finalize AI MVP", "top_k": 3}  # removed ignore_memory
url = "http://localhost:8000/chat"
payload = {"query": "Finalize AI MVP", "top_k": 3}  # removed ignore_memory
r = requests.post(url, json=payload)

print(r.status_code)  # should be 200 if OK
print(r.json())       # should now parse as JSON
print(r.text)
