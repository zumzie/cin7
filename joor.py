import requests

class JoorAPI:
    def __init__(self, creds, endpoint_v4,):
        default_endpoint = "https://apisandbox.jooraccess.com/v4"
        self.creds = creds
        self.endpoint_v4 = endpoint_v4
        self.api_token = creds["api_token"]

    def auth_token(self):
        endpoint =  "https://atlas-sandbox.jooraccess.com/auth"

        auth_data = {
            "grant_type": "password",
            "client_id": self.creds["client_id"],
            "client_secret": self.creds["client_secret"],
            "username": self.creds["client_secret"],
            "password": self.creds["password"]
        }

    def send_data(self):
        pass

    def get_data(self):
        pass

    def get_products(self):
        JoorAPI.get_data()

    def get_customers(self):
        JoorAPI.get_data()

    def get_orders(self):
        JoorAPI.get_data()

    def post_images(self):
        JoorAPI.send_data()
    
    def post_products(self):
        JoorAPI.send_data()

    def post_images(self):
        JoorAPI.send_data()

    def post_inventory(self):
        JoorAPI.send_data()