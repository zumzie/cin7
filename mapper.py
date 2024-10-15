class Mapper:
    def __init__(self, prodData, orderData, customerData):
        self.productData = prodData
        self.customerData = customerData
        self.orderData = orderData


    def mapProducts(self):
        mapped_products = []

        for product in self.productData:
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
        for sku in self.productData:
            new_sku = {}
            new_sku['product_id'] = sku['product_id']
            new_sku['external_id'] = sku['external_id']
            new_sku['sku_identifier'] = sku['sku_identifier']
            mapped_skus.append(new_sku)
        
        return mapped_skus
    
    def mapImages(self):
        pass

    def mapInventory(self):
        pass
