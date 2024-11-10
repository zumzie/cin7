import json




## CLEAN UP MAPPER, SHOULD JUST BE INITIALIZING OF DATA
class Mapper():
    def __init__(self, prod_data, customer_data, order_data, joor_order_data):
        self.product_data = prod_data
        self.customer_data = customer_data
        self.order_data = order_data
        self.joor_order_data = joor_order_data

    def mapProducts(self):
        mapped_products = []

        for product in self.product_data:
            new_prod = {}
            new_prod['name'] = product['name']
            new_prod['description'] = product['description']
            new_prod['id'] = str(product['id'])
            new_prod['product_identifier'] = product['styleCode']
            mapped_products.append(new_prod)

        return mapped_products
    
    def mapSkus(self):

        mapped_skus = []
        #Iterate through product data then variants

        for product in self.product_data:
            for sku in product['productOptions']:
                new_sku = {}
                new_sku['product_id'] = product['id']
                new_sku['external_id'] = product['styleCode']
                new_sku['sku_identifier'] = sku['code']
                new_sku['trait_values'] = [
                    {
                        'trait_name': 'Size',
                        'value': sku['option1'],
                        'order_minimum': 0
                    },
                    {
                        'trait_name': 'Color',
                        'value': sku['option2'],
                        'order_minimum': 0
                    }
                ]
                mapped_skus.append(new_sku)


        '''
        for product in self.product_data:
            sku_group = {}
            sku_group[product['id']] = product['productOptions']
            mapped_skus.append(sku_group)
        '''
            
            #for skus in product['productOptions']:
                #sku_group[product['id']] = []
                #sku_group.append(skus)
                
                #print(json.dumps(skus, indent=4),'\n')
        
            #new_sku = {}
            #new_sku['product_id'] = sku['product_id']
            #new_sku['external_id'] = sku['external_id']
            #new_sku['sku_identifier'] = sku['sku_identifier']
            #mapped_skus.append(new_sku)
            #print(json.dumps(sku_group, indent=4),'\n')
        
        return mapped_skus
    


    def mapImages(self):
        asset_data = []
        for product in self.product_data:
            #print(json.dumps(product,indent=4),'\n')
            count = 1
            for count, img in enumerate(product['images']):
                product_asset = {
                    'product': {
                        'id': product['id'],  # Replace with ID pulled from API call
                    },
                        'asset': {
                            'type': 'image',
                            'source_url': img['link'],
                    },
                        'display_order': count + 1 
                    }
                # Append the new dictionary to the asset_data list
                asset_data.append(product_asset)

        ## Map Variant Assets
        ## TODO
        return asset_data

    def mapInventory(self, inv_data):
        inventory = {"inventory_items": []}
        for prod_inv in inv_data:
            inventory_data = {
                        "warehouse":  prod_inv["branchName"],
                        "inventory_date":  "IMMEDIATE",
                        "style_number":  prod_inv["styleCode"],
                        "style_identifier":  prod_inv["code"],
                        "color_code":  prod_inv["option1"],
                        "size":  prod_inv["option2"],
                        "inventory":  prod_inv["available"],
                    }
            
            inventory["inventory_items"].append(inventory_data)

        return [inventory]
    
    def mapCollections(self):
        pass

    def mapOrders(self):
        # Order to JOOR
        cin_orders = []
        joor_orders = []
        
        # Orders to JOOR
        '''
        # Need to add a conditional statement so if function is called, check to see
        # which data set needs to be mapped
        '''
        for order in self.order_data:
            cin_order_obj = {
                "customer_code": "CUSTOMER",
                "price_type_id": "4",
                "price_type_name": order["currencyCode"],
                "status": "IN_PROGRESS",
                "payment_method_code": order["paymentTerms"],
                "tracking_number": order["trackingCode"],
                "export_status": "SUCCESS",              
                "po_number": order["id"],
                "comments": order["internalComments"]
            }
            cin_orders.append(cin_order_obj)

        # Orders to Cin7
        for j_order in self.joor_order_data:
            joor_order_obj = {
                "reference": "custom-" + str(j_order["order_id"]),
                "cuurencyCode": j_order["order_currency"],
                "total": j_order["order_total"],
                "internalComments": j_order["order_comments"],
                "lineItems": []
            }
            for l_item in j_order["line_items"]:
                item =  {
                    "productOptionId": l_item["item_style_id"],
                    "code": l_item["item_style_identifier"],
                    "name": l_item["item_name"],
                    "qty": l_item["item_quantity"],
                    "styleCode": l_item["item_number"],
                    "barcode": l_item["item_upc"],
                    "lineComments": l_item["item_color_comment"],
                    "unitPrice": l_item["item_price"],
                }
                joor_order_obj["lineItems"].append(item)
            joor_orders.append(joor_order_obj)

        # Order to Cin7
        return cin_orders, joor_orders
    
    # Mapping Customers to send to JOOR
    def mapCustomers(self):
        joor_customers = []

        # Map Customers to JOOR
        '''
        # Need to add a conditional statement so if function is called, check to see
        # which data set needs to be mapped
        '''
        for customer in self.customer_data:
            customer_obj = {
                "customer_code": customer["company"],
                "customer_alias": customer["company"],
                "customer_name": customer["firstName"]+ " " + customer["lastName"],
                "customer_email": customer["email"],
                "customer_contact_name": customer["firstName"],
                "billing": [
                    {
                        "billing_addresses": [
                            {
                                "billing_code": "test",
                                "billing_name": customer["firstName"]+ " " +customer["lastName"],
                                "billing_phone": customer["phone"],
                                "billing_address_1": customer["postalAddress1"],
                                "billing_address_2": customer["postalAddress2"],
                                "billing_city": customer["postalCity"],
                                "billing_state": customer["postalState"],
                                "billing_postal_code": customer["postCode"],
                                "billing_country": customer["country"],
                            }
                        ],
                    }
                ],
                "shipping": {
                    "shipping_addresses": [
                        {
                            "shipping_code": "test",
                            "shipping_phone": customer["phone"],
                            "shipping_email": customer["email"],
                            "shipping_address_1": customer["address1"],
                            "shipping_address_2": customer["address2"],
                            "shipping_city": customer["city"],
                            "shipping_state": customer["state"],
                            "shipping_postal_code": customer["postCode"],
                            "shipping_country": customer["country"],
                        }
                    ],
                },
            }
            customer_obj["price_types"] = {
                "price_type_currency_code": customer["priceColumn"],
                "price_type_label": customer["priceColumn"],
                "price_type_retail_currency_code": "AUD",
            }
        joor_customers.append(customer_obj)

        # Map Customers to Cin7

        return [{"bulk_connections": {"connection": joor_customers}}]



