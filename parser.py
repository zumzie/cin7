class Parser:
    def __init__(self, prodData, orderData, customerData):
        self.productData = prodData
        self.customerData = customerData
        self.orderData = orderData

    def parseProducts(self):
        temp_prod_data = []
        keys_to_delete = ['tags','subCategory', 'orderType', 'volume',
                          'productType','productSubtype', 'salesAccount',
                          'purchasesAccount', 'importCustomsDuty', 'weight',
                          'height', 'length', 'width', 'pdfUpload', 'pdfDescription']
        for prod in self.productData:
            for key in list(prod.keys()):
                if key in keys_to_delete:
                    del prod[key]
            temp_prod_data.append(prod)
        return temp_prod_data