import requests


# ============ GET request ============


url  = "https://api.github.com/user/1"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
# }

response = requests.get(url)

print("===== Status Code: =====")
print(response.status_code)

print("===== URL: =====")
print(response.url)

print("===== Headers: =====")
print(response.headers)

print("===== Response Text: =====")
print(response.text)

print("===== Response JSON: =====")
if response.status_code == 200:
    print(response.json())
else:
    print(f"Request failed with status {response.status_code}, skipping .json()")



# ============ GET request with query parameters ============


def get_response_with_query_params(url, params):
    response = requests.get(url, params=params)

    json_result = (
        response.json() if response.status_code == 200
        else f"Request failed with status {response.status_code}, skipping .json()"
    )

    return {
        "status_code": response.status_code,
        "url": response.url,
        "headers": response.headers,
        "text": response.text,
        "json": json_result,
    }


url_with_params = "https://api.github.com/users/mojombo/repos"
params = {
    "per_page": 5,
    "page": 1
}

get_response = get_response_with_query_params(url_with_params, params)
# print(get_response)

data = get_response["json"]
print(data)
print(type(data))
print(len(data))



# ============ POST request ============


def post_request(url, data):

    response = requests.post(url, json=data)

    json_result = (
        response.json() if response.status_code in (200, 201)
        else f"Request failed with status {response.status_code}, skipping .json()"
    )

    return {
        "status_code": response.status_code,
        "method": response.request.method,
        "headers": response.request.headers,
        "json": json_result,
    }



url = "https://postman-echo.com/post"

payload = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "topic": "HTTP" 
}

response = post_request(url, payload)

print(response)


# ============ raise_for_status() ============

url = "https://api.github.com/users/mojombo"
# url = "https://api.github.com/users/this-user-should-not-exist-987654321"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    print(response.status_code)
    print(response.json())

except requests.RequestException as e:
    print(f"Request failed: {e}")
