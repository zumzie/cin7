import json
from mapper import *
from parser import *



def readFile(raw_data):
    with open(raw_data) as data_file:
        data = json.load(data_file)
    return data

def writeFile(incoming_data, file_name):
    with open(file_name, "w") as outputted_data:
        json.dump(incoming_data, outputted_data, indent=4)


def main():

    rawProdData = 'temp_data/cin_products.json'
    rawCustomerData = 'temp_data/cin_customers.json'
    rawOrderData = 'temp_data/cin_orders.json'

    prod_data = readFile(rawProdData)
    customer_data = readFile(rawCustomerData)
    order_data = readFile(rawOrderData)

    
    # Parse Data
    parser = Parser(prod_data, customer_data, order_data)
    parsed_products = parser.parseProducts()

    writeFile(parsed_products, 'created_files/parsedProducts.json')


    # Map Data
    mapper = Mapper(parsed_products, customer_data, order_data)
    mapped_products = mapper.mapProducts()

    writeFile(mapped_products, 'created_files/mappedProducts.json')

    # Aggregate Data

    # Route Data



if __name__ == "__main__":
    main()
