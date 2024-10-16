import json
import os

from mapper import *
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

    rawProdData = 'temp_data/cin_products.json'
    rawCustomerData = 'temp_data/cin_customers.json'
    rawOrderData = 'temp_data/cin_orders.json'

    prod_data = readFile(rawProdData)
    customer_data = readFile(rawCustomerData)
    order_data = readFile(rawOrderData)

    
    # Parse Data
    parser = Parser(prod_data, customer_data, order_data)
    parsed_products = parser.parseProducts()

    writeFile(parsed_products, 'temp_data/parsedProducts.json')


    # Map Data
    mapper = Mapper(parsed_products, customer_data, order_data)
    mapped_products = mapper.mapProducts()
    mapped_skus = mapper.mapSkus()

    writeFile(mapped_products, 'created_files/mappedProducts.json')
    writeFile(mapped_skus, 'created_files/mappedSkus.json')

    slack_bot = SlackAPI(slack_api_token)

    test = slack_bot.send_channel_message()
    # Aggregate Data



    # Route Data



if __name__ == "__main__":
    main()