## ADD IN REST OF PRODUCT MAPPER
class MapProducts(Mapper):
    def __init__(self, prod_data, customer_data, order_data, joor_order_data):
        super().__init__(prod_data, customer_data, order_data, joor_order_data)

    def __repr__(self):
        return f"MapProducts(mappings={{'products': {len(MapProducts.mapProducts(self))}, 'skus': {len(MapProducts.mapSkus(self))}}})"

    def mapProducts(self):
        mapped_products = []

        for product in self.product_data:
            new_prod = {}
            new_prod['name'] = product['name']
            new_prod['description'] = product['description']
            new_prod['product_identifier'] = str(product['id'])
            new_prod['external_id'] = product['styleCode']
            mapped_products.append(new_prod)
        return mapped_products
    
    def mapSkus(self):
        mapped_skus = []

        #Iterate through product data then variants
        for product in self.product_data:
            for sku in product['productOptions']:
                new_sku = {}
                new_sku['product_id'] = product['id']
                new_sku['external_id'] = product['styleCode']
                new_sku['sku_identifier'] = sku['code']
                new_sku['trait_values'] = [
                    {
                        'trait_name': 'Size',
                        'value': sku['option1'],
                        'order_minimum': 0
                    },
                    {
                        'trait_name': 'Color',
                        'value': sku['option2'],
                        'order_minimum': 0
                    }
                ]
                mapped_skus.append(new_sku)
        
        return mapped_skus
    
    def mapPrices(self):
        mapped_prices = []

        #Iterate through product data then variants for prices
        for product in self.product_data:
            for sku in product['productOptions']:
                new_sku_price = {}
                new_sku_price['sku_identifier'] = sku['code']
                new_sku_price['price_type_id'] = ''
                new_sku_price['wholesale_value'] = str(sku['wholesalePrice'])
                new_sku_price['retail_price'] = str(sku['retailPrice'])
                mapped_prices.append(new_sku_price)
        
        return mapped_prices


    
    def mapImages(self):
        asset_data = []
        for product in self.product_data:
            #print(json.dumps(product,indent=4),'\n')
            count = 1
            for count, img in enumerate(product['images']):
                product_asset = {
                    'product': {
                        'id': product['id'],  # Replace with ID pulled from API call
                    },
                        'asset': {
                            'type': 'image',
                            'source_url': img['link'],
                    },
                        'display_order': count + 1 
                    }
                # Append the new dictionary to the asset_data list
                asset_data.append(product_asset)

        ## Map Variant Assets
        ## TODO
        return asset_data

    def mapInventory(self, inv_data):
        inventory = {"inventory_items": []}
        for prod_inv in inv_data:
            inventory_data = {
                        "warehouse":  prod_inv["branchName"],
                        "inventory_date":  "IMMEDIATE",
                        "style_number":  prod_inv["styleCode"],
                        "style_identifier":  prod_inv["code"],
                        "color_code":  prod_inv["option1"],
                        "size":  prod_inv["option2"],
                        "inventory":  prod_inv["available"],
                    }
            
            inventory["inventory_items"].append(inventory_data)

        return [inventory]