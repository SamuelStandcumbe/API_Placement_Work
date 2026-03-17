from locust import HttpUser, task, between

class UserFlow(HttpUser):
    wait_time = between(1, 2)
    host = ""
    default_headers = {"accept": "application/json"}
    print("Attempting login")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {
            "access-token": "",
            "accept": "application/json"
        }
        
        self.token = None
    
    def on_start(self):
        print("Attempting login")

        try:
            res = self.client.post(
                "/dev/api/v2/auth/token/create",
                headers=self.headers,
                params={
                    "user_id": "",
                    "tenant_id": "",
                    "role": "user"
                },
                timeout=10
            )
            
            print("Response received, status code:", res.status_code)
            print("Response content:", res.text)
            
            # Only try to read token if login was successful
            if res.status_code == 200:
                # getting token from response
                self.token = res.json()["access_token"]
                
                # setting up headers and adding in bearer token
                self.headers["Authorization"] = f"Bearer {self.token}"
                
                print("Login successful, bearer token added.")
            else:
                print("Login failed, token not created.")
            
        except Exception as e:
            print(f"Error during login: {e}")
            
    # get the agents endpoint
    @task()
    def get_agents(self):
        print("Attempting to get agents with headers:", self.headers)
        
        # Call the agents endpoint
        response = self.client.get(
            "/dev/api/v2/data/agents",
            headers=self.headers,
            name="GET /api/v2/data/agents"
        )
        
        print("Agents status code:", response.status_code)
        print("Agents response:", response.text)
    
    # get the knowledge collections endpoint
    @task()
    def list_collections(self):
        print("Attempting to get knowledge collections with headers:", self.headers)
        
        # Call the knowledge collections endpoint
        response = self.client.get(
            "/dev/api/v2/data/knowledge/collections",
            headers=self.headers,
            name="GET /api/v2/data/knowledge/collections"
        )
        
        print("Collections status code:", response.status_code)
        print("Collections response:", response.text)
