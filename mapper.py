import json

class Mapper:
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
    
    def mapOrders(self):

        # Order to JOOR
        cin_orders = []
        joor_orders = []
        
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

        for j_order in self.joor_order_data:
            joor_order_obj = {
                "reference": "custom-" + str(j_order["order_id"]),
                "price_type_id": "4",
                "cuurencyCode": j_order["order_currency"],
                "export_status": "SUCCESS",              
                "total": j_order["order_total"],
                "internalComments": j_order["order_comments"],
                "lineItems": []
            }
            print(j_order)
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
