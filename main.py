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


def main():

    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    slack_api_token = os.environ['slack_bot_api']

    raw_product_data = 'temp_data/cin_products.json'
    raw_customer_data = 'temp_data/cin_customers.json'
    raw_order_data = 'temp_data/cin_orders.json'
    inventory_data = 'temp_data/cin_inventory.json'

    raw_j_order_data = 'temp_data/joor_orders.json'

    prod_data = readFile(raw_product_data)
    customer_data = readFile(raw_customer_data)
    order_data = readFile(raw_order_data)
    inven_data = readFile(inventory_data)
    joor_order_data = readFile(raw_j_order_data)

    
    # Gather Data

    ## Create
    # Parse Data
    parser = Parser(prod_data, customer_data, order_data)
    parsed_products = parser.parseProducts()

    writeFile(parsed_products, 'temp_data/parsedProducts.json')

    # Initialize Classes
    mapper = Mapper(parsed_products, customer_data, order_data, joor_order_data)
    product_mapper = MapProducts(parsed_products, customer_data, order_data, joor_order_data)
    
    # Map Product Data
    mapped_products = product_mapper.mapProducts()
    mapped_skus = product_mapper.mapSkus()
    mapped_images = product_mapper.mapImages()
    mapped_inventory = product_mapper.mapInventory(inven_data)

    print(product_mapper)

    # Map Order Data
    mapped_cin_orders, mapped_joor_orders = mapper.mapOrders()

    # Map Customer Data
    mapped_customers = mapper.mapCustomers()

    # Write data (temp)
    writeFile(mapped_products, 'created_files/mappedProducts.json')
    writeFile(mapped_skus, 'created_files/mappedSkus.json')
    writeFile(mapped_images, 'created_files/mappedImages.json')
    writeFile(mapped_inventory, 'created_files/mappedInventory.json')
    writeFile(mapped_cin_orders, 'created_files/mappedOrders.json')
    writeFile(mapped_joor_orders, 'created_files/joorOrderData.json')
    writeFile(mapped_customers, 'created_files/mappedCustomerData.json')

    slack_bot = SlackAPI(slack_api_token)

    #test = slack_bot.send_channel_message()
    # Aggregate Data
    


    # Route Data
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
    #joor_api = JoorAPI(creds)
    
    # POST Products
    #posted_products = joor_api.post_products(mapped_products)

    '''
    add conditional statement to see if we have ids from skus then add them into the correct product
    '''
    #posted_skus = joor_api.post_skus(mapped_skus)
    
    # POST Customers

    # POST Orders

    ## Update



if __name__ == "__main__":
    main()
