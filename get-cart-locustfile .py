from locust import task, run_single_user
from locust import FastHttpUser 
from insert_product import login

class add_to_cart(FastHttpUser ):
    def __init__(self, environment):
        super().__init__(environment)
        self.username = "test123"
        self.password = "test123"
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")

    host = "http://localhost:5000"
    
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User -Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    @task
    def t(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Cookies": f"token={self.token}",
            "Referer": "http://localhost:5000/product/1",
        }

        # Use self.client.get directly for better readability and performance
        with self.client.get("/cart", headers={**self.default_headers, **headers}, catch_response=True) as resp:
            if resp.status_code == 200:
                resp.success()  # Mark the response as successful
            else:
                resp.failure(f"Request failed with status code: {resp.status_code}")

if __name__ == "__main__":
    run_single_user(add_to_cart)
