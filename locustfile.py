from locust import HttpUser, task, between
import base64

class OpenBMCTest(HttpUser):
    wait_time = between(1, 3)
    host = "https://localhost:2443"
    
    def on_start(self):
        credentials = base64.b64encode(b"root:0penBmc").decode("utf-8")
        self.headers = {"Authorization": f"Basic {credentials}"}

    @task
    def get_system_info(self):
        self.client.get("/redfish/v1/Systems/system", 
                       headers=self.headers, verify=False)

    @task
    def get_power_state(self):
        self.client.get("/redfish/v1/Chassis/chassis/Power", 
                       headers=self.headers, verify=False)

class PublicAPITest(HttpUser):
    wait_time = between(1, 3)
    host = "https://jsonplaceholder.typicode.com"

    @task
    def get_posts(self):
        self.client.get("/posts")

    @task
    def get_weather(self):
        self.client.get("http://wttr.in/?format=3")