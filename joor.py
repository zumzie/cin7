import requests

class JoorAPI:
    def __init__(self, creds):
        self.base_endpoint = "https://apisandbox.jooraccess.com/"
        self.creds = creds
        self.endpoint_v4 = "https://apisandbox.jooraccess.com/"

        #self.api_token = creds["api_token"]

    def authenticate(self):
        endpoint =  "https://atlas-sandbox.jooraccess.com/auth"
        auth_data = {
            "grant_type": "password",
            "client_id": self.creds["client_id"],
            "client_secret": self.creds["client_secret"],
            "username": self.creds["client_secret"],
            "password": self.creds["password"]
        }
        headers = {
            "Content-Type": "application/json"
        }

        # Send API call to get bearer token
        response = requests.post(endpoint,auth_data)
        print(response)

        match response.status_code:
            case 200:
                return response
            case 401:
                return "Invalid Credentials"
            case _:
                return None

    def send_data(self, endpoint, payload, token, flag):
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            "accept": "application/json"
        }
        if flag == 'create':
            url = self.base_endpoint + endpoint + '/bulk_create' + '?account=43450'
            return requests.post(url, json=payload, headers=header)
        elif flag == 'update':
            url = self.base_endpoint + endpoint + '/bulk_update' '?account=43450'
            return requests.post(url, json=payload, headers=header)


    def get_data(self, endpoint, token):
        url = self.base_endpoint + endpoint + '?account=43450'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            "accept": "application/json"
        }
        
        request = requests.get(url, headers=headers)
        return request

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


class JoorProducts():
    def __init__(self, creds, _t):
        self.creds = creds
        self._t = _t
        self.api = JoorAPI(creds)

    # Product API Calls
    def get_products(self):
        products = '/v4/products'
        request = self.api.get_data(products, self._t)

        return request

    def get_skus(self):
        products = '/v4/skus'
        JoorAPI.send_data()
    
    def get_prices(self):
        products = '/v4/prices'
        JoorAPI.get_data()

    def get_collections(self):
        products = '/v4/collections'
        JoorAPI.get_data()

    def get_seasons(self):
        season_endpoint = '/v4/seasons'
        JoorAPI.get_data()

    def post_products(self, payload, flag):
        products_endpoint = '/v4/products'
        return self.api.send_data(products_endpoint, payload, self._t, flag)

    def post_skus(self, payload):
        skus_endpoint = '/v4/skus/bulk_create'
        return self.api.send_data(skus_endpoint, payload, self._t)
    
    def post_prices(self):
        prices_endpoint = '/v4/prices/bulk_create'
        self.api.send_data()
    
    def post_images(self, payload):
        prices_endpoint = '/v4/assets/products'
        self.api.send_data(prices_endpoint, payload, self._t)

    def post_inventory(self, payload):
        inventory_endpoint = '/v2/bulk-inventory'
        self.api.send_data(inventory_endpoint, payload, self._t)

    def post_collections(self, payload, flag):
        collections_endpoint = '/v4/collections'
        self.api.send_data(collections_endpoint, payload, self._t, flag)
        pass