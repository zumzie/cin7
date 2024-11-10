import json
import os

from mapper import *
from joor import *
from parser import *
from utils.slack import *

from pathlib import Path
from dotenv import load_dotenv

def readFile(raw_data):
    with open(raw_data) as data_file:
        data = json.load(data_file)
    return data

def writeFile(incoming_data, file_name):
    with open(file_name, "w") as outputted_data:
        json.dump(incoming_data, outputted_data, indent=4)


def compare_products(cin_products, joor_products):
    products_to_create = []
    products_to_update = []
    if joor_products is None:
        return
    
    joor_product_ids = {j_product['product_identifier'] for j_product in joor_products['data']}

    print(joor_product_ids)
    for c_product in cin_products:
        c_product_id = str(c_product['id'])
        if c_product_id in joor_product_ids:
            # Product exists in Joor, so we update it
            products_to_update.append(c_product)
            print(f"Found a match for {c_product_id}, UPDATE that bih")
        else:
            # Product does not exist in Joor, so we create it
            products_to_create.append(c_product)
            print(f"No match for {c_product_id}, CREATE that bih")

    return products_to_create, products_to_update



def main():

    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    slack_api_token = os.environ['slack_bot_api']

    j_products_exist_flag = False
    c_products_exist_flag = False

    raw_product_data = 'temp_data/cin_products.json'
    raw_customer_data = 'temp_data/cin_customers.json'
    raw_order_data = 'temp_data/cin_orders.json'
    inventory_data = 'temp_data/cin_inventory.json'
    joor_product_data = 'temp_data/joor_products.json'

    raw_j_order_data = 'temp_data/joor_orders.json'

    prod_data = readFile(raw_product_data)
    customer_data = readFile(raw_customer_data)
    order_data = readFile(raw_order_data)
    inven_data = readFile(inventory_data)
    joor_order_data = readFile(raw_j_order_data)
    joor_prod_data = readFile(joor_product_data)

    products_to_create = []
    products_to_update = []

    
    # Gather Data
    '''
    Send data to specific API endpoint
    '''
    creds = {
        "client_id": "",
        "client_secret": "",
        "username": "",
        "password": "",
        "v2_endpoint": "",
        "v4_endpoint": "",
    }

    token = {
        "api_token": ""
    }

    ## Figure this shit out sometime (AUTHENTICATION FLOW)
    joor_auth = JoorAPI(creds)
    joor_api = JoorProducts(joor_auth, token['api_token'])
    
    ''''
    # Prod Flow
    '''
    if prod_data is not None:
        j_products_exist_flag = True

    if j_products_exist_flag is True:   
        joor_products = joor_api.get_products()

    products_to_create, products_to_update = compare_products(prod_data, joor_prod_data)


    ## Compare JOOR products to Shopify, remove products that
    ## don't need to be updated from JOOR, grab IDs

    ## Create
    # Parse Data
    parser = Parser(products_to_create, customer_data, order_data)
    created_parsed_products = parser.parseProducts()

    writeFile(created_parsed_products, 'temp_data/parsedProducts.json')

    # Initialize Classes
    mapper = Mapper(created_parsed_products, customer_data, order_data, joor_order_data)
    product_mapper = MapProducts(created_parsed_products, customer_data, order_data, joor_order_data)
    
    # Map Product Data
    mapped_products = product_mapper.mapProducts()
    mapped_skus = product_mapper.mapSkus()
    mapped_prices = product_mapper.mapPrices()
    mapped_images = product_mapper.mapImages()
    mapped_inventory = product_mapper.mapInventory(inven_data)

    # Map Order Data
    mapped_cin_orders, mapped_joor_orders = mapper.mapOrders()

    # Map Customer Data
    mapped_customers = mapper.mapCustomers()

    # Write data (temp)
    writeFile(mapped_products, 'created_files/mappedProducts.json')
    writeFile(mapped_skus, 'created_files/mappedSkus.json')
    writeFile(mapped_prices, 'created_files/mappedPrices.json')
    writeFile(mapped_images, 'created_files/mappedImages.json')
    writeFile(mapped_inventory, 'created_files/mappedInventory.json')
    writeFile(mapped_cin_orders, 'created_files/mappedOrders.json')
    writeFile(mapped_joor_orders, 'created_files/joorOrderData.json')
    writeFile(mapped_customers, 'created_files/mappedCustomerData.json')


    slack_bot = SlackAPI(slack_api_token)
    #test = slack_bot.send_channel_message()
    
    # Aggregate Data


    # Route Data

    
    # POST Products
    posted_products = joor_api.post_products(mapped_products)
    temp_account_id = '12411'
    posted_message =  f'Products successfully posted for account {temp_account_id}'

    # Products posted successfully message #
    #slack_bot.send_channel_message(posted_message)


    '''
    # Posted Response data (TEMPORARY)
    '''
    posted_response_data = 'response_files/products_posted_response.json'
    posted_response = readFile(posted_response_data)

    # POST SKUs
    skus_to_create = []
    for created_prod in posted_response['data']:
        c_product_id = str(created_prod['product_identifier'])
        for sku in mapped_skus:
            if c_product_id == str(sku['product_id']):
                sku['product_id'] = created_prod['id']
                skus_to_create.append(sku)

    posted_skus = joor_api.post_skus(skus_to_create)
    posted_message =  f'SKUs successfully posted for account {temp_account_id}'
    #slack_bot.send_channel_message(posted_message)

    # POST PRICES
    skus_response_data = 'response_files/skus_posted_response.json'
    skus_response = readFile(skus_response_data)

    prices_to_create = []
    for sku_response in skus_response['data']:
        for sku_price in mapped_prices:
            if sku_price['sku_identifier'] == sku_response['sku_identifier']:
                sku_price['id'] = sku_response['id']

                prices_to_create.append(sku_price)
    for sku_price in prices_to_create:
        del sku_price['sku_identifier']

    # POST IMAGES
    posted_images = joor_api.post_images(mapped_images)

    print(mapped_images)
    # POST INVENTORY
    posted_inventory = joor_api.post_images(mapped_inventory)
    
    # POST Customers

    # POST Orders

    ## Update



if __name__ == "__main__":
    main()
