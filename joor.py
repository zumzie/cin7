import requests

class JoorAPI:
    def __init__(self, creds):
        default_endpoint = "https://apisandbox.jooraccess.com/v4"
        self.creds = creds
        self.endpoint_v4 = "https://apisandbox.jooraccess.com/v4"
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

    # Customer API Calls
    def get_customers(self):
        JoorAPI.get_data()

    def post_customers(self):
        JoorAPI.send_data()

    # Orders API Calls
    def get_orders(self):
        order_api = '/orders'
        JoorAPI.get_data()

    def send_orders(self):
        order_api = '/orders/bulk_create'
        JoorAPI.send_data()


class JoorProducts(JoorAPI):
    def __init__(self, creds, _t):
        super().__init__(self, creds)
        self._t = _t

    # Product API Calls
    def get_products(self):
        products = '/products'
        JoorAPI.get_data()

    def get_skus(self):
        products = '/skus'
        JoorAPI.send_data()
    
    def get_prices(self):
        products = '/prices'
        JoorAPI.get_data()

    def get_collections(self):
        products = '/collections'
        JoorAPI.get_data()

    def post_products(self):
        products = '/products/bulk_create'
        JoorAPI.send_data()

    def post_skus(self):
        products = '/skus/bulk_create'
        JoorAPI.send_data()

    def post_prices(self):
        products = '/prices/bulk_create'
        JoorAPI.get_data()

    def post_prices(self):
        products = '/prices/bulk_create'
        JoorAPI.get_data()

    def post_images(self):
        JoorAPI.send_data()

    def post_inventory(self):
        JoorAPI.send_data()

