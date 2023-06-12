import requests
class About:
    def tool_decription(self):
        print("#"*100)
        print("API TESTER")
        print("#"*100)
        print("\n"*5)
About().tool_decription()
class Api:
    def test(self,api_url, method="GET", headers=None, params=None, data=None):
        try:
            response = requests.request(method, api_url, headers=headers, params=params, data=data)
            response.raise_for_status()
            print(f"API: {api_url}")
            print(f"Method: {method}")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}\n")
        except requests.exceptions.RequestException as e:
            print(f"API: {api_url}")
            print(f"Error: {e}\n")
        print("-"*100)


api = Api()

login = "https://example/api/login"
api.test(login, method="POST", headers={"Authorization": "Bearer your_token"}, data={"username": "100222","password":"123456"})

api_url = "https://example/api"
api.test(api_url)

