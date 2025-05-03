import requests

def query_lm_studio(prompt):
    url = "http://192.168.0.14:1234/v1/completions"
    payload = {
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.7
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"].strip()
    else:
        raise Exception(f"LM Studio error: {response.status_code} - {response.text}")